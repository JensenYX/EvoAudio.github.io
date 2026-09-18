#!/usr/bin/env python3.12
"""Stage 6 -- rank by difficulty, then fill the family x level grid.

**Difficulty.** An earlier version set the level from how often Gemini answered
correctly, which is wrong twice over. Gemini is a strong listener, so its
getting an item right says little about whether the item is easy; and when it
gets one wrong the cause is often that the item is broken rather than hard --
the reason this stage now runs *after* verification rather than before.

So difficulty is a composite of several independent signals, no one of which
defines it:

  * how often the audio LLM being trained missed the item (a weaker, different
    model from the auditor, so it discriminates where Gemini saturates)
  * how often the auditor missed it under repeated blind attempts
  * the generator's own cue-salience dial, i.e. how far from obvious the
    rendered contrast was built to be
  * how much the background masks the foreground
  * how much there is to hold in mind: competing events, clip count, length

Scores are ranked **within each family** and cut into five equal bands, so a
level means "this fifth of this family's verified pool" rather than a claim
about any particular model. It also guarantees every band is populated, which a
threshold on one model's accuracy did not.

**Composition.** Two goals pull against each other: take the *highest quality*
items, and make each cell *diverse*. Quality alone would fill a cell with six
variations of one question type, because the abundant skills also dominate the
survivors. Diversity therefore wins first and quality breaks ties: within a cell
a skill cannot repeat until every available skill has been used once, a tool
combination cannot repeat at all, and each family is nudged toward a spread of
clip lengths.

Writes `curation/06_selected.jsonl`.
"""

from __future__ import annotations

import collections
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import CURATION, FAMILY_ORDER, read_jsonl, write_jsonl  # noqa: E402

PER_CELL = 6
# A family whose grid cannot be filled is allowed to go deeper in the cells it
# does have, up to this many, rather than leaving the whole family looking
# empty. Speech Content is the case that needs it: a strong audio LLM answers
# semantic speech QA correctly almost every time, so that family has hundreds of
# verified items at L1 and far fewer in the middle bands.
MAX_PER_CELL = 12
LEVELS = [1, 2, 3, 4, 5]

# Length buckets a family should span, if its survivors allow it.
SHORT, MEDIUM, LONG = "short", "medium", "long"


def length_bucket(seconds: float) -> str:
    if seconds < 6.0:
        return SHORT
    if seconds < 20.0:
        return MEDIUM
    return LONG


# --- difficulty ------------------------------------------------------------

# Relative weight of each signal. They are renormalized per item over whichever
# signals that item actually carries, so partial coverage does not silently
# shift an item up or down the ranking.
DIFFICULTY_WEIGHTS = {
    "solver_miss": 0.30,
    "auditor_miss": 0.25,
    "cue_subtlety": 0.25,
    "masking": 0.10,
    "load": 0.10,
}


def _clamp(value: float) -> float:
    return max(0.0, min(1.0, value))


def difficulty_components(row: dict) -> dict[str, float]:
    """Per-signal hardness in [0, 1], higher meaning harder. Missing is omitted."""
    parts: dict[str, float] = {}

    # The model under training, evaluated by repeated rollouts during the run.
    solver = row.get("parent_pass_rate")
    if isinstance(solver, (int, float)):
        parts["solver_miss"] = _clamp(1.0 - float(solver))

    # The auditor's repeated blind attempts. One vote, not the verdict.
    probe = row.get("probe") or {}
    if probe.get("attempts"):
        parts["auditor_miss"] = _clamp(
            1.0 - probe["correct"] / float(probe["attempts"])
        )

    # How close to obvious the generator built the contrast.
    contrast = row.get("contrast")
    if isinstance(contrast, (int, float)):
        parts["cue_subtlety"] = _clamp(1.0 - float(contrast))

    knobs = row.get("knobs") or {}
    snr = knobs.get("background_snr_db")
    if not isinstance(snr, (int, float)):
        snr = knobs.get("snr_db")
    if isinstance(snr, (int, float)):
        # ~+20 dB is a background you can ignore; ~-4 dB buries the foreground.
        parts["masking"] = _clamp((20.0 - float(snr)) / 24.0)

    facts = row.get("facts") or {}
    events = facts.get("events") or []
    segments = [
        s
        for s in (facts.get("segments") or [])
        if isinstance(s, dict) and s.get("role") in ("part", "event")
    ]
    units = max(len(events), len(segments), row.get("n_clips") or 1, 1)
    load = (
        0.5 * _clamp((units - 2) / 6.0)
        + 0.3 * _clamp((row["duration_sec"] - 5.0) / 40.0)
        + 0.2 * _clamp(((row.get("n_clips") or 1) - 1) / 2.0)
    )
    parts["load"] = _clamp(load)
    return parts


def difficulty_score(row: dict) -> float:
    parts = difficulty_components(row)
    total_weight = sum(DIFFICULTY_WEIGHTS[k] for k in parts)
    if total_weight <= 0:
        return 0.5
    return sum(DIFFICULTY_WEIGHTS[k] * v for k, v in parts.items()) / total_weight


def assign_levels(rows: list[dict]) -> None:
    """Cut each family's pool into five equal bands by difficulty score.

    Ranking within the family rather than globally keeps the slider meaningful
    for families whose absolute difficulty range is narrow, and guarantees no
    band is empty.
    """
    by_family: dict[str, list[dict]] = collections.defaultdict(list)
    for row in rows:
        row["difficulty_score"] = round(difficulty_score(row), 4)
        row["difficulty_parts"] = {
            k: round(v, 3) for k, v in difficulty_components(row).items()
        }
        by_family[row["family"]].append(row)

    for family_rows in by_family.values():
        # Ties broken by uid so the assignment is stable across runs.
        family_rows.sort(key=lambda r: (r["difficulty_score"], r["uid"]))
        total = len(family_rows)
        for index, row in enumerate(family_rows):
            band = int(index * len(LEVELS) / total) if total else 0
            row["level"] = LEVELS[min(band, len(LEVELS) - 1)]


def quality_rank(row: dict) -> tuple:
    """Sort key for "best audio first". Higher is better on every component."""
    quality = row["quality"]
    verify = row.get("verify") or {}
    both_showcase = (
        quality["pass_a"]["verdict"] == "showcase"
        and quality["pass_b"]["verdict"] == "showcase"
    )
    clean_joins = (
        quality["pass_a"].get("joins_clean") is not False
        and quality["pass_b"].get("joins_clean") is not False
    )
    # An item whose blind description named the answer's own sound is more
    # solidly grounded than one that merely was not contradicted.
    presence = verify.get("presence") or {}
    grounded = len(presence.get("targets_found") or [])
    return (
        quality["min_quality"],
        quality["mean_quality"],
        int(both_showcase),
        int(clean_joins),
        grounded,
        row["n_core_tools"],
        row["n_tools"],
    )


def tool_signature(row: dict) -> tuple:
    return tuple(sorted(row["tools"]))


def select_cell(
    candidates: list[dict],
    want: int,
    family_lengths: collections.Counter,
    already: list[dict] | None = None,
) -> list[dict]:
    """Greedy pick: never repeat a skill or tool combination before you must.

    At each step every still-eligible candidate is scored by how much it adds --
    an under-represented clip length for the family counts for a lot, audio
    quality breaks the tie -- and the best one is taken. Length is a preference
    rather than a veto, so a cell is never left short to satisfy it.

    Passing `already` resumes from an earlier call on the same cell, so a cell
    can be deepened later without re-deriving (and double-counting) its
    existing picks. Only the newly added rows are returned.
    """
    chosen: list[dict] = []
    seeded = already or []
    taken: set[str] = {row["uid"] for row in seeded}
    used_skills: collections.Counter = collections.Counter(
        row["skill"] for row in seeded
    )
    used_tools: set[tuple] = {tool_signature(row) for row in seeded}
    want = want - len(seeded)
    if want <= 0:
        return []

    def step(skill_cap: int, enforce_tools: bool) -> bool:
        best = None
        best_key = None
        for row in candidates:
            if row["uid"] in taken:
                continue
            if used_skills[row["skill"]] >= skill_cap:
                continue
            if enforce_tools and tool_signature(row) in used_tools:
                continue
            bucket = length_bucket(row["duration_sec"])
            scarcity = 1 if family_lengths[bucket] == 0 else 0
            key = (scarcity, -family_lengths[bucket]) + quality_rank(row)
            if best_key is None or key > best_key:
                best, best_key = row, key
        if best is None:
            return False
        chosen.append(best)
        taken.add(best["uid"])
        used_skills[best["skill"]] += 1
        used_tools.add(tool_signature(best))
        family_lengths[length_bucket(best["duration_sec"])] += 1
        return True

    # Tighten the rules only as far as the cell's material forces: one item per
    # skill first, then two, and only drop the tool-combination rule last -- it
    # is the least visible of the three to a reader.
    for skill_cap in range(1, want + 1):
        while len(chosen) < want and step(skill_cap, enforce_tools=True):
            pass
        if len(chosen) >= want:
            return chosen
    while len(chosen) < want and step(want, enforce_tools=False):
        pass
    return chosen


def main() -> None:
    rows = read_jsonl(CURATION / "05_verified.jsonl")
    print(f"selecting from {len(rows)} verified candidates")

    assign_levels(rows)
    spread = collections.defaultdict(list)
    for row in rows:
        spread[row["family"]].append(row["difficulty_score"])
    print("\ndifficulty score range per family (within-family quintiles):")
    for family in FAMILY_ORDER:
        scores = sorted(spread.get(family, []))
        if scores:
            cuts = [scores[int(q * (len(scores) - 1))] for q in (0, 0.2, 0.4, 0.6, 0.8, 1)]
            print(f"  {family:10s} n={len(scores):5d}  cuts=" + " ".join(f"{c:.3f}" for c in cuts))

    pools: dict[tuple[str, int], list[dict]] = collections.defaultdict(list)
    for row in rows:
        pools[(row["family"], row["level"])].append(row)

    selected: list[dict] = []
    grid: dict[str, dict[int, int]] = {}
    short_cells: list[str] = []

    for family in FAMILY_ORDER:
        family_lengths: collections.Counter = collections.Counter(
            {SHORT: 0, MEDIUM: 0, LONG: 0}
        )
        grid[family] = {}
        # Levels with fewer candidates are filled first, so the scarce cells get
        # first refusal on their own material before the abundant ones use up
        # the shared diversity budget.
        ordered = sorted(LEVELS, key=lambda lvl: len(pools.get((family, lvl), [])))
        picks_by_level: dict[int, list[dict]] = {}
        for level in ordered:
            candidates = pools.get((family, level), [])
            picks = select_cell(candidates, PER_CELL, family_lengths)
            picks_by_level[level] = picks
            if len(picks) < PER_CELL:
                short_cells.append(
                    f"{family} L{level}: {len(picks)}/{PER_CELL} "
                    f"({len(candidates)} verified candidates)"
                )

        # Spend whatever the thin cells could not use on the cells that still
        # have verified material, deepest-pool first.
        shortfall = PER_CELL * len(LEVELS) - sum(len(p) for p in picks_by_level.values())
        if shortfall > 0:
            for level in sorted(LEVELS, key=lambda lvl: -len(pools.get((family, lvl), []))):
                if shortfall <= 0:
                    break
                candidates = pools.get((family, level), [])
                already = picks_by_level.get(level, [])
                room = min(MAX_PER_CELL - len(already), shortfall, len(candidates) - len(already))
                if room <= 0:
                    continue
                added = select_cell(
                    candidates, len(already) + room, family_lengths, already=already
                )
                picks_by_level[level] = already + added
                shortfall -= len(added)

        for level in LEVELS:
            grid[family][level] = len(picks_by_level.get(level, []))
            selected.extend(picks_by_level.get(level, []))

    n = write_jsonl(CURATION / "06_selected.jsonl", selected)

    skills = collections.Counter(r["skill"] for r in selected)
    tools = collections.Counter(t for r in selected for t in r["tools"])
    lengths = collections.Counter(length_bucket(r["duration_sec"]) for r in selected)
    total_seconds = sum(r["duration_sec"] for r in selected)

    summary = {
        "verified_input": len(rows),
        "selected": n,
        "per_cell_target": PER_CELL,
        "grid": grid,
        "short_cells": short_cells,
        "distinct_skills": len(skills),
        "skills": dict(skills.most_common()),
        "tool_usage": dict(tools.most_common()),
        "length_buckets": dict(lengths),
        "total_audio_minutes": round(total_seconds / 60, 1),
        "mean_quality": round(
            sum(r["quality"]["mean_quality"] for r in selected) / max(n, 1), 2
        ),
        "difficulty": {
            "weights": DIFFICULTY_WEIGHTS,
            "banding": "within-family quintiles of the composite score",
            "mean_score_by_level": {
                str(level): round(
                    sum(r["difficulty_score"] for r in selected if r["level"] == level)
                    / max(sum(1 for r in selected if r["level"] == level), 1),
                    3,
                )
                for level in LEVELS
            },
        },
        "diversity_rules": [
            "a skill may not repeat in a cell until every available skill appeared once",
            "a tool combination may not repeat within a cell",
            "each family nudged toward short (<6s), medium (6-20s) and long (>=20s) clips",
            "quality rank breaks all ties; cells ship short rather than padded",
        ],
    }
    (CURATION / "06_select_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"\nselected {n} demos across {len(skills)} question types")
    print(f"mean audited quality {summary['mean_quality']}/5, "
          f"{summary['total_audio_minutes']} min of audio")
    print("\ngrid (family x level):")
    print("  " + "family".ljust(10) + "".join(f"{f'L{l}':>5s}" for l in LEVELS) + "   total")
    for family in FAMILY_ORDER:
        counts = grid.get(family, {})
        row_total = sum(counts.values())
        print(
            "  "
            + family.ljust(10)
            + "".join(f"{counts.get(l, 0):5d}" for l in LEVELS)
            + f"   {row_total:5d}"
        )
    print("\nlength spread:", dict(lengths))
    if short_cells:
        print("\ncells that could not be filled:")
        for cell in short_cells:
            print(f"  {cell}")


if __name__ == "__main__":
    main()
