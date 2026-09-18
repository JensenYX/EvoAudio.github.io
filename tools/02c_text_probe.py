#!/usr/bin/env python3.12
"""Stage 2c -- can the question be answered without listening?

The later runs record a text-only pass rate and stage 1 gates on it; it is the
single most productive gate in the pipeline, removing 18k items whose answer
follows from the wording alone. The `evo4` run predates that field and logs only
one text-only attempt, which is too thin to trust: a four-option question is
guessed correctly 25% of the time, so a single lucky guess would discard a good
item and a single unlucky one would admit a leaky question.

So items flagged `needs_text_probe` are re-probed here properly: three attempts
with the options reshuffled each time, **no audio attached**. An item is dropped
if two or more attempts land on the answer, which is well above chance.

These calls carry no audio, so they are far cheaper than anything downstream,
which is why this runs before the listening audits rather than after.

Writes `curation/02c_probed.jsonl`.
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

WORKERS = 160
ATTEMPTS = 3
MAX_CORRECT = 1  # two or more correct out of three is treated as leakage
LETTERS = "ABCDEFGH"

PROMPT = """Answer this multiple-choice question.

{question}
{options}

You have NOT been given the audio. Choose the option that is most likely
correct from the wording alone. Guess if you have to; do not refuse.
Respond with JSON only: {{"answer": "<letter>"}}"""


_cache_lock = threading.Lock()
_progress_lock = threading.Lock()
_done = 0


def attempt(row: dict, index: int) -> dict | None:
    rng = random.Random(f"{row['uid']}::text::{index}")
    options = list(row["options"])
    rng.shuffle(options)
    gold = LETTERS[next(i for i, o in enumerate(options) if o["id"] == row["answer"])]
    rendered = "\n".join(f"{LETTERS[i]}. {o['text']}" for i, o in enumerate(options))
    prompt = PROMPT.format(question=row["question"], options=rendered)
    for _ in range(3):
        # No audio: the whole point is to see the question in isolation.
        text = gemini_call(prompt, [], temperature=1.0, max_tokens=2048)
        letter = parse_choice_letter(text)
        if letter:
            return {"picked": letter, "gold": gold, "correct": letter == gold}
    return None


def run(args):
    global _done
    row, index, cache_fh = args
    result = attempt(row, index)
    with _cache_lock:
        cache_fh.write(
            json.dumps(
                {"uid": row["uid"], "attempt": index, "result": result},
                ensure_ascii=False,
            )
            + "\n"
        )
        cache_fh.flush()
    with _progress_lock:
        _done += 1
        if _done % 500 == 0:
            print(f"  {_done} text probes done", flush=True)
    return row["uid"], index, result


def load_cache() -> dict[tuple[str, int], dict]:
    path = CURATION / "02c_text_cache.jsonl"
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


def main() -> None:
    rows = read_jsonl(CURATION / "02b_shortlist.jsonl")
    needs = [r for r in rows if r.get("needs_text_probe")]
    passthrough = [r for r in rows if not r.get("needs_text_probe")]
    print(
        f"{len(rows)} shortlisted; {len(passthrough)} already carry a recorded "
        f"text-only rate, {len(needs)} need probing"
    )

    cache = load_cache()
    jobs = [
        (row, index)
        for row in needs
        for index in range(ATTEMPTS)
        if (row["uid"], index) not in cache
    ]
    print(f"{len(cache)} cached, {len(jobs)} probe calls to run")

    if jobs:
        started = time.time()
        with (CURATION / "02c_text_cache.jsonl").open("a") as cache_fh:
            with ThreadPoolExecutor(max_workers=WORKERS) as pool:
                for uid, index, result in pool.map(
                    run, [(row, index, cache_fh) for row, index in jobs]
                ):
                    if result is not None:
                        cache[(uid, index)] = result
        print(f"  finished in {(time.time()-started)/60:.1f} min")

    kept = list(passthrough)
    score_hist = collections.Counter()
    dropped_by_skill = collections.Counter()
    incomplete = 0

    for row in needs:
        results = [cache.get((row["uid"], i)) for i in range(ATTEMPTS)]
        got = [r for r in results if r]
        if len(got) < ATTEMPTS:
            incomplete += 1
            continue
        correct = sum(1 for r in got if r["correct"])
        score_hist[correct] += 1
        if correct > MAX_CORRECT:
            dropped_by_skill[row["skill"]] += 1
            continue
        kept.append({**row, "text_probe": {"attempts": ATTEMPTS, "correct": correct}})

    n = write_jsonl(CURATION / "02c_probed.jsonl", kept)
    summary = {
        "shortlisted": len(rows),
        "probed": len(needs),
        "kept": n,
        "dropped_as_leaky": sum(dropped_by_skill.values()),
        "incomplete": incomplete,
        "attempts": ATTEMPTS,
        "max_correct_allowed": MAX_CORRECT,
        "score_histogram": {f"{k}/{ATTEMPTS}": v for k, v in sorted(score_hist.items())},
        "dropped_by_skill": dict(dropped_by_skill.most_common()),
        "by_family": dict(collections.Counter(r["family"] for r in kept)),
    }
    (CURATION / "02c_text_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"\nkept {n} (of which {len(needs)} were probed here)")
    print(f"dropped as answerable without audio: {summary['dropped_as_leaky']}")
    print("\ntext-only score distribution over probed items:")
    for score in sorted(score_hist):
        flag = "  <- dropped" if score > MAX_CORRECT else ""
        print(f"  {score_hist[score]:5d}  {score}/{ATTEMPTS} correct{flag}")
    if dropped_by_skill:
        print("\nmost leak-prone skills:")
        for skill, count in dropped_by_skill.most_common(10):
            print(f"  {count:5d}  {skill}")


if __name__ == "__main__":
    main()
