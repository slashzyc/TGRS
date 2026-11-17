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
from matplotlib.colors import BoundaryNorm, ListedColormap, Normalize
from matplotlib.patches import Rectangle
import numpy as np

from figure_style import (AMBER, BLUE, CMAP, GRID, INK, LIGHT_AMBER, LIGHT_BLUE,
                          MUTED, PALE, RED, style_context, save_figure)
from render_workflow import make_figure as make_workflow_figure


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
STATES = ("extract_valid", "fewer_than_2_candidates", "no_overlap", "time_invalid")


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


def finish(fig: plt.Figure, number: int, output_dir: Path, preview_dir: Path | None) -> None:
    titles = {1: "Selection, capacity stopping and replay integrity",
              2: "Evaluation opportunity matrix", 3: "Processing states by station role",
              4: "Legacy cumulative acquisition profile", 5: "Detailed processing diagnostics"}
    save_figure(fig, output_dir / f"figure{number}.pdf", title=titles[number],
                subject="Editorial rendering from reported aggregate values; see data/README.md",
                creator="Matplotlib; scripts/render_figures.py",
                preview_path=preview_dir / f"figure{number}.png" if preview_dir else None)
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


def figure1() -> plt.Figure:
    return make_workflow_figure()


def figure2() -> plt.Figure:
    rows = read_csv("figure2_station_blocks.csv")
    values = matrix(rows, tuple(f"block_{i:02d}" for i in range(1, 6)))
    fig = plt.figure(figsize=(3.5, 3.4))
    fig.text(0.185, 0.982, "150 opportunities · 3/40 cells ≥8", fontsize=8.2,
             fontweight="bold", va="top")
    ax = fig.add_axes([0.185, 0.260, 0.780, 0.675])
    discrete = ListedColormap([CMAP(i / 9) for i in range(10)])
    norm = BoundaryNorm(np.arange(-0.5, 10.5), discrete.N)
    mesh = ax.pcolormesh(np.arange(6), np.arange(9), values, cmap=discrete,
                        norm=norm, shading="flat", linewidth=0.45,
                        edgecolors="white", rasterized=False)
    ax.add_patch(Rectangle((5.12, 0), 0.78, 8, facecolor=PALE, edgecolor="none", zorder=0))
    ax.plot([5.12, 5.12], [0, 8], color=GRID, linewidth=0.7)
    ax.set_xlim(0, 5.95)
    ax.set_ylim(8, 0)
    ax.set_xticks(np.arange(5) + 0.5, [f"{i:02d}" for i in range(1, 6)])
    ax.set_yticks(np.arange(8) + 0.5, [r["station"] for r in rows])
    ax.set_xlabel("28-day reporting block", labelpad=5)
    ax.tick_params(length=0, pad=4, labelsize=8.2)
    for spine in ax.spines.values():
        spine.set_visible(False)
    for i in range(8):
        for j in range(5):
            v = int(values[i, j])
            color = MUTED if v == 0 else annotation_color(v / 9)
            ax.text(j + 0.5, i + 0.5, str(v), ha="center", va="center", fontsize=9,
                    color=color, fontweight="bold" if v >= 8 else "normal")
            if v >= 8:
                ax.add_patch(Rectangle((j + 0.035, i + 0.035), 0.93, 0.93,
                                      fill=False, edgecolor=AMBER, linewidth=1.15))
        ax.text(5.52, i + 0.5, rows[i]["total"], ha="center", va="center",
                fontsize=8.5, fontweight="bold", color=INK)
    ax.text(5.52, -0.34, "Total", ha="center", va="center", fontsize=8.2,
            color=MUTED, clip_on=False)
    cax = fig.add_axes([0.235, 0.108, 0.625, 0.033])
    cb = fig.colorbar(mesh, cax=cax, orientation="horizontal", ticks=np.arange(10))
    cb.solids.set_rasterized(False)
    cb.solids.set_edgecolor("face")
    cb.outline.set_visible(False)
    cb.ax.tick_params(labelsize=8, length=2, width=0.5, pad=2)
    cb.set_label("Opportunities per station–block", fontsize=8, labelpad=4)
    return fig


def figure3() -> plt.Figure:
    rows = read_csv("figure3_terminal_counts.csv")
    values = matrix(rows)
    fig = plt.figure(figsize=(3.5, 2.95))
    ax = fig.add_axes([0.320, 0.195, 0.645, 0.620])
    positions = np.arange(4)
    roles = [(-0.16, BLUE, BLUE, None), (0.16, LIGHT_AMBER, AMBER, "/")]
    for i, (offset, color, edge, hatch) in enumerate(roles):
        bars = ax.barh(positions + offset, values[i], height=0.265, color=color,
                       edgecolor=edge, linewidth=0.65, hatch=hatch,
                       label=f"{rows[i]['role']} (n={int(rows[i]['total']):,})", zorder=3)
        for bar, value in zip(bars, values[i]):
            ax.text(float(value) + 10, bar.get_y() + bar.get_height() / 2,
                    str(int(value)), va="center", fontsize=8.2, color=INK)
    ax.set_yticks(positions, ["Valid extraction", "<2 valid\ncandidates", "No overlap", "Time invalid"])
    ax.set_ylim(3.58, -0.58)
    ax.set_xlim(0, 710)
    ax.set_xticks([0, 200, 400, 600])
    ax.set_xlabel("Station-file rows", labelpad=5)
    ax.grid(axis="x", color=GRID, linewidth=0.45, zorder=0)
    clean_axis(ax)
    ax.tick_params(axis="y", length=0, pad=5, labelsize=8.2)
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper left", bbox_to_anchor=(0.315, 0.993),
               frameon=False, fontsize=8.2, ncol=1, labelspacing=0.45,
               handlelength=1.6, borderaxespad=0, handletextpad=0.6)
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
                        linewidth=0.45, edgecolors="white", rasterized=False)
    ax.set_xlim(0, 4)
    ax.set_ylim(len(rows), 0)
    labels = [f"{r['group'].replace('_', ' ')} (n={r['total']})"
              if r['panel'] == 'source_block' else r['group'] for r in rows]
    ax.set_yticks(np.arange(len(rows)) + 0.5, labels)
    ax.set_xticks(np.arange(4) + 0.5,
                  ["Valid", "<2 valid\ncandidates", "No\noverlap", "Time\ninvalid"])
    ax.tick_params(length=0, pad=4, labelsize=8.3)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.set_title(title, loc="left", pad=10, fontsize=10, fontweight="bold")
    if rows[0]['panel'] == 'stratum':
        ax.axhline(4, color="white", linewidth=1.1)
    for i in range(len(rows)):
        for j in range(4):
            p = float(percent[i, j])
            color = annotation_color(p / 100)
            ax.text(j + 0.5, i + 0.27, str(int(values[i, j])), ha="center", va="center",
                    fontsize=9, fontweight="bold", color=color)
            ax.text(j + 0.5, i + 0.74, f"{p:.0f}%", ha="center", va="center",
                    fontsize=8.0, color=color)
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
    cax = fig.add_axes([0.285, 0.062, 0.530, 0.023])
    cb = fig.colorbar(mesh, cax=cax, orientation="horizontal", ticks=[0, 25, 50, 75, 100])
    cb.solids.set_rasterized(False)
    cb.ax.tick_params(labelsize=8, length=2, width=0.5, pad=2)
    cb.solids.set_edgecolor("face")
    cb.outline.set_visible(False)
    cb.set_label("Within-row percentage", fontsize=8, labelpad=3)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "paper" / "figures")
    parser.add_argument("--preview-dir", type=Path)
    parser.add_argument("--include-legacy", action="store_true",
                        help="Also redraw the superseded cumulative-only figure4.pdf.")
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.preview_dir is not None:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
    summary = check_transcription()
    makers = {1: figure1, 2: figure2, 3: figure3, 5: figure5}
    if args.include_legacy:
        makers[4] = figure4
    with style_context():
        for number, make in sorted(makers.items()):
            finish(make(), number, args.output_dir, args.preview_dir)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
