---
name: research-figure-production
description: Curate figure data, plan, render, review, and audit complete scientific figures from dedicated SciencePlots Python scripts.
---

# Research Figure Production

Use Planning mode in `figure_review` and Final mode in `figure_production`. Read `references/figure-data-contract.md` in both modes. During planning, consult the relevant analytical-task section of `references/chart-selection-guide.md`; inspect only triggered entries in `references/chart-caveat-checklist.md`. Read `references/python-plotting-patterns.md` only when a code pattern is needed.

Render every governed figure from a dedicated `.py` script under `exp/figures/`; keep artifacts under `data/figures/`. Import `scienceplots` and use `science` plus `no-latex` by default.

## Planning: `figure_review`

1. Verify complete sources and matching passing `aggregation-validation.json`.
2. Curate only row/key-preserving display tables and record the transformation or identity manifest.
3. Map every metric, condition, coverage/failure state, and sensitivity to the draft set.
4. Record chart candidates, basis, caveats, selection, and coverage in `figure-plan.json` and `figure-coverage.json`.
5. Render drafts, write their manifest, and run `validate_figure_script.py` in planning mode.
6. Present every draft and coverage through `$human-research-review-gate`; record feedback, the first-presentation milestone, predicates, and outgoing rules.

## Final: `figure_production`

1. Implement every in-scope request from the exact feedback reference; label schematics distinctly from data figures.
2. Execute the final script and write `figure_manifest.json` linking sources, plan, coverage, caveats, hashes, environment, exports, and feedback.
3. Inspect intended-size raster previews and write `figure_integrity_audit.json` for meaning, coverage, encodings, traceability, and readability.
4. Run `validate_figure_script.py` in final mode, then record predicates and outgoing rules.

Optional assets provide a script structure and plotting helpers; copy only what the figure needs.

## Output

Return the mode's script, tables when curated, exports, manifests, validation/audit, predicates, and feedback or next decision.

## Guardrails

- Account for every condition, failure, and sensitivity; explain every encoding.
- New production quantities belong in the computation path, not only plotting code.
- Drafts become final only after researcher feedback.
