# Revision notes

Revision date: 16 November 2026 (America/New_York).

## Changes completed

1. Rebuilt the supplied 20-page single-column anonymous PDF as an IEEE journal manuscript with a separate supplement and a combined reading copy.
2. Shortened the title and rewrote the prose to reduce repetition, administrative jargon, and formulaic transitions. The study remains an exploratory negative readiness audit; no wind-performance result was introduced.
3. Added Yichen Zhu, Mutong Li, Yongzhi Li, and Guanchao Tong in the requested order. Mutong Li and Yongzhi Li share second authorship; Guanchao Tong is the corresponding author. The first three authors have the supplied Wenzhou-Kean affiliation, and the corresponding author’s college, postcode, and email match the official university page.
4. Added a transparent acknowledgment covering ChatGPT-assisted language revision, organization, LaTeX preparation, and plotting code. No unobserved author approval or absence of prior AI use is asserted.
5. Rebuilt all five displays as vector figures using values already reported in the source PDF. The original images are retained for traceability. Figure 3 uses grouped horizontal bars to make small counts legible; no counts changed.
6. Converted reference entries to IEEE style and ordered them by first citation. The original 17 entries were retained; one verified 2023 source on leakage was added for context. Historical sources retain their actual years and are not presented as current performance baselines.
7. Replaced the incorrect provenance-section reference with a live LaTeX reference. Removed the unsupported reference to a missing execution-lineage table; the supplement preserves only the events actually described in the supplied document.
8. Consolidated long artifact paths, precise byte totals, station coordinates, original runtime commands, and historical test reports in the supplement. Moved an interpreter-entrypoint failure out of the scientific results section.
9. Distinguished the public editorial companion repository from the original scientific research pack, which was not supplied and was not found by the targeted file search.
10. Clarified the full four-round alternate-file loop in Figure 1 and the use of file sensing time for every row in Figure 5(c). Final pagination is 10 pages for the main manuscript and four pages for the supplement.

## Scientific facts preserved

The main result remains 150/400 evaluation opportunities, a minimum cell count of 0/8, and 3/40 cells reaching eight. The v4.1 source capacity decision remains failed; the v5 replay-integrity decision remains passed. The original record reports 62 matching comparisons, 13 passing integrity checks, and zero outcome reads. The revised manuscript does not represent these author-reported findings as newly reproduced experiments.

Both known provenance defects remain: a stale temporary Parquet locator and missing separate per-probe receipts. The reported 27- and 165-test passes remain historical reports. The 185-opportunity candidate-rule calculation remains an arithmetic upper bound, not a new sensitivity experiment. The 20%/25% margins remain configured attrition allowances, not a power analysis.

## Items the authors still need to resolve

- Supply and archive the original code, receipts, predictor extracts, case Parquet, and logs if independent reproduction is to be claimed.
- Verify the source study’s station-region/product-sector mapping, including station 42056, against the actual selection and extraction code. The supplied region labels were preserved rather than silently reassigned after the result.
- Confirm complete authorship, shared second authorship, corresponding-author responsibility, all author ORCIDs, and any funding, prior-publication, or competing-interest disclosures required by the submission system.
- Decide whether a broader prospective validation study is needed to substantiate methodological generality. Language editing does not change the single-design exploratory evidence.

## Scope relative to the general research prompt

This was a manuscript-revision task, not a new experimental campaign. The release contains 18 references, with 10 dated 2021 onward; it does not claim to meet a 30-reference quota or a 90% recent-reference threshold. It does not claim new SOTA model comparisons, 10–15 experimental repetitions, ablations, formal power analysis, or independent audit replication. Those would require a separately specified study and the missing source materials.

## Validation scope

Presentation checks cover the transcribed numerical arrays and their totals, acquisition arithmetic, figure dimensions, citation keys and order, figure references, author names, disclosure presence, PDF font embedding, and visual layout. The check report is in `docs/presentation_check.json`. These checks are separate from the original study’s tests.
