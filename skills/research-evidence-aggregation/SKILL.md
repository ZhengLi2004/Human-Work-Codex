---
name: research-evidence-aggregation
description: Build complete traceable run, aggregate, and condition-merged tables and validate them in `aggregation-validation.json`.
---

# Research Evidence Aggregation

Read `references/evidence-artifact-contract.md` for schemas and validation fields. Use `assets/validate_aggregation_tables.m` when its contract fits.

Follow the contract's source authority order. Missing authority, unresolved conflict, or incompatible grain blocks aggregation. Implement in MATLAB by default through `$research-computing-implementation`; keep code in `exp/` and artifacts in `data/tables/`.

## Workflow

1. Verify source identities, fingerprints, revisions, grain, schemas, stable keys, statuses, ranges, time rules, and join cardinalities.
2. Build `runs` on the complete planned skeleton at the independent-run grain, retaining every identity and status.
3. Compute within the defined unit, then produce one `aggregate_full` row per planned combination and complete `condition_merged` tables.
4. Write tables in bulk and record formulas, keys, versions, coverage, paths, and hashes.
5. Write `aggregation-validation.json` with core and risk-relevant checks; block publication when it is unsafe.

Example: if one of three planned repeats fails, retain the condition with `n_planned: 3`, `n_valid: 2`, and one failure; do not drop the run identity or condition.

Preserve coverage, dispersion, and traceability. Never select only successful or favorable runs, pool lower-level observations without the TODO-defined estimator, or change exclusions after viewing result direction.

## Output

Return `runs`, `aggregate_full`, `condition_merged`, manifest, validation paths, and failure/missingness/comparability counts.
