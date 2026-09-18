#!/usr/bin/env python3.12
"""Stage 7 -- write the page's assets.

Copies each selected clip into `assets/audio/`, computes the 640-point
waveform envelope the player draws (the browser never decodes audio), turns the
generator's construction record into the human-readable evidence lines shown
under each card, and writes `assets/data/demos.json`.

Audio stays lossless 16 kHz mono WAV. There is no ffmpeg on this machine, and a
lossy round-trip would risk the very cues these demos exist to demonstrate --
a page about hearing a 3 dB level difference should not ship the audio through
a psychoacoustic model that discards "inaudible" detail.

Also writes `DATA_CARD.md` (what every stage did) and `REVIEW.md` (a contact
sheet for human veto).
"""

from __future__ import annotations

import collections
import json
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import (  # noqa: E402
    CURATION,
    FAMILY_META,
    FAMILY_ORDER,
    REPO,
    TOOL_META,
    gold_text,
    read_jsonl,
    read_wav,
    waveform_peaks,
)

EMPTY_CELL_NOTE = "No demo at this level in this family yet."

AUDIO_DIR = REPO / "assets" / "audio"
DATA_DIR = REPO / "assets" / "data"
PEAK_BUCKETS = 640

LEVELS = [
    {"level": 1, "name": "Salient", "score_label": ""},
    {"level": 2, "name": "Clear", "score_label": ""},
    {"level": 3, "name": "Moderate", "score_label": ""},
    {"level": 4, "name": "Subtle", "score_label": ""},
    {"level": 5, "name": "Near-threshold", "score_label": ""},
]

# The page states what the slider does and nothing about how the set was built.
DIFFICULTY_NOTE = "Drag to move from the most salient cues to the subtlest."

# Readable names for the internal skill ids.
SKILL_LABEL = {
    "speed_pattern3": "Speaking-rate pattern",
    "pitch_pattern3": "Pitch pattern",
    "volume_pattern3": "Loudness pattern",
    "sentence_intonation": "Sentence intonation",
    "pause_after_word": "Pause placement",
    "syllable_count": "Syllable count",
    "disfluency_type": "Disfluency type",
    "speech_pair_compare": "Utterance pair comparison",
    "final_consonant_match": "Final consonant match",
    "compound_speech_reasoning": "Compound prosody reasoning",
    "speaker_match5": "Speaker identity match",
    "speaker_count": "Speaker count",
    "dialogue_turns": "Dialogue turn count",
    "dialogue_turns_real": "Dialogue turn count (real speech)",
    "speaker_gender": "Speaker gender",
    "language_id": "Language identification",
    "content_qa": "Speech content QA",
    "dialogue_qa": "Dialogue reasoning",
    "speech_semantic_qa_real": "Intent / paraphrase",
    "real_emotion": "Emotion recognition",
    "sound_mixture_real": "Sound mixture",
    "sound_louder_real": "Relative loudness",
    "sound_duration_real": "Event duration",
    "sound_change_real": "Acoustic change",
    "sound_reasoning_real": "Sound cause reasoning",
    "sound_count_real": "Event count",
    "sound_order_real": "Event order",
    "sound_id_real": "Sound identification",
    "audioset_sound_id": "Sound identification (AudioSet)",
    "scene_from_sounds": "Scene inference",
    "speech_in_scene": "Speech within a scene",
    "music_repeat_detection": "Repeated passage",
    "music_order_concat": "Musical segment order",
    "music_segment_louder": "Musical dynamics",
    "music_dynamics_real": "Musical dynamics (real)",
    "music_tempo_change": "Tempo change",
    "music_speed_compare": "Tempo comparison",
    "music_pitch_shift_compare": "Pitch comparison",
    "music_genre_real": "Genre",
    "music_vocals_present": "Vocals present",
    "music_instrument_present": "Instrument identification",
    "long_scene_real": "Long scene QA",
    "multi_clip_crossref": "Cross-clip reference",
    "multi_compare_attr": "Cross-clip comparison",
    "multi_same_speaker": "Same speaker across clips",
    "multi_contains": "Cross-clip presence",
}


def humanize_number(value) -> str:
    if isinstance(value, float):
        return f"{value:.2f}".rstrip("0").rstrip(".")
    return str(value)


def _source_speakers(facts: dict) -> list[str]:
    """Speaker ids the source corpus already carried, in first-heard order."""
    ids: list[str] = []
    for segment in facts.get("segments") or []:
        speaker = (segment.get("truth") or {}).get("speaker")
        if speaker and str(speaker) not in ids:
            ids.append(str(speaker))
    return ids[:6]


def evidence_lines(row: dict) -> list[str]:
    """Turn the construction record into the lines shown under a card.

    Only facts that came out of the generator or an independent measurement are
    used, so every line is traceable to how the audio was made.
    """
    facts = row.get("facts") or {}
    lines: list[str] = []

    # Measurements taken on the rendered audio, which is the strongest evidence.
    metric_names = {
        "rate": "speaking rate (syllables/s)",
        "f0": "fundamental frequency (Hz)",
        "rms": "segment level (dBFS)",
        "centroid": "spectral centroid (Hz)",
        "tempo": "tempo (BPM)",
    }
    for check in facts.get("checks") or []:
        kind = check.get("check")
        if kind == "seg_order" and check.get("values"):
            metric = metric_names.get(check.get("metric"), check.get("metric"))
            values = ", ".join(humanize_number(v) for v in check["values"])
            lines.append(f"measured {metric} per segment: [{values}]")
        elif kind == "tempo_dir" and check.get("tempo"):
            values = ", ".join(humanize_number(v) for v in check["tempo"])
            lines.append(f"measured tempo (BPM) per half: [{values}]")
        elif kind == "bg_below":
            lines.append(
                f"background at {humanize_number(check.get('bg_rms'))} dBFS sits under "
                f"the foreground at {humanize_number(check.get('event_min_rms'))} dBFS"
            )
        elif kind == "pause_gap" and check.get("gaps"):
            spans = ", ".join(
                f"{float(a):.2f}\u2013{float(b):.2f}s" for a, b in check["gaps"][:3]
            )
            lines.append(f"measured silence in the rendered audio at {spans}")

    # The construction parameters themselves.
    if facts.get("pattern"):
        lines.append(f"constructed pattern: {facts['pattern']}")
    if facts.get("levels"):
        lines.append("segment levels as built: " + " - ".join(map(str, facts["levels"])))
    knobs = row.get("knobs") or {}
    for key, label in (
        ("ratio", "speaking-rate ratio applied"),
        ("factor", "time-stretch factor applied"),
        ("semitones", "pitch shift applied (semitones)"),
        ("db", "level step applied (dB)"),
        ("gap", "silence gap inserted (s)"),
        ("background_snr_db", "background mixed at SNR (dB)"),
        ("snr_db", "background mixed at SNR (dB)"),
    ):
        value = knobs.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            lines.append(f"{label}: {humanize_number(round(float(value), 2))}")

    for key, label in (
        ("word", "synthesized word"),
        ("syllables", "syllable count from the script"),
        ("final_ipa", "final consonant (IPA)"),
        ("language", "TTS language"),
        ("gender", "voice gender on record"),
        ("genre", "source genre label"),
        ("instrument", "source instrument label"),
        ("emotion", "corpus emotion label"),
        ("scene", "scene as composed"),
        ("label", "source label"),
        ("background_label", "background source"),
        ("background", "background source"),
    ):
        if facts.get(key):
            lines.append(f"{label}: {facts[key]}")

    # Pause construction: which word the gap follows and how long it is.
    if facts.get("pause_after"):
        pause_sec = facts.get("pause_sec")
        length = f", {humanize_number(round(float(pause_sec), 2))} s long" if pause_sec else ""
        lines.append(f"silence inserted after the word \u201c{facts['pause_after']}\u201d{length}")

    # Speaker and turn structure, which is the answer for the counting tasks.
    if isinstance(facts.get("speakers"), int):
        lines.append(f"distinct speakers as cast: {facts['speakers']}")
    if isinstance(facts.get("turns"), int):
        lines.append(f"dialogue turns as composed: {facts['turns']}")
    if facts.get("speaker_counts"):
        counts = ", ".join(str(c) for c in facts["speaker_counts"])
        lines.append(f"speakers per clip as cast: [{counts}]")
    if isinstance(facts.get("answer_clip"), int):
        lines.append(f"the clip that carries the answer: clip {facts['answer_clip'] + 1}")
    if isinstance(facts.get("voices"), dict) and facts["voices"]:
        cast = ", ".join(f"{role} = {voice}" for role, voice in list(facts["voices"].items())[:5])
        lines.append(f"TTS voices cast per role: {cast}")
    if facts.get("excerpts") and isinstance(facts["excerpts"], dict):
        spans = ", ".join(
            f"{name} at {humanize_number(round(float(info.get('offset', 0)), 2))}s"
            for name, info in list(facts["excerpts"].items())[:4]
            if isinstance(info, dict)
        )
        if spans:
            lines.append(f"source excerpts taken from: {spans}")
    if facts.get("same_clip_b") is True:
        lines.append("the repeated segments are the same source excerpt, reused")

    # Source material identity.
    speaker_ids = _source_speakers(facts)
    if speaker_ids:
        lines.append("source recording speaker ids: " + ", ".join(speaker_ids))
    # The `evo4` run records its construction differently: per-source levels
    # keyed by slot id, spans instead of segments, and corpus clip ids.
    rms = facts.get("source_rms_dbfs")
    if isinstance(rms, dict) and len(rms) > 1:
        levels = ", ".join(
            f"{slot} {humanize_number(round(float(value), 1))}"
            for slot, value in sorted(rms.items())
            if isinstance(value, (int, float))
        )
        if levels:
            lines.append(f"source levels as mixed (dBFS): {levels}")
    spans = facts.get("spans")
    if isinstance(spans, dict) and len(spans) > 1:
        rendered = ", ".join(
            f"{slot} {float(span[0]):.2f}\u2013{float(span[1]):.2f}s"
            for slot, span in sorted(spans.items())
            if isinstance(span, (list, tuple)) and len(span) == 2
        )
        if rendered:
            lines.append(f"segment placement on the timeline: {rendered}")
    transcripts = facts.get("transcripts")
    if isinstance(transcripts, dict) and transcripts:
        joined = "  /  ".join(
            f"\u201c{str(text)[:90]}\u201d" for _, text in sorted(transcripts.items())
        )
        lines.append(f"scripted lines: {joined[:300]}")
    for key, label in (
        ("dialogue_id", "source dialogue"),
        ("clip_id", "source clip"),
        ("source", "source corpus"),
        ("script_id", "source script"),
    ):
        if facts.get(key):
            lines.append(f"{label}: {facts[key]}")
    if isinstance(facts.get("speakers"), list) and facts["speakers"]:
        lines.append(
            "speakers as cast: " + ", ".join(str(s) for s in facts["speakers"][:6])
        )
    if isinstance(facts.get("genders"), list) and any(facts["genders"]):
        lines.append(
            "voice genders on record: "
            + ", ".join(str(g) for g in facts["genders"] if g)
        )

    if facts.get("clip_labels"):
        lines.append("clip source labels: " + ", ".join(map(str, facts["clip_labels"])))
    if facts.get("cues"):
        lines.append("scene cues layered in: " + ", ".join(map(str, facts["cues"])))
    if facts.get("onsets"):
        onsets = ", ".join(f"{float(t):.2f}s" for t in facts["onsets"][:8])
        lines.append(f"event onsets on the timeline: [{onsets}]")

    # Drop duplicates while keeping order, and keep the card readable.
    seen = set()
    unique = []
    for line in lines:
        if line not in seen:
            seen.add(line)
            unique.append(line)
    return unique[:7]


def transcript_of(row: dict) -> str:
    """The script the TTS was asked to say, when the item has one."""
    texts: list[str] = []
    for segment in (row.get("facts") or {}).get("segments") or []:
        truth = segment.get("truth") or {}
        text = truth.get("text")
        if text and text not in texts:
            texts.append(str(text))
    return "  /  ".join(f"\u201c{t}\u201d" for t in texts[:4])


def main() -> None:
    rows = read_jsonl(CURATION / "06_selected.jsonl")
    if not rows:
        sys.exit("nothing selected; run the earlier stages first")

    if AUDIO_DIR.exists():
        shutil.rmtree(AUDIO_DIR)
    AUDIO_DIR.mkdir(parents=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    demos: list[dict] = []
    seen_ids: set[str] = set()
    total_bytes = 0

    for row in rows:
        # Stable, readable id: family, level, skill, and a short hash tail.
        base = f"{row['family']}-l{row['level']}-{row['skill'].replace('_','-')}"
        demo_id = base
        suffix = 2
        while demo_id in seen_ids:
            demo_id = f"{base}-{suffix}"
            suffix += 1
        seen_ids.add(demo_id)

        target_dir = AUDIO_DIR / row["family"] / demo_id
        target_dir.mkdir(parents=True, exist_ok=True)

        clips = []
        for index, source in enumerate(row["audio"], start=1):
            name = "clip.wav" if len(row["audio"]) == 1 else f"clip{index}.wav"
            destination = target_dir / name
            shutil.copyfile(source, destination)
            total_bytes += destination.stat().st_size
            samples, sample_rate = read_wav(str(destination))
            clips.append(
                {
                    "url": f"assets/audio/{row['family']}/{demo_id}/{name}",
                    "duration_sec": round(samples.size / sample_rate, 3),
                    "sample_rate": sample_rate,
                    "peaks": waveform_peaks(samples, PEAK_BUCKETS),
                }
            )

        demos.append(
            {
                "id": demo_id,
                "family": row["family"],
                "level": row["level"],
                "skill": row["skill"],
                "skill_label": SKILL_LABEL.get(row["skill"], row["skill"]),
                "question": row["question"],
                "options": [{"id": o["id"], "text": o["text"]} for o in row["options"]],
                "answer": row["answer"],
                "answer_text": gold_text(row),
                "duration_sec": round(sum(c["duration_sec"] for c in clips), 2),
                "clips": clips,
                "tools": [
                    {
                        "id": tool,
                        "label": TOOL_META[tool]["label"],
                        "core": bool(TOOL_META[tool]["core"]),
                    }
                    for tool in row["tools"]
                ],
                "n_tools": row["n_tools"],
                "transcript": transcript_of(row),
                "evidence": evidence_lines(row),
                # Kept out of the rendered card; useful when reviewing the set.
                "audit": {
                    "quality_mean": row["quality"]["mean_quality"],
                    "difficulty_score": row.get("difficulty_score"),
                    "heard": row["quality"]["pass_a"]["heard"],
                },
            }
        )

    # How many verified candidates existed per cell, so a thin cell on the page
    # can say *why* it is thin instead of implying the audio was not good enough.
    verified_counts: dict[str, collections.Counter] = collections.defaultdict(
        collections.Counter
    )
    verified_path = CURATION / "05_verified.jsonl"
    if verified_path.exists():
        for row in read_jsonl(verified_path):
            verified_counts[row["family"]][row["level"]] += 1

    families = []
    for family in FAMILY_ORDER:
        if not any(d["family"] == family for d in demos):
            continue
        counts = verified_counts.get(family, collections.Counter())
        families.append(
            {
                "id": family,
                "name": FAMILY_META[family]["name"],
                "blurb": FAMILY_META[family]["blurb"],
                "verified_per_level": {str(lvl): counts.get(lvl, 0) for lvl in range(1, 6)},
            }
        )

    total_seconds = sum(d["duration_sec"] for d in demos)
    payload = {
        "generated_note": "Built by tools/01..07 in this repository; see DATA_CARD.md.",
        "families": families,
        "levels": LEVELS,
        "default_level": 3,
        "difficulty_note": DIFFICULTY_NOTE,
        "empty_cell_note": EMPTY_CELL_NOTE,
        # The strip under the abstract describes the *system*: the tool library
        # and question-type counts are the paper's, not this page's subset.
        "system": {
            "question_types": 47,
            "audio_tools": 24,
            "families": 6,
            "evolution_rounds": 13,
        },
        "summary": {
            "n_demos": len(demos),
            "n_skills": len({d["skill"] for d in demos}),
            "n_tools": len({t["id"] for d in demos for t in d["tools"]}),
            "total_minutes": round(total_seconds / 60, 1),
            "mean_quality": round(
                sum(d["audit"]["quality_mean"] for d in demos) / len(demos), 2
            ),
        },
        "demos": demos,
    }
    (DATA_DIR / "demos.json").write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":"))
    )

    write_data_card(rows, demos, total_bytes)
    write_review_sheet(rows, demos)

    print(f"exported {len(demos)} demos")
    print(f"  audio: {total_bytes/1024/1024:.1f} MB in {AUDIO_DIR.relative_to(REPO)}")
    print(f"  index: {(DATA_DIR/'demos.json').stat().st_size/1024:.0f} KB")
    print(f"  {payload['summary']['n_skills']} question types, "
          f"{payload['summary']['n_tools']} tools, "
          f"{payload['summary']['total_minutes']} min of audio")


def _stage_summary(name: str) -> dict:
    path = CURATION / name
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def write_data_card(rows: list[dict], demos: list[dict], total_bytes: int) -> None:
    pool = _stage_summary("01_pool_summary.json")
    screen = _stage_summary("02_screen_summary.json")
    short = _stage_summary("02b_shortlist_summary.json")
    quality = _stage_summary("03_quality_summary.json")
    probe = _stage_summary("04_probe_summary.json")
    verify = _stage_summary("05_verify_summary.json")
    select = _stage_summary("06_select_summary.json")

    grid = select.get("grid", {})
    grid_rows = []
    for family in FAMILY_ORDER:
        counts = grid.get(family, {})
        cells = " | ".join(str(counts.get(str(lvl), counts.get(lvl, 0))) for lvl in range(1, 6))
        grid_rows.append(f"| {FAMILY_META[family]['name']} | {cells} | {sum(counts.values())} |")

    lines = [
        "# Demo data card",
        "",
        "How the audio on this page was chosen, stage by stage. Every number "
        "below is written by the scripts in `tools/`; the machine-readable "
        "summaries live in `curation/*_summary.json`.",
        "",
        "## Why a selection pipeline at all",
        "",
        "EvoAudio generates training data at scale and much of it is not fit "
        "for a demo page. On a 48-item random sample of already-gated "
        "candidates, an early blind listening audit returned 21% showcase, 33% "
        "acceptable and 46% reject, with audible distortion, abrupt cuts, "
        "robotic synthesis and one clip that was pure silence. The pipeline is "
        "therefore built to discard most of what it sees.",
        "",
        "That first 21% was pessimistic for one avoidable reason: the draft "
        "rubric counted deliberate structure as damage. Many question types are "
        "*built* by concatenating unrelated segments -- that is the item, not a "
        "flaw -- and the draft was rejecting them for \"obvious splices\", along "
        "with marking sound-event clips down for containing no speech. The "
        "production rubric states the intended segment count up front and asks "
        "whether each join is *clean* rather than whether a join exists. With "
        f"that corrected, {quality.get('kept','-')} of "
        f"{quality.get('audited','-')} shortlisted candidates "
        f"({round(100*(quality.get('showcase_rate') or 0))}%) came back "
        "showcase-grade from both passes.",
        "",
        "## Stages",
        "",
        "| Stage | In | Out | Gate |",
        "| --- | --- | --- | --- |",
        f"| 1. Metadata gates | {pool.get('scanned','-')} | {pool.get('kept','-')} | "
        "audio present, acoustic checks hold (incl. `measured_ok`), not answerable "
        "from the question text alone, 1-60 s, at least 3 tools and 2 core transforms, deduplicated |",
        f"| 2. Signal screen | {screen.get('screened','-')} | {screen.get('kept','-')} | "
        "inaudible level, dead HF band, DC offset, unexplained dead air, clip "
        "starting/ending mid-sound, clicks at declared seams |",
        f"| 2b. Stratified shortlist | {short.get('screened_input','-')} | "
        f"{short.get('shortlisted','-')} | rare skills taken whole, artifact-prone "
        "skills over-sampled, spread over contrast bands and clip lengths |",
        f"| 3. Two blind listening audits | {quality.get('audited','-')} | "
        f"{quality.get('kept','-')} | both passes: quality >= 4/5, no artifact, "
        "clean joins, speech not robotic, at least one pass would showcase it |",
        f"| 4. Difficulty probe | {probe.get('probed','-')} | {probe.get('complete','-')} | "
        "5 blind attempts, options reshuffled each time, temperature 1.0 |",
        f"| 5. Informed correctness audit | {verify.get('input','-')} | "
        f"{verify.get('kept','-')} | both passes: cue audible, intended answer "
        "defensible and unique |",
        f"| 6. Diversity-constrained selection | {select.get('verified_input','-')} | "
        f"{select.get('selected','-')} | no repeated skill or tool combination per "
        "cell until forced, clip-length spread per family, quality breaks ties |",
        "",
        "## What shipped",
        "",
        f"- **{len(demos)} demos**, {len({d['skill'] for d in demos})} of the "
        f"system's question types, {len({t['id'] for d in demos for t in d['tools']})} distinct tools",
        f"- {round(sum(d['duration_sec'] for d in demos)/60, 1)} minutes of audio, "
        f"{total_bytes/1024/1024:.1f} MB as lossless 16 kHz mono WAV",
        f"- mean audited audio quality {select.get('mean_quality','-')}/5",
        "",
        "| Family | L1 | L2 | L3 | L4 | L5 | Total |",
        "| --- | --- | --- | --- | --- | --- | --- |",
        *grid_rows,
        "",
    ]

    if select.get("short_cells"):
        lines += [
            "### Cells that shipped short",
            "",
            "No cell was padded with weaker audio. Where the verified pool could "
            "not fill five slots, the page says so:",
            "",
            *[f"- {cell}" for cell in select["short_cells"]],
            "",
        ]

    lines += [
        "## Difficulty",
        "",
        "No single model defines difficulty. The auditor is strong enough that "
        "answering correctly says little about whether an item is easy, and when "
        "it answers wrongly the cause is often a broken item rather than a hard "
        "one -- which is why difficulty is computed only after verification. "
        "The score combines how often the audio LLM under training missed the "
        "item, how often the auditor missed it under repeated blind attempts, "
        "the generator's own cue-salience setting, how far the background masks "
        "the foreground, and how much there is to hold in mind. Scores are "
        "ranked within each family and cut into five equal bands.",
        "",
        "Signal weights: "
        + ", ".join(
            f"{k} {v}" for k, v in (select.get("difficulty") or {}).get("weights", {}).items()
        ),
        "",
        "| Level | Band |",
        "| --- | --- |",
        *[
            f"| L{entry['level']} {entry['name']} | "
            f"{'easiest' if entry['level'] == 1 else 'hardest' if entry['level'] == 5 else 'middle'} "
            f"fifth of the family's verified pool |"
            for entry in LEVELS
        ],
        "",
        "Auditor blind-score distribution over the probed pool (one input among "
        "several, not the level itself): "
        + ", ".join(f"{k} -> {v}" for k, v in (probe.get("score_histogram") or {}).items()),
        "",
        "## Role of the auditing model",
        "",
        "Gemini 3.5 Flash is used only as a listening instrument: it rates audio "
        "quality, measures difficulty, and checks that the constructed answer "
        "survives rendering. It never supplies an answer. Every label on the "
        "page comes from the construction record of the audio itself, which is "
        "the property that makes EvoAudio's supervision verifiable.",
        "",
        "## Reproducing",
        "",
        "```bash",
        "python3.12 tools/01_scan_pool.py",
        "python3.12 tools/02_signal_screen.py",
        "python3.12 tools/02b_shortlist.py",
        "python3.12 tools/03_gemini_quality.py      # resumable, cached",
        "python3.12 tools/04_gemini_probe.py        # resumable, cached",
        "python3.12 tools/05_gemini_correctness.py  # resumable, cached",
        "python3.12 tools/06_select.py",
        "python3.12 tools/07_export.py",
        "python3.12 tools/make_evolution_figure.py",
        "```",
        "",
        "The three Gemini stages cache every call in `curation/*_cache.jsonl` and "
        "skip what is already done, so an interrupted run can simply be "
        "restarted. Credentials come from `EVOAUDIO_GEMINI_APP_ID` and "
        "`EVOAUDIO_GEMINI_APP_KEY`.",
        "",
    ]
    (REPO / "DATA_CARD.md").write_text("\n".join(lines))


def write_review_sheet(rows: list[dict], demos: list[dict]) -> None:
    """A contact sheet: skim every shipping demo and veto anything unwanted."""
    # `demos` was built by iterating `rows` in order, so the two line up.
    paired = list(zip(demos, rows))
    paired.sort(key=lambda pair: (pair[0]["family"], pair[0]["level"]))

    lines = [
        "# Review sheet",
        "",
        f"All {len(demos)} shipping demos, grouped by family and difficulty, with "
        "what the two listening audits reported. Anything listed here can be "
        "removed by deleting its id from `curation/06_selected.jsonl` and re-running "
        "`tools/07_export.py`.",
        "",
    ]

    current = None
    for demo, row in paired:
        key = (demo["family"], demo["level"])
        if key != current:
            current = key
            lines += [
                "",
                f"## {FAMILY_META[demo['family']]['name']} \u2014 L{demo['level']}",
                "",
            ]
        quality = row["quality"]
        verify = row.get("verify") or {}
        report = verify.get("report") or {}
        judgement = verify.get("judgement") or {}
        lines += [
            f"### `{demo['id']}`",
            "",
            f"- **Question** {demo['question']}",
            f"- **Answer** {demo['answer']}. {demo['answer_text']}",
            f"- **Audio** [{demo['clips'][0]['url']}]({demo['clips'][0]['url']})"
            + (f" (+{len(demo['clips'])-1} more clips)" if len(demo["clips"]) > 1 else "")
            + f" \u00b7 {demo['duration_sec']}s \u00b7 {demo['n_tools']} tools",
            f"- **Quality** pass A {quality['pass_a']['quality']}/5 "
            f"({quality['pass_a']['verdict']}), pass B {quality['pass_b']['quality']}/5 "
            f"({quality['pass_b']['verdict']})",
            f"- **Heard, blind** {report.get('summary', '')}",
            f"- **Why the answer stands** {judgement.get('reason', '')}",
            f"- **Difficulty** score {row.get('difficulty_score')} "
            f"(auditor answered {row['probe']['correct']}/{row['probe']['attempts']} blind, "
            f"training solver {row.get('parent_pass_rate')})",
            "",
        ]
    (REPO / "REVIEW.md").write_text("\n".join(lines))


if __name__ == "__main__":
    main()
