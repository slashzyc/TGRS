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
from figure_style import (BLUE, TEAL, LIGHT_TEAL, AMBER, LIGHT_AMBER,
                          INK, MUTED, RED, clean_axis, style_context, save_figure)


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


def make_figure(summary: dict) -> plt.Figure:
    fig = plt.figure(figsize=(7.16, 3.2))
    local = fig.add_axes([0.088, 0.265, 0.350, 0.570])
    total = fig.add_axes([0.605, 0.265, 0.370, 0.570])

    stations = summary["station_deficits"]
    positions = np.arange(len(stations))
    deficits = [station["positive_cell_deficit"] for station in stations]
    local.barh(positions, deficits, height=0.60, color=TEAL, edgecolor=TEAL,
               linewidth=0.5, zorder=3)
    local.set_yticks(positions, [station["station"] for station in stations])
    local.invert_yaxis()
    local.set_xlim(0, 45)
    local.set_xticks([0, 10, 20, 30, 40])
    local.set_xlabel("Minimum added opportunities\nfor all five cells to reach 8", labelpad=5, fontsize=8)
    for y, deficit in zip(positions, deficits):
        local.text(deficit + 0.8, y, str(deficit), va="center", ha="left",
                   fontsize=8.5, color=TEAL, weight="bold")
    clean_axis(local, grid_axis="x")
    local.tick_params(axis="y", length=0, pad=5)
    local.text(0, 1.055, "Total positive cell deficit: 171", transform=local.transAxes,
               ha="left", va="bottom", fontsize=8, color=MUTED)

    bases = [0, summary["reported_opportunities"], summary["total_after_minimal_cell_filling"]]
    heights = [summary["reported_opportunities"], summary["minimum_cell_gap_additions"],
               summary["remaining_total_gap_after_cell_filling"]]
    colors = [BLUE, LIGHT_TEAL, LIGHT_AMBER]
    edges = [BLUE, TEAL, AMBER]
    hatches = [None, "/", "."]
    width = 0.62
    for x, bottom, height, color, edge, hatch in zip(range(3), bases, heights, colors, edges, hatches):
        total.bar(x, height, bottom=bottom, width=width, color=color, edgecolor=edge,
                  linewidth=0.75, hatch=hatch, zorder=3)
        label = str(height) if x == 0 else f"+{height}"
        total.text(x, bottom + height / 2, label, ha="center", va="center",
                   color="white" if x == 0 else INK, fontsize=10, weight="bold", zorder=4,
                   bbox=None if x == 0 else {"facecolor": color, "edgecolor": "none", "pad": 1.5})
        if x < 2:
            top = bottom + height
            total.plot([x + width / 2, x + 1 - width / 2], [top, top],
                       color=MUTED, lw=0.65, zorder=2)
    total.text(1, summary["total_after_minimal_cell_filling"] + 9, "321",
               ha="center", va="bottom", fontsize=10, weight="bold", color=TEAL)
    total.axhline(summary["total_threshold"], color=RED, linestyle=(0, (4, 3)),
                  lw=0.8, zorder=2)
    total.text(-0.48, summary["total_threshold"] + 8, "Required: 400", color=RED,
               ha="left", va="bottom", fontsize=8)
    total.set_xlim(-0.55, 2.55)
    total.set_ylim(0, 455)
    total.set_yticks([0, 100, 200, 300, 400])
    total.set_xticks([0, 1, 2], ["Reported\ncount", "Fill cell\ndeficits", "Remaining\ntotal gap"])
    total.set_ylabel("Total opportunities", labelpad=4, fontsize=8.5)
    clean_axis(total, grid_axis="y")
    total.text(0, 1.055, "Existing counts retained; additions only",
               transform=total.transAxes, ha="left", va="bottom", fontsize=8, color=MUTED)

    fig.text(0.088, 0.965, "(a) Cell deficits by station", weight="bold", fontsize=10, va="top")
    fig.text(0.605, 0.965, "(b) Two-part capacity shortfall", weight="bold", fontsize=10, va="top")
    fig.text(0.52, 0.045, "Arithmetic lower bounds on reported counts; no acquisition forecast.",
             ha="center", va="center", fontsize=8, color=MUTED)
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
    pdf_path = args.output_dir / "capacity_shortfall.pdf"
    with style_context():
        fig = make_figure(summary)
        save_figure(fig, pdf_path,
                    title="Cell deficits and the two-part capacity shortfall",
                    subject="Arithmetic lower bounds from source-reported station-block counts; no acquisition forecast",
                    creator="Matplotlib; scripts/render_capacity_shortfall.py",
                    preview_path=(args.preview_dir / "capacity_shortfall.png")
                    if args.preview_dir is not None else None)
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
