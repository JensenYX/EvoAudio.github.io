#!/usr/bin/env python3.12
"""Redraw the paper's evolution figure for the web.

Same numbers as Figure 3 in the paper, read straight out of
`fig2_three_benchmarks_data.json`, but retuned for a screen: the page's own
palette, a lighter grid, bigger type, and a legend that reads as one row.

Two files are written, because one 2x2 chart scaled down to phone width leaves
unreadable axis labels:

    assets/figures/evolution-wide.svg   2 x 2, for desktop
    assets/figures/evolution-tall.svg   1 x 4, for narrow screens

Text is converted to paths so the chart renders identically regardless of which
fonts the viewer has, which matters because an <img>-embedded SVG cannot load
the page's webfonts.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.lines import Line2D  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DATA = Path(
    "/apdcephfs_tj6/share_303840540/hunyuan/jensenwang/git_warehouse/self_envolving"
    "/RSI_icassp_v5/fig2_three_benchmarks_data.json"
)
OUT_DIR = REPO / "assets" / "figures"

# Five lines that stay separable on white and in greyscale, tuned to sit beside
# the page's deep-blue primary.
MODEL_STYLE = {
    "Qwen2.5-Omni": {"color": "#0b57d0", "marker": "o"},
    "MiMo-Audio": {"color": "#d1495b", "marker": "s"},
    "Kimi-Audio": {"color": "#0f8a72", "marker": "^"},
    "MiniCPM-o 4.5": {"color": "#7d5ba6", "marker": "D"},
    "Audio Flamingo 3": {"color": "#d98014", "marker": "P"},
}

PANELS = [
    ("mean", "Three-benchmark average"),
    ("mmsu", "MMSU"),
    ("mmau_pro", "MMAU-Pro"),
    ("mmar", "MMAR"),
]

INK = "#16233d"
INK_SOFT = "#5b6880"
GRID = "#e4e9f2"
AXIS = "#aab4c5"


def series(model: dict, key: str) -> tuple[list[int], list[float]]:
    xs, ys = [], []
    for point in model["plot_points"]:
        chosen = point.get("selected") or {}
        if not chosen.get("available"):
            continue
        value = (
            chosen.get("mean_full_raw")
            if key == "mean"
            else (chosen.get("suites_full_raw") or {}).get(key)
        )
        if value is None:
            continue
        xs.append(point["attempt"])
        ys.append(float(value))
    return xs, ys


def style_axes(ax, title: str, *, show_xlabel: bool, show_ylabel: bool) -> None:
    ax.set_title(title, fontsize=12.5, fontweight="600", color=INK, pad=9)
    ax.grid(True, color=GRID, linewidth=0.9)
    ax.set_axisbelow(True)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(AXIS)
        ax.spines[side].set_linewidth(0.9)
    ax.tick_params(colors=INK_SOFT, labelsize=10, length=3, width=0.9)
    ax.set_xticks([0, 2, 4, 6, 8, 10, 12])
    if show_xlabel:
        ax.set_xlabel("Evolution attempt", fontsize=11, color=INK_SOFT, labelpad=6)
    if show_ylabel:
        ax.set_ylabel("Accuracy (%)", fontsize=11, color=INK_SOFT, labelpad=6)


def draw(data: dict, layout: str) -> Path:
    if layout == "wide":
        fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.4))
        flat = axes.ravel()
        legend_y = 0.965
        top = 0.885
        hspace, wspace = 0.30, 0.20
    else:
        fig, axes = plt.subplots(4, 1, figsize=(5.6, 13.6))
        flat = axes
        legend_y = 0.982
        top = 0.930
        hspace, wspace = 0.34, 0.20

    fig.patch.set_facecolor("white")

    for index, (key, title) in enumerate(PANELS):
        ax = flat[index]
        for name, style in MODEL_STYLE.items():
            model = data["models"].get(name)
            if not model:
                continue
            xs, ys = series(model, key)
            if not xs:
                continue
            ax.plot(
                xs,
                ys,
                color=style["color"],
                marker=style["marker"],
                markersize=4.6,
                markeredgecolor="white",
                markeredgewidth=0.7,
                linewidth=1.9,
                solid_capstyle="round",
                clip_on=True,
            )
        if layout == "wide":
            style_axes(ax, title, show_xlabel=index >= 2, show_ylabel=index % 2 == 0)
        else:
            style_axes(ax, title, show_xlabel=index == 3, show_ylabel=True)

    handles = [
        Line2D(
            [],
            [],
            color=style["color"],
            marker=style["marker"],
            markersize=5.2,
            markeredgecolor="white",
            markeredgewidth=0.7,
            linewidth=1.9,
            label=name,
        )
        for name, style in MODEL_STYLE.items()
    ]
    fig.legend(
        handles=handles,
        loc="upper center",
        bbox_to_anchor=(0.5, legend_y),
        ncol=5 if layout == "wide" else 2,
        frameon=False,
        fontsize=10.5,
        handlelength=1.9,
        columnspacing=1.5,
        labelcolor=INK,
    )
    fig.subplots_adjust(
        left=0.085 if layout == "wide" else 0.15,
        right=0.985,
        top=top,
        bottom=0.075 if layout == "wide" else 0.045,
        hspace=hspace,
        wspace=wspace,
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"evolution-{layout}.svg"
    fig.savefig(out, format="svg", facecolor="white")
    plt.close(fig)
    return out


def main() -> None:
    if not DATA.exists():
        sys.exit(f"missing source data: {DATA}")
    data = json.loads(DATA.read_text())

    # Keep text as vector outlines: the chart is loaded through <img>, which
    # cannot reach the page's webfonts.
    matplotlib.rcParams.update(
        {
            "svg.fonttype": "path",
            "font.family": "sans-serif",
            "font.sans-serif": ["DejaVu Sans"],
            "axes.unicode_minus": False,
        }
    )

    for layout in ("wide", "tall"):
        path = draw(data, layout)
        print(f"wrote {path.relative_to(REPO)}  ({path.stat().st_size/1024:.0f} KB)")

    # Record what the panels mean, so the page caption cannot drift from the data.
    (OUT_DIR / "evolution-meta.json").write_text(
        json.dumps(
            {
                "metric": data["metric"],
                "checkpoint_policy": data.get("checkpoint_policy"),
                "models": list(MODEL_STYLE),
                "panels": [title for _, title in PANELS],
                "attempts": 14,
                "colors": {name: st["color"] for name, st in MODEL_STYLE.items()},
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
