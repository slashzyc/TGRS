#!/usr/bin/env python3
"""Render publication figures from labelled values in the supplied manuscript.

This is an editorial plotting script, not a replication of the NOAA/ASCAT study.
Read data/README.md for provenance and the limits of these aggregate values.
All plots use vector artists and embedded TrueType fonts in their PDF exports.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STATES = ("extract_valid", "fewer_than_2_candidates", "no_overlap", "time_invalid")
BLUE = "#315E7D"
LIGHT_BLUE = "#C9D9E4"
INK = "#202A32"
GRID = "#DDE2E7"
RED = "#9E493F"
AMBER = "#996A21"
CMAP = LinearSegmentedColormap.from_list(
    "paper_blue", ["#F7FAFC", "#D5E3ED", "#98B6CD", "#537F9E", "#244B68"]
)


def read_csv(name: str) -> list[dict[str, str]]:
    with (DATA / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def matrix(rows: list[dict[str, str]], keys: tuple[str, ...] = STATES) -> np.ndarray:
    return np.asarray([[int(row[k]) for k in keys] for row in rows], dtype=int)


def check_transcription() -> dict[str, object]:
    """Check arithmetic without claiming verification of underlying observations."""
    rows2 = read_csv("figure2_station_blocks.csv")
    mat2 = matrix(rows2, tuple(f"block_{i:02d}" for i in range(1, 6)))
    assert mat2.shape == (8, 5)
    assert np.array_equal(mat2.sum(axis=1), [int(r["total"]) for r in rows2])
    assert int(mat2.sum()) == 150
    assert int(np.count_nonzero(mat2 == 0)) == 9
    assert int(np.count_nonzero(mat2 >= 8)) == 3

    rows3 = read_csv("figure3_terminal_counts.csv")
    assert [r["role"] for r in rows3] == ["Evaluation", "Development"]
    mat3 = matrix(rows3)
    assert np.array_equal(mat3.sum(axis=1), [1024, 512])
    assert np.array_equal(mat3.sum(axis=1), [int(r["total"]) for r in rows3])

    rows4 = read_csv("figure4_budget_capacity.csv")
    byte_totals = np.asarray([int(r["cumulative_science_bytes"]) for r in rows4])
    opportunities = np.asarray([int(r["evaluation_opportunities"]) for r in rows4])
    increments = np.diff(np.r_[0, opportunities])
    assert np.array_equal(increments, [int(r["increment"]) for r in rows4])
    assert np.array_equal([int(r["active_files"]) for r in rows4], [96, 104, 112, 120, 128])
    assert (np.diff(byte_totals) > 0).all()
    assert int(byte_totals[-1]) == 9418446350 < 10_000_000_000

    rows5 = read_csv("figure5_terminal_counts.csv")
    percent_rows = read_csv("figure5_display_percentages.csv")
    expected_percent = {(r["panel"], r["group"]): r for r in percent_rows}
    checked_percentages = 0
    for row in rows5:
        n = int(row["total"])
        assert sum(int(row[k]) for k in STATES) == n
        printed = expected_percent[(row["panel"], row["group"])]
        for key in STATES:
            assert int(f"{100 * int(row[key]) / n:.0f}") == int(printed[key])
            checked_percentages += 1
    for panel in ("stratum", "station", "source_block"):
        selected = [r for r in rows5 if r["panel"] == panel]
        assert np.array_equal(matrix(selected).sum(axis=0), mat3[0])
        assert sum(int(r["total"]) for r in selected) == 1024
    assert [int(r["total"]) for r in rows5 if r["panel"] == "source_block"] == [184, 224, 176, 224, 216]
    assert [int(r["extract_valid"]) for r in rows5 if r["panel"] == "station"] == [int(r["total"]) for r in rows2]

    return {
        "status": "aggregate transcription arithmetic passed",
        "figure2": {"cells": 40, "total": 150, "zero_cells": 9, "cells_at_least_8": 3},
        "figure3": {"evaluation_rows": 1024, "development_rows": 512},
        "figure4": {
            "active_files": [96, 104, 112, 120, 128],
            "opportunities": opportunities.tolist(),
            "increments": increments.tolist(),
            "byte_increments_after_primary": np.diff(byte_totals).tolist(),
            "remaining_bytes": int(10_000_000_000 - byte_totals[-1]),
        },
        "figure5": {"count_cells": 84, "matched_percentage_labels": checked_percentages,
                    "each_panel_state_totals": mat3[0].tolist()},
        "scope": "Checks supplied manuscript aggregates only; no independent experimental replication.",
    }


def style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans",
        "font.size": 8.5,
        "axes.labelsize": 8.5,
        "axes.titlesize": 9.5,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "axes.linewidth": 0.7,
        "axes.edgecolor": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "savefig.facecolor": "white",
    })


def finish(fig: plt.Figure, number: int, output_dir: Path, preview_dir: Path | None) -> None:
    fig.savefig(output_dir / f"figure{number}.pdf", metadata={
        "Title": f"Figure {number}: revised manuscript display",
        "Subject": "Editorial rendering from transcribed aggregate values; see data/README.md",
        "Creator": "Matplotlib; scripts/render_figures.py",
    })
    if preview_dir is not None:
        fig.savefig(preview_dir / f"figure{number}.png", dpi=200)
    plt.close(fig)


def clean_axis(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(width=0.7, length=3)


def annotation_color(fraction: float) -> str:
    """Choose the higher-contrast foreground against the plotted cell color."""
    def luminance(rgb: object) -> float:
        values = np.asarray(rgb, dtype=float)[:3]
        linear = np.where(values <= 0.04045, values / 12.92,
                          ((values + 0.055) / 1.055) ** 2.4)
        return float(np.dot(linear, [0.2126, 0.7152, 0.0722]))
    background = luminance(CMAP(fraction))
    dark = luminance(matplotlib.colors.to_rgb(INK))
    white_contrast = 1.05 / (background + 0.05)
    dark_contrast = (background + 0.05) / (dark + 0.05)
    return "white" if white_contrast > dark_contrast else INK


def node(ax: plt.Axes, x: float, y: float, width: float, height: float,
         text: str, kind: str = "blue", fontsize: float = 8.1) -> None:
    palette = {
        "blue": ("#EDF3F7", BLUE),
        "red": ("#F8EEEC", RED),
        "amber": ("#FBF5E9", AMBER),
        "green": ("#EDF4F0", "#47715B"),
        "gray": ("#F4F5F6", "#68747E"),
    }
    fill, edge = palette[kind]
    ax.add_patch(FancyBboxPatch((x, y), width, height,
        boxstyle="round,pad=0.005,rounding_size=0.008", lw=0.85,
        edgecolor=edge, facecolor=fill, zorder=2))
    ax.text(x + width / 2, y + height / 2, text, ha="center", va="center",
            fontsize=fontsize, linespacing=1.16, zorder=3)


def arrow(ax: plt.Axes, start: tuple[float, float], end: tuple[float, float],
          color: str = "#5A6873") -> None:
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>",
        mutation_scale=8, linewidth=0.95, color=color, shrinkA=1, shrinkB=1, zorder=1))


def figure1() -> plt.Figure:
    values = {r["parameter"]: int(r["value"]) for r in read_csv("figure1_flow_parameters.csv")}
    fig = plt.figure(figsize=(7.16, 4.55))
    ax = fig.add_axes([0.01, 0.01, 0.98, 0.98])
    ax.set(xlim=(0, 1), ylim=(0, 1))
    ax.axis("off")
    ax.text(0.015, 0.976, "(a) Frozen selection and capacity assessment", fontsize=10,
            fontweight="bold", va="top")
    y, h = 0.730, 0.170
    node(ax, 0.015, y, 0.185, h, f"Official listing\n{values['listing_requests']:,} requests")
    node(ax, 0.235, y, 0.185, h,
         f"Frozen selector\n{values['strata']} strata × {values['temporal_bins']} bins\n{values['primary_files']} primary files")
    node(ax, 0.455, y, 0.265, h,
         f"Predictor accounting\n{values['stations']} stations × active files\nDeduplicate; zero-fill {values['evaluation_stations']} × {values['reporting_blocks']}")
    node(ax, 0.755, y, 0.230, h,
         f"G0-v4.1 capacity gate\n≥{values['capacity_threshold']} total opportunities\n≥{values['cell_threshold']} per station–block", "red", 8.0)
    for start, end in [(0.200, 0.235), (0.420, 0.455), (0.720, 0.755)]:
        arrow(ax, (start, y + h / 2), (end, y + h / 2))
    node(ax, 0.455, 0.535, 0.265, 0.110,
         f"Activate next complete\n{values['files_per_round']}-file round\nUp to four rounds", "amber", 7.8)
    ax.plot([0.800, 0.800, 0.640], [0.730, 0.685, 0.685], color=AMBER, lw=0.95, zorder=1)
    arrow(ax, (0.640, 0.685), (0.640, 0.645), AMBER)
    arrow(ax, (0.515, 0.645), (0.515, 0.730), AMBER)
    ax.text(0.504, 0.687, "Failure; an alternate\nround remains", fontsize=7.2,
            ha="right", va="center", color=AMBER)
    node(ax, 0.755, 0.505, 0.230, 0.140,
         f"FAIL_EXHAUSTED\n{values['final_opportunities']} / {values['capacity_threshold']} opportunities\nMinimum cell: {values['minimum_cell']} / {values['cell_threshold']}\nB1 closed", "red", 7.8)
    arrow(ax, (0.880, 0.730), (0.880, 0.645), RED)
    ax.text(0.895, 0.687, f"Failure after\nround {values['final_round']}", fontsize=7.0,
            va="center", color=RED)

    ax.axhline(0.465, xmin=0.015, xmax=0.985, color=GRID, lw=0.8)
    ax.text(0.015, 0.445, "(b) Source result and replay integrity", fontsize=10,
            fontweight="bold", va="top")
    ax.text(0.055, 0.325, "v4.1\nsource", fontsize=8.1, ha="center", va="center")
    ax.text(0.055, 0.155, "v5\naudit", fontsize=8.1, ha="center", va="center")
    node(ax, 0.120, 0.275, 0.185, 0.100, "Frozen v4.1 design\nPredictors only")
    node(ax, 0.350, 0.275, 0.195, 0.100, "G0-v4.1: FAIL\nSource capacity", "red")
    node(ax, 0.590, 0.275, 0.165, 0.100, "B1 closed", "gray")
    node(ax, 0.120, 0.105, 0.185, 0.100, "Post-result\nv5 identity", "amber")
    node(ax, 0.350, 0.105, 0.195, 0.100, "Digest-bound\nreplay", "green")
    node(ax, 0.590, 0.105, 0.165, 0.100, "G0-v5: PASS\nIntegrity only", "green", 7.8)
    node(ax, 0.800, 0.105, 0.185, 0.270,
         f"Outcome vault\nclosed\n\n{values['outcome_reads']} outcome reads\nB1 remained closed", "gray", 7.8)
    for center_y in (0.325, 0.155):
        for start, end in ((0.305, 0.350), (0.545, 0.590), (0.755, 0.800)):
            arrow(ax, (start, center_y), (end, center_y))
    arrow(ax, (0.2125, 0.275), (0.2125, 0.205), AMBER)
    ax.text(0.225, 0.240, "New audit identity", fontsize=7.3, color=AMBER, va="center")
    return fig


def figure2() -> plt.Figure:
    rows = read_csv("figure2_station_blocks.csv")
    values = matrix(rows, tuple(f"block_{i:02d}" for i in range(1, 6)))
    fig = plt.figure(figsize=(3.5, 3.4))
    fig.text(0.195, 0.985, "150 opportunities; 3/40 cells ≥8", fontsize=7.7, va="top")
    ax = fig.add_axes([0.195, 0.260, 0.755, 0.680])
    mesh = ax.pcolormesh(np.arange(6), np.arange(9), values, cmap=CMAP,
                        vmin=0, vmax=9, shading="flat", linewidth=0.35,
                        edgecolors="white", rasterized=False)
    ax.set_xlim(0, 6.0)
    ax.set_ylim(8, 0)
    ax.set_xticks(np.arange(5) + 0.5, [f"{i:02d}" for i in range(1, 6)])
    ax.set_yticks(np.arange(8) + 0.5, [r["station"] for r in rows])
    ax.set_xlabel("28-day reporting block", labelpad=4)
    ax.tick_params(length=0, pad=4)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(8):
        for j in range(5):
            v = int(values[i, j])
            ax.text(j + 0.5, i + 0.5, str(v), ha="center", va="center", fontsize=9,
                    color=annotation_color(v / 9),
                    fontweight="bold" if v >= 8 else "normal")
            if v >= 8:
                ax.add_patch(Rectangle((j + 0.035, i + 0.035), 0.93, 0.93,
                                      fill=False, edgecolor=AMBER, linewidth=1.25))
        ax.text(5.55, i + 0.5, rows[i]["total"], ha="center", va="center", fontsize=8)
    ax.text(5.55, -0.34, "Total", ha="center", va="center", fontsize=8, clip_on=False)
    cax = fig.add_axes([0.240, 0.105, 0.520, 0.027])
    cb = fig.colorbar(mesh, cax=cax, orientation="horizontal", ticks=[0, 3, 6, 9])
    cb.solids.set_rasterized(False)
    cb.outline.set_linewidth(0.5)
    cb.ax.tick_params(labelsize=7.5, length=2, pad=2)
    cb.set_label("Opportunities per station–block", fontsize=7.7, labelpad=3)
    return fig


def figure3() -> plt.Figure:
    rows = read_csv("figure3_terminal_counts.csv")
    values = matrix(rows)
    fig = plt.figure(figsize=(3.5, 2.95))
    ax = fig.add_axes([0.320, 0.190, 0.640, 0.625])
    positions = np.arange(4)
    for i, (offset, color, hatch) in enumerate([(-0.17, BLUE, None), (0.17, LIGHT_BLUE, "////")]):
        bars = ax.barh(positions + offset, values[i], height=0.28, color=color,
                       edgecolor=BLUE, linewidth=0.5, hatch=hatch,
                       label=f"{rows[i]['role']} (n={int(rows[i]['total']):,})", zorder=3)
        for bar, value in zip(bars, values[i]):
            ax.text(float(value) + 9, bar.get_y() + bar.get_height() / 2,
                    str(int(value)), va="center", fontsize=8)
    ax.set_yticks(positions, ["Valid extraction", "<2 valid\ncandidates", "No overlap", "Time invalid"])
    ax.set_ylim(3.58, -0.58)
    ax.set_xlim(0, 710)
    ax.set_xticks([0, 200, 400, 600])
    ax.set_xlabel("Station-file rows", labelpad=4)
    ax.grid(axis="x", color=GRID, linewidth=0.6, zorder=0)
    clean_axis(ax)
    ax.tick_params(axis="y", length=0, pad=6)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.58, 0.993),
               frameon=False, fontsize=8, ncol=1, labelspacing=0.4, handlelength=1.5)
    return fig


def figure4() -> plt.Figure:
    rows = read_csv("figure4_budget_capacity.csv")
    x = np.asarray([int(r["cumulative_science_bytes"]) / 1e9 for r in rows])
    y = np.asarray([int(r["evaluation_opportunities"]) for r in rows])
    fig = plt.figure(figsize=(3.5, 2.95))
    ax = fig.add_axes([0.170, 0.200, 0.780, 0.615])
    ax.plot(x, y, color=BLUE, lw=1.5, marker="o", markersize=4.5,
            markeredgecolor="white", markeredgewidth=0.6, zorder=4)
    for xi, yi in zip(x, y):
        ax.annotate(str(int(yi)), (xi, yi), xytext=(0, 7), textcoords="offset points",
                    ha="center", va="bottom", fontsize=8)
    ax.axhline(400, color=RED, linestyle=(0, (4, 2.5)), lw=1.0)
    ax.text(6.96, 410, "Capacity threshold: 400", color=RED, fontsize=7.6, va="bottom")
    ax.axvline(10.0, color="#6D767D", linestyle=(0, (1.2, 2.0)), lw=1.0)
    ax.text(10.035, 250, "10.0 GB cap", rotation=90, fontsize=7.4,
            ha="left", va="center", color="#59636B")
    ax.set_xlim(6.85, 10.19)
    ax.set_ylim(0, 445)
    ax.set_xticks([7, 8, 9, 10])
    ax.set_yticks([0, 100, 200, 300, 400])
    ax.set_xlabel("Transferred science data (decimal GB)", labelpad=5, fontsize=8)
    ax.set_ylabel("Evaluation opportunities", labelpad=5)
    ax.grid(axis="y", color=GRID, lw=0.6, zorder=0)
    clean_axis(ax)
    top = ax.twiny()
    top.set_xlim(ax.get_xlim())
    top.set_xticks(x, [r["active_files"] for r in rows])
    top.set_xlabel("Active files", labelpad=5, fontsize=8)
    top.tick_params(length=2, pad=3, width=0.5, labelsize=7.7)
    top.spines[["left", "right", "bottom"]].set_visible(False)
    top.spines["top"].set_color(GRID)
    top.spines["top"].set_linewidth(0.6)
    return fig


def diagnostic_panel(ax: plt.Axes, rows: list[dict[str, str]], title: str) -> object:
    values = matrix(rows)
    denominators = np.asarray([int(r["total"]) for r in rows])
    percent = 100 * values / denominators[:, None]
    mesh = ax.pcolormesh(np.arange(5), np.arange(len(rows) + 1), percent,
                        cmap=CMAP, norm=Normalize(0, 100), shading="flat",
                        linewidth=0.4, edgecolors="white", rasterized=False)
    ax.set_xlim(0, 4)
    ax.set_ylim(len(rows), 0)
    labels = []
    for row in rows:
        if row["panel"] == "source_block":
            labels.append(f"{row['group'].replace('_', ' ')} (n={row['total']})")
        else:
            labels.append(row["group"])
    ax.set_yticks(np.arange(len(rows)) + 0.5, labels)
    ax.set_xticks(np.arange(4) + 0.5,
                  ["Valid", "<2 valid\ncandidates", "No\noverlap", "Time\ninvalid"])
    ax.tick_params(length=0, pad=4, labelsize=8)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, loc="left", pad=10, fontsize=9.5, fontweight="bold")
    for i in range(len(rows)):
        for j in range(4):
            p = float(percent[i, j])
            ax.text(j + 0.5, i + 0.5, f"{int(values[i, j])}\n{p:.0f}%",
                    ha="center", va="center", fontsize=8.4, linespacing=1.08,
                    color=annotation_color(p / 100))
    return mesh


def figure5() -> plt.Figure:
    rows = read_csv("figure5_terminal_counts.csv")
    fig = plt.figure(figsize=(7.16, 6.0))
    axes = [fig.add_axes([0.125, 0.510, 0.330, 0.420]),
            fig.add_axes([0.610, 0.510, 0.330, 0.420]),
            fig.add_axes([0.190, 0.180, 0.750, 0.225])]
    for ax, panel, title in zip(axes, ["stratum", "station", "source_block"],
                                ["(a) Stratum", "(b) Evaluation station", "(c) Source-file sensing block"]):
        mesh = diagnostic_panel(ax, [r for r in rows if r["panel"] == panel], title)
    cax = fig.add_axes([0.285, 0.062, 0.530, 0.017])
    cb = fig.colorbar(mesh, cax=cax, orientation="horizontal", ticks=[0, 25, 50, 75, 100])
    cb.solids.set_rasterized(False)
    cb.ax.tick_params(labelsize=7.5, length=2, pad=2)
    cb.outline.set_linewidth(0.5)
    cb.set_label("Within-row percentage", fontsize=8, labelpad=3)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "paper" / "figures")
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.preview_dir is not None:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    summary = check_transcription()
    style()
    for number, make in enumerate([figure1, figure2, figure3, figure4, figure5], start=1):
        finish(make(), number, args.output_dir, args.preview_dir)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
