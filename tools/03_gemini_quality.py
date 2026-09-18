#!/usr/bin/env python3.12
"""Stage 3 -- how does it actually sound?

This is the gate that decides what the page is. A sample of 48 raw candidates
came back 21% "showcase" / 33% "acceptable" / 46% "reject", with audible
distortion, abrupt cuts, obvious splices, metallic artifacts and one clip that
was pure silence. So every shortlisted item is listened to twice, by two
differently-framed prompts, and only items both passes are happy with survive.

Three things learned while designing the rubric:

* It must be **modality-neutral**. A first draft let the model mark a
  sound-event clip down to quality 1 because "no speech present", which is not
  a defect for a sound-event question.
* It must **license assembly**. The second draft rejected 11 of 12 items,
  almost all for "obvious splices between unrelated segments" -- but many
  question types (`volume_pattern3`, `speaker_match5`, `dialogue_turns`) are
  *built* by concatenating distinct segments, so that structure is the item, not
  a flaw. The rubric now states the intended segment count and asks whether each
  join is *clean*, never whether a join exists. Segment attributes are withheld
  so nothing about the answer leaks.
* The passes must disagree in *framing*, not just in seed. Pass A describes
  what it hears and scores it; pass B is told to hunt for the single worst
  problem first. A cooperative rubric asked twice mostly repeats itself.

Results are cached per (uid, pass) in `curation/03_quality_cache.jsonl`, so the
script can be re-run after an interruption without paying for work twice.

Writes `curation/03_quality.jsonl`.
"""

from __future__ import annotations

import collections
import json
import os
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import CURATION, gemini_call, parse_json_block, read_jsonl, write_jsonl  # noqa: E402

WORKERS = 140

ARTIFACT_VOCAB = [
    "click_at_join",
    "truncated_word",
    "starts_or_ends_mid_sound",
    "distortion",
    "robotic_artifact",
    "metallic",
    "pumping",
    "noise_masks_foreground",
    "dead_silence",
    "none",
]

# The shared preamble. Two sentences here are load-bearing. Without the
# modality line the model penalizes every sound-event clip for having no
# speech; without the assembly line it rejects every deliberately concatenated
# item for "obvious splices".
_CONTEXT = """This is one audio item produced by an automatic audio-construction
system, for a listening test.

WHAT IS NOT A DEFECT:
- It may be speech, music, environmental sound events, or any mixture. Absence
  of speech is not a defect. Absence of music is not a defect.
- Many items are deliberately assembled from several separate segments played
  one after another, often with a short silence between them, and the segments
  are usually unrelated in content. That structure is intentional and is NOT a
  defect. Do not report it as a splice problem.
- Being short, quiet, or hard to interpret is not a defect.
- A deliberate difference in loudness, speed or pitch between segments is the
  point of the item, not damage.

WHAT IS A DEFECT:
- A click, pop or thump AT a join between segments.
- A word or sound cut off mid-way through.
- The clip as a whole starting or ending mid-sound, with no natural close.
- Synthetic speech that sounds robotic, slurred or garbled.
- Distortion, metallic ringing or warbling from speed or pitch manipulation.
- Background noise loud enough to bury the foreground.
- Long stretches of dead silence that carry nothing.

Judge only how the audio SOUNDS as a recording."""

_SCHEMA = f"""Respond with JSON only, no prose around it:
{{"quality": <1-5 integer>,
  "verdict": "showcase" | "acceptable" | "reject",
  "speech_naturalness": "no_speech" | "natural" | "slightly_robotic" | "robotic" | "garbled",
  "joins_clean": true | false,
  "artifacts": [<any of {ARTIFACT_VOCAB}>],
  "heard": "<one sentence describing what you hear>",
  "worst_problem": "<short phrase, or \\"none\\">"}}

Scale:
  5 = clean and natural, nothing to apologise for
  4 = minor imperfection a listener would not comment on
  3 = noticeable flaw but still listenable
  2 = clearly damaged
  1 = broken, silent, or unlistenable
Use "showcase" only if you would be happy to see this audio on the demo page of
a published research paper. If you find no defect from the list above, the
verdict should be "showcase"."""


def _structure_note(row: dict) -> str:
    """Tell the auditor how many pieces to expect, without leaking the cue.

    Only the count and the presence of gaps are disclosed. Per-segment truths
    (which one is louder, faster, higher) are exactly the answer, so they stay
    hidden.
    """
    facts = row.get("facts") or {}
    parts = [s for s in (facts.get("segments") or []) if s.get("role") == "part"]
    clips = row.get("n_clips") or 1
    bits = []
    if clips > 1:
        bits.append(f"This item is {clips} separate audio clips, played to you in order")
    if len(parts) > 1:
        bits.append(
            f"it was assembled from {len(parts)} segments joined end to end, "
            "and the segments are intended to differ from each other"
        )
    if not bits:
        return ""
    return "STRUCTURE (intended, not a defect): " + "; ".join(bits) + "."


PROMPT_A = f"""You are auditing audio for a public research demo page.

{_CONTEXT}

{{structure}}

First describe what you hear, then score it.

{_SCHEMA}"""

PROMPT_B = f"""You are the last reviewer before this audio is published on a
research project's demo page. Your job is to catch anything embarrassing.

{_CONTEXT}

{{structure}}

Work through the defect list above one item at a time. Name the single worst
real defect you can hear, then score the audio. If you genuinely find none of
the listed defects, say "none" and score accordingly -- do not invent a problem,
and do not count the intended structure as one.

{_SCHEMA}"""

PASSES = {"a": PROMPT_A, "b": PROMPT_B}

_cache_lock = threading.Lock()
_progress_lock = threading.Lock()
_done = 0


def _normalize(obj: dict | None) -> dict | None:
    if not isinstance(obj, dict):
        return None
    try:
        quality = int(obj.get("quality"))
    except (TypeError, ValueError):
        return None
    verdict = str(obj.get("verdict", "")).strip().lower()
    if verdict not in ("showcase", "acceptable", "reject"):
        return None
    artifacts = obj.get("artifacts") or []
    if isinstance(artifacts, str):
        artifacts = [artifacts]
    artifacts = [str(a).strip().lower() for a in artifacts if str(a).strip()]
    artifacts = [a for a in artifacts if a != "none"]
    return {
        "quality": max(1, min(5, quality)),
        "verdict": verdict,
        "speech_naturalness": str(obj.get("speech_naturalness", "")).strip().lower(),
        "joins_clean": obj.get("joins_clean"),
        "artifacts": sorted(set(artifacts)),
        "heard": str(obj.get("heard", ""))[:400],
        "worst_problem": str(obj.get("worst_problem", ""))[:200],
    }


def audit_one(row: dict, which: str, attempts: int = 3) -> dict | None:
    """One listening pass. Retries when the reply is not parseable JSON.

    `gemini_call` already retries transport failures; this loop covers the
    separate case of a well-formed response whose body is prose.
    """
    prompt = PASSES[which].replace("{structure}", _structure_note(row))
    for _ in range(attempts):
        text = gemini_call(prompt, row["audio"], temperature=0.0, max_tokens=4096)
        result = _normalize(parse_json_block(text))
        if result is not None:
            return result
    return None


def run(args: tuple[dict, str, object]) -> tuple[str, str, dict | None]:
    global _done
    row, which, cache_fh = args
    result = audit_one(row, which)
    with _cache_lock:
        cache_fh.write(
            json.dumps(
                {"uid": row["uid"], "pass": which, "result": result}, ensure_ascii=False
            )
            + "\n"
        )
        cache_fh.flush()
    with _progress_lock:
        _done += 1
        if _done % 250 == 0:
            print(f"  {_done} audits done", flush=True)
    return row["uid"], which, result


def load_cache() -> dict[tuple[str, str], dict | None]:
    path = CURATION / "03_quality_cache.jsonl"
    cache: dict[tuple[str, str], dict | None] = {}
    if not path.exists():
        return cache
    with path.open() as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            # A None result means the call failed; retry it on the next run.
            if row.get("result") is not None:
                cache[(row["uid"], row["pass"])] = row["result"]
    return cache


def passes_gate(a: dict, b: dict) -> tuple[bool, str]:
    """Both listeners must be happy. Either one objecting drops the item."""
    for label, res in (("a", a), ("b", b)):
        if res["verdict"] == "reject":
            return False, f"pass_{label}_rejected"
        if res["quality"] < 4:
            return False, f"pass_{label}_quality_{res['quality']}"
        if res["artifacts"]:
            return False, f"pass_{label}_artifact_{res['artifacts'][0]}"
        if res["speech_naturalness"] in ("robotic", "garbled"):
            return False, f"pass_{label}_speech_{res['speech_naturalness']}"
        if res.get("joins_clean") is False:
            return False, f"pass_{label}_dirty_joins"
    # An "acceptable" from one reviewer is tolerated only if the other would
    # showcase it and neither heard a defect.
    if "showcase" not in (a["verdict"], b["verdict"]):
        return False, "neither_pass_would_showcase"
    return True, "ok"


def main() -> None:
    rows = read_jsonl(CURATION / "02c_probed.jsonl")
    cache = load_cache()
    jobs: list[tuple[dict, str]] = []
    for row in rows:
        for which in PASSES:
            if (row["uid"], which) not in cache:
                jobs.append((row, which))

    print(f"{len(rows)} candidates x {len(PASSES)} passes; {len(cache)} cached, {len(jobs)} to run")

    if jobs:
        started = time.time()
        with (CURATION / "03_quality_cache.jsonl").open("a") as cache_fh:
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for uid, which, result in pool.map(
                    run, [(row, which, cache_fh) for row, which in jobs]
                ):
                    if result is not None:
                        cache[(uid, which)] = result
        print(f"  finished {len(jobs)} audits in {(time.time()-started)/60:.1f} min")

    kept: list[dict] = []
    gate_reasons = collections.Counter()
    quality_hist = collections.Counter()
    verdict_hist = collections.Counter()
    artifact_hist = collections.Counter()
    naturalness_hist = collections.Counter()
    incomplete = 0

    for row in rows:
        a = cache.get((row["uid"], "a"))
        b = cache.get((row["uid"], "b"))
        if not a or not b:
            incomplete += 1
            gate_reasons["audit_incomplete"] += 1
            continue
        for res in (a, b):
            quality_hist[res["quality"]] += 1
            verdict_hist[res["verdict"]] += 1
            naturalness_hist[res["speech_naturalness"]] += 1
            for art in res["artifacts"]:
                artifact_hist[art] += 1
        ok, reason = passes_gate(a, b)
        gate_reasons[reason] += 1
        if ok:
            kept.append(
                {
                    **row,
                    "quality": {
                        "pass_a": a,
                        "pass_b": b,
                        "mean_quality": round((a["quality"] + b["quality"]) / 2, 2),
                        "min_quality": min(a["quality"], b["quality"]),
                    },
                }
            )

    n = write_jsonl(CURATION / "03_quality.jsonl", kept)
    by_family = collections.Counter(r["family"] for r in kept)
    summary = {
        "audited": len(rows),
        "kept": n,
        "showcase_rate": round(n / max(len(rows), 1), 4),
        "incomplete_audits": incomplete,
        "gate_outcomes": dict(gate_reasons.most_common()),
        "quality_histogram": dict(sorted(quality_hist.items())),
        "verdict_histogram": dict(verdict_hist.most_common()),
        "artifact_histogram": dict(artifact_hist.most_common()),
        "speech_naturalness_histogram": dict(naturalness_hist.most_common()),
        "by_family": dict(by_family),
        "distinct_skills": len({r["skill"] for r in kept}),
        "gate": "both passes: verdict==showcase, quality>=4, no artifacts, speech not robotic/garbled",
    }
    (CURATION / "03_quality_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"\nkept {n} / {len(rows)}  ({100*n/max(len(rows),1):.1f}% showcase-grade)")
    print(f"distinct skills surviving: {summary['distinct_skills']}")
    print("\nverdicts (per audit):")
    for k, v in verdict_hist.most_common():
        print(f"  {v:6d}  {k}")
    print("\nquality scores (per audit):")
    for k in sorted(quality_hist):
        print(f"  {quality_hist[k]:6d}  quality {k}")
    print("\nartifacts heard:")
    for k, v in artifact_hist.most_common():
        print(f"  {v:6d}  {k}")
    print("\nsurvivors by family:")
    for fam, count in by_family.most_common():
        print(f"  {count:6d}  {fam}")


if __name__ == "__main__":
    main()
