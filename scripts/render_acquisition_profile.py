#!/usr/bin/env python3
"""Plot reported acquisition totals and their descriptive marginal yields.

This AI-assisted editorial visualization reads the transcribed source-study
totals in data/figure4_budget_capacity.csv. It does not acquire satellite data,
rerun the original audit, estimate an optimal policy, or simulate new rounds.
Each rate is the observed opportunity increment divided by its byte increment
in decimal GB (1 GB = 1,000,000,000 bytes). The CSV retains integer byte totals
and round-trip float precision; the display uses rounded labels.
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
from figure_style import (BLUE, TEAL, LIGHT_TEAL, INK, MUTED, GRID, RED,
                          clean_axis, style_context, save_figure)


def derive_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    """Reconcile the five reported stages and derive only adjacent increments."""
    with (DATA / "figure4_budget_capacity.csv").open(newline="", encoding="utf-8") as f:
        source = list(csv.DictReader(f))
    byte_totals = [int(r["cumulative_science_bytes"]) for r in source]
    counts = [int(r["evaluation_opportunities"]) for r in source]
    if byte_totals != [7003624776, 7614139230, 8210344923, 8800674162, 9418446350]:
        raise ValueError("Acquisition byte totals differ from the reported source record")
    if counts != [114, 125, 134, 145, 150]:
        raise ValueError("Opportunity totals differ from the reported source record")
    if [int(r["active_files"]) for r in source] != [96, 104, 112, 120, 128]:
        raise ValueError("The five stages must contain the primary set and four full rounds")

    derived = []
    for i, (previous, current) in enumerate(zip(source, source[1:]), start=1):
        byte_increment = int(current["cumulative_science_bytes"]) - int(previous["cumulative_science_bytes"])
        count_increment = int(current["evaluation_opportunities"]) - int(previous["evaluation_opportunities"])
        if count_increment != int(current["increment"]) or byte_increment <= 0:
            raise ValueError("A source-stage increment does not reconcile")
        decimal_gb = byte_increment / 1e9
        rate = count_increment / decimal_gb
        derived.append({
            "alternate_round": str(i),
            "source_previous_stage": previous["stage"],
            "source_current_stage": current["stage"],
            "additional_evaluation_opportunities": str(count_increment),
            "new_science_bytes": str(byte_increment),
            "new_science_decimal_gb": f"{decimal_gb:.9f}",
            "opportunities_per_decimal_gb": format(rate, ".17g"),
        })
    return source, derived


def make_figure(source: list[dict[str, str]], derived: list[dict[str, str]]) -> plt.Figure:
    fig = plt.figure(figsize=(7.16, 3.2))
    cumulative = fig.add_axes([0.080, 0.245, 0.365, 0.520])
    marginal = fig.add_axes([0.600, 0.245, 0.375, 0.520])

    x = np.asarray([int(r["cumulative_science_bytes"]) / 1e9 for r in source])
    y = np.asarray([int(r["evaluation_opportunities"]) for r in source])
    cumulative.plot(x, y, color=BLUE, lw=1.8, marker="o", markersize=5.2,
                    markeredgecolor="white", markeredgewidth=0.7, zorder=4)
    for xi, yi in zip(x, y):
        cumulative.annotate(str(int(yi)), (xi, yi), xytext=(0, 8),
                            textcoords="offset points", ha="center", va="bottom",
                            fontsize=8.5, color=BLUE)
    cumulative.axhline(400, color=RED, linestyle=(0, (4, 3)), lw=0.8, zorder=2)
    cumulative.text(6.96, 410, "Required: 400", color=RED, fontsize=8, va="bottom")
    cumulative.axvline(10.0, color=MUTED, linestyle=(0, (1.2, 2.5)), lw=0.75, zorder=2)
    cumulative.text(10.035, 245, "10.0 GB cap", rotation=90, fontsize=8,
                    ha="left", va="center", color=MUTED)
    cumulative.set_xlim(6.85, 10.25)
    cumulative.set_ylim(0, 450)
    cumulative.set_xticks([7, 8, 9, 10])
    cumulative.set_yticks([0, 100, 200, 300, 400])
    cumulative.set_xlabel("Transferred science data (decimal GB)", labelpad=5, fontsize=8)
    cumulative.set_ylabel("Evaluation opportunities", labelpad=4)
    clean_axis(cumulative, grid_axis="y")

    top = cumulative.twiny()
    top.set_xlim(cumulative.get_xlim())
    top.set_xticks(x, [r["active_files"] for r in source])
    top.set_xlabel("Active files", labelpad=4, fontsize=8, color=MUTED)
    top.tick_params(length=2, pad=3, width=0.5, labelsize=8)
    top.spines[["left", "right", "bottom"]].set_visible(False)
    top.spines["top"].set_color(GRID)
    top.spines["top"].set_linewidth(0.5)

    rounds = np.asarray([int(r["alternate_round"]) for r in derived])
    rates = np.asarray([float(r["opportunities_per_decimal_gb"]) for r in derived])
    bars = marginal.bar(rounds, rates, width=0.84, color=LIGHT_TEAL,
                        edgecolor=TEAL, linewidth=0.75, zorder=3)
    for bar, row, rate in zip(bars, derived, rates):
        center = bar.get_x() + bar.get_width()/2
        marginal.text(center, rate + 0.65, f"{rate:.2f}",
                      ha="center", va="bottom", fontsize=9, color=TEAL, weight="bold")
        marginal.text(center, 4.1, f"{row['additional_evaluation_opportunities']} opp.",
                      ha="center", va="center", color=INK, fontsize=8.5)
        marginal.text(center, 1.75, f"{float(row['new_science_decimal_gb']):.3f} GB",
                      ha="center", va="center", color=INK, fontsize=8)
    marginal.set_xlim(0.45, 4.55)
    marginal.set_ylim(0, 24)
    marginal.set_xticks(rounds)
    marginal.set_yticks([0, 5, 10, 15, 20])
    marginal.set_xlabel("Alternate round", labelpad=5)
    marginal.set_ylabel("Added opportunities per decimal GB", labelpad=4)
    clean_axis(marginal, grid_axis="y")
    marginal.text(0, 1.11, "Within bars: added count and transfer volume",
                  transform=marginal.transAxes, ha="left", va="center", fontsize=8,
                  color=MUTED)

    fig.text(0.080, 0.965, "(a) Cumulative capacity", fontsize=10, weight="bold", va="top")
    fig.text(0.600, 0.965, "(b) Marginal acquisition yield", fontsize=10,
             weight="bold", va="top")
    fig.text(0.52, 0.040,
             "Descriptive arithmetic from the executed sequence; no counterfactual policy comparison.",
             ha="center", va="center", fontsize=8, color=MUTED)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "paper/figures")
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    source, derived = derive_rows()
    csv_path = DATA / "acquisition_marginal_yield.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(derived[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(derived)
    pdf_path = args.output_dir / "acquisition_profile.pdf"
    with style_context():
        fig = make_figure(source, derived)
        save_figure(fig, pdf_path,
                    title="Reported acquisition capacity and descriptive marginal yield",
                    subject="Derived from transcribed source-manuscript totals; no new experiment",
                    creator="Matplotlib; scripts/render_acquisition_profile.py",
                    preview_path=(args.preview_dir / "acquisition_profile.png")
                    if args.preview_dir is not None else None)
        plt.close(fig)
    print(json.dumps({
        "output_pdf": str(pdf_path), "derived_csv": str(csv_path),
        "additional_opportunities": [int(r["additional_evaluation_opportunities"]) for r in derived],
        "new_science_bytes": [int(r["new_science_bytes"]) for r in derived],
        "opportunities_per_decimal_gb": [float(r["opportunities_per_decimal_gb"]) for r in derived],
        "scope": "Descriptive adjacent-stage arithmetic; no independent experimental replay.",
    }, indent=2))


if __name__ == "__main__":
    main()
