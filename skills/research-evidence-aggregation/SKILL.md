---
name: research-evidence-aggregation
description: Build complete traceable run, aggregate, and condition-merged tables and validate them in `aggregation-validation.json`.
---

# Research Evidence Aggregation

Read `references/evidence-artifact-contract.md` for schemas and validation fields. Use `assets/validate_aggregation_tables.m` when its contract fits.

Follow the contract's source authority order. Missing authority, unresolved conflict, or incompatible grain blocks aggregation. Implement in MATLAB by default through `$research-computing-implementation`; keep code in `exp/` and artifacts in `data/tables/`.

## Evidence outcome

Reconcile authoritative sources with the complete planned skeleton before calculating summaries. Validate grain, schema, stable keys, status coverage, ranges, applicable time rules, and join cardinality. Build `runs` at its declared grain, calculate within the TODO-defined unit, and retain one `aggregate_full` row per planned combination plus complete `condition_merged` tables.

For uncertainty or inference, use `$research-statistical-analysis` to verify independent units, per-analysis n, estimators, assumptions, and comparison coverage. Keep contrasts at their own grain when needed; operational run counts need not equal statistical sample sizes.

Publish tables in bulk with traceable formulas, versions, coverage, and hashes. Integrate structural and applicable statistical checks into `aggregation-validation.json`. The bundled helper supplies structural evidence only; the executor resolves remaining checks before setting the final `passed` value. Blocking findings prevent publication as validated evidence.

Example: if one of three planned repeats fails, retain the condition with `n_planned: 3`, `n_valid: 2`, and one failure; do not drop the run identity or condition.

Preserve coverage, dispersion, and traceability. Never select only successful or favorable runs, pool lower-level observations without the TODO-defined estimator, or change exclusions after viewing result direction.

## Output

Return `runs`, `aggregate_full`, `condition_merged`, manifest, validation paths, and failure/missingness/comparability counts.
