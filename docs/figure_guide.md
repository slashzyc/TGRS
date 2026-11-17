# Figure guide and assistance scope

The current paper contains five main figures and one supplementary figure. The new station map adds geographic context; the expanded acquisition figure adds an explicitly derived marginal-yield panel. The original detailed processing diagnostic is retained in the supplement to keep the main manuscript at ten pages.

| Display | PDF source | Inputs and purpose |
| --- | --- | --- |
| Figure 1 | `paper/figures/figure1.pdf` | Source workflow, complete alternate rounds, capacity failure, and the distinct replay-integrity result. |
| Figure 2 — new | `paper/figures/station_map.pdf` | Twelve reported station coordinates and roles over the cited Natural Earth land subset. The map does not infer satellite footprints or validate the original sector assignment. |
| Figure 3 | `paper/figures/figure2.pdf` | The 8-by-5 evaluation matrix, including zero cells and the configured cell threshold. |
| Figure 4 | `paper/figures/figure3.pdf` | Evaluation/development terminal counts with their actual denominators. |
| Figure 5 — expanded | `paper/figures/acquisition_profile.pdf` | Original cumulative capacity and cost, plus additional opportunities per additional decimal GB in each of the four alternate rounds. |
| Figure S1 | `paper/figures/figure5.pdf` | Complete processing-state counts by file stratum, station and source-file sensing block. These are three groupings of the same 1,024 records. |

The earlier cumulative-only `figure4.pdf` and five extracted original images are retained for revision history. They are not additional experiments or extra figures in the current manuscript.

## New arithmetic

For alternate round r, marginal yield is `(N[r] - N[r-1]) / ((bytes[r] - bytes[r-1]) / 1e9)`.

| Round | Added opportunities | Additional bytes | Opportunities per decimal GB |
| --- | ---: | ---: | ---: |
| 1 | 11 | 610,514,454 | 18.02 |
| 2 | 9 | 596,205,693 | 15.10 |
| 3 | 11 | 590,329,239 | 18.63 |
| 4 | 5 | 617,772,188 | 8.09 |

These ratios summarize the executed acquisition sequence. They do not compare unexecuted strategies, establish an optimal policy, or constitute an additional acquisition experiment.

## Meaning of partial AI assistance

ChatGPT assisted specific manuscript-preparation tasks: language and organization, LaTeX, figure layouts, plotting code, and editorial consistency checks. Both the earlier figure redrawing and the new displays involved AI-assisted code. The statement therefore does not imply that only the two new display elements involved AI.

The scientific counts, reported station coordinates, and prior audit outcomes were supplied in the source manuscript. Natural Earth supplies the land geometry. The marginal-yield values are a documented calculation from the source counts and bytes. No generative-image model was used to synthesize scientific imagery, and no original acquisition or replay experiment was run during this revision. The wording concerns this revision and does not infer the provenance of work performed before the supplied manuscript.

The manuscript's Acknowledgment names the tool, affected text sections, and the extent of assistance. Human-author review and responsibility remain to be finalized; this document does not assert that approval has already occurred.
