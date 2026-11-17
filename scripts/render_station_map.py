#!/usr/bin/env python3
"""Render source-reported station locations; this is not a coverage analysis.

The offline Natural Earth land subset contains unchanged source features.
Station coordinates and roles are transcribed from Supplementary Table S1.
The axes use an equidistant cylindrical projection with standard parallel 32 N.
No satellite footprint, product-sector boundary, or new observation is inferred.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import PathPatch, Rectangle
from matplotlib.path import Path as MplPath

ROOT = Path(__file__).resolve().parents[1]
STANDARD_PARALLEL = 32.0
X_SCALE = math.cos(math.radians(STANDARD_PARALLEL))
INK = "#26343d"
BLUE = "#28749a"
ORANGE = "#b96720"
LAND = "#e6e9e8"
COAST = "#849198"
WATER = "#f7fbfd"
NE_STATIONS = {"44008", "44020", "44027"}


def x_project(longitude: float) -> float:
    return longitude * X_SCALE


def read_stations() -> list[dict]:
    with (ROOT / "data/station_locations.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 12 and len({r["station"] for r in rows}) == 12
    assert sum(r["role"] == "Evaluation" for r in rows) == 8
    assert sum(r["role"] == "Development" for r in rows) == 4
    for row in rows:
        row["lat"] = float(row["latitude_deg_n"])
        row["lon"] = float(row["longitude_deg_e"])
    return rows


def add_polygon(ax: plt.Axes, rings: list) -> None:
    vertices, codes = [], []
    for ring in rings:
        if len(ring) < 4:
            continue
        for i, (lon, lat) in enumerate(ring):
            vertices.append((x_project(lon), lat))
            codes.append(MplPath.MOVETO if i == 0 else MplPath.LINETO)
        codes[-1] = MplPath.CLOSEPOLY
    if vertices:
        ax.add_patch(PathPatch(MplPath(vertices, codes), facecolor=LAND,
                               edgecolor=COAST, linewidth=0.4,
                               zorder=2, clip_on=True))


def draw_land(ax: plt.Axes, features: list) -> None:
    for feature in features:
        geometry = feature["geometry"]
        if geometry["type"] == "Polygon":
            add_polygon(ax, geometry["coordinates"])
        elif geometry["type"] == "MultiPolygon":
            for polygon in geometry["coordinates"]:
                add_polygon(ax, polygon)
        else:
            raise ValueError("Unexpected land geometry")


def setup_axis(ax: plt.Axes, extent: tuple, features: list,
               xticks: list, yticks: list) -> None:
    west, east, south, north = extent
    ax.set_facecolor(WATER)
    ax.set_xlim(x_project(west), x_project(east))
    ax.set_ylim(south, north)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xticks([x_project(x) for x in xticks])
    ax.set_xticklabels([f"{abs(x):g}°W" for x in xticks])
    ax.set_yticks(yticks)
    ax.set_yticklabels([f"{y:g}°N" for y in yticks])
    ax.grid(color="#d8e0e4", linewidth=0.5, zorder=1)
    ax.tick_params(length=2.5, width=0.6, pad=3)
    draw_land(ax, features)
    for spine in ax.spines.values():
        spine.set_color(COAST)
        spine.set_linewidth(0.6)


def plot_station(ax: plt.Axes, row: dict, label_offset: tuple | None) -> None:
    evaluation = row["role"] == "Evaluation"
    x, y = x_project(row["lon"]), row["lat"]
    marker, color = ("o", BLUE) if evaluation else ("^", ORANGE)
    if row["station"] == "42056":
        ax.scatter([x], [y], s=91, facecolors="none", edgecolors=ORANGE,
                   linewidths=0.9, zorder=4)
    ax.scatter([x], [y], s=34 if evaluation else 43, marker=marker,
               facecolors=color, edgecolors="white", linewidths=0.6, zorder=5)
    if label_offset is not None:
        dx, dy = label_offset
        ax.annotate(row["station"], xy=(x, y), xytext=(dx, dy),
                    textcoords="offset points", fontsize=8.3, color=INK,
                    ha="left" if dx >= 0 else "right", va="center",
                    arrowprops={"arrowstyle": "-", "color": "#a8b2b7",
                                "lw": 0.5, "shrinkA": 2, "shrinkB": 4},
                    bbox={"facecolor": "white", "edgecolor": "none",
                          "alpha": 0.85, "pad": 0.35}, zorder=6)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "paper/figures/station_map.pdf")
    parser.add_argument("--preview", type=Path)
    args = parser.parse_args()

    plt.rcParams.update({
        "font.family": "DejaVu Sans", "font.size": 8.5,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": INK, "ytick.color": INK,
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "savefig.facecolor": "white",
    })
    stations = read_stations()
    basemap = json.loads((ROOT / "data/basemaps/natural_earth_50m_land_station_region.geojson").read_text())
    features = basemap["features"]
    fig = plt.figure(figsize=(7.16, 4.2))
    main_ax = fig.add_axes([0.065, 0.145, 0.55, 0.79])
    inset = fig.add_axes([0.70, 0.475, 0.27, 0.45])
    setup_axis(main_ax, (-98, -64, 17, 46), features,
               [-95, -85, -75, -65], [20, 25, 30, 35, 40, 45])
    setup_axis(inset, (-73, -64.5, 39.5, 45.5), features,
               [-72, -68], [40, 42, 44])
    main_ax.set_title("(a) Selected station locations", loc="left", pad=7,
                      fontsize=9.2, fontweight="bold")
    inset.set_title("(b) Northeastern detail", loc="left", pad=7,
                    fontsize=9.2, fontweight="bold")

    offsets = {
        "41047": (7, -1), "44014": (7, -1),
        "42056": (9, -6), "42001": (7, 6),
        "42036": (8, -8), "42035": (8, 24),
        "41008": (8, 3), "42002": (8, -8),
        "42039": (-8, 11),
    }
    for row in stations:
        plot_station(main_ax, row, offsets.get(row["station"]))
    inset_offsets = {"44008": (9, -8), "44020": (-8, 8), "44027": (8, -1)}
    for row in stations:
        if row["station"] in NE_STATIONS:
            plot_station(inset, row, inset_offsets[row["station"]])

    main_ax.add_patch(Rectangle((x_project(-73), 39.5),
                               x_project(-64.5) - x_project(-73), 6,
                               fill=False, edgecolor="#647780", linewidth=0.8,
                               linestyle=(0, (3, 2)), zorder=3))
    main_ax.text(x_project(-73.7), 44.7, "b", ha="right", va="center",
                 fontsize=9, fontweight="bold")
    main_ax.text(x_project(-90.2), 22.2, "Gulf of\nMexico", ha="center",
                 va="center", fontsize=8.2, color="#6b838e", fontstyle="italic")
    main_ax.text(x_project(-72.6), 33, "Atlantic Ocean", ha="center",
                 va="center", rotation=52, fontsize=8.5,
                 color="#6b838e", fontstyle="italic")

    handles = [
        Line2D([], [], marker="o", linestyle="none", markersize=6,
               markerfacecolor=BLUE, markeredgecolor="white", label="Evaluation (n = 8)"),
        Line2D([], [], marker="^", linestyle="none", markersize=7,
               markerfacecolor=ORANGE, markeredgecolor="white", label="Development (n = 4)"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.69, 0.44),
               frameon=False, fontsize=8.5, handletextpad=0.5,
               labelspacing=0.6, borderpad=0)
    fig.text(0.70, 0.245, "42056: Yucatan Basin", fontsize=8.3,
             fontweight="bold", color=INK)
    fig.text(0.70, 0.202, "Source selection label: Gulf", fontsize=8.1)
    fig.text(0.70, 0.159, "Product coverage unverified", fontsize=8.1)
    fig.text(0.065, 0.055, "Source-reported station coordinates; no satellite footprints shown.",
             fontsize=8, color="#51646e")
    fig.text(0.065, 0.013, "Land: Natural Earth 1:50m. Equidistant cylindrical projection (32°N).",
             fontsize=8, color="#51646e")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(args.output, metadata={
        "Title": "Source-reported coastal ASCAT station locations",
        "Subject": "Station coordinates from the source manuscript; Natural Earth 1:50m land. Geographic context, not a satellite coverage analysis.",
        "Creator": "Matplotlib; scripts/render_station_map.py",
    })
    if args.preview:
        args.preview.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(args.preview, dpi=220)
    plt.close(fig)
    print(json.dumps({"stations": len(stations), "evaluation": 8,
                      "development": 4, "basemap_features": len(features),
                      "output": str(args.output)}))


if __name__ == "__main__":
    main()
