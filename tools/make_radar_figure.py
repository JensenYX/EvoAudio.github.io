#!/usr/bin/env python3.12
"""Three radars comparing training regimes, one per backbone.

The evolution curves above show that the loop improves a model over rounds.
They do not show *why the loop* rather than some cheaper schedule. These
radars answer that: on each backbone, five training regimes are drawn over the
same nine benchmark axes, so the reader can see that the gain is not simply
"more GRPO".

Only three of the paper's five backbones appear. Qwen2.5-Omni, Audio Flamingo 3
and Kimi-Audio carry the full ablation; MiMo-Audio and MiniCPM-o were run with
the base model and EvoAudio (GRPO) only, so a five-way radar for them would be
mostly empty.

Style follows `plot_first_radar.py`: clockwise polar axes, a tick range chosen
per spoke so differences stay legible, soft sector backgrounds per benchmark,
dashed tick contours, and the method of interest drawn in brand blue over
dimmed comparators.

Writes `assets/figures/regimes-wide.svg` (1x3, desktop) and
`assets/figures/regimes-tall.svg` (3x1, narrow screens).
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import numpy as np  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402
from matplotlib.patches import Patch  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT_DIR = REPO / "assets" / "figures"

# Nine axes, grouped by benchmark. Labels stay short because three panels share
# the width of one figure; the sector colour says which benchmark each belongs
# to, which is what disambiguates the two "Percep." spokes.
AXES = [
    ("Percep.", "MMSU"),
    ("Reason.", "MMSU"),
    ("Speech", "MMAU-Pro"),
    ("Sound", "MMAU-Pro"),
    ("Music", "MMAU-Pro"),
    ("Signal", "MMAR"),
    ("Percep.", "MMAR"),
    ("Seman.", "MMAR"),
    ("Culture", "MMAR"),
]

METHODS = [
    "Base",
    "Static-profile GRPO",
    "Pooled GRPO",
    "EvoAudio (SFT)",
    "EvoAudio (GRPO)",
]
HIGHLIGHT = 4  # EvoAudio (GRPO)

# Accuracy (%) from the paper's main table, in AXES order per method.
MODELS = {
    "Qwen2.5-Omni-7B": {
        "Base": [44.5, 79.4, 57.8, 45.3, 64.0, 55.8, 54.0, 67.2, 58.9],
        "Static-profile GRPO": [54.7, 81.9, 61.4, 51.6, 65.9, 58.4, 56.8, 67.3, 62.3],
        "Pooled GRPO": [52.0, 81.1, 61.7, 50.5, 64.7, 56.9, 55.9, 66.6, 61.5],
        "EvoAudio (SFT)": [58.5, 82.9, 62.0, 50.9, 65.2, 55.8, 56.4, 67.2, 61.0],
        "EvoAudio (GRPO)": [61.5, 82.9, 62.9, 51.3, 67.1, 61.6, 57.6, 67.4, 69.4],
    },
    "Audio Flamingo 3 (7B)": {
        "Base": [50.5, 78.1, 56.2, 47.4, 63.1, 57.6, 53.4, 65.6, 55.3],
        "Static-profile GRPO": [54.1, 79.9, 59.1, 52.1, 65.9, 60.6, 54.4, 66.7, 56.7],
        "Pooled GRPO": [52.1, 79.1, 58.2, 49.8, 64.1, 59.5, 53.5, 65.7, 57.8],
        "EvoAudio (SFT)": [56.0, 81.4, 59.3, 53.9, 65.6, 63.5, 54.6, 67.1, 57.8],
        "EvoAudio (GRPO)": [58.0, 81.4, 59.4, 56.1, 66.0, 69.8, 55.2, 68.7, 58.9],
    },
    "Kimi-Audio-7B-Instruct": {
        "Base": [39.0, 74.3, 58.9, 37.1, 56.1, 46.5, 47.3, 63.1, 51.1],
        "Static-profile GRPO": [44.6, 76.9, 63.8, 51.0, 59.5, 54.5, 50.5, 66.4, 57.1],
        "Pooled GRPO": [42.1, 75.6, 61.3, 45.9, 60.4, 50.9, 49.3, 64.4, 56.6],
        "EvoAudio (SFT)": [43.3, 76.3, 62.5, 47.6, 58.7, 52.3, 50.4, 64.9, 55.5],
        "EvoAudio (GRPO)": [45.7, 77.3, 63.8, 56.9, 60.6, 57.0, 51.0, 66.8, 57.6],
    },
}

COLORS = {
    "Base": "#6B7280",
    "Static-profile GRPO": "#8B7355",
    "Pooled GRPO": "#B64342",
    "EvoAudio (SFT)": "#2AA3B8",
    "EvoAudio (GRPO)": "#0b57d0",
}
LINEWIDTHS = [1.3, 1.3, 1.3, 1.5, 2.3]
LINE_ALPHAS = [0.72, 0.72, 0.72, 0.80, 0.98]
FILL_ALPHAS = [0.04, 0.04, 0.04, 0.05, 0.15]
MARKER_SIZES = [12, 12, 12, 14, 26]

GROUP_FILL = {"MMSU": "#DDE7F2", "MMAU-Pro": "#DEEBDE", "MMAR": "#F6E2DD"}
GROUP_INK = {"MMSU": "#1F3A66", "MMAU-Pro": "#2F5E2F", "MMAR": "#7A2E2A"}

R_LO, R_HI = 34.0, 88.0
N_RINGS = 4


def axis_ranges(model: dict) -> list[tuple[float, float]]:
    """Pick a radial window per spoke.

    A shared 0-100 scale would squash every method onto the same ring: the five
    regimes differ by a few points, not by tens. Each spoke therefore gets a
    window anchored below the weakest method and just above the strongest, so
    the polygons separate. The lower anchor keeps a margin so no vertex lands on
    the centre.
    """
    windows = []
    for i in range(len(AXES)):
        values = [model[m][i] for m in METHODS]
        lo, hi = min(values), max(values)
        span = max(hi - lo, 1.5)
        windows.append((lo - 0.55 * span, hi + 0.18 * span))
    return windows


def to_radius(value: float, window: tuple[float, float]) -> float:
    lo, hi = window
    frac = 0.5 if hi <= lo else (value - lo) / (hi - lo)
    return R_LO + (R_HI - R_LO) * float(np.clip(frac, 0.0, 1.0))


def draw_panel(ax, name: str, model: dict, angles: np.ndarray, *, label_size: float) -> None:
    windows = axis_ranges(model)
    closed = np.append(angles, angles[0])

    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    ax.set_facecolor("white")
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim(0, R_HI + 16)

    # Sector background per benchmark, so the nine spokes read as three blocks.
    half = abs(angles[1] - angles[0]) / 2.0
    start = 0
    for i in range(1, len(AXES) + 1):
        if i == len(AXES) or AXES[i][1] != AXES[start][1]:
            a0, a1 = angles[start] - half, angles[i - 1] + half
            ax.bar(
                (a0 + a1) / 2.0,
                R_HI - 0.5,
                width=abs(a1 - a0),
                bottom=0.5,
                color=GROUP_FILL[AXES[start][1]],
                edgecolor="white",
                linewidth=0.8,
                alpha=1.0,
                zorder=0,
            )
            start = i

    # Tick contours. Radii are uniform because each spoke is independently
    # normalized, so a ring is "the same fraction of this spoke's window".
    for k in range(N_RINGS):
        r = R_LO + (R_HI - R_LO) * k / (N_RINGS - 1)
        outer = k == N_RINGS - 1
        ax.plot(
            closed,
            np.full(len(closed), r),
            color="#3A3A3A" if outer else "#9A9A9A",
            linewidth=0.9 if outer else 0.5,
            linestyle="-" if outer else (0, (2, 2)),
            zorder=2,
        )
    for a in angles:
        ax.plot([a, a], [0, R_HI], color="#B5B5B5", linewidth=0.5, zorder=2)

    for index, method in enumerate(METHODS):
        is_top = index == HIGHLIGHT
        radii = np.array([to_radius(v, w) for v, w in zip(model[method], windows)])
        ax.plot(
            closed,
            np.append(radii, radii[0]),
            color=COLORS[method],
            linewidth=LINEWIDTHS[index],
            alpha=LINE_ALPHAS[index],
            solid_joinstyle="round",
            zorder=7 if is_top else 4,
        )
        ax.fill(
            closed,
            np.append(radii, radii[0]),
            color=COLORS[method],
            alpha=FILL_ALPHAS[index],
            zorder=6 if is_top else 3,
        )
        ax.scatter(
            angles,
            radii,
            s=MARKER_SIZES[index],
            color=COLORS[method],
            edgecolors="white" if is_top else "none",
            linewidths=0.8 if is_top else 0,
            alpha=1.0 if is_top else 0.8,
            zorder=8 if is_top else 5,
        )

    # Spoke labels, pinned outward so they never cross the outer ring.
    for angle, (label, group) in zip(angles, AXES):
        sx, sy = np.sin(angle), np.cos(angle)
        ha = "center" if abs(sx) < 0.30 else ("left" if sx > 0 else "right")
        va = "center" if abs(sy) < 0.30 else ("bottom" if sy > 0 else "top")
        ax.text(
            angle,
            R_HI + 5.0,
            label,
            fontsize=label_size,
            ha=ha,
            va=va,
            color=GROUP_INK[group],
            fontweight="bold",
            zorder=9,
            clip_on=False,
        )

    ax.set_title(name, fontsize=label_size + 2.4, fontweight="bold", color="#16233d", pad=26)


def build(layout: str) -> Path:
    n = len(MODELS)
    if layout == "wide":
        fig, axes = plt.subplots(
            1, n, figsize=(13.4, 5.5), subplot_kw={"projection": "polar"}
        )
        label_size = 8.6
        legend_y, top, wspace = 0.985, 0.74, 0.34
    else:
        fig, axes = plt.subplots(
            n, 1, figsize=(5.4, 15.4), subplot_kw={"projection": "polar"}
        )
        label_size = 9.4
        legend_y, top, wspace = 0.992, 0.90, 0.2

    fig.patch.set_facecolor("white")
    # Ascending angles with theta_direction=-1 lays the spokes out clockwise in
    # list order, so the three benchmark blocks read MMSU, MMAU-Pro, MMAR the
    # way they are written. Starting from 2*pi instead would mirror them.
    angles = np.linspace(0, 2 * np.pi, len(AXES), endpoint=False)
    for ax, (name, model) in zip(np.atleast_1d(axes), MODELS.items()):
        draw_panel(ax, name, model, angles, label_size=label_size)

    method_handles = [
        Line2D(
            [0],
            [0],
            color=COLORS[m],
            linewidth=LINEWIDTHS[i] + 0.7,
            marker="o",
            markersize=6 if i == HIGHLIGHT else 5,
            markerfacecolor=COLORS[m],
            markeredgecolor=COLORS[m],
            alpha=max(LINE_ALPHAS[i], 0.75),
            label=m,
        )
        for i, m in enumerate(METHODS)
    ]
    group_handles = [
        Patch(facecolor=GROUP_FILL[g], edgecolor=GROUP_INK[g], linewidth=1.1, label=g)
        for g in ("MMSU", "MMAU-Pro", "MMAR")
    ]

    groups_legend = fig.legend(
        handles=group_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, legend_y),
        ncol=3,
        fontsize=10.5,
        frameon=False,
        handlelength=1.3,
        handleheight=1.0,
        columnspacing=1.6,
        handletextpad=0.5,
    )
    for text, group in zip(groups_legend.get_texts(), ("MMSU", "MMAU-Pro", "MMAR")):
        text.set_color(GROUP_INK[group])
        text.set_fontweight("bold")

    methods_legend = fig.legend(
        handles=method_handles,
        loc="upper center",
        bbox_to_anchor=(0.5, legend_y - 0.052),
        ncol=5 if layout == "wide" else 2,
        fontsize=10.5,
        frameon=False,
        handlelength=2.2,
        columnspacing=1.7,
        handletextpad=0.6,
    )
    for text in methods_legend.get_texts():
        text.set_color("#16233d")
    fig.add_artist(groups_legend)

    fig.subplots_adjust(left=0.05, right=0.95, top=top, bottom=0.03, wspace=wspace, hspace=0.34)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"regimes-{layout}.svg"
    fig.savefig(out, format="svg", facecolor="white", bbox_inches="tight", pad_inches=0.12)
    plt.close(fig)
    return out


def main() -> None:
    matplotlib.rcParams.update(
        {
            # The chart is embedded through <img>, which cannot reach the
            # page's webfonts, so text ships as outlines.
            "svg.fonttype": "path",
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.unicode_minus": False,
        }
    )
    for layout in ("wide", "tall"):
        path = build(layout)
        print(f"wrote {path.relative_to(REPO)}  ({path.stat().st_size/1024:.0f} KB)")

    (OUT_DIR / "regimes-meta.json").write_text(
        json.dumps(
            {
                "source": "paper main results table",
                "models": list(MODELS),
                "methods": METHODS,
                "axes": [f"{g}: {a}" for a, g in AXES],
                "note": "per-spoke radial windows; radius is relative within a spoke",
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
