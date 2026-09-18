#!/usr/bin/env python3.12
"""Stage 2 -- signal-level screen.

Every candidate's waveform is measured locally before any API call, so the paid
listening passes only ever see audio that is not obviously broken.

Thresholds were calibrated on a 600-item sample of the pool. Two findings shape
them. First, the generators already peak-limit (peak caps at 0.89) and
loudness-normalize (RMS sits at -22 dBFS), so clipping is a non-issue and is
only checked as a tripwire. Second, a global sample-to-sample jump threshold is
useless at 16 kHz -- it flagged 74% of clips -- so concatenation clicks are
instead measured *at the seams* the construction timeline declares, against the
local noise floor of the same clip.

Writes `curation/02_screened.jsonl` plus a rejection log.
"""

from __future__ import annotations

import collections
import json
import os
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from common import CURATION, read_jsonl, read_wav, write_jsonl  # noqa: E402

# --- thresholds ------------------------------------------------------------
MIN_PEAK = 0.05            # below this the clip is inaudible at normal volume
MIN_RMS_DB = -45.0         # overall level floor
MAX_SILENCE_FRAC = 0.50    # share of frames far below the clip's own level
MAX_UNEXPLAINED_GAP = 1.5  # seconds of dead air the timeline does not explain
EDGE_MS = 5.0              # window used to spot an abrupt start/end
EDGE_MARGIN_DB = 6.0       # edge energy this close to full level == hard cut
MIN_HF_FRACTION = 1e-4     # energy above 6 kHz; below this the band is dead
MAX_DC = 0.01
SEAM_JUMP_RATIO = 8.0      # seam jump vs. the clip's own jump distribution
SEAM_JUMP_ABS = 0.08       # and it has to be audible in absolute terms
MAX_CLIP_FRACTION = 1e-3

FRAME_SEC = 0.02


def _frame_db(x: np.ndarray, sr: int) -> np.ndarray:
    n = int(FRAME_SEC * sr)
    if n <= 0 or x.size < n:
        return np.array([])
    frames = x[: (x.size // n) * n].reshape(-1, n)
    return 20 * np.log10(np.sqrt(np.mean(frames ** 2, axis=1)) + 1e-12)


def _longest_dead_run(frame_db: np.ndarray, floor_db: float) -> float:
    """Longest stretch of frames under `floor_db`, in seconds."""
    if frame_db.size == 0:
        return 0.0
    dead = frame_db < floor_db
    best = run = 0
    for flag in dead:
        run = run + 1 if flag else 0
        best = max(best, run)
    return best * FRAME_SEC


def _intended_gap_budget(facts: dict) -> float:
    """Longest silence the construction record says should be there."""
    budget = 0.0
    knobs_gap = facts.get("gap")
    if isinstance(knobs_gap, (int, float)):
        budget = max(budget, float(knobs_gap))
    segments = [s for s in (facts.get("segments") or []) if s.get("role") == "part"]
    segments.sort(key=lambda s: s.get("start", 0.0))
    for prev, nxt in zip(segments, segments[1:]):
        gap = float(nxt.get("start", 0.0)) - float(prev.get("end", 0.0))
        budget = max(budget, gap)
    # Leading silence before the first segment counts too.
    if segments:
        budget = max(budget, float(segments[0].get("start", 0.0)))
    return budget


def _seam_times(facts: dict) -> list[float]:
    """Boundaries where two rendered pieces were joined."""
    times = set()
    for seg in facts.get("segments") or []:
        if seg.get("role") not in ("part", "event"):
            continue
        for key in ("start", "end"):
            value = seg.get(key)
            if isinstance(value, (int, float)) and value > 0.01:
                times.add(round(float(value), 3))
    return sorted(times)


def _worst_seam(x: np.ndarray, sr: int, seams: list[float]) -> float:
    """Largest seam jump expressed as a multiple of the clip's typical jump."""
    if x.size < sr // 10 or not seams:
        return 0.0
    diff = np.abs(np.diff(x))
    typical = float(np.percentile(diff, 99.5)) + 1e-9
    worst = 0.0
    half = max(int(0.002 * sr), 2)
    for t in seams:
        centre = int(t * sr)
        lo, hi = max(centre - half, 0), min(centre + half, diff.size)
        if hi <= lo:
            continue
        local = float(np.max(diff[lo:hi]))
        if local < SEAM_JUMP_ABS:
            continue
        worst = max(worst, local / typical)
    return worst


def measure(path: str, facts: dict) -> dict:
    x, sr = read_wav(path)
    out: dict[str, float | bool | str] = {"sr": sr, "samples": int(x.size)}
    if x.size == 0:
        out["fatal"] = "empty_file"
        return out

    peak = float(np.max(np.abs(x)))
    rms = float(np.sqrt(np.mean(x ** 2)))
    rms_db = 20 * np.log10(rms + 1e-12)
    out.update(
        peak=round(peak, 4),
        rms_db=round(rms_db, 2),
        dc=round(float(np.mean(x)), 5),
        clip_frac=round(float(np.mean(np.abs(x) >= 0.999)), 6),
        duration=round(x.size / sr, 3),
    )

    fdb = _frame_db(x, sr)
    if fdb.size:
        out["silence_frac"] = round(float(np.mean(fdb < rms_db - 35)), 4)
        out["longest_dead_sec"] = round(_longest_dead_run(fdb, max(rms_db - 45, -70)), 2)
    else:
        out["silence_frac"] = 0.0
        out["longest_dead_sec"] = 0.0

    edge = max(int(EDGE_MS / 1000 * sr), 1)
    if x.size > 4 * edge:
        head = 20 * np.log10(np.sqrt(np.mean(x[:edge] ** 2)) + 1e-12) - rms_db
        tail = 20 * np.log10(np.sqrt(np.mean(x[-edge:] ** 2)) + 1e-12) - rms_db
        out["head_rel_db"] = round(float(head), 2)
        out["tail_rel_db"] = round(float(tail), 2)
    else:
        out["head_rel_db"] = out["tail_rel_db"] = -99.0

    window = x[: sr * 10] if x.size > sr * 10 else x
    spectrum = np.abs(np.fft.rfft(window)) ** 2
    freqs = np.fft.rfftfreq(window.size, 1 / sr)
    total = float(spectrum.sum()) + 1e-12
    out["hf_frac"] = round(float(spectrum[freqs > 6000].sum() / total), 6)

    out["seam_ratio"] = round(_worst_seam(x, sr, _seam_times(facts)), 2)
    out["intended_gap"] = round(_intended_gap_budget(facts), 2)
    return out


def verdict(metrics: list[dict], facts: dict) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    for m in metrics:
        if m.get("fatal"):
            reasons.append(str(m["fatal"]))
            continue
        if m["peak"] < MIN_PEAK:
            reasons.append("inaudible_peak")
        if m["rms_db"] < MIN_RMS_DB:
            reasons.append("level_too_low")
        if m["clip_frac"] > MAX_CLIP_FRACTION:
            reasons.append("clipping")
        if abs(m["dc"]) > MAX_DC:
            reasons.append("dc_offset")
        if m["silence_frac"] > MAX_SILENCE_FRAC:
            reasons.append("mostly_silent")
        if m["longest_dead_sec"] > max(MAX_UNEXPLAINED_GAP, m["intended_gap"] + 0.4):
            reasons.append("unexplained_dead_air")
        if m["tail_rel_db"] > -EDGE_MARGIN_DB:
            reasons.append("abrupt_tail_cut")
        if m["head_rel_db"] > -EDGE_MARGIN_DB:
            reasons.append("abrupt_head_cut")
        if m["hf_frac"] < MIN_HF_FRACTION:
            reasons.append("dead_high_band")
        if m["seam_ratio"] > SEAM_JUMP_RATIO:
            reasons.append("seam_click")
    return (not reasons), sorted(set(reasons))


def process(row: dict) -> dict:
    try:
        metrics = [measure(p, row.get("facts") or {}) for p in row["audio"]]
    except Exception as exc:  # unreadable / truncated file
        return {**row, "signal": {"ok": False, "reasons": ["unreadable"], "error": str(exc)[:160]}}
    ok, reasons = verdict(metrics, row.get("facts") or {})
    return {**row, "signal": {"ok": ok, "reasons": reasons, "metrics": metrics}}


def main() -> None:
    rows = read_jsonl(CURATION / "01_pool.jsonl")
    print(f"screening {len(rows)} candidates ...")

    results: list[dict] = []
    with ThreadPoolExecutor(max_workers=16) as pool:
        for i, res in enumerate(pool.map(process, rows), 1):
            results.append(res)
            if i % 4000 == 0:
                print(f"  {i}/{len(rows)}")

    kept = [r for r in results if r["signal"]["ok"]]

    reasons = collections.Counter()
    for r in results:
        for reason in r["signal"]["reasons"]:
            reasons[reason] += 1

    n = write_jsonl(CURATION / "02_screened.jsonl", kept)
    by_family = collections.Counter(r["family"] for r in kept)
    summary = {
        "screened": len(results),
        "kept": n,
        "rejected": len(results) - n,
        "reject_reasons": dict(reasons.most_common()),
        "by_family": dict(by_family),
        "distinct_skills": len({r["skill"] for r in kept}),
        "thresholds": {
            "min_peak": MIN_PEAK,
            "min_rms_db": MIN_RMS_DB,
            "max_silence_frac": MAX_SILENCE_FRAC,
            "max_unexplained_gap_sec": MAX_UNEXPLAINED_GAP,
            "edge_margin_db": EDGE_MARGIN_DB,
            "min_hf_fraction": MIN_HF_FRACTION,
            "max_dc": MAX_DC,
            "seam_jump_ratio": SEAM_JUMP_RATIO,
        },
    }
    (CURATION / "02_screen_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False)
    )

    print(f"\nkept {n} / {len(results)}  ({100*n/len(results):.1f}%)")
    print("\nreject reasons (an item can trip several):")
    for reason, count in reasons.most_common():
        print(f"  {count:6d}  {reason}")
    print("\nsurvivors by family:")
    for fam, count in by_family.most_common():
        print(f"  {count:6d}  {fam}")


if __name__ == "__main__":
    main()
