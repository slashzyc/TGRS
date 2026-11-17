# Coastal ASCAT benchmark readiness manuscript

**Outcome-Blind Readiness Assessment of a 128-File Coastal ASCAT Benchmark**

Yichen Zhu, Mutong Li, Yongzhi Li, and Guanchao Tong  
Wenzhou-Kean University, Wenzhou 325060, China  
Mutong Li and Yongzhi Li share second authorship.  
Corresponding author: Guanchao Tong, tguancha@kean.edu

This repository contains the manuscript prepared for **IEEE Transactions on Geoscience and Remote Sensing (TGRS)** and its presentation materials. It is a pre-submission author manuscript; no submission, acceptance, or independent reproduction is claimed.

## Read the manuscript

- [Complete reading copy: main text and supplement](deliverables/TGRS_Complete_Manuscript.pdf)
- [Main manuscript in IEEE journal format](deliverables/TGRS_Manuscript.pdf)
- [Supplementary material](deliverables/TGRS_Supplement.pdf)
- [Revision notes](docs/revision_notes.md)
- [Figure guide and assistance scope](docs/figure_guide.md)
- [Submission audit, 17 November 2026](docs/submission_audit_2026-11-17.md)

## What the study reports

The source manuscript describes a fixed set of 128 NOAA Coastal ASCAT files, eight evaluation stations, four development stations, and five 28-day blocks. It reports 150 unique evaluation opportunities against a requirement of 400, a minimum station–block count of zero against eight, and three of 40 cells reaching eight. The source capacity check failed, while a subsequent deterministic audit of that failure record passed. The reported source record contains zero NDBC wind-outcome reads, so no wind-performance comparison was performed.

## Repository scope

Included:

- Editable LaTeX manuscript and supplemental text.
- IEEEtran journal class, unmodified, with its original license notice.
- Seven displayed vector figures: six in the main text and one in the supplement, plus the earlier figure versions and original extracted images.
- A station map with a bundled Natural Earth land subset, a cost plot with a descriptive marginal-yield panel, and a two-panel display of local and overall capacity shortfalls.
- CSV transcriptions of source counts and coordinates, plus separately labeled arithmetic derivations of marginal yields and positive cell deficits.
- Plotting, document-building, and presentation-consistency utilities.
- Reference-verification, policy, provenance, and revision records.

**The original acquisition and replay research pack is not included.** This repository does not contain the 128 source receipts, predictor extract tree, evaluation Parquet, acquisition logs, or original replay implementation. Its plotting and checking scripts are editorial utilities, not replacements for those scientific artifacts. The supplement lists the original research-pack paths and reported commands so that the authors can complete that release.

## Build

Use a standard TeX Live or MiKTeX installation with the packages declared in the two TeX entry points. The manuscript includes its own IEEEtran class. A normal installation of `latexmk` can build the files directly:

```bash
cd paper
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
cd ../supplement
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

From the repository root, the Python build helper also assembles the complete reading copy and runs the presentation checks:

```bash
python -m pip install -r requirements-editorial.txt
python scripts/build.py
```

The committed vector figures are sufficient for compiling the manuscript. To regenerate them from the transcribed CSVs:

```bash
python scripts/render_figures.py
python scripts/render_station_map.py
python scripts/render_acquisition_profile.py
python scripts/render_capacity_shortfall.py
```

The numeric checks verify internal consistency of the **reported** display values. They do not validate the original observation acquisition or reproduce its outcome-access audit.

## Author review and declarations

Author order and shared second authorship follow the supplied instructions. The corresponding author’s affiliation and public professional email were checked against [Wenzhou-Kean University](https://csmt.wku.edu.cn/en/node/2000). The current manuscript includes a scoped AI-assistance acknowledgment. It identifies the preparation tasks that used ChatGPT, including language revision, LaTeX, figure layouts, plotting code, and editorial checks, while identifying the source manuscript and public basemap as the numerical and geographic inputs. It does not characterize the original scientific study as AI-generated. Funding, competing interests, individual contribution roles, and approvals have not been invented; the authors must supply any applicable information before submission.

See [TGRS policy notes](docs/tgrs_policy_notes.md), [reference verification](docs/reference_verification.md), and [editorial tools](docs/editorial_tools.md).

## Rights

No new blanket license is asserted for the manuscript, its source-study results, or NOAA-derived material. Rights remain with the respective holders. IEEEtran retains its original LaTeX Project Public License notice. The bundled Natural Earth land subset is public domain; its immutable source and version are recorded in `data/basemaps/natural_earth_provenance.json`. Public availability of the companion files is not a claim that all underlying source data may be redistributed without review.
