#!/usr/bin/env python3.12
"""Stage 1 -- build the candidate pool.

Unions the `evo6_sft` training packs (43 skills, the full tool library) with the
already-scanned inventory from the earlier curation run (27 skills), maps every
source family onto the paper's six, and drops items that metadata alone rules
out. Writes `curation/01_pool.jsonl`.
"""

from __future__ import annotations

import collections
import glob
import gzip
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (  # noqa: E402
    CURATION,
    EXEC_OUTPUTS,
    FAMILY_OF_EVO4_SKILL,
    FAMILY_OF_SOURCE,
    LEGACY_INVENTORY,
    audio_paths,
    core_tool_count,
    extract_tools,
    extract_tools_evo4,
    generator_checks_ok,
    option_texts,
    write_jsonl,
)

MIN_DURATION = 1.0
MAX_DURATION = 60.0
MIN_TOOL_TYPES = 3
MIN_CORE_TOOLS = 2

# Runs contributing to the pool. `evo6_sft` carries the full 43-skill library;
# the legacy inventory adds the skills that run does not build (sound counting
# and ordering, long scenes); `evo4` is the only run drawing on real emotional
# speech corpora, which Speech Content needs.
SFT_GLOB = str(EXEC_OUTPUTS / "evo6_sft" / "*" / "pack" / "train_items.jsonl")
EVO4_GLOB = str(EXEC_OUTPUTS / "evo4" / "*" / "pack" / "train_items.jsonl")


def _iter_pack(pattern: str, run: str):
    for path in sorted(glob.glob(pattern)):
        gen = os.path.basename(os.path.dirname(os.path.dirname(path)))
        with open(path) as fh:
            for lineno, line in enumerate(fh):
                line = line.strip()
                if not line:
                    continue
                try:
                    item = json.loads(line)
                except json.JSONDecodeError:
                    continue
                yield item, {
                    "run": run,
                    "generation": gen,
                    "source_file": os.path.relpath(path, EXEC_OUTPUTS.parent.parent),
                    "source_line": lineno,
                }


def iter_sft_items():
    yield from _iter_pack(SFT_GLOB, "evo6_sft")


def iter_evo4_items():
    yield from _iter_pack(EVO4_GLOB, "evo4")


def iter_legacy_items():
    with gzip.open(LEGACY_INVENTORY, "rt") as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            item = row["item"]
            gen = row["uid"].split("__")[-1].split("-")[0] if "__" in row["uid"] else ""
            yield item, {
                "run": row["run"],
                "generation": gen,
                "source_file": row["source_file"],
                "source_line": row["source_line"],
                "legacy_tools": row.get("tools") or [],
            }


def construction_identity(item: dict, tools: list[str]) -> str:
    """Hash what the item *is*, so re-renders of one recipe collapse to one row.

    Question text plus the sorted option set plus the source provenance tree:
    two items that differ only by output filename hash the same.
    """
    facts = item.get("facts") or {}
    payload = json.dumps(
        {
            "q": item.get("question", "").strip().lower(),
            "opts": sorted(o.strip().lower() for o in option_texts(item)),
            "answer": item.get("answer"),
            "sources": item.get("sources"),
            "segments": facts.get("segments"),
            "tools": tools,
        },
        sort_keys=True,
        ensure_ascii=False,
        default=str,
    )
    return hashlib.sha256(payload.encode()).hexdigest()[:24]


def main() -> None:
    rejects = collections.Counter()
    kept: list[dict] = []
    seen_identity: dict[str, str] = {}
    seen_audio: set[str] = set()
    scanned = 0

    for item, prov in (
        list(iter_sft_items()) + list(iter_legacy_items()) + list(iter_evo4_items())
    ):
        scanned += 1
        is_evo4 = prov["run"] == "evo4"

        family = (
            FAMILY_OF_EVO4_SKILL.get(item.get("skill"))
            if is_evo4
            else FAMILY_OF_SOURCE.get(item.get("family"))
        )
        if family is None:
            rejects["unmapped_family"] += 1
            continue

        paths = audio_paths(item)
        if not paths:
            rejects["no_audio_path"] += 1
            continue
        if not all(os.path.exists(p) for p in paths):
            rejects["audio_missing_on_disk"] += 1
            continue

        # The text-only probe: if the question can be answered without the
        # audio, it is not a listening demo. `evo4` predates the recorded
        # pass-rate and instead logs a single text-only attempt, so its items
        # only get a provisional pass here and are re-probed properly in stage
        # 2c before any audio is auditioned.
        verification = item.get("verification") or {}
        if is_evo4:
            leak = verification.get("leak") or {}
            if leak.get("correct") is not False:
                rejects["answerable_without_audio"] += 1
                continue
        else:
            if verification.get("question_only_pass_rate") not in (0, 0.0):
                rejects["answerable_without_audio"] += 1
                continue

        if not generator_checks_ok(item):
            rejects["generator_check_failed"] += 1
            continue

        duration = item.get("duration_sec")
        if not isinstance(duration, (int, float)):
            rejects["no_duration"] += 1
            continue
        if not (MIN_DURATION <= duration <= MAX_DURATION):
            rejects["duration_out_of_range"] += 1
            continue

        options = option_texts(item)
        if len(options) < 3:
            rejects["too_few_options"] += 1
            continue
        normalized = [o.strip().lower() for o in options]
        if len(set(normalized)) != len(normalized):
            rejects["duplicate_options"] += 1
            continue
        if not item.get("answer"):
            rejects["no_answer"] += 1
            continue

        tools = extract_tools_evo4(item) if is_evo4 else extract_tools(item)
        if prov.get("legacy_tools"):
            # The legacy scan already resolved that run's provenance tree; keep
            # whichever view names more tools.
            from common import TOOL_ALIASES, TOOL_META

            legacy = set()
            for name in prov["legacy_tools"]:
                canon = TOOL_ALIASES.get(name, name)
                if canon in TOOL_META:
                    legacy.add(canon)
            if len(legacy) > len(tools):
                tools = sorted(legacy | set(tools))

        if len(tools) < MIN_TOOL_TYPES:
            rejects["too_few_tools"] += 1
            continue
        if core_tool_count(tools) < MIN_CORE_TOOLS:
            rejects["too_few_core_transforms"] += 1
            continue

        identity = construction_identity(item, tools)
        if identity in seen_identity:
            rejects["duplicate_construction"] += 1
            continue
        audio_key = "|".join(sorted(paths))
        if audio_key in seen_audio:
            rejects["duplicate_audio"] += 1
            continue
        seen_identity[identity] = item.get("item_id", "")
        seen_audio.add(audio_key)

        facts = item.get("facts") or {}
        kept.append(
            {
                "uid": f"{prov['run']}__{item.get('item_id') or identity}",
                "identity": identity,
                "family": family,
                "source_family": item.get("family") or f"evo4:{item['skill']}",
                "needs_text_probe": is_evo4,
                "skill": item["skill"],
                "type": item.get("type"),
                "domain": item.get("domain"),
                "question": item["question"],
                "options": item["options"],
                "answer": item["answer"],
                "audio": paths,
                "duration_sec": round(float(duration), 3),
                "n_clips": len(paths),
                "tools": tools,
                "n_tools": len(tools),
                "n_core_tools": core_tool_count(tools),
                "generator_difficulty": item.get("difficulty"),
                "contrast": (item.get("knobs") or {}).get("contrast"),
                "knobs": item.get("knobs") or {},
                "parent_pass_rate": item.get("parent_pass_rate"),
                "checks": facts.get("checks") or [],
                "facts": facts,
                "tts_utts": item.get("tts_utts") or [],
                "provenance": {k: v for k, v in prov.items() if k != "legacy_tools"},
            }
        )

    CURATION.mkdir(parents=True, exist_ok=True)
    n = write_jsonl(CURATION / "01_pool.jsonl", kept)

    by_family = collections.Counter(r["family"] for r in kept)
    by_skill = collections.Counter(r["skill"] for r in kept)
    summary = {
        "scanned": scanned,
        "kept": n,
        "rejects": dict(rejects.most_common()),
        "distinct_skills": len(by_skill),
        "distinct_source_families": len({r["source_family"] for r in kept}),
        "by_family": dict(by_family),
        "by_skill": dict(by_skill.most_common()),
        "gates": {
            "duration_sec": [MIN_DURATION, MAX_DURATION],
            "min_tool_types": MIN_TOOL_TYPES,
            "min_core_transforms": MIN_CORE_TOOLS,
            "question_only_pass_rate": 0,
            "generator_checks": "all ok, measured_ok not false",
        },
    }
    (CURATION / "01_pool_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"scanned {scanned} -> kept {n}")
    print(f"distinct skills: {len(by_skill)}  source families: {summary['distinct_source_families']}")
    print("\nby family:")
    for fam, count in by_family.most_common():
        print(f"  {count:6d}  {fam}")
    print("\nrejects:")
    for reason, count in rejects.most_common():
        print(f"  {count:6d}  {reason}")


if __name__ == "__main__":
    main()
