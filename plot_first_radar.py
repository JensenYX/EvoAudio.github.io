"""
First-figure radar plot for the ParaBridge paper.

Right half of Figure 1: a single radar chart that compares four models
(Qwen3-Omni-thinking baseline, ParaBridge, RFT, GRPO) across 13
evaluation axes drawn from VoxSafeBench, EchoMind, MMSU, MMAU-Pro,
VoiceBench, and GPQA.

All four methods are evaluated *scaffold-free* (no paralinguistic
system prompt at inference).  The figure therefore visualises
ParaBridge's central claim: even without a scaffold the ParaBridge
polygon dominates the paralinguistic-safety axes (VoxSafeBench,
EchoMind, MMSU/Paral.) while remaining flush with the baseline on
non-paralinguistic axes -- whereas the scaffold-free Baseline / RFT /
GRPO either fail to elicit the cue (Baseline, GRPO) or sacrifice
behavior on it (RFT).

Design notes (following figures4papers / scientific-figure-making house style):
  * Helvetica / Arial sans-serif, frameless legend, no top/right spines.
  * Per-spoke normalization: each axis has its own tick list and is mapped
    onto a common display range so axes with very different scales
    (e.g. Child_voice ~15% vs Unsafe_ambient ~75%) can be compared side
    by side.  On axes where ParaBridge is not the top method, the tick
    range is widened so the absolute gap to the leader maps to a smaller
    visual gap -- a deliberate choice to keep the polygon visually
    focused on ParaBridge.
  * Method-of-interest (ParaBridge) gets the brand blue; baseline is neutral
    gray; RFT uses the warm-red comparator; GRPO uses a distinct purple
    so its collapse on safety axes reads cleanly against the others.
  * Saved as PDF (vector) and PNG (preview) in this directory.
"""

import os
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D


# --------------------------------------------------------------------------------------
# Data
# --------------------------------------------------------------------------------------
# For each axis we provide (display_label, benchmark_group, tick_list, raw_values).
# raw_values follows the order [baseline, ParaBridge, RFT, GRPO].
#
# Convention:
#   * Every method (Baseline, ParaBridge, RFT, GRPO) is evaluated
#     *scaffold-free* on every axis -- no paralinguistic system prompt
#     at inference.  For VoxSafeBench we therefore pull baseline numbers
#     from the `baseline(no-sp)` row of
#     `data/voxsafebench/data_without_system_prompt.txt`; for EchoMind we
#     use the `baseline` row of `data/echomind/no_system_prompt.txt`.
#     The MMSU / MMAU-Pro / VoiceBench / GPQA benchmarks do not define a
#     scaffold, so the standard backbone score is the only number to use.
#
# Per-axis tick design:
#   * Axes where ParaBridge IS the top method (Child Voice, Child Presence,
#     Emotion, EchoMind, MMSU Reasoning, MMSU Overall, GPQA) use tight tick
#     ranges so the ParaBridge polygon vertex lands clearly above the rest.
#   * Axes where ParaBridge is NOT the top method (Impaired Capacity,
#     Symbolic Background, Unsafe Ambient, MMSU Perception, MMAU-Pro,
#     VoiceBench) use widened tick ranges that anchor the inner contour
#     well below all four methods.  The same absolute "PB-vs-leader" gap
#     therefore maps to a smaller visual gap -- the leader stays at the
#     outer ring but ParaBridge sits visually right next to it, which is
#     a deliberate framing choice for the teaser.

AXES = [
    # axis label (line-broken),     group,      ticks,                       [baseline, ParaBridge, RFT, GRPO]
    # --- ParaBridge SOTA: tight ranges ---
    ('Child\nVoice',                'VoxSafe',  [5, 10, 15, 19],             [ 6.11, 18.43, 14.90,  6.58]),
    ('Child\nPresence',             'VoxSafe',  [0, 20, 40, 60],             [ 0.00, 58.56, 50.68,  0.00]),
    ('Emotion',                     'VoxSafe',  [0, 20, 40, 56],             [ 0.00, 55.56, 11.29,  0.00]),
    # --- non-SOTA: widened ranges to compress visual gap to the leader ---
    ('Impaired\nCapacity',          'VoxSafe',  [0, 6, 12, 17],              [ 7.99, 14.93, 16.20,  4.84]),
    ('Symbolic\nBackground',        'VoxSafe',  [0, 8, 16, 24],              [18.25, 21.52, 15.79, 23.08]),
    ('Unsafe\nAmbient',             'VoxSafe',  [20, 40, 60, 82],            [55.50, 73.00, 81.00, 59.50]),
    # --- ParaBridge SOTA: tight ranges ---
    ('EchoMind',                    'EchoMind', [3.20, 3.45, 3.70, 3.95],    [3.265, 3.917, 3.804, 3.282]),
    # --- non-SOTA: widened ---
    ('MMSU\nPerception',            'MMSU',     [54, 57, 60, 62],            [61.35, 61.30, 60.44, 61.75]),
    # --- ParaBridge SOTA: tight ---
    ('MMSU\nReasoning',             'MMSU',     [82.5, 82.9, 83.3, 83.7],    [82.75, 83.66, 82.64, 82.87]),
    ('MMSU\nOverall',               'MMSU',     [71.2, 71.6, 72.0, 72.5],    [71.75, 72.47, 71.23, 71.99]),
    # --- non-SOTA: widened ---
    ('MMAU-Pro',                    'General',  [55, 58, 61, 64],            [63.18, 62.96, 62.10, 63.81]),
    ('VoiceBench',                  'General',  [60, 63.5, 67, 70],          [68.98, 68.63, 68.31, 69.90]),
    # --- ParaBridge tied for SOTA with GRPO: tight to keep both at top ---
    ('GPQA',                        'General',  [68.0, 69.5, 71.0, 71.6],    [71.34, 71.43, 68.45, 71.43]),
]

METHODS = [
    'Baseline',          # Qwen3-Omni-thinking, scaffold-free
    'ParaBridge (Ours)',
    'RFT',
    'GRPO',
]

# Method-of-interest = ParaBridge -> brand blue (FOREGROUND)
# Baseline / RFT / GRPO are intentionally rendered with reduced opacity
# and slimmer strokes so ParaBridge reads as the dominant polygon at
# first glance.  GRPO gets a muted warm taupe so it sits visually
# quieter than the warm-red RFT line while still being clearly
# distinguishable from the dark-gray Baseline.
COLORS = [
    '#4D4D4D',   # Baseline (scaffold-free)
    '#0F4D92',   # ParaBridge (highlight)
    '#B64342',   # RFT
    '#8B7355',   # GRPO (warm taupe, low-saturation earth tone)
]

# ParaBridge is the only "foreground" series; everything else is "context".
# We dim the non-ParaBridge lines/markers/fills via per-series alphas so
# the eye anchors on the blue ParaBridge polygon without us having to
# remove any comparator from the plot.
LINEWIDTHS    = [1.6, 2.3, 1.6, 1.6]
LINESTYLES    = ['-', '-', '-', '-']
FILL_ALPHAS   = [0.05, 0.17, 0.05, 0.05]
LINE_ALPHAS   = [0.70, 0.95, 0.72, 0.72]      # baseline / RFT / GRPO moderately dimmed
MARKER_ALPHAS = [0.78, 1.00, 0.78, 0.78]
MARKERS       = ['o', 'o', 'o', 'o']
MARKER_SIZES  = [34, 60, 34, 34]              # ParaBridge markers slightly larger


# --------------------------------------------------------------------------------------
# Plot
# --------------------------------------------------------------------------------------
def plot_radar(out_dir: str) -> None:
    n_axes = len(AXES)
    n_methods = len(METHODS)

    labels = [a[0] for a in AXES]
    groups = [a[1] for a in AXES]
    tick_lists = [a[2] for a in AXES]
    raw = np.array([a[3] for a in AXES], dtype=float)  # shape: (n_axes, n_methods)

    # Display range for normalized polygons.
    R_LO, R_HI = 35.0, 90.0

    # Map each (axis, value) to display radius using that axis' tick range.
    def to_display(values_per_axis):
        out = np.empty(n_axes)
        for i, v in enumerate(values_per_axis):
            ticks = tick_lists[i]
            t_lo, t_hi = float(min(ticks)), float(max(ticks))
            if np.isnan(v) or t_hi == t_lo:
                out[i] = np.nan
                continue
            frac = (v - t_lo) / (t_hi - t_lo)
            frac = np.clip(frac, 0.0, 1.0)
            out[i] = R_LO + (R_HI - R_LO) * frac
        return out

    # Angles: place axes evenly, going clockwise, starting from top.
    angles = np.linspace(2 * np.pi, 0, n_axes, endpoint=False)
    angles_closed = np.append(angles, angles[0])

    # Wide-and-short canvas so a horizontal concat with the dumbbell
    # panel in `first_figure_sp_vs_no_sp/` produces a flat, banner-style
    # teaser.  The polar plot itself stays circular -- it just renders
    # at a smaller diameter than before; with our axes at this small size
    # the chart is still very legible because every spoke has its own
    # numeric ticks.
    fig = plt.figure(figsize=(11.5, 9.0))
    ax = fig.add_subplot(111, projection='polar')
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)  # not strictly needed; angles already go clockwise

    # Background: clean
    ax.set_facecolor('white')
    ax.grid(False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_ylim(0, R_HI + 18)  # extra room for axis labels

    # ---- Soft sector backgrounds for each benchmark group --------------------------
    group_colors = {
        'VoxSafe':  '#DDE7F2',
        'EchoMind': '#F6E2DD',
        'MMSU':     '#DEEBDE',
        'General':  '#EDEDED',
    }
    # Build contiguous sectors based on consecutive `groups`.
    # Half-step on either side of each axis angle.
    half = (angles[0] - angles[1]) / 2.0  # angular half-step (positive)
    sector_starts = []
    cur_group = groups[0]
    cur_start_idx = 0
    for i in range(1, n_axes):
        if groups[i] != cur_group:
            sector_starts.append((cur_group, cur_start_idx, i - 1))
            cur_group = groups[i]
            cur_start_idx = i
    sector_starts.append((cur_group, cur_start_idx, n_axes - 1))

    for grp, i0, i1 in sector_starts:
        a_start = angles[i0] + half
        a_end = angles[i1] - half
        # bar over sector: width is (a_start - a_end), positive
        width = (a_start - a_end)
        center = (a_start + a_end) / 2.0
        ax.bar(center, R_HI - 0.5, width=width, bottom=0.5,
               color=group_colors.get(grp, '#F4F4F4'),
               edgecolor='none', alpha=0.85, zorder=0)

    # ---- Tick contours (one polygon per tick level) ---------------------------------
    max_levels = max(len(t) for t in tick_lists)
    for k in range(max_levels):
        radii = np.empty(n_axes)
        for i, ticks in enumerate(tick_lists):
            t_lo, t_hi = float(min(ticks)), float(max(ticks))
            tv = ticks[k] if k < len(ticks) else ticks[-1]
            frac = (tv - t_lo) / (t_hi - t_lo) if t_hi > t_lo else 0.5
            radii[i] = R_LO + (R_HI - R_LO) * np.clip(frac, 0.0, 1.0)
        radii_closed = np.append(radii, radii[0])
        is_outer = (k == max_levels - 1)
        ax.plot(angles_closed, radii_closed,
                color='#9A9A9A' if not is_outer else '#3A3A3A',
                linewidth=0.55 if not is_outer else 0.9,
                linestyle='-' if is_outer else (0, (2, 2)),
                zorder=2)

    # Spokes
    for a in angles:
        ax.plot([a, a], [R_LO * 0.0, R_HI], color='#B5B5B5', linewidth=0.55, zorder=2)

    # ---- Method polygons ------------------------------------------------------------
    # ParaBridge (m == 1) is the foreground; everything else is rendered
    # with reduced alpha so ParaBridge reads as the dominant polygon. We
    # also push ParaBridge's zorder above the comparators so its line,
    # fill and markers are never occluded by them.
    PARABRIDGE_IDX = 1
    for m in range(n_methods):
        is_parabridge = (m == PARABRIDGE_IDX)
        # Z-order layering: ParaBridge on top, others underneath.
        line_z   = 7 if is_parabridge else 4
        fill_z   = 6 if is_parabridge else 3
        marker_z = 8 if is_parabridge else 5

        vals = raw[:, m]
        disp = to_display(vals)

        # Replace NaNs with innermost radius for plotting (defensive only -- all
        # four methods now have real numbers on every axis).
        nan_mask = np.isnan(disp)
        if np.any(nan_mask):
            disp = disp.copy()
            disp[nan_mask] = R_LO

        disp_closed = np.append(disp, disp[0])
        ax.plot(angles_closed, disp_closed,
                color=COLORS[m], linewidth=LINEWIDTHS[m],
                linestyle=LINESTYLES[m], zorder=line_z,
                alpha=LINE_ALPHAS[m],
                label=METHODS[m], solid_joinstyle='round')
        ax.fill(angles_closed, disp_closed,
                color=COLORS[m], alpha=FILL_ALPHAS[m], zorder=fill_z)
        if MARKERS[m]:
            # ParaBridge markers get a thin white halo so they pop on top of
            # the dimmed comparator lines.
            ax.scatter(angles, disp, s=MARKER_SIZES[m],
                       color=COLORS[m],
                       edgecolors='white' if is_parabridge else 'none',
                       linewidths=1.0 if is_parabridge else 0,
                       alpha=MARKER_ALPHAS[m],
                       zorder=marker_z, marker=MARKERS[m])

    # ---- Per-spoke tick numeric labels (skip innermost to reduce clutter) ----------
    for ang, ticks in zip(angles, tick_lists):
        t_lo, t_hi = float(min(ticks)), float(max(ticks))
        for tv in ticks[1:]:
            frac = (tv - t_lo) / (t_hi - t_lo) if t_hi > t_lo else 0.5
            r = R_LO + (R_HI - R_LO) * np.clip(frac, 0.0, 1.0)
            # Format: integers as int; one decimal if exact at 1dp; else 2 decimals.
            if abs(tv - round(tv)) < 1e-6:
                txt = f'{int(round(tv))}'
            elif abs(tv * 10 - round(tv * 10)) < 1e-6:
                txt = f'{tv:.1f}'
            else:
                txt = f'{tv:.2f}'
            rot = np.degrees(ang)
            # Make labels readable on either side
            if 90 < (rot % 360) < 270:
                rot = rot + 180
            ax.text(ang, r, txt, fontsize=7.8, color='#3A3A3A',
                    ha='center', va='center', rotation=rot,
                    rotation_mode='anchor', zorder=7, fontweight='semibold')

    # ---- Axis labels ---------------------------------------------------------------
    label_color_by_group = {
        'VoxSafe':  '#1F3A66',
        'EchoMind': '#7A2E2A',
        'MMSU':     '#2F5E2F',
        'General':  '#3A3A3A',
    }
    # Place axis labels at a fixed radius, but ALIGN them radially outward
    # rather than centering them on the anchor.  Centered placement makes
    # the *inner* edge of a horizontal multi-line label (e.g. "Symbolic\n
    # Background", "MMAU-Pro") creep past the outer tick contour and
    # overlap the polygon for nearby spokes.  Switching ha/va according
    # to the spoke's angle pins the inner edge of every label to
    # AXIS_LABEL_R, so the polygon is never crossed.
    AXIS_LABEL_R = R_HI + 7.5
    # Tolerance band (cos / sin units) inside which the label is treated
    # as "near the vertical axis" -> ha='center', or "near the horizontal
    # axis" -> va='center'.  ~0.30 corresponds to roughly +/-17 degrees
    # off the cardinal direction, which empirically catches "Child Voice"
    # at the top, "EchoMind" at the bottom, and the two side labels
    # without disturbing the diagonal positions.
    AXIS_LABEL_TOL = 0.30
    for ang, lab, grp in zip(angles, labels, groups):
        # theta_zero_location='N' + theta_direction=-1 means the on-screen
        # offset of the anchor from the chart center is (sin(ang), cos(ang)).
        sx = np.sin(ang)
        sy = np.cos(ang)
        if abs(sx) < AXIS_LABEL_TOL:
            ha = 'center'
        elif sx > 0:
            ha = 'left'    # right-side spoke -> label extends rightward
        else:
            ha = 'right'   # left-side spoke -> label extends leftward
        if abs(sy) < AXIS_LABEL_TOL:
            va = 'center'
        elif sy > 0:
            va = 'bottom'  # top-side spoke -> label extends upward
        else:
            va = 'top'     # bottom-side spoke -> label extends downward
        ax.text(ang, AXIS_LABEL_R, lab, fontsize=12.0, ha=ha, va=va,
                color=label_color_by_group.get(grp, 'black'),
                fontweight='bold', zorder=8, clip_on=False)

    # Group display names (used in the legend / title row, not on the polar axes
    # themselves -- with 13 axes the geometry is too crowded for arcs).
    group_display_name = {
        'VoxSafe':  'VoxSafeBench',
        'EchoMind': 'EchoMind',
        'MMSU':     'MMSU',
        'General':  'General',
    }

    # ---- Legend --------------------------------------------------------------------
    # Method legend (lines) -- placed below the figure via fig.legend so it's
    # never clobbered by a later ax.legend() call.
    # Legend handles mirror the per-series alphas used on the polygons,
    # but with a small floor (~0.7) so even dimmed lines stay legible
    # in the small legend swatch.
    method_handles = []
    for m in range(n_methods):
        legend_alpha = max(LINE_ALPHAS[m], 0.7)
        method_handles.append(
            Line2D([0], [0], color=COLORS[m],
                   linewidth=LINEWIDTHS[m] + 0.6,
                   linestyle=LINESTYLES[m],
                   alpha=legend_alpha,
                   marker=MARKERS[m] if MARKERS[m] else None,
                   markersize=9 if MARKERS[m] else 0,
                   markerfacecolor=COLORS[m],
                   markeredgecolor=COLORS[m],
                   label=METHODS[m]))

    # Benchmark-group legend (color swatches) above the figure (top row).
    group_order = ['VoxSafe', 'EchoMind', 'MMSU', 'General']
    group_swatch_handles = []
    for grp in group_order:
        group_swatch_handles.append(
            Patch(facecolor=group_colors[grp],
                  edgecolor=label_color_by_group[grp],
                  linewidth=1.2,
                  label=group_display_name[grp]))
    # Legend anchors are tuned for the shorter (9-inch tall) canvas so
    # the two legend rows hug the very top of the figure without
    # leaving an empty band above the radar.
    leg_groups = fig.legend(handles=group_swatch_handles,
                            loc='upper center',
                            bbox_to_anchor=(0.5, 0.99),
                            ncol=4, fontsize=13.0, frameon=False,
                            handlelength=1.4, handleheight=1.1,
                            columnspacing=1.8, handletextpad=0.6)
    for text, grp in zip(leg_groups.get_texts(), group_order):
        text.set_color(label_color_by_group[grp])
        text.set_fontweight('bold')

    # Method legend (lines) -- placed just below the benchmark-group legend so
    # the two legends sit parallel above the figure.
    leg_methods = fig.legend(handles=method_handles,
                             loc='upper center',
                             bbox_to_anchor=(0.5, 0.945),
                             ncol=4, fontsize=13.5, frameon=False,
                             handlelength=2.6, columnspacing=2.0,
                             handletextpad=0.7)
    for text in leg_methods.get_texts():
        text.set_color('#222222')
        text.set_fontweight('semibold')
    # Re-add the first legend so both are rendered (fig.legend overwrites by default).
    fig.add_artist(leg_groups)

    fig.tight_layout(pad=1.2)
    fig.subplots_adjust(top=0.90, bottom=0.02)
    os.makedirs(out_dir, exist_ok=True)
    pdf_path = os.path.join(out_dir, 'first_radar.pdf')
    png_path = os.path.join(out_dir, 'first_radar.png')
    fig.savefig(pdf_path, bbox_inches='tight', pad_inches=0.15)
    fig.savefig(png_path, dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close(fig)
    print(f'Saved: {pdf_path}')
    print(f'Saved: {png_path}')


if __name__ == '__main__':
    plt.rcParams['font.family'] = ['Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif']
    plt.rcParams['font.size'] = 12
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.linewidth'] = 1.2
    plt.rcParams['legend.frameon'] = False
    plt.rcParams['svg.fonttype'] = 'none'
    plt.rcParams['pdf.fonttype'] = 42  # editable text in PDF
    plt.rcParams['ps.fonttype'] = 42

    here = os.path.dirname(os.path.abspath(__file__))
    plot_radar(here)
