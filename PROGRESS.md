# Revision progress

## v1: evidence and format review

- Complete 20-page supplied PDF read; all five figures are present.
- IEEE TGRS requirements and IEEE AI assistance disclosure policy checked against official sources.
- Requested author order: Yichen Zhu, Mutong Li, Yongzhi Li, Guanchao Tong; Mutong Li and Yongzhi Li share second authorship; Guanchao Tong is corresponding author.
- Main result to preserve: 150/400 total opportunities, minimum 0/8 per cell, 3/40 cells reaching threshold.
- Source capacity gate failed; subsequent replay integrity passed; zero outcome reads are a claim about the original repository record.
- User-designated GitHub repository is empty; the supplied material contains no original experimental code, extract tree, receipt tree, or case Parquet.
- Defects found: stale section reference for provenance limitations; reference to an execution-lineage supplementary table absent from the supplied PDF.

## v2: reconstruction and scholarly revision

- Rewrote the complete manuscript and reconstructed editable IEEEtran LaTeX sources.
- Added the four authors, shared second authorship, verified corresponding-author email, and an acknowledgment of the actual AI assistance used.
- Rebuilt all five figures from transcribed source values as vector PDFs; retained the original figure images for comparison.
- Retained the 17 original references and added one verified source on data leakage; ordered all 18 references by first citation.
- Prepared a separate supplement with source-reported station coordinates, byte totals, artifact inventory, commands, and unresolved provenance limitations.

## v3: final presentation validation

- Compiled the 10-page main manuscript, 4-page supplement, and 14-page combined reading copy.
- Confirmed the 150/400 total, minimum 0/8 cell, 3/40 qualifying cells, terminal-state marginals, all 84 diagnostic count cells, rounded percentages, and exact transfer arithmetic.
- Resolved citation and cross-reference issues and checked all PDF pages visually. Fonts are embedded, and there are no unresolved references or overfull text lines.
- Clarified that all four alternate rounds are processed before the final capacity failure, and that every row in the block diagnostic is grouped by source-file sensing time.
- Completed independent checks of the manuscript and delivery documentation. The machine-readable presentation report is `docs/presentation_check.json`.

These checks concern the revised presentation and reported values. The original scientific experiment and replay were not rerun.

## v4: author-requested acknowledgment removal and submission audit

- Removed the manuscript acknowledgment on 17 November 2026 at the author's request. The disclosure-policy issue remains explicitly unresolved in the audit, rather than being counted as a presentation failure or silently certified as compliant.
- Corrected abstract and figure-caption self-containment, author-note styling, and overbroad outcome-access wording.
- Added a source-linked note distinguishing station 42056's original Gulf selection label from its NDBC Yucatan Basin metadata, without changing station membership or counts.
- Recompiled and checked the 10-page main manuscript and 4-page supplement. Scientific readiness is not certified; see `docs/submission_audit_2026-11-17.md`.

## v5: geographic context, marginal-yield display, and scoped acknowledgment

- Added a 12-station map with a cited, offline Natural Earth 1:50m land subset.
- Expanded the acquisition plot to include four descriptive marginal-yield ratios; transferred the detailed processing diagnostic to Supplementary Figure S1.
- Reduced repeated discussion by approximately 500 words and clarified the protocol-defined thresholds, contribution, and remaining implementation gaps.
- Restored a truthful acknowledgment of specific AI-assisted preparation tasks and documented the distinct sources of counts, coordinates, land geometry, and arithmetic derivations.
- Current pagination: 10 main pages, five supplement pages, 15 combined pages. All numeric and presentation checks passed; original scientific reproduction remains outstanding.


## v6: compact prose, repaired typography, and capacity shortfalls

- Removed long, nonbreaking stored labels from narrow main-text columns; preserved exact strings in Supplementary Table S3 and retained run/package identifiers in the original-evidence inventory.
- Added Figure 6, derived from the 40 reported station-block counts: cell gaps sum to 171, minimal cell filling retains a total of 321, and the remaining total gap is 79.
- Reduced generic and repeated context while retaining specific coastal ASCAT and contemporary workflow/asset-provenance developments. No scientific observations or performance experiments were added.
- Updated scoped AI assistance, source/derived data documentation, and numeric consistency checks.
- Final manuscript: ten pages including references and acknowledgment, six main figures; supplement: five pages with Figure S1 and Table S3; combined copy: 15 pages. The ten-page author constraint is now a checked build gate.

## v7: publication figure styling and reusable exports

- Installed Scientific Visualization v1.4 from a pinned K-Dense-AI upstream revision and applied its figure-size, typography, vector-export, and evidence-preservation guidance.
- Redesigned all seven current figures with consistent font hierarchy, restrained colors, direct values, role-specific shapes, sparse hatching, and aligned panels. The workflow now separates headings from body text; the diagnostic matrices distinguish counts from percentages.
- Preserved every source and derived data file byte-for-byte, all figure canvas dimensions, and the source-capacity versus replay-integrity distinction.
- Added numbered PDF, editable SVG, and 600 ppi PNG files for each figure, a seven-page figure-only gallery, and shared styling code. Original figure images and the superseded cumulative-only plot remain available for traceability.
- Recompiled the ten-page main manuscript, five-page supplement, and 15-page reading copy; all seven displayed figures remain vector-based with embedded fonts. Scientific acquisition and replay were not rerun.
