#!/usr/bin/env python3
"""Render the reported capacity and replay workflow at its final print size.

The figure is an editorial schematic of the supplied source record. All
numeric labels come from figure1_flow_parameters.csv; styling does not add
an experimental step or imply that replay integrity authorizes B1.
"""
from __future__ import annotations

import argparse
import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

from figure_style import (
    AMBER, BLUE, GRID, INK, LIGHT_AMBER, LIGHT_BLUE, LIGHT_TEAL, MUTED,
    PALE, RED, TEAL, save_figure, style_context,
)


ROOT = Path(__file__).resolve().parents[1]


def _parameters() -> dict[str, int]:
    with (ROOT / "data/figure1_flow_parameters.csv").open(newline="", encoding="utf-8") as stream:
        values = {row["parameter"]: int(row["value"]) for row in csv.DictReader(stream)}
    expected = {
        "listing_requests": 1232, "strata": 8, "temporal_bins": 12,
        "primary_files": 96, "stations": 12, "evaluation_stations": 8,
        "reporting_blocks": 5, "capacity_threshold": 400, "cell_threshold": 8,
        "files_per_round": 8, "final_round": 4, "final_opportunities": 150,
        "minimum_cell": 0, "outcome_reads": 0,
    }
    if values != expected:
        raise ValueError("Workflow parameters differ from the reported source record")
    return values


def _node(ax: plt.Axes, x: float, y: float, width: float, height: float,
          title: str, body: str = "", *, accent: str = BLUE,
          fill: str = PALE) -> None:
    """Use a small, consistent title/body hierarchy inside fixed-size boxes."""
    ax.add_patch(FancyBboxPatch(
        (x, y), width, height, boxstyle="round,pad=0.005,rounding_size=0.009",
        linewidth=0.7, edgecolor=accent, facecolor=fill, zorder=2,
    ))
    if body:
        line_count = body.count("\n") + 1
        # The canvas is 327.6 pt high; the spacing below preserves >=8 pt text.
        title_y = y + height / 2 + (line_count * 9.5) / (2 * 327.6)
        ax.text(x + width / 2, title_y, title, ha="center", va="center",
                fontsize=8.5, weight="bold", color=accent, zorder=4)
        ax.text(x + width / 2, title_y - 12.0 / 327.6, body,
                ha="center", va="top", fontsize=8.1, linespacing=1.18,
                color=INK, zorder=4)
    else:
        ax.text(x + width / 2, y + height / 2, title, ha="center", va="center",
                fontsize=8.5, weight="bold", color=accent, zorder=4)


def _arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float],
           color: str = MUTED, *, style: str = "-") -> None:
    ax.add_patch(FancyArrowPatch(
        start, end, arrowstyle="-|>", mutation_scale=8.5, linewidth=0.8,
        color=color, linestyle=style, shrinkA=1.5, shrinkB=1.5, zorder=3,
    ))


def make_figure() -> plt.Figure:
    """Create the fixed 7.16 x 4.55 inch figure inside the caller's style context."""
    values = _parameters()
    fig = plt.figure(figsize=(7.16, 4.55))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")

    ax.text(0.025, 0.975, "(a) Frozen selection and capacity assessment",
            fontsize=10, weight="bold", va="top", color=INK)
    row_y, row_h = 0.755, 0.150
    _node(ax, 0.025, row_y, 0.155, row_h, "Official listing",
          f"{values['listing_requests']:,} requests", fill=PALE)
    _node(ax, 0.205, row_y, 0.180, row_h, "Frozen selection",
          f"{values['strata']} strata × {values['temporal_bins']} bins\n{values['primary_files']} primary files",
          fill=PALE)
    _node(ax, 0.410, row_y, 0.310, row_h, "Predictor accounting",
          f"{values['stations']} stations × active files\nDeduplicate; zero-fill {values['evaluation_stations']} × {values['reporting_blocks']}",
          fill=LIGHT_BLUE)
    _node(ax, 0.745, row_y, 0.230, row_h, "G0-v4.1 capacity",
          f"≥{values['capacity_threshold']} opportunities\nAND ≥{values['cell_threshold']} per station–block",
          accent=RED, fill=PALE)
    for left, right in [(0.180, 0.205), (0.385, 0.410), (0.720, 0.745)]:
        _arrow(ax, (left + 0.004, row_y + row_h / 2),
               (right - 0.004, row_y + row_h / 2))

    ax.text(0.025, 0.635, "Frozen acquisition policy", fontsize=8.5,
            weight="bold", color=BLUE, va="top")
    ax.text(0.025, 0.598, "Whole rounds only\nNo individual file replacement",
            fontsize=8.1, linespacing=1.25, color=MUTED, va="top")
    _node(ax, 0.410, 0.525, 0.310, 0.125, "Next complete alternate round",
          f"{values['files_per_round']} files per round; up to {values['final_round']} rounds",
          accent=AMBER, fill=LIGHT_AMBER)
    _node(ax, 0.745, 0.505, 0.230, 0.155, "FAIL_EXHAUSTED",
          f"{values['final_opportunities']} / {values['capacity_threshold']} opportunities\nMinimum cell: {values['minimum_cell']} / {values['cell_threshold']}\nB1 closed",
          accent=RED, fill=PALE)

    # Failure with an available alternate returns to predictor accounting.
    ax.plot([0.790, 0.790, 0.670], [0.750, 0.708, 0.708],
            color=AMBER, linewidth=0.8, zorder=1)
    _arrow(ax, (0.670, 0.708), (0.670, 0.655), AMBER)
    ax.text(0.660, 0.696, "Fail; round remains", fontsize=8.0,
            color=AMBER, ha="right", va="top")
    _arrow(ax, (0.455, 0.655), (0.455, 0.750), AMBER)
    ax.text(0.442, 0.709, "Recount", fontsize=8.0, color=AMBER,
            ha="right", va="center")
    _arrow(ax, (0.920, 0.750), (0.920, 0.665), RED)
    ax.text(0.905, 0.710, f"Fail after\nround {values['final_round']}",
            fontsize=8.0, color=RED, ha="right", va="center", linespacing=1.12)

    ax.plot([0.025, 0.975], [0.470, 0.470], color=GRID, linewidth=0.65)
    ax.text(0.025, 0.448, "(b) Source result and replay integrity",
            fontsize=10, weight="bold", va="top", color=INK)

    top_y, bottom_y, node_h = 0.282, 0.092, 0.112
    top_center, bottom_center = top_y + node_h / 2, bottom_y + node_h / 2
    ax.text(0.075, top_center, "SOURCE\nv4.1", fontsize=8.0,
            weight="bold", ha="center", va="center", color=MUTED, linespacing=1.25)
    ax.text(0.075, bottom_center, "AUDIT\nv5", fontsize=8.0,
            weight="bold", ha="center", va="center", color=MUTED, linespacing=1.25)
    _node(ax, 0.150, top_y, 0.190, node_h, "Frozen v4.1 design", "Predictors only")
    _node(ax, 0.380, top_y, 0.200, node_h, "G0-v4.1: FAIL", "Source capacity",
          accent=RED)
    _node(ax, 0.620, top_y, 0.155, node_h, "B1 closed", accent=MUTED)
    _node(ax, 0.150, bottom_y, 0.190, node_h, "Post-result audit", "New v5 identity",
          accent=AMBER, fill=LIGHT_AMBER)
    _node(ax, 0.380, bottom_y, 0.200, node_h, "Digest-bound", "Replay of records",
          accent=TEAL, fill=LIGHT_TEAL)
    _node(ax, 0.620, bottom_y, 0.155, node_h, "G0-v5: PASS", "Integrity only",
          accent=TEAL, fill=LIGHT_TEAL)
    _node(ax, 0.815, bottom_y, 0.160, top_y + node_h - bottom_y,
          "Outcome vault", f"Closed\n\n{values['outcome_reads']} outcome reads\nB1 remained closed",
          accent=MUTED, fill=PALE)
    for center in (top_center, bottom_center):
        for left, right in [(0.340, 0.380), (0.580, 0.620), (0.775, 0.815)]:
            _arrow(ax, (left + 0.004, center), (right - 0.004, center))
    _arrow(ax, (0.245, top_y - 0.005), (0.245, bottom_y + node_h + 0.005), AMBER)
    ax.text(0.265, 0.240, "New audit identity", fontsize=8.0,
            color=AMBER, ha="left", va="center")
    ax.text(0.500, 0.025, "Replay consistency does not change the source capacity decision.",
            fontsize=8.0, color=MUTED, ha="center", va="center")
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "paper/figures")
    parser.add_argument("--preview-dir", type=Path,
                        default=ROOT.parent / "tmp/professional_figures")
    args = parser.parse_args()
    with style_context():
        fig = make_figure()
        save_figure(
            fig, args.output_dir / "figure1.pdf",
            title="Frozen selection, capacity assessment, and replay integrity",
            subject="Source-reported workflow and counts; the replay pass does not authorize B1",
            creator="Matplotlib; scripts/render_workflow.py",
            preview_path=args.preview_dir / "figure1.png",
        )
        plt.close(fig)


if __name__ == "__main__":
    main()
