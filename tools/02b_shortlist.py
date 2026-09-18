#!/usr/bin/env python3.12
"""Stage 2b -- stratified shortlist for the paid listening passes.

Roughly four in five raw items are unfit for a demo page, so the shortlist is
sized far above the ~150 that ship. It is built to protect three things the
final page needs and that a random sample would lose:

* **Rare skills.** Several question types have only 17-70 surviving candidates
  (`speech_semantic_qa_real`, `music_instrument_present`, `language_id`, ...).
  Every one of those is taken whole; they are the difference between covering
  the tool library and covering the three skills that happen to be abundant.
* **Artifact-prone skills.** `speed_pattern3` and `pitch_pattern3` are the most
  valuable demos and the most likely to sound broken, so they are over-sampled
  and biased toward moderate transform magnitudes.
* **Spread.** Within a skill, picks are round-robined across contrast bands and
  duration bins rather than taken off the top of one sort order.

Writes `curation/02b_shortlist.jsonl`.
"""

from __future__ import annotations

import collections
import json
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import CURATION, FAMILY_ORDER, read_jsonl, write_jsonl  # noqa: E402

# Families the page is thinnest on get the biggest share of the audit budget.
#
# Speech Content and Speakers get the most because their difficulty spread is
# the narrowest: a strong audio LLM answers semantic speech QA correctly almost
# every time, so hundreds of content candidates collapse onto the easiest level
# and the middle bands have to be mined out of a much larger pool.
FAMILY_BUDGET = {
    "content": 3000,
    "speakers": 2200,
    "prosody": 1600,
    "music": 1600,
    "multi": 1400,
    "sound": 1200,
}

# A skill with no more candidates than this is taken whole.
RARE_SKILL_CEILING = 150

CONTRAST_BANDS = [(0.82, 1.01), (0.66, 0.82), (0.50, 0.66), (0.33, 0.50), (0.0, 0.33)]
DURATION_BINS = [(0.0, 5.0), (5.0, 12.0), (12.0, 25.0), (25.0, 61.0)]


def contrast_band(value: float | None) -> int:
    if value is None:
        return 2
    for i, (lo, hi) in enumerate(CONTRAST_BANDS):
        if lo <= value < hi:
            return i
    return len(CONTRAST_BANDS) - 1


def duration_bin(seconds: float) -> int:
    for i, (lo, hi) in enumerate(DURATION_BINS):
        if lo <= seconds < hi:
            return i
    return len(DURATION_BINS) - 1


def transform_penalty(row: dict) -> float:
    """How likely the item's transform magnitude is to sound damaged.

    Extreme stretch ratios and large pitch shifts are exactly what produced the
    "extreme distortion and inconsistent speech rate" complaints, so they sort
    last without being excluded -- some of them still render cleanly, and the
    listening audit is the arbiter.
    """
    knobs = row.get("knobs") or {}
    penalty = 0.0

    for key in ("ratio", "factor"):
        value = knobs.get(key)
        if isinstance(value, (int, float)) and value > 0:
            # Distance in octaves-of-speed from 1.0; ~0.5 is already drastic.
            magnitude = abs(math.log2(value))
            penalty += max(0.0, magnitude - 0.45) * 4.0

    semitones = knobs.get("semitones")
    if isinstance(semitones, (int, float)):
        penalty += max(0.0, abs(semitones) - 7.0) * 0.35

    db = knobs.get("db")
    if isinstance(db, (int, float)):
        penalty += max(0.0, abs(db) - 18.0) * 0.12

    # Background loud enough to mask the cue.
    snr = knobs.get("background_snr_db")
    if isinstance(snr, (int, float)):
        penalty += max(0.0, 8.0 - snr) * 0.25

    return penalty


def fitness(row: dict) -> float:
    """Higher is a better demo candidate, before anyone has listened."""
    score = 0.0
    score += 1.2 * row["n_core_tools"]     # more of the library on display
    score += 0.4 * row["n_tools"]
    score -= transform_penalty(row)
    metrics = (row.get("signal") or {}).get("metrics") or [{}]
    m = metrics[0]
    # A clip that uses its headroom and is not mostly silence reads better.
    score -= 2.0 * float(m.get("silence_frac") or 0.0)
    if (m.get("hf_frac") or 0.0) > 0.01:
        score += 0.3
    return score


def allocate(budget: int, counts: dict[str, int]) -> dict[str, int]:
    """Split a family budget across its skills, boosting the small ones.

    Weights go as sqrt(count), so an abundant skill does not crowd out the rest,
    then leftovers from capped skills are redistributed.
    """
    remaining = dict(counts)
    quota: dict[str, int] = {s: 0 for s in counts}
    left = budget
    for _ in range(6):
        active = {s: n for s, n in remaining.items() if n > 0}
        if not active or left <= 0:
            break
        total_weight = sum(math.sqrt(n) for n in active.values())
        handed_out = 0
        for skill, available in active.items():
            share = int(left * math.sqrt(available) / total_weight)
            take = min(share, available)
            quota[skill] += take
            remaining[skill] -= take
            handed_out += take
        if handed_out == 0:
            # Budget too small to divide further; hand the rest out round-robin.
            for skill in sorted(active, key=lambda s: -remaining[s]):
                if left - handed_out <= 0:
                    break
                quota[skill] += 1
                remaining[skill] -= 1
                handed_out += 1
        left -= handed_out
    return quota


def pick_spread(rows: list[dict], take: int, rng: random.Random) -> list[dict]:
    """Round-robin across (contrast band, duration bin) cells by fitness."""
    if take >= len(rows):
        return list(rows)
    cells: dict[tuple[int, int], list[dict]] = collections.defaultdict(list)
    for row in rows:
        cells[(contrast_band(row.get("contrast")), duration_bin(row["duration_sec"]))].append(row)
    for bucket in cells.values():
        rng.shuffle(bucket)
        bucket.sort(key=fitness, reverse=True)

    order = sorted(cells)
    chosen: list[dict] = []
    while len(chosen) < take:
        progressed = False
        for key in order:
            bucket = cells[key]
            if bucket:
                chosen.append(bucket.pop(0))
                progressed = True
                if len(chosen) >= take:
                    break
        if not progressed:
            break
    return chosen


def main() -> None:
    rng = random.Random(20260917)
    rows = read_jsonl(CURATION / "02_screened.jsonl")
    print(f"shortlisting from {len(rows)} screened candidates")

    by_family: dict[str, list[dict]] = collections.defaultdict(list)
    for row in rows:
        by_family[row["family"]].append(row)

    shortlist: list[dict] = []
    report: dict[str, dict] = {}

    for family in FAMILY_ORDER:
        pool = by_family.get(family, [])
        if not pool:
            continue
        by_skill: dict[str, list[dict]] = collections.defaultdict(list)
        for row in pool:
            by_skill[row["skill"]].append(row)

        rare = {s: r for s, r in by_skill.items() if len(r) <= RARE_SKILL_CEILING}
        common = {s: r for s, r in by_skill.items() if len(r) > RARE_SKILL_CEILING}

        taken: dict[str, int] = {}
        for skill, candidates in rare.items():
            shortlist.extend(candidates)
            taken[skill] = len(candidates)

        budget = max(FAMILY_BUDGET.get(family, 700) - sum(taken.values()), 0)
        if common:
            quota = allocate(budget, {s: len(r) for s, r in common.items()})
            for skill, want in quota.items():
                if want <= 0:
                    continue
                picked = pick_spread(common[skill], want, rng)
                shortlist.extend(picked)
                taken[skill] = len(picked)

        report[family] = {
            "available": len(pool),
            "shortlisted": sum(taken.values()),
            "rare_skills_taken_whole": sorted(rare),
            "per_skill": dict(sorted(taken.items(), key=lambda kv: -kv[1])),
        }

    rng.shuffle(shortlist)
    n = write_jsonl(CURATION / "02b_shortlist.jsonl", shortlist)

    summary = {
        "screened_input": len(rows),
        "shortlisted": n,
        "family_budget": FAMILY_BUDGET,
        "rare_skill_ceiling": RARE_SKILL_CEILING,
        "by_family": report,
        "distinct_skills": len({r["skill"] for r in shortlist}),
    }
    (CURATION / "02b_shortlist_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"shortlisted {n} candidates across {summary['distinct_skills']} skills\n")
    for family in FAMILY_ORDER:
        if family in report:
            info = report[family]
            print(f"  {family:9s} {info['shortlisted']:5d} / {info['available']:5d} available")
            print(f"            {info['per_skill']}")


if __name__ == "__main__":
    main()
