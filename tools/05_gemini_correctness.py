#!/usr/bin/env python3.12
"""Stage 5 -- is the question actually true of the audio?

The first version of this stage showed the auditor the intended answer and the
construction timeline and asked "is this cue audible?". That does not work. On
a long-scene item whose answer was "baby laughing", the informed auditor
reported hearing "a gasp at 19s, a drawer at 26s, and a baby laughing at 39s" --
an almost verbatim readback of the timeline it had just been handed -- while the
*blind* quality pass on the same file heard "hand clapping, a gong crash, a
person speaking, and a revving engine". There was no baby. Handing a model the
answer and asking it to confirm the answer buys nothing but agreement.

So nothing here ever sees the intended answer next to the audio. Three steps:

  5a  Describe (blind).  The model lists the sound events it can hear with
      rough times and transcribes any speech. It is not shown the question,
      the options, the answer, or the construction record.
  5b  Judge (deaf).  A second call sees the question, the options, the intended
      answer and the *text* of 5a -- but no audio. It can only reason over what
      was actually reported, so it cannot hallucinate corroboration.
  5c  Presence test with decoys (blind).  The model is asked which of a handful
      of candidate sounds are present. The list mixes the answer's own label
      with two labels drawn from another item entirely. Claiming a decoy is
      present means its hearing cannot be trusted on this file, so the item is
      dropped regardless of what it said about the real label.

Writes `curation/05_verified.jsonl`.
"""

from __future__ import annotations

import collections
import json
import os
import random
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (  # noqa: E402
    CURATION,
    gemini_call,
    gold_text,
    parse_json_block,
    read_jsonl,
    write_jsonl,
)

WORKERS = 240

# ---------------------------------------------------------------------------
# 5a -- blind description
# ---------------------------------------------------------------------------

# What to ask for, per family. The first version asked only for a list of
# sound events and a transcript, which quietly destroyed every comparison and
# prosody question type: the judge downstream had no evidence about loudness
# order, speed, pitch or tempo, so it ruled those answers "unsupported" and
# skills like `speed_pattern3` and `music_dynamics_real` fell to 0% survival.
# These blocks ask for the observable dimensions each family is built around --
# still without revealing the question, the options or the claimed answer.
_FOCUS = {
    "prosody": """Also report, for the speech specifically:
- If there are several utterances or segments, number them in order and for
  EACH one give: how loud it is relative to the others (loudest / middle /
  quietest), how fast it is spoken (fast / medium / slow), and how high the
  voice sits (high / medium / low).
- Any clearly audible silent pause inside the speech: give the word spoken
  immediately before the pause and roughly how long the pause lasts.
- Whether the pitch rises, falls, rises-then-falls or falls-then-rises over the
  utterance as a whole.
- Any disfluency: a repeated word, a filled hesitation, a false start, or a
  self-correction, quoted exactly.
- How many syllables the spoken word or phrase has, if only a word or two is
  said.""",
    "speakers": """Also report, about the voices:
- How many distinct speakers you can hear, and what makes each distinguishable.
- For each speaker, whether they sound like an adult man, an adult woman or a
  child.
- How many times the speaker changes, i.e. the number of conversational turns.
- What language each speaker is using.
- Whether any voice recurs later in the recording.""",
    "content": """Also report, about what is said:
- A full transcript, attributing each line to a speaker when there are several.
- The emotion each speaker's delivery conveys, judged from the voice rather
  than the words.
- Anything a speaker states, corrects, or contradicts later.""",
    "sound": """Also report, about the sound events:
- Rank the events by loudness, saying which is loudest and which is quietest.
- For each event, roughly how long it lasts, and which are noticeably longer or
  shorter than the others.
- How many times each distinct kind of sound occurs.
- Whether any sound changes character, gets louder, or gets quieter while it
  plays.
- What kind of place or situation the combination of sounds suggests.""",
    "music": """Also report, about the music:
- The tempo, and whether it speeds up, slows down or stays constant; if it
  changes, say where.
- Whether the pitch is higher or lower in one part than another.
- Which part is played loudest and which quietest.
- Which instruments you can hear, and whether anyone is singing.
- Whether any passage repeats; if so, which sections are the same as each
  other, numbered in order.
- What genre it sounds like.""",
    "multi": """Also report, treating each clip separately and numbering them:
- What is in each clip, described on its own.
- How many distinct speakers are in each clip, if any speech is present.
- Which clip is longer, which is louder, and anything the clips share.
- Within a single long recording, the order of events and which occurs last.""",
}

DESCRIBE_PROMPT = """Listen to this audio and report what is in it. You are not
being asked any question about it; just describe it as accurately as you can.

{structure}

Report every distinct sound you can hear, in the order they occur, with an
approximate time in seconds. Name sounds concretely ("a dog barking", "a drawer
closing", "a cymbal crash"), not vaguely ("a noise"). If speech is present,
transcribe it.

{focus}

Do not guess at anything you cannot actually hear. It is better to report less
than to invent an event, a word, or a difference that is not there. If you
genuinely cannot tell one of the things asked above, say so rather than
choosing arbitrarily.

Respond with JSON only:
{{"events": [{{"time_sec": <number>, "sound": "<short description>"}}],
  "speech_transcript": "<what is said, or empty>",
  "music": "<short description, or empty>",
  "observations": "<your answers to the focus points above, a few sentences>",
  "summary": "<one sentence>"}}"""


# ---------------------------------------------------------------------------
# 5b -- judging over the description, with no audio
# ---------------------------------------------------------------------------

JUDGE_PROMPT = """A listening-test item is being checked before publication.
You cannot hear the audio. Instead you are given an independent listener's
report of what is in it, produced without any knowledge of the question.

LISTENER'S REPORT:
{report}

THE QUESTION: {question}
THE OPTIONS:
{options}
THE ITEM CLAIMS THE ANSWER IS: {answer_id}. {answer_text}

Decide, using only the report:

1. supported -- does the report bear out what the claimed answer asserts? The
   report was asked to describe loudness order, speed, pitch, timing, speaker
   counts, tempo changes and repetition where relevant, so for most questions
   the evidence should be there to check. Treat a paraphrase as a match: "the
   third segment is the loudest" supports an answer of "the third utterance".
2. contradicted -- does the report positively indicate a *different* option is
   the right one?
3. another_option_fits -- would some other option fit the report at least as
   well as the claimed one?
4. not_addressed -- is the report simply silent on the property the question
   turns on, so that it neither supports nor contradicts the answer?

If the report describes entirely different content from what the answer names
-- a different sound, a different instrument, a different speaker -- that is
"contradicted", not merely unsupported.

Respond with JSON only:
{{"supported": true | false,
  "contradicted": true | false,
  "another_option_fits": true | false,
  "not_addressed": true | false,
  "reason": "<one sentence>"}}"""


# ---------------------------------------------------------------------------
# 5c -- presence test with decoys
# ---------------------------------------------------------------------------

PRESENCE_PROMPT = """Listen to this audio. For each candidate below, say whether
you can actually hear it in this recording.

Some of these are not in the recording at all. Say "no" for those. Do not
assume that a listed item must be present.

CANDIDATES:
{candidates}

Respond with JSON only:
{{"present": ["<the candidates you can hear>"], "absent": ["<the rest>"]}}"""


_cache_lock = threading.Lock()
_progress_lock = threading.Lock()
_done = 0
_total = 0


def _structure_note(row: dict) -> str:
    clips = row.get("n_clips") or 1
    if clips > 1:
        return f"You are given {clips} separate clips, in order: clip 1 first, then clip 2, and so on."
    return ""


def describe(row: dict) -> dict | None:
    prompt = DESCRIBE_PROMPT.format(
        structure=_structure_note(row), focus=_FOCUS.get(row["family"], "")
    )
    for _ in range(3):
        text = gemini_call(prompt, row["audio"], temperature=0.0, max_tokens=6144)
        obj = parse_json_block(text)
        if isinstance(obj, dict) and ("events" in obj or "summary" in obj):
            events = obj.get("events") or []
            if not isinstance(events, list):
                events = []
            return {
                "events": [
                    {
                        "time_sec": e.get("time_sec"),
                        "sound": str(e.get("sound", ""))[:120],
                    }
                    for e in events
                    if isinstance(e, dict)
                ][:20],
                "speech_transcript": str(obj.get("speech_transcript", ""))[:800],
                "music": str(obj.get("music", ""))[:300],
                "observations": str(obj.get("observations", ""))[:1500],
                "summary": str(obj.get("summary", ""))[:300],
            }
    return None


def _report_text(report: dict) -> str:
    lines = []
    for event in report["events"]:
        when = event.get("time_sec")
        stamp = f"{float(when):.1f}s" if isinstance(when, (int, float)) else "?"
        lines.append(f"  - {stamp}: {event['sound']}")
    body = "\n".join(lines) if lines else "  (no discrete events reported)"
    out = f"Events heard:\n{body}"
    if report["speech_transcript"]:
        out += f"\nSpeech transcribed: \u201c{report['speech_transcript']}\u201d"
    if report["music"]:
        out += f"\nMusic: {report['music']}"
    if report.get("observations"):
        out += f"\nDetailed observations: {report['observations']}"
    if report["summary"]:
        out += f"\nOverall: {report['summary']}"
    return out


def judge(row: dict, report: dict) -> dict | None:
    prompt = JUDGE_PROMPT.format(
        report=_report_text(report),
        question=row["question"],
        options="\n".join(f"  {o['id']}. {o['text']}" for o in row["options"]),
        answer_id=row["answer"],
        answer_text=gold_text(row),
    )
    for _ in range(3):
        # No audio on purpose: the judge must reason over the report alone.
        text = gemini_call(prompt, [], temperature=0.0, max_tokens=2048)
        obj = parse_json_block(text)
        if isinstance(obj, dict) and "supported" in obj:
            return {
                "supported": bool(obj.get("supported")),
                "contradicted": bool(obj.get("contradicted")),
                "another_option_fits": bool(obj.get("another_option_fits")),
                "not_addressed": bool(obj.get("not_addressed")),
                "reason": str(obj.get("reason", ""))[:300],
            }
    return None


def _target_labels(row: dict) -> list[str]:
    """Concrete sound labels the construction record says are in the audio."""
    facts = row.get("facts") or {}
    labels: list[str] = []

    def add(value):
        if isinstance(value, str) and 2 < len(value) < 60:
            cleaned = value.strip()
            if cleaned.lower() not in ("speech", "music", "") and cleaned not in labels:
                labels.append(cleaned)

    answer = facts.get("answer")
    if isinstance(answer, dict):
        add(answer.get("label"))
    for key in ("label", "instrument", "genre", "background_label", "background"):
        add(facts.get(key))
    for event in facts.get("events") or []:
        if isinstance(event, dict):
            add(event.get("label"))
    for item in facts.get("labels") or []:
        add(item)
    for item in facts.get("cues") or []:
        add(item)
    return labels[:6]


def presence(row: dict, decoys: list[str]) -> dict | None:
    targets = _target_labels(row)
    if not targets or not decoys:
        return {"skipped": True}
    rng = random.Random(f"{row['uid']}::presence")
    candidates = targets[:3] + decoys[:2]
    rng.shuffle(candidates)
    prompt = PRESENCE_PROMPT.format(
        candidates="\n".join(f"  - {c}" for c in candidates)
    )
    for _ in range(3):
        text = gemini_call(prompt, row["audio"], temperature=0.0, max_tokens=2048)
        obj = parse_json_block(text)
        if isinstance(obj, dict) and "present" in obj:
            reported = obj.get("present") or []
            if isinstance(reported, str):
                reported = [reported]
            reported_lower = {str(x).strip().lower() for x in reported}
            return {
                "skipped": False,
                "targets": targets[:3],
                "decoys": decoys[:2],
                "reported_present": sorted(reported_lower),
                "decoy_claimed": sorted(
                    d for d in decoys[:2] if d.strip().lower() in reported_lower
                ),
                "targets_found": sorted(
                    t for t in targets[:3] if t.strip().lower() in reported_lower
                ),
            }
    return None


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def _progress(label: str) -> None:
    global _done
    with _progress_lock:
        _done += 1
        if _done % 250 == 0:
            print(f"  {_done}/{_total} {label}", flush=True)


def load_cache(name: str) -> dict:
    path = CURATION / name
    cache: dict = {}
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
            if row.get("result") is not None:
                cache[row["uid"]] = row["result"]
    return cache


def _run_stage(rows, cache, name, worker, label):
    jobs = [r for r in rows if r["uid"] not in cache]
    global _done, _total
    _done, _total = 0, len(jobs)
    print(f"{label}: {len(cache)} cached, {len(jobs)} to run")
    if not jobs:
        return
    started = time.time()
    with (CURATION / name).open("a") as fh:
        def task(row):
            result = worker(row)
            with _cache_lock:
                fh.write(
                    json.dumps({"uid": row["uid"], "result": result}, ensure_ascii=False)
                    + "\n"
                )
                fh.flush()
            _progress(label)
            return row["uid"], result

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            for uid, result in pool.map(task, jobs):
                if result is not None:
                    cache[uid] = result
    print(f"  done in {(time.time()-started)/60:.1f} min")


def main() -> None:
    rows = read_jsonl(CURATION / "04_probe.jsonl")
    print(f"verifying {len(rows)} items\n")

    # 5a -- blind description.
    desc_cache = load_cache("05a_describe_cache.jsonl")
    _run_stage(rows, desc_cache, "05a_describe_cache.jsonl", describe, "descriptions")

    described = [r for r in rows if desc_cache.get(r["uid"])]

    # 5c -- decoy labels are borrowed from a different item of the same family,
    # so they are plausible for the domain but absent from this recording.
    by_family: dict[str, list[str]] = collections.defaultdict(list)
    for row in rows:
        by_family[row["family"]].extend(_target_labels(row))
    decoy_for: dict[str, list[str]] = {}
    for row in described:
        own = {label.lower() for label in _target_labels(row)}
        pool = [x for x in by_family[row["family"]] if x.lower() not in own]
        rng = random.Random(f"{row['uid']}::decoy")
        rng.shuffle(pool)
        picked, seen = [], set()
        for label in pool:
            if label.lower() in seen:
                continue
            seen.add(label.lower())
            picked.append(label)
            if len(picked) == 2:
                break
        decoy_for[row["uid"]] = picked

    pres_cache = load_cache("05c_presence_cache.jsonl")
    _run_stage(
        described,
        pres_cache,
        "05c_presence_cache.jsonl",
        lambda r: presence(r, decoy_for.get(r["uid"], [])),
        "presence tests",
    )

    # 5b -- judge the report, without audio.
    judge_cache = load_cache("05b_judge_cache.jsonl")
    _run_stage(
        described,
        judge_cache,
        "05b_judge_cache.jsonl",
        lambda r: judge(r, desc_cache[r["uid"]]),
        "judgements",
    )

    kept: list[dict] = []
    reasons = collections.Counter()
    before = collections.Counter()
    after = collections.Counter()
    examples: list[dict] = []

    for row in rows:
        before[row["level"]] += 1
        report = desc_cache.get(row["uid"])
        verdict = judge_cache.get(row["uid"])
        pres = pres_cache.get(row["uid"])
        if not report or not verdict or not pres:
            reasons["incomplete"] += 1
            continue

        # The decoy control only makes sense where the construction record
        # names discrete, audible objects. A music item's "target" is a genre
        # or a key, which is not something to answer "can you hear it?" about.
        decoy_applies = row["family"] in ("sound", "multi") and not pres.get("skipped")

        problem = None
        if decoy_applies and pres.get("decoy_claimed"):
            problem = "heard_a_decoy"
        elif decoy_applies and not pres.get("targets_found"):
            problem = "target_sound_not_heard"
        elif verdict["contradicted"]:
            problem = "answer_contradicted_by_report"
        elif verdict["another_option_fits"]:
            problem = "another_option_fits"
        elif not verdict["supported"]:
            problem = (
                "report_silent_on_the_property"
                if verdict.get("not_addressed")
                else "answer_unsupported_by_report"
            )

        reasons[problem or "ok"] += 1
        if problem:
            if len(examples) < 60:
                examples.append(
                    {
                        "uid": row["uid"],
                        "skill": row["skill"],
                        "family": row["family"],
                        "question": row["question"],
                        "intended": f"{row['answer']}. {gold_text(row)}",
                        "problem": problem,
                        "heard": report["summary"],
                        "reason": verdict["reason"],
                        "decoy_claimed": pres.get("decoy_claimed"),
                    }
                )
            continue

        after[row["level"]] += 1
        kept.append(
            {
                **row,
                "verify": {
                    "report": report,
                    "judgement": verdict,
                    "presence": pres,
                },
            }
        )

    n = write_jsonl(CURATION / "05_verified.jsonl", kept)
    summary = {
        "input": len(rows),
        "kept": n,
        "gate_outcomes": dict(reasons.most_common()),
        "blind_level_before": dict(sorted(before.items())),
        "blind_level_after": dict(sorted(after.items())),
        "by_family": dict(collections.Counter(r["family"] for r in kept)),
        "design": (
            "the audio is described blind; a second deaf call judges that "
            "description against the claimed answer; a decoy presence test "
            "discards files the listener mis-hears"
        ),
        "rejected_examples": examples,
    }
    (CURATION / "05_verify_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"\nkept {n} / {len(rows)}")
    print("\ngate outcomes:")
    for reason, count in reasons.most_common():
        print(f"  {count:6d}  {reason}")
    print("\nrejection rate by blind-probe score (0/5 = model always missed it):")
    for level in range(1, 6):
        b, a = before.get(level, 0), after.get(level, 0)
        rate = f"{100*(b-a)/b:.0f}%" if b else "-"
        print(f"  probe-level {level}: {b:5d} -> {a:5d}  ({rate} rejected)")
    if examples:
        print("\nsample rejections:")
        for ex in examples[:10]:
            print(f"  {ex['problem']:34s} {ex['skill'][:22]:22s} {ex['intended'][:38]}")
            print(f"     heard: {ex['heard'][:95]}")


if __name__ == "__main__":
    main()
