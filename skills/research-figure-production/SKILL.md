---
name: research-figure-production
description: Curate figure data, render complete scientific figures, apply journal style, and audit dedicated SciencePlots Python scripts.
---

# Research Figure Production

Use Planning mode in `figure_review` and Final mode in `figure_production`. Read `references/figure-data-contract.md` and the common workflow plus selected profile in `references/journal-figure-style.md`. During planning, consult the relevant task section of `references/chart-selection-guide.md` and only triggered entries in `references/chart-caveat-checklist.md`. Read `references/python-plotting-patterns.md` only when code guidance is needed.

Render every governed figure from a dedicated `.py` script under `exp/figures/`; keep artifacts under `data/figures/`. Import `scienceplots` and use `science` plus `no-latex` by default.

## Planning: `figure_review`

Build a draft set that answers the scientific questions and accounts for every metric, condition, coverage/failure state, and sensitivity. Start from complete sources with a matching passing `aggregation-validation.json`; curated display tables preserve rows and keys. Use `$research-statistical-analysis` for applicable statistical reporting and panel-to-analysis traceability.

Choose charts and composition from the scientific task and method basis. Record the mapping, caveats, coverage, journal profile, final dimensions, and panel layout in `figure-plan.json` and `figure-coverage.json`. Render the complete data mapping, then apply the whole-figure publication-style pass. Seaborn semantic interfaces are useful when they express that mapping without implicit aggregation; preserve the `science` style base and produced scientific quantities.

Write the manifest and validate the script. Present every draft with coverage through `$human-research-review-gate`, then record feedback, the presentation milestone, predicates, and all outgoing rules.

## Final: `figure_production`

Implement the recorded feedback within its approved scientific scope and label schematics distinctly. Re-render, apply the selected journal profile to the complete composite, and export at the recorded physical size.

Write `figure_manifest.json` and audit the data contract and triggered chart caveats programmatically where possible. Inspect thumbnails only when a specific visual question remains; record the evidence and any unresolved limits. Record semantic, statistical, coverage, layout, readability, and traceability findings in `figure_integrity_audit.json`. Run `validate_figure_script.py` in final mode, integrate findings the script cannot establish, and prepare predicate evidence and outgoing rules.

Optional assets provide a script structure and plotting helpers; copy only what the figure needs.

## Output

Present the complete draft or final figure set and link its scripts, sources, and integrity evidence. Explain material limitations and the feedback or lifecycle decision needed; keep detailed audit fields in the artifacts.
