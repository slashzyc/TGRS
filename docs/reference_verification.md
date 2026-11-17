# Reference metadata and relevance checks

## Scope and status

- Access/check date: **16 November 2026**, using the user's **America/New_York** date.
- Checked by: an AI-assisted editorial workflow using publisher, standards-body, government, and author-institution sources.
- Accountable human source review and final author approval: **not recorded by this workflow**.
- Input: the 17 references in the supplied manuscript PDF. One relevant reference, Kapoor and Narayanan (2023), was added to explain the motivation for keeping evaluation outcomes separate from design decisions.
- The `R01`--`R18` identifiers below are audit identifiers. `R01`--`R17` follow the original PDF's bibliography order; final IEEE citation numbers may differ because they follow first citation in the revised text.

This record checks bibliographic identity and whether the intended citation role is appropriate. It is not a systematic review, a replication of the original study's literature search, an independent verification of the manuscript's research-pack files, or an experimental reproduction. A metadata match does not establish that every statement in the cited paper has been checked.

**Result:** no title/DOI mismatch was found among the original 17 references. In particular, the Soisuvarn (2023), Lindsley (2016), and Kedron and Frazier (2022) references match primary records. They should not be removed on a presumption that they were fabricated.

## Original references

### R01 — Cloud-native repositories

**R. P. Abernathey et al., "Cloud-Native Repositories for Big Scientific Data," Computing in Science & Engineering, vol. 23, no. 2, pp. 26--35, 2021.**

- DOI: [10.1109/MCSE.2021.3059437](https://doi.org/10.1109/MCSE.2021.3059437).
- Primary record opened: [U.S. Geological Survey publication page](https://www.usgs.gov/publications/cloud-native-repositories-big-scientific-data).
- Observed match: title, authors, year, journal, and DOI. The original volume and pagination are retained.
- Intended role: analysis-ready/cloud-optimized storage and data-proximate computation. This source does not establish the capacity of the manuscript's selected ASCAT benchmark.
- Disposition: retain; format in IEEE style.

### R02 — Registered Reports

**C. D. Chambers, Z. Dienes, R. D. McIntosh, P. Rotshtein, and K. Willmes, "Registered Reports: Realigning incentives in scientific publishing," Cortex, vol. 66, pp. A1--A2, 2015.**

- DOI: [10.1016/j.cortex.2015.03.022](https://doi.org/10.1016/j.cortex.2015.03.022).
- Author-institution record opened: [Cardiff University ORCA](https://orca.cardiff.ac.uk/id/eprint/73305/).
- Observed match: title, authors, journal, volume, pages, year, and DOI.
- Intended role: explain the difference between local prespecification and a Registered Report. It is a historical methodological source, not a current remote-sensing baseline.
- Disposition: retain with that limited role.

### R03 — Landsat analysis-ready data

**J. L. Dwyer, D. P. Roy, B. Sauer, C. B. Jenkerson, H. K. Zhang, and L. Lymburner, "Analysis Ready Data: Enabling analysis of the Landsat archive," Remote Sensing, vol. 10, no. 9, Art. no. 1363, 2018.**

- DOI: [10.3390/rs10091363](https://doi.org/10.3390/rs10091363).
- Primary records: [USGS publication page](https://www.usgs.gov/publications/analysis-ready-data-enabling-analysis-landsat-archive) and [USGS Publications Warehouse](https://pubs.usgs.gov/publication/70201790).
- Observed match: title, authors, year, volume, issue, article number, and DOI in the official records returned by search. A later direct Warehouse fetch returned HTTP 403.
- Intended role: the established meaning of analysis-ready data. It is not evidence about NOAA Coastal UHR ASCAT performance.
- Disposition: retain as background.

### R04 — ASCAT instrument and product guide

**EUMETSAT, ASCAT User Guide, EUM/OPS-EPS/MAN/04/0028, version 6, 1 November 2022.**

- Primary document opened: [EUMETSAT official PDF](https://www-cdn.eumetsat.int/files/2022-12/ASCAT%20User%20Guide.pdf).
- Observed match: title, document identifier, version, and the document's printed date, "v6 e-signed, 1 November 2022."
- DOI: none supplied in the source citation; retain the official document URL rather than inventing one.
- Intended role: ASCAT geometry, product context, and coverage. This guide does not identify the processor version of the manuscript's 128 selected NOAA files.
- Disposition: retain; repair URL spacing introduced by PDF text extraction.

### R05 — Dataset documentation

**T. Gebru, J. Morgenstern, B. Vecchione, J. W. Vaughan, H. Wallach, H. Daume III, and K. Crawford, "Datasheets for Datasets," Communications of the ACM, vol. 64, no. 12, pp. 86--92, 2021.**

- DOI: [10.1145/3458723](https://doi.org/10.1145/3458723).
- Publisher pages: [ACM Digital Library](https://dl.acm.org/doi/10.1145/3458723) and [Communications of the ACM](https://cacm.acm.org/research/datasheets-for-datasets/).
- Observed match: the publisher's indexed metadata returned the title, all seven authors, year, volume, issue, pages, and DOI. Direct article-page retrieval returned HTTP 403; this is a **publisher-metadata check, not a newly completed full-text review**.
- Intended role: explicit descriptions of dataset composition, processing, intended uses, and limitations.
- Disposition: retain; preserve the accented author spelling in the final bibliography where supported.

### R06 — Remote-sensing reproducibility

**P. Kedron and A. E. Frazier, "How to Improve the Reproducibility, Replicability, and Extensibility of Remote Sensing Research," Remote Sensing, vol. 14, no. 21, Art. no. 5471, 2022.**

- DOI: [10.3390/rs14215471](https://doi.org/10.3390/rs14215471).
- Publisher article opened: [MDPI](https://www.mdpi.com/2072-4292/14/21/5471).
- Observed match: title, both authors, journal, volume, issue, article number, and DOI. The publisher gives 31 October 2022 as the publication date.
- Intended role: directly relevant context on remote-sensing reproducibility, benchmark data, and provenance.
- Disposition: retain. No title/DOI correction is needed.

### R07 — BagIt packaging

**J. Kunze, J. Littman, E. Madden, J. Scancella, and C. Adams, The BagIt File Packaging Format (V1.0), RFC 8493, October 2018.**

- Primary standard opened: [RFC Editor](https://www.rfc-editor.org/info/rfc8493/).
- Observed match: title, five authors, RFC number, version, and date.
- Intended role: manifests and file fixity. The manuscript does not claim BagIt conformance.
- Disposition: retain the canonical RFC URL.

### R08 — Workflow-run provenance

**S. Leo et al., "Recording provenance of workflow runs with RO-Crate," PLOS ONE, vol. 19, no. 9, Art. no. e0309210, 2024.**

- DOI: [10.1371/journal.pone.0309210](https://doi.org/10.1371/journal.pone.0309210).
- Publisher article opened: [PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0309210).
- Observed match: title, author list, year, volume, issue, article number, and DOI; publication date 10 September 2024.
- Intended role: records linking workflow plans, executions, inputs, outputs, and provenance. The manuscript's custom records are not represented as a standards-conformant implementation.
- Disposition: retain.

### R09 — High-resolution ASCAT wind validation

**R. D. Lindsley, J. R. Blodgett, and D. G. Long, "Analysis and Validation of High-Resolution Wind From ASCAT," IEEE Transactions on Geoscience and Remote Sensing, vol. 54, no. 10, pp. 5699--5711, 2016.**

- DOI: [10.1109/TGRS.2016.2570245](https://doi.org/10.1109/TGRS.2016.2570245).
- Author-institution record opened: [David Long publications, Brigham Young University](https://www.scp.byu.edu/long/LongPub.html).
- Observed match: title, three authors, year, journal, volume, issue, pages, and DOI. "Wind" is singular in the title.
- Intended role: historical high-resolution ASCAT product development and validation, not a new performance baseline executed for this audit.
- Disposition: retain. No DOI correction is needed.

### R10 — PROV-DM

**L. Moreau and P. Missier, Eds., PROV-DM: The PROV Data Model, W3C Recommendation, 30 April 2013.**

- Primary standard opened: [W3C dated Recommendation](https://www.w3.org/TR/2013/REC-prov-dm-20130430/).
- Observed match: title, editors, status, and date.
- Intended role: general provenance concepts. A standard's actual publication date must not be replaced with the access year merely to make the bibliography appear recent.
- Disposition: retain; no PROV-DM conformance claim is made.

### R11 — Preregistration

**B. A. Nosek, C. R. Ebersole, A. C. DeHaven, and D. T. Mellor, "The preregistration revolution," Proceedings of the National Academy of Sciences, vol. 115, no. 11, pp. 2600--2606, 2018.**

- DOI: [10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114).
- Publisher article opened: [PNAS](https://www.pnas.org/doi/10.1073/pnas.1708274114).
- Publisher-linked metadata: [Crossmark record](https://crossmark.crossref.org/dialog-content?doi=10.1073%2Fpnas.1708274114&domain=pdf).
- Observed match: title, authors, year, and DOI; online publication 12 March 2018 and print publication 13 March 2018.
- Intended role: prospective specification versus post-result analysis. The manuscript's local freeze is not described as public preregistration.
- Disposition: retain.

### R12 — STAC

**Open Geospatial Consortium, SpatioTemporal Asset Catalog (STAC) Community Standard, OGC 25-004, version 1.1, 2025.**

- Primary standard opened: [OGC document 25-004](https://docs.ogc.org/cs/25-004/25-004.html).
- Observed match: title, organization, identifier, and version. Approval date: 9 September 2025; publication date: 14 October 2025.
- DOI: none supplied; the canonical standard URL is used.
- Intended role: discovery and links for spatiotemporal assets, distinct from the application-level capacity rule.
- Disposition: retain.

### R13 — Earth-observation quality principles

**QA4EO Task Team, A Quality Assurance Framework for Earth Observation: Principles, version 4.0, 14 January 2010.**

- Primary document opened: [QA4EO official PDF](https://qa4eo.org/docs/QA4EO_Principles_v4.0.pdf).
- Observed match: title, authoring group, version, and date on the document.
- Intended role: historical principles of traceable quality evidence and fitness for purpose. It must not be the sole evidence for claims about current field-wide bottlenecks.
- Disposition: retain only for that background role.

### R14 — RO-Crate

**S. Soiland-Reyes et al., "Packaging research artefacts with RO-Crate," Data Science, vol. 5, no. 2, pp. 97--138, 2022.**

- DOI: [10.3233/DS-210053](https://doi.org/10.3233/DS-210053).
- Author-institution record opened: [University of Manchester Research Explorer](https://research.manchester.ac.uk/en/publications/packaging-research-artefacts-with-ro-crate/).
- Observed match: title, complete author list, year, journal, volume, issue, pages, and DOI. The record lists RO-Crate Community as a group author and publication on 20 July 2022.
- Intended role: machine-readable research-object packaging. The manuscript's release does not claim RO-Crate conformance.
- Disposition: retain.

### R15 — NOAA Coastal UHR ASCAT processor

**S. Soisuvarn, Z. Jelenak, P. S. Chang, Q. Zhu, and C. G. Shoup, "High-Resolution Coastal Winds From the NOAA Near Real-Time ASCAT Processor," IEEE Transactions on Geoscience and Remote Sensing, vol. 61, pp. 1--12, Art. no. 5208612, 2023.**

- DOI: [10.1109/TGRS.2023.3279764](https://doi.org/10.1109/TGRS.2023.3279764).
- Primary record opened: [NOAA Institutional Repository](https://repository.library.noaa.gov/view/noaa/66349).
- Additional official listing opened: [NOAA Ocean Winds Team product directory](https://manati.star.nesdis.noaa.gov/datasets/OceanWindsTeam.php).
- Observed match: full title, five authors, year, journal, volume, page range, article number, and DOI.
- Intended role: the closest product-method reference for the NOAA Coastal UHR family. Its validation results are not results of the present readiness audit.
- Disposition: retain. No title/DOI correction is needed.

### R16 — Earlier coastal ASCAT retrieval

**A. Verhoef, M. Portabella, and A. Stoffelen, "High-Resolution ASCAT Scatterometer Winds Near the Coast," IEEE Transactions on Geoscience and Remote Sensing, vol. 50, no. 7, pp. 2481--2487, 2012.**

- DOI: [10.1109/TGRS.2011.2175001](https://doi.org/10.1109/TGRS.2011.2175001).
- Author-institution record opened: [Royal Netherlands Meteorological Institute](https://www.knmi.nl/research/publications/high-resolution-ascat-scatterometer-winds-near-the-coast-791e8ac1-15fb-4121-b858-8c6837b2ac4b).
- Observed match: title, authors, publication year, journal, volume, pages, and DOI. The 2011 component of the DOI does not make the 2012 publication year incorrect.
- Intended role: historical coastal retrieval context, not a contemporary benchmark comparison.
- Disposition: retain.

### R17 — Current instrument metadata

**World Meteorological Organization, "Instrument: ASCAT," OSCAR/Space instrument record, last updated 1 June 2026.**

- Primary record opened: [WMO OSCAR/Space](https://space.oscar.wmo.int/instruments/view/ascat).
- Observed match: instrument name and the displayed last-update date, 2026-06-01.
- Intended role: instrument geometry and broad observing characteristics. Nominal global coverage does not determine support at each selected station under the manuscript's extraction rules.
- Access-date handling: the original manuscript reported access on 4 November 2026. This editorial check occurred on 16 November 2026. These are different events; the earlier access date has not been independently reconstructed.
- Disposition: retain as a dynamic official source, with the applicable access date made explicit.

## Added reference

### R18 — Leakage and evaluation design

**S. Kapoor and A. Narayanan, "Leakage and the reproducibility crisis in machine-learning-based science," Patterns, vol. 4, no. 9, Art. no. 100804, 2023.**

- DOI: [10.1016/j.patter.2023.100804](https://doi.org/10.1016/j.patter.2023.100804).
- Publisher record: [Patterns/ScienceDirect](https://www.sciencedirect.com/science/article/pii/S2666389923001599).
- Author-institution record: [Princeton University](https://collaborate.princeton.edu/en/publications/leakage-and-the-reproducibility-crisis-in-machine-learning-based-/).
- Additional indexed record: [PubMed](https://pubmed.ncbi.nlm.nih.gov/37720327/).
- Observed match: publisher and institution search records agree on the title, both authors, year, journal, volume, issue, article number, and DOI. The publisher search result supplied the abstract and highlights; a direct full-page retrieval returned HTTP 403.
- Intended role: the limited motivation that evaluation leakage can lead to optimistic findings, making separation of outcome inspection from design decisions useful. This citation does not establish that the manuscript eliminates all leakage, has external isolation, or improves ASCAT accuracy.
- Disposition: add to the Introduction; list in Related Work as the sole newly added research citation.

## Editorial decisions and remaining limits

1. Preserve authentic references, identifiers, publication years, and source roles. Convert their presentation to IEEE style and fix broken URLs introduced by PDF extraction.
2. Retain older references only where they identify the historical method, concept, or actual standard being discussed. Do not call them current state-of-the-art comparators.
3. Do not present this descriptive audit as a performance comparison: the supplied manuscript reports that outcome-based wind evaluation never proceeded.
4. The revised reference list contains **18 items**, not an asserted 30-source literature review. This check does not certify the earlier general prompt's numerical bibliography targets or a 90% recent-reference fraction.
5. The original literature-map dates and archived-search claims remain reports from the source manuscript. This workflow has not reconstructed those searches or established exhaustive novelty.
6. No unrelated references were added to the scientific bibliography. Editorial software and skill provenance belong in the separate editorial-tools record.
7. Human authors still need to approve source interpretation, the final wording, the bibliography, and any statement that depends on the unavailable original research pack.
