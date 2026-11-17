# Figure style and reproducible exports

The professional-figure revision applies Scientific Visualization v1.4 to the six main figures and Figure S1. The skill was installed from [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills), pinned to commit `ec59a29a03d5c40f73ab40878df04860bc00e876`. The installed skill is available at https://chatgpt.com/skills?skill_id=6afc6dc0cd648191b19896c194abbe54. Its tooling citation and the scope of AI assistance are recorded in [editorial_tools.md](editorial_tools.md) and [figure_guide.md](figure_guide.md).

## Scientific content and page budget

This is a presentation revision. Source counts, station coordinates, map geometry, denominators, thresholds, calculations, and reported outcomes are unchanged. The data files remain byte-identical to the preceding revision. The reported capacity result and the replay-integrity result remain distinct; the derived acquisition yields and shortfalls remain explicitly descriptive arithmetic.

Each figure retains its physical canvas size. This preserves the existing figure allocation in the ten-page main manuscript; the supplement remains five pages.

| Display | Width × height (inches) | 600 ppi PNG (pixels) |
| --- | ---: | ---: |
| Figure 1 — Workflow | 7.16 × 4.55 | 4296 × 2730 |
| Figure 2 — Station map | 7.16 × 4.20 | 4296 × 2520 |
| Figure 3 — Opportunity matrix | 3.50 × 3.40 | 2100 × 2040 |
| Figure 4 — Processing states | 3.50 × 2.95 | 2100 × 1770 |
| Figure 5 — Acquisition profile | 7.16 × 3.20 | 4296 × 1920 |
| Figure 6 — Capacity shortfall | 7.16 × 3.20 | 4296 × 1920 |
| Figure S1 — Processing diagnostics | 7.16 × 6.00 | 4296 × 3600 |

The 3.5-inch and 7.16-inch widths follow the single-column and double-column sizes in the [IEEE graphics guidance](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/create-graphics-for-your-article/resolution-and-size/). The manuscript uses vector PDF figures. The 600 ppi PNGs are review and reuse companions; the IEEE guide distinguishes the resolution requirements for different raster categories.

## Typography and visual hierarchy

`scripts/figure_style.py` applies a scoped Matplotlib style, so individual renderers do not leave global plotting settings behind. The figures use DejaVu Sans, at least 8 pt text at the exported canvas size, and 10 pt panel titles where present. PDF fonts are embedded as TrueType; SVG text remains text rather than being converted to paths. When editing an SVG, use DejaVu Sans to preserve the measured line lengths.

Titles, axes, direct values, and scope notes have a consistent hierarchy. Light grid lines and restrained borders support comparison without competing with the data. Extra whitespace is reduced through aligned panels and labels while retaining the fixed canvas. Exports use `bbox_inches=None`; automatic tight cropping must not change the physical dimensions.

The acquisition plots use dark blue for the reported cumulative series and pale teal bars with teal outlines for the derived marginal yields. Figure 6 distinguishes the observed 150 from the derived additions using fill, sparse hatching, and explicit numeric labels; 321 is emphasized at the intermediate total. Threshold lines retain their numeric labels and distinct line patterns. Other figures retain their own legends and category labels; the palette is not a universal substitute for those definitions.

## Accessibility and interpretation

Color is accompanied by text, shapes, line patterns, or hatching where it encodes a distinction. Station roles use different marker shapes; the grouped counts and waterfall use redundant hatching; cells and bars display their values. The blue sequential scales represent magnitude, with zero cells retained and the original count or percentage denominator made explicit.

The local palette audit checks the six dark text colors against white at a screen contrast ratio of at least 4.5:1. This is a limited text-contrast check. Several colors are similar in grayscale, so hue alone should not be used to identify categories. Direct labels and redundant encodings remain necessary; no palette certification is asserted.

The figures do not introduce uncertainty intervals, estimated satellite footprints, or alternative-policy results. Derived additions remain explicitly identified as arithmetic bounds. The acquisition and capacity-shortfall footers retain the descriptive and nonforecast scope. Replotting the record does not independently validate the original scientific experiment or audit.

## Rendering and deliverables

Run from the repository root:

```bash
python3 scripts/render_figures.py
python3 scripts/render_station_map.py
python3 scripts/render_acquisition_profile.py
python3 scripts/render_capacity_shortfall.py
```

`render_figures.py` renders the workflow, opportunity matrix, role-specific processing counts, and supplementary diagnostic. It imports the workflow implementation from `scripts/render_workflow.py`; that script can also regenerate Figure 1 by itself. The map and two derived displays have their own renderers because their data sources and calculations differ. The superseded cumulative-only figure is excluded by default and is available only through `render_figures.py --include-legacy`.

`save_figure()` in `scripts/figure_style.py` writes the source PDF under `paper/figures/` and the corresponding numbered PDF, editable SVG, and 600 ppi PNG under `deliverables/figures/`. The seven export stems are listed in [figure_guide.md](figure_guide.md). PDF creation and modification timestamps are omitted; titles, subjects, and creator metadata describe each figure's scope. Optional previews support visual inspection without replacing the publication exports.

For the complete manuscript build, `python3 scripts/build.py --regenerate-figures` regenerates the current figures before compiling the main manuscript and supplement and checking reported values. The plotting commands need the repository's Python dependencies; the complete build also needs the configured LaTeX environment. Neither route runs a new ASCAT acquisition or replay experiment.

The build also creates `deliverables/TGRS_Figure_Gallery.pdf`: a seven-page, bookmarked collection retaining each figure's native canvas. This is a figure-only review copy; consult the manuscript and supplement for the captions and evidence scope.

The current exports have been checked for the fixed dimensions, embedded PDF fonts, minimum text size, and absence of rasterized chart content in the PDFs. Scientific interpretation and final author approval remain the responsibility of the human authors. These presentation checks do not establish journal acceptance.
