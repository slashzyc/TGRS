# TGRS submission audit — 17 November 2026

## Assessment

**Presentation: passed after the current revisions. The AI acknowledgment is restored with a stated scope; scientific readiness and human-author approval remain unestablished.** The current manuscript is an exploratory audit of one selected design. Its internal reported counts are consistent, but the available companion materials do not establish independent scientific reproducibility or the methodological advance expected of a TGRS contribution.

The current version restores the AI-assistance acknowledgment following the author's request to identify the specific tasks involved. It names ChatGPT (OpenAI), the affected text sections, LaTeX preparation, figure layouts, plotting code, and editorial checks. It distinguishes this preparation work from the source study's reported observations and audit results. This addresses the earlier missing-disclosure issue without claiming that the entire scientific study was AI-generated or that all authors have already approved the revision. See [IEEE's policy](https://journals.ieeeauthorcenter.ieee.org/become-an-ieee-journal-author/publishing-ethics/guidelines-and-policies/submission-and-peer-review-policies/).

## Verified presentation

| Item | Observed state |
| --- | --- |
| Main manuscript | IEEEtran journal template, 10-point body, two columns, US Letter; 10 pages |
| Supplement | Separate title, authors, page numbering, and supplementary table and figure numbers; five pages |
| Complete reading copy | Main manuscript followed by supplement; 15 pages |
| Abstract | One paragraph, 243 words; no citation, footnote, or displayed equation; NOAA expanded |
| Index Terms | Five entries in alphabetical order |
| Authors | Four names, affiliations, shared-second-authorship note, corresponding author and email |
| Figures | Six main figures and Supplementary Figure S1, all vector; station map, marginal-yield panel, and capacity-shortfall panels included |
| References | 19 numbered entries in first-citation order, including the Natural Earth basemap; no unresolved citation keys |
| PDF integrity | Embedded fonts, no unresolved references, no overfull text lines or detected clipping |
| Reported values | Matrix, terminal-state marginals, 84 diagnostic counts, percentages, transfer arithmetic, 12 mapped coordinates, four marginal-yield calculations, and all 40 cell-deficit calculations reconcile |

The machine-readable numerical and PDF results are in [presentation_check.json](presentation_check.json). These are checks of presentation and transcription, not of the original experimental inputs. Bibliographic metadata and numbering checks are not a claim that all scientific propositions in all cited full texts have undergone independent human verification.

The main template matches the [TGRS author guidance](https://www.grss-ieee.org/publications/author-resources/tgrs-information-for-authors/). TGRS uses single-anonymous review, so names may remain. Ten pages is a 2026 overlength-charge threshold, not a hard manuscript maximum. The author separately requested a ten-page maximum for this revision, and the build now enforces that constraint. Final typeset pagination may differ. The [IEEE style manual](https://journals.ieeeauthorcenter.ieee.org/wp-content/uploads/sites/7/IEEE-Editorial-Style-Manual-for-Authors.pdf) informs the abstract, keywords, and author-footnote checks.

For submission, use the main PDF and [separate supplementary file](https://journals.ieeeauthorcenter.ieee.org/create-your-ieee-journal-article/prepare-supplementary-materials/). The combined reading copy is provided for convenience.

## Scientific issues requiring author evidence or judgment

### 1. Original evidence and implementation — high priority

The repository lacks the original acquisition, extraction, and replay implementation; the 128 source receipts; predictor extracts; 150-row case Parquet; 62-comparison ledger; and original test logs. Their reported paths in the supplement do not make them available. The editorial plotting utilities cannot verify the reported original replay or outcome-access counters.

Supply a versioned original research package or a review-accessible evidence deposit, with actual access conditions. This is a gap in this manuscript's central audit claims; it is not a claim that TGRS universally requires unrestricted public release of every dataset or codebase.

### 2. Station-to-product coverage mapping — high priority

The source protocol assigned station 42056 to a Gulf selection stratum. [NDBC's station metadata](https://www.ndbc.noaa.gov/station_page.php?station=42056) identifies it as Yucatan Basin at 19.820 N, 84.980 W. The supplement already qualified the region as a source selection label; that label and every count have been preserved.

[NOAA's Coastal UHR product notes](https://manati.star.nesdis.noaa.gov/datasets/AscatCoastalUHR.php) explain that coastal zones depend on swath/coast intersections and may span regions. Product-sector labels alone do not establish coverage of the chosen station. Verify the selection region boundaries, ec/gc mapping, and actual footprints of the selected files. The 128 no-overlap outcomes at 42056 do not themselves prove a mapping error or its cause.

The NDBC metadata were available through official indexed station records; direct station-page fetches returned HTTP 403 during this review. Historical deployment files were not reconstructed, and current weather observations were not used in the analysis.

### 3. Reconstructing the selection and extraction — high priority

The prose does not fully supply the candidate station universe, region eligibility boundaries, hash function and salts, canonical hash inputs, complete selected-file manifest, field mapping, or time-decoding implementation. These may exist in the original package, but were not provided. Release the actual configuration and implementation rather than inventing missing details.

### 4. Methodological advance and generality — editorial risk

The paper clearly separates a failed capacity decision from a successful integrity replay. However, its demonstrated contribution remains a combination of existing principles and one fixed design. The current evidence does not show how the procedure advances routine data prechecks or existing workflow audits in a generalizable way. This is a substantive TGRS fit/novelty risk, not a prohibition on negative results. Stronger contribution claims should follow new evidence, not rhetorical expansion.

The official scope emphasizes significant research and novel methodological advancement. It does not establish a universal requirement for a wind-model SOTA comparison, a minimum of 30 references, a fixed recent-reference percentage, or a particular number of repeated experiments.

### 5. Thresholds and processing states — unresolved validation

The 400/8 readiness criteria follow configured 320/6 downstream minima and allow 20%/25% attrition. The downstream minima lack a demonstrated precision or power basis. This does not invalidate the descriptive result that the selected design failed its configured rule, but limits the scientific meaning of that rule.

The 211 evaluation records classified as time-invalid require representative underlying records and time-decoding checks. Their cause cannot be inferred from aggregate bars. Likewise, the two known receipt/locator defects remain unresolved. No new sensitivity experiment or repair has been represented as completed.

## Author and submission information still to finalize

- Confirm all authors' substantive contributions, author order, shared second authorship, final review, and corresponding-author responsibility.
- Verify each author's ORCID and complete the corresponding author's postal address, telephone, and email in the submission system. The manuscript has the verified professional email; personal telephone details were not invented.
- Prepare author biographies and photographs. The TGRS page uses both “should” and “recommended” wording, so their current absence is listed as an item to prepare, not as a verified absolute ban on initial submission.
- Supply any applicable funding, competing-interest, prior-publication, and permission information. No absent declaration has been replaced by an unsupported “none.”
- Use the current [TGRS submission portal](https://ieee.atyponrex.com/journal/tgrs). No submission has been made by this workflow.

## Changes in this follow-up

The scoped acknowledgment was restored; a station map and marginal-yield panel were added; the detailed diagnostic figure was moved to Supplementary Figure S1; and repetitive discussion was removed. The subsequent revision added the two-panel capacity-shortfall figure, moved long stored labels to Supplementary Table S3, fixed URL/identifier spacing, and removed about 530 further words from the background, discussion, and limitations while retaining the ten-page main manuscript. The contribution and threshold claims were tightened, NOAA was expanded, figure codes were defined, author-note styling was corrected, and outcome-access wording was limited to the recorded workflow. All original numerical results, station assignments, and capacity/replay decisions remain unchanged. No scientific acquisition or experiment was run.

**Recommended disposition:** retain this as a revised pre-submission draft. Provide the original evidence, verify the station/product mapping and selection implementation, and have the human authors assess the methodological contribution before treating it as ready for TGRS review.
