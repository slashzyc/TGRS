#!/usr/bin/env python3
"""Draw allocation-dependent arithmetic shortfalls from the reported matrix.

This ChatGPT-assisted editorial code reads the 40 source-reported cell counts
and the two configured thresholds. It creates no new observations, estimates
no acquisition yield, and does not rerun the original scientific workflow.
The calculation preserves all existing opportunities, including surplus in
cells already above their threshold, and considers additions only.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
BLUE = "#315E7D"
LIGHT_BLUE = "#AFC6D5"
SAND = "#DFC8A7"
INK = "#202A32"
GRID = "#DDE2E7"
RED = "#9E493F"


def derive_data() -> tuple[list[dict[str, int | str]], dict]:
    """Retain the 40 counts and derive positive, nontransferable cell gaps."""
    matrix_path = DATA / "figure2_station_blocks.csv"
    threshold_path = DATA / "figure1_flow_parameters.csv"
    with matrix_path.open(newline="", encoding="utf-8") as stream:
        matrix = list(csv.DictReader(stream))
    with threshold_path.open(newline="", encoding="utf-8") as stream:
        parameters = {row["parameter"]: int(row["value"])
                      for row in csv.DictReader(stream)}
    cell_threshold = parameters["cell_threshold"]
    total_threshold = parameters["capacity_threshold"]
    blocks = parameters["reporting_blocks"]
    if (cell_threshold, total_threshold, blocks) != (8, 400, 5):
        raise ValueError("Configured thresholds or block count differ from the source record")
    if len(matrix) != parameters["evaluation_stations"]:
        raise ValueError("Evaluation station count does not reconcile")

    cells = []
    station_summaries = []
    for row in matrix:
        counts = [int(row[f"block_{block:02d}"]) for block in range(1, blocks + 1)]
        if min(counts) < 0 or sum(counts) != int(row["total"]):
            raise ValueError(f"Station row does not reconcile: {row['station']}")
        for block, count in enumerate(counts, start=1):
            cells.append({
                "station": row["station"],
                "reporting_block": f"Block_{block:02d}",
                "reported_opportunities": count,
                "cell_threshold": cell_threshold,
                "positive_cell_deficit": max(cell_threshold - count, 0),
                "surplus_above_cell_threshold": max(count - cell_threshold, 0),
                "reaches_cell_threshold": int(count >= cell_threshold),
            })
        station_summaries.append({
            "station": row["station"],
            "reported_opportunities": sum(counts),
            "positive_cell_deficit": sum(max(cell_threshold - count, 0) for count in counts),
            "deficient_cells": sum(count < cell_threshold for count in counts),
        })

    observed = sum(cell["reported_opportunities"] for cell in cells)
    local_gap = sum(cell["positive_cell_deficit"] for cell in cells)
    excess = sum(cell["surplus_above_cell_threshold"] for cell in cells)
    after_cell_filling = observed + local_gap
    remaining_total_gap = max(total_threshold - after_cell_filling, 0)
    if observed != parameters["final_opportunities"]:
        raise ValueError("Observed total differs from the reported workflow total")
    if after_cell_filling != cell_threshold * len(cells) + excess:
        raise ValueError("Cell-filling arithmetic does not retain the existing surplus")
    if [station["positive_cell_deficit"] for station in station_summaries] != [39, 18, 11, 26, 40, 10, 21, 6]:
        raise ValueError("Derived station deficits differ from the audited source matrix")
    if (observed, local_gap, after_cell_filling, remaining_total_gap) != (150, 171, 321, 79):
        raise ValueError("Derived aggregate shortfalls do not reconcile")

    source_files = []
    for path in (matrix_path, threshold_path):
        source_files.append({
            "path": path.relative_to(ROOT).as_posix(),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    summary = {
        "scope": "Arithmetic lower bounds on the fixed reported counts; no new observations or acquisition forecast.",
        "source_files": source_files,
        "population": "Eight evaluation stations across five valid center-pixel reporting blocks.",
        "counting_unit": "Unique station-observation opportunities",
        "cell_threshold": cell_threshold,
        "total_threshold": total_threshold,
        "total_cells": len(cells),
        "reported_opportunities": observed,
        "zero_cells": sum(cell["reported_opportunities"] == 0 for cell in cells),
        "cells_below_threshold": sum(cell["reported_opportunities"] < cell_threshold for cell in cells),
        "cells_reaching_threshold": sum(cell["reaches_cell_threshold"] for cell in cells),
        "minimum_cell_gap_additions": local_gap,
        "existing_surplus_above_cell_threshold": excess,
        "total_after_minimal_cell_filling": after_cell_filling,
        "remaining_total_gap_after_cell_filling": remaining_total_gap,
        "minimum_total_additions_for_both_thresholds": max(total_threshold - observed, local_gap),
        "station_deficits": station_summaries,
        "formula": "d[s,b] = max(cell_threshold - N[s,b], 0); D[s] = sum_b d[s,b]",
        "interpretation": "All existing opportunities are retained. At least 171 additions must fall in the 37 deficient cells in the required amounts; another 79 additions are needed for the overall total. This does not establish that such opportunities exist or can be acquired.",
        "surplus_note": "One existing cell contains nine opportunities. Its surplus is retained but cannot cancel another cell's deficit, so minimal cell filling gives 321 rather than 320.",
        "ai_assistance": "ChatGPT assisted figure design and plotting code; numerical inputs are transcribed source counts and explicitly stated arithmetic.",
    }
    return cells, summary


def set_style() -> None:
    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5,
        "axes.labelsize": 8.5, "axes.titlesize": 9.5,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "axes.linewidth": 0.7, "axes.edgecolor": INK,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK,
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "savefig.facecolor": "white",
    })


def make_figure(summary: dict) -> plt.Figure:
    fig = plt.figure(figsize=(7.16, 3.2))
    local = fig.add_axes([0.088, 0.265, 0.350, 0.570])
    total = fig.add_axes([0.605, 0.265, 0.370, 0.570])

    stations = summary["station_deficits"]
    positions = np.arange(len(stations))
    deficits = [station["positive_cell_deficit"] for station in stations]
    local.barh(positions, deficits, height=0.65, color=BLUE, edgecolor=BLUE, linewidth=0.5)
    local.set_yticks(positions, [station["station"] for station in stations])
    local.invert_yaxis()
    local.set_xlim(0, 45)
    local.set_xticks([0, 10, 20, 30, 40])
    local.set_xlabel("Minimum added opportunities\nfor all five cells to reach 8", labelpad=5, fontsize=8)
    for y, deficit in zip(positions, deficits):
        local.text(deficit + 0.8, y, str(deficit), va="center", ha="left", fontsize=8.5)
    local.spines[["top", "right"]].set_visible(False)
    local.tick_params(width=0.7, length=3)
    local.set_axisbelow(True)
    local.grid(axis="x", color=GRID, lw=0.6)
    local.text(0, 1.055, "Sum of positive cell deficits: 171", transform=local.transAxes,
               ha="left", va="bottom", fontsize=8)

    bases = [0, summary["reported_opportunities"], summary["total_after_minimal_cell_filling"]]
    heights = [summary["reported_opportunities"], summary["minimum_cell_gap_additions"],
               summary["remaining_total_gap_after_cell_filling"]]
    colors = [BLUE, LIGHT_BLUE, SAND]
    hatches = [None, "///", "..."]
    width = 0.62
    for x, bottom, height, color, hatch in zip(range(3), bases, heights, colors, hatches):
        total.bar(x, height, bottom=bottom, width=width, color=color, edgecolor=BLUE,
                  linewidth=0.6, hatch=hatch, zorder=3)
        label = str(height) if x == 0 else f"+{height}"
        total.text(x, bottom + height / 2, label, ha="center", va="center",
                   color="white" if x == 0 else INK, fontsize=9, weight="bold", zorder=4,
                   bbox=None if x == 0 else {"facecolor": color, "edgecolor": "none", "pad": 1.0})
        if x < 2:
            top = bottom + height
            total.plot([x + width / 2, x + 1 - width / 2], [top, top],
                       color="#7F8B94", lw=0.7, zorder=2)
    total.text(1, summary["total_after_minimal_cell_filling"] + 9, "321",
               ha="center", va="bottom", fontsize=8.5)
    total.axhline(summary["total_threshold"], color=RED, linestyle=(0, (4, 2.5)), lw=0.9, zorder=2)
    total.text(-0.48, summary["total_threshold"] + 8, "Required: 400", color=RED,
               ha="left", va="bottom", fontsize=8)
    total.set_xlim(-0.55, 2.55)
    total.set_ylim(0, 455)
    total.set_yticks([0, 100, 200, 300, 400])
    total.set_xticks([0, 1, 2], ["Reported\ncount", "Fill cell\ndeficits", "Remaining\ntotal gap"])
    total.set_ylabel("Total opportunities", labelpad=4, fontsize=8)
    total.spines[["top", "right"]].set_visible(False)
    total.tick_params(width=0.7, length=3)
    total.set_axisbelow(True)
    total.grid(axis="y", color=GRID, lw=0.6)
    total.text(0, 1.055, "Preserve existing counts; consider additions only",
               transform=total.transAxes, ha="left", va="bottom", fontsize=8)

    fig.text(0.088, 0.965, "(a) Cell deficits by station", weight="bold", fontsize=9.5, va="top")
    fig.text(0.605, 0.965, "(b) Two-part capacity shortfall", weight="bold", fontsize=9.5, va="top")
    fig.text(0.52, 0.045, "Arithmetic lower bounds on reported counts; no acquisition forecast.",
             ha="center", va="center", fontsize=8)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "paper/figures")
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    cells, summary = derive_data()
    csv_path = DATA / "capacity_cell_shortfalls.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(cells[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(cells)
    json_path = DATA / "capacity_shortfall_summary.json"
    json_path.write_text(json.dumps(summary, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")
    set_style()
    fig = make_figure(summary)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = args.output_dir / "capacity_shortfall.pdf"
    fig.savefig(pdf_path, metadata={
        "Title": "Cell deficits and the two-part capacity shortfall",
        "Subject": "Arithmetic lower bounds from source-reported station-block counts; no acquisition forecast",
        "Creator": "Matplotlib; scripts/render_capacity_shortfall.py",
        "CreationDate": None,
        "ModDate": None,
    })
    if args.preview_dir is not None:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.preview_dir / "capacity_shortfall.png", dpi=220)
    plt.close(fig)
    print(json.dumps({
        "output_pdf": str(pdf_path), "derived_csv": str(csv_path), "summary_json": str(json_path),
        "cell_deficits": [station["positive_cell_deficit"] for station in summary["station_deficits"]],
        "minimum_cell_gap_additions": summary["minimum_cell_gap_additions"],
        "total_after_minimal_cell_filling": summary["total_after_minimal_cell_filling"],
        "remaining_total_gap_after_cell_filling": summary["remaining_total_gap_after_cell_filling"],
        "scope": summary["scope"],
    }, indent=2))


if __name__ == "__main__":
    main()
