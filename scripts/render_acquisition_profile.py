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
BLUE = "#315E7D"
INK = "#202A32"
GRID = "#DDE2E7"
RED = "#9E493F"


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


def clean_axis(ax: plt.Axes) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(width=0.7, length=3)
    ax.set_axisbelow(True)
    ax.grid(axis="y", color=GRID, lw=0.6)


def make_figure(source: list[dict[str, str]], derived: list[dict[str, str]]) -> plt.Figure:
    fig = plt.figure(figsize=(7.16, 3.2))
    cumulative = fig.add_axes([0.080, 0.235, 0.365, 0.525])
    marginal = fig.add_axes([0.600, 0.235, 0.375, 0.525])

    x = np.asarray([int(r["cumulative_science_bytes"]) / 1e9 for r in source])
    y = np.asarray([int(r["evaluation_opportunities"]) for r in source])
    cumulative.plot(x, y, color=BLUE, lw=1.5, marker="o", markersize=4.5,
                    markeredgecolor="white", markeredgewidth=0.6, zorder=4)
    for xi, yi in zip(x, y):
        cumulative.annotate(str(int(yi)), (xi, yi), xytext=(0, 7),
                            textcoords="offset points", ha="center", va="bottom", fontsize=8)
    cumulative.axhline(400, color=RED, linestyle=(0, (4, 2.5)), lw=1.0)
    cumulative.text(6.96, 410, "Required: 400", color=RED, fontsize=8, va="bottom")
    cumulative.axvline(10.0, color="#6D767D", linestyle=(0, (1.2, 2.0)), lw=1.0)
    cumulative.text(10.035, 245, "10.0 GB cap", rotation=90, fontsize=8,
                    ha="left", va="center", color="#59636B")
    cumulative.set_xlim(6.85, 10.25)
    cumulative.set_ylim(0, 450)
    cumulative.set_xticks([7, 8, 9, 10])
    cumulative.set_yticks([0, 100, 200, 300, 400])
    cumulative.set_xlabel("Transferred science data (decimal GB)", labelpad=5, fontsize=8)
    cumulative.set_ylabel("Evaluation opportunities", labelpad=4)
    clean_axis(cumulative)

    top = cumulative.twiny()
    top.set_xlim(cumulative.get_xlim())
    top.set_xticks(x, [r["active_files"] for r in source])
    top.set_xlabel("Active files", labelpad=4, fontsize=8)
    top.tick_params(length=2, pad=3, width=0.5, labelsize=8)
    top.spines[["left", "right", "bottom"]].set_visible(False)
    top.spines["top"].set_color(GRID)
    top.spines["top"].set_linewidth(0.6)

    rounds = np.asarray([int(r["alternate_round"]) for r in derived])
    rates = np.asarray([float(r["opportunities_per_decimal_gb"]) for r in derived])
    bars = marginal.bar(rounds, rates, width=0.76, color=BLUE, edgecolor=BLUE,
                        linewidth=0.6, zorder=3)
    for bar, row, rate in zip(bars, derived, rates):
        marginal.text(bar.get_x() + bar.get_width()/2, rate + 0.6, f"{rate:.2f}",
                      ha="center", va="bottom", fontsize=8.5)
        inside = (f"{row['additional_evaluation_opportunities']} opp.\n"
                  f"{float(row['new_science_decimal_gb']):.3f} GB")
        marginal.text(bar.get_x() + bar.get_width()/2, min(rate*0.50, 8.5), inside,
                      ha="center", va="center", color="white", fontsize=8, linespacing=1.3)
    marginal.set_xlim(0.45, 4.55)
    marginal.set_ylim(0, 24)
    marginal.set_xticks(rounds)
    marginal.set_yticks([0, 5, 10, 15, 20])
    marginal.set_xlabel("Alternate round", labelpad=5)
    marginal.set_ylabel("Added opportunities per decimal GB", labelpad=4)
    clean_axis(marginal)
    marginal.text(0.5, 1.11, "Within bars: added count and transfer cost",
                  transform=marginal.transAxes, ha="center", va="center", fontsize=8)

    fig.text(0.080, 0.965, "(a) Cumulative capacity", fontsize=9.5, weight="bold", va="top")
    fig.text(0.600, 0.965, "(b) Marginal yield by alternate round", fontsize=9.5,
             weight="bold", va="top")
    fig.text(0.52, 0.035,
             "Descriptive arithmetic from the executed sequence; no counterfactual policy comparison.",
             ha="center", va="center", fontsize=8)
    return fig


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=ROOT / "paper/figures")
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    source, derived = derive_rows()
    csv_path = DATA / "acquisition_marginal_yield.csv"
    with csv_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(derived[0]))
        writer.writeheader()
        writer.writerows(derived)
    set_style()
    fig = make_figure(source, derived)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = args.output_dir / "acquisition_profile.pdf"
    fig.savefig(pdf_path, metadata={
        "Title": "Reported acquisition capacity and descriptive marginal yield",
        "Subject": "Derived from transcribed source-manuscript totals; no new experiment",
        "Creator": "Matplotlib; scripts/render_acquisition_profile.py",
    })
    if args.preview_dir is not None:
        args.preview_dir.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.preview_dir / "acquisition_profile.png", dpi=220)
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
