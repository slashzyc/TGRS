# Editorial tools and scope

This revision used ChatGPT (OpenAI), the Scientific Writing skill v2.3, the Scientific Visualization skill v1.4, IEEEtran 1.8b, Python/Matplotlib, and local PDF inspection tools. The manuscript contains an acknowledgment describing the actual language, formatting, and figure-presentation assistance. No new scientific experiments were run during the editorial revision.

Scientific Writing upstream source: https://github.com/K-Dense-AI/scientific-agent-skills/tree/main/skills/scientific-writing
License: MIT. The skill is an editorial procedure, not a remote-sensing baseline or source of empirical evidence. Its files are not bundled into this manuscript repository.

Scientific Visualization v1.4 was installed from [K-Dense-AI/scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills), pinned to commit `ec59a29a03d5c40f73ab40878df04860bc00e876`. Installed skill: https://chatgpt.com/skills?skill_id=6afc6dc0cd648191b19896c194abbe54. Its guidance was applied to the existing scientific displays: fixed physical dimensions, readable typography, direct labels, restrained color and hatching, and vector exports. It did not supply scientific data or generate new experimental results. The upstream skill files are not bundled into this manuscript repository.

Tooling citation for the shared skill library, covering both Scientific Writing and Scientific Visualization (metadata checked against the arXiv record):
Kassis, T., Agarwal, V., He, Y., Patel, D., and Brueckner, A. M. (2026). *Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents*. arXiv:2609.00065. https://doi.org/10.48550/arXiv.2609.00065

The professional-figure revision uses `scripts/figure_style.py` for common typography, colors, and exports; `scripts/render_workflow.py` renders the workflow from the reported parameters. Seven current figures have numbered PDF, editable SVG, and 600 ppi PNG companions in `deliverables/figures/`. Their input data, calculations, and physical canvas sizes are unchanged. See [figure_style.md](figure_style.md) for the rendering choices and [figure_guide.md](figure_guide.md) for figure-specific provenance and interpretation.

The original empirical results are treated as author-reported values from the supplied PDF. Replotting or checking their internal arithmetic does not independently validate the original acquisition, outcome-access counters, or replay.

A human author must review the scientific record and final author metadata before submission. This statement does not imply that such approval has already occurred.
