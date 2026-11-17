"""Shared editorial figure style and fixed-size publication exports.

Guidance: Scientific Visualization v1.4 (K-Dense). Source values and
transformations remain in the individual plotting scripts and data files.
"""
from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import shutil

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap

ROOT = Path(__file__).resolve().parents[1]
INK = "#1D2C38"
MUTED = "#566B78"
BLUE = "#235F7D"
LIGHT_BLUE = "#C8DDE8"
TEAL = "#167D83"
LIGHT_TEAL = "#D9ECEA"
AMBER = "#A96522"
LIGHT_AMBER = "#EEDFC9"
RED = "#AB453E"
GRID = "#E5EBEF"
PALE = "#F5F8FA"
CMAP = LinearSegmentedColormap.from_list(
    "tgrs_depth", ["#F5F8FA", "#D8E7EE", "#A7C6D7", "#5C92B0", "#235F7D"]
)

DISPLAY_NAMES = {
    "figure1": "Fig_01_Workflow",
    "station_map": "Fig_02_Station_Map",
    "figure2": "Fig_03_Opportunity_Matrix",
    "figure3": "Fig_04_Processing_States",
    "acquisition_profile": "Fig_05_Acquisition_Profile",
    "capacity_shortfall": "Fig_06_Capacity_Shortfall",
    "figure5": "Fig_S1_Processing_Diagnostics",
}

@contextmanager
def style_context():
    """Apply the journal figure style without leaking global rc settings."""
    with mpl.rc_context({
        "font.family": "DejaVu Sans", "font.size": 8.5,
        "axes.labelsize": 8.5, "axes.titlesize": 10,
        "xtick.labelsize": 8, "ytick.labelsize": 8,
        "axes.linewidth": 0.65, "axes.edgecolor": MUTED,
        "text.color": INK, "axes.labelcolor": INK,
        "xtick.color": MUTED, "ytick.color": MUTED,
        "xtick.major.width": 0.65, "ytick.major.width": 0.65,
        "axes.titleweight": "bold", "hatch.linewidth": 0.45,
        "lines.solid_capstyle": "round", "lines.dash_capstyle": "butt",
        "pdf.fonttype": 42, "ps.fonttype": 42,
        "svg.fonttype": "none", "savefig.facecolor": "white",
        "figure.facecolor": "white", "axes.facecolor": "white",
        "mathtext.default": "regular", "mathtext.fontset": "dejavusans",
    }):
        yield

def clean_axis(ax: plt.Axes, grid_axis: str | None = None) -> None:
    ax.spines[["top", "right"]].set_visible(False)
    for name in ["bottom", "left"]:
        ax.spines[name].set_linewidth(0.65)
        ax.spines[name].set_color(MUTED)
    ax.tick_params(width=0.65, length=3)
    ax.set_axisbelow(True)
    if grid_axis:
        ax.grid(axis=grid_axis, color=GRID, linewidth=0.45)

def save_figure(fig: plt.Figure, pdf_path: Path, *, title: str,
                subject: str, creator: str, preview_path: Path | None = None) -> None:
    """Export exact-size PDF and numbered PDF/SVG/600-ppi PNG companions."""
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(pdf_path, bbox_inches=None, facecolor="white", metadata={
        "Title": title, "Subject": subject, "Creator": creator,
        "CreationDate": None, "ModDate": None,
    })
    name = DISPLAY_NAMES.get(pdf_path.stem)
    if name:
        directory = ROOT / "deliverables/figures"
        directory.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(pdf_path, directory / f"{name}.pdf")
        fig.savefig(directory / f"{name}.svg", bbox_inches=None, facecolor="white",
                    metadata={"Title": title, "Description": subject, "Date": None})
        fig.savefig(directory / f"{name}.png", dpi=600, bbox_inches=None,
                    facecolor="white", metadata={"Title": title, "Description": subject})
    if preview_path:
        preview_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(preview_path, dpi=220, bbox_inches=None, facecolor="white")
