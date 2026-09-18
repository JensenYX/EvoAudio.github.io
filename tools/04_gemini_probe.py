#!/usr/bin/env python3.12
"""Stage 4 -- measure difficulty instead of asserting it.

The generators tag each item easy/medium/hard and record the `contrast` knob
they turned to get there, but neither predicts how hard the item actually is:
across the 27 skills with enough data, contrast correlates with the solver's
pass rate positively for 13 of them and negatively for 14. Announcing those
tags as difficulty on a demo page would be announcing noise.

So difficulty is measured directly. Every quality survivor is answered five
times blind by Gemini 3.5 Flash at temperature 1.0, with the option order
reshuffled on each attempt so position bias cannot masquerade as competence,
and the level is set by how many attempts landed on the constructed answer.

Writes `curation/04_probe.jsonl`.
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
    parse_choice_letter,
    read_jsonl,
    write_jsonl,
)

WORKERS = 140
ATTEMPTS = 5
LETTERS = "ABCDEFGH"

PROMPT = """Listen to the audio and answer the multiple-choice question.

{question}
{options}

Base your answer only on what you can hear. Respond with JSON only:
{{"answer": "<letter>"}}"""

MULTI_CLIP_PREFIX = (
    "You are given {n} separate audio clips, in order: clip 1 first, then "
    "clip 2, and so on.\n\n"
)

_cache_lock = threading.Lock()
_progress_lock = threading.Lock()
_done = 0


def shuffled_prompt(row: dict, attempt: int) -> tuple[str, str]:
    """Build the prompt for one attempt and return it with the gold letter.

    The seed is derived from the item id, so a re-run reproduces the same five
    orderings and the measured level is stable.
    """
    rng = random.Random(f"{row['uid']}::{attempt}")
    options = list(row["options"])
    rng.shuffle(options)
    gold_index = next(
        i for i, opt in enumerate(options) if opt["id"] == row["answer"]
    )
    rendered = "\n".join(
        f"{LETTERS[i]}. {opt['text']}" for i, opt in enumerate(options)
    )
    prefix = (
        MULTI_CLIP_PREFIX.format(n=row["n_clips"]) if row["n_clips"] > 1 else ""
    )
    prompt = prefix + PROMPT.format(question=row["question"], options=rendered)
    return prompt, LETTERS[gold_index]


def attempt_once(row: dict, attempt: int) -> dict | None:
    prompt, gold = shuffled_prompt(row, attempt)
    for _ in range(3):
        text = gemini_call(prompt, row["audio"], temperature=1.0, max_tokens=2048)
        letter = parse_choice_letter(text)
        if letter:
            return {"attempt": attempt, "picked": letter, "gold": gold, "correct": letter == gold}
    return None


def run(args):
    global _done
    row, attempt, cache_fh = args
    result = attempt_once(row, attempt)
    with _cache_lock:
        cache_fh.write(
            json.dumps(
                {"uid": row["uid"], "attempt": attempt, "result": result},
                ensure_ascii=False,
            )
            + "\n"
        )
        cache_fh.flush()
    with _progress_lock:
        _done += 1
        if _done % 250 == 0:
            print(f"  {_done} attempts done", flush=True)
    return row["uid"], attempt, result


def load_cache() -> dict[tuple[str, int], dict]:
    path = CURATION / "04_probe_cache.jsonl"
    cache: dict[tuple[str, int], dict] = {}
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
                cache[(row["uid"], row["attempt"])] = row["result"]
    return cache


def level_for(correct: int) -> int:
    """5 of 5 correct is the easiest band; 0 or 1 is the hardest.

    Five attempts give six possible scores and the page shows five levels, so
    0 and 1 share the hardest band -- the distinction between "never" and
    "once in five" is inside the noise of five samples anyway.
    """
    return {5: 1, 4: 2, 3: 3, 2: 4, 1: 5, 0: 5}[correct]


def main() -> None:
    rows = read_jsonl(CURATION / "03_quality.jsonl")
    cache = load_cache()
    jobs = [
        (row, attempt)
        for row in rows
        for attempt in range(ATTEMPTS)
        if (row["uid"], attempt) not in cache
    ]
    print(
        f"{len(rows)} items x {ATTEMPTS} attempts; {len(cache)} cached, {len(jobs)} to run"
    )

    if jobs:
        started = time.time()
        with (CURATION / "04_probe_cache.jsonl").open("a") as cache_fh:
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for uid, attempt, result in pool.map(
                    run, [(row, attempt, cache_fh) for row, attempt in jobs]
                ):
                    if result is not None:
                        cache[(uid, attempt)] = result
        print(f"  finished {len(jobs)} attempts in {(time.time()-started)/60:.1f} min")

    out: list[dict] = []
    incomplete = 0
    score_hist = collections.Counter()
    level_by_family = collections.defaultdict(collections.Counter)

    for row in rows:
        attempts = [cache.get((row["uid"], i)) for i in range(ATTEMPTS)]
        got = [a for a in attempts if a]
        if len(got) < ATTEMPTS:
            incomplete += 1
            continue
        correct = sum(1 for a in got if a["correct"])
        level = level_for(correct)
        score_hist[correct] += 1
        level_by_family[row["family"]][level] += 1
        out.append(
            {
                **row,
                "probe": {
                    "attempts": ATTEMPTS,
                    "correct": correct,
                    "picks": [a["picked"] for a in got],
                    "golds": [a["gold"] for a in got],
                },
                "level": level,
            }
        )

    n = write_jsonl(CURATION / "04_probe.jsonl", out)
    summary = {
        "probed": len(rows),
        "complete": n,
        "incomplete": incomplete,
        "score_histogram": {f"{k}/5": v for k, v in sorted(score_hist.items())},
        "level_mapping": {"5/5": 1, "4/5": 2, "3/5": 3, "2/5": 4, "0-1/5": 5},
        "level_by_family": {
            fam: dict(sorted(counts.items())) for fam, counts in level_by_family.items()
        },
    }
    (CURATION / "04_probe_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"\ncomplete probes: {n} / {len(rows)} (incomplete {incomplete})")
    print("\nblind score distribution:")
    for score in sorted(score_hist):
        print(f"  {score_hist[score]:5d}  {score}/5 correct  -> L{level_for(score)}")
    print("\nlevel x family:")
    header = "  " + "family".ljust(10) + "".join(f"{f'L{l}':>7s}" for l in range(1, 6))
    print(header)
    for fam, counts in level_by_family.items():
        print("  " + fam.ljust(10) + "".join(f"{counts.get(l, 0):7d}" for l in range(1, 6)))


if __name__ == "__main__":
    main()
