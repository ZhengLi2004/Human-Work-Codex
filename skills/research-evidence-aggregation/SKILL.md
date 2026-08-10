---
name: research-evidence-aggregation
description: Convert immutable scientific runs into complete traceable run-level, aggregate, and condition-merged tables, then validate controlling sources, grain, keys, coverage, joins, and calculations in aggregation-validation.json. Preserve every planned combination, repeat, failure, and source path; do not substitute weaker sources or infer grouping rules from results.
---

# Research Evidence Aggregation

## Overview

Create the complete factual tables required by the TODO and by downstream Work figure production. The aggregation must be reproducible from immutable raw outputs and must retain failed, missing, invalid, and incomplete combinations.

Read `references/evidence-artifact-contract.md` for schemas and the required `aggregation-validation.json` contract. Use `assets/validate_aggregation_tables.m` when its table contract matches the task.

## Entry requirements

Resolve controlling sources in this order before aggregation:

1. the TODO for scientific meaning;
2. task-state YAML and the frozen task manifest for lifecycle state and planned task identities;
3. the raw-result index and immutable raw outputs for observed execution facts;
4. derived tables, which control only after reconciliation with the sources above.

Compare overlapping sources by fingerprint or revision, intended grain, schema, stable keys, coverage, status counts, and time scope. Stop on an unresolved conflict, missing controlling source, or incompatible grain. Do not replace a missing source with a convenient table.

Resolve from the TODO and controlling technical sources:

- every task variable and planned value;
- control variables and comparability rules;
- complete planned combination set;
- independent-repeat unit and required repeat count;
- metric definitions and direction;
- failure, missingness, exclusion, invalidation, and incomparability rules;
- raw-result index and code/data/config versions.

Stop when a missing definition would change grouping or statistical meaning.

Implement non-plotting aggregation in MATLAB by default through `$research-computing-implementation`. Use the Python I/O guidance below only for a documented Python-only exception.

## Workflow

1. Validate the TODO fingerprint, task-state revision, frozen task manifest, raw-result index, and raw-output references. Record the controlling path for every planned field and observed fact.
2. Confirm the intended analysis grain, schema, stable keys, duplicate and missing keys, statuses, ranges, time coverage and timezone rules when applicable, and declared join cardinalities before computing aggregates.
3. Build `runs` with one row per independent run, including all variables, controls, repeat IDs, statuses, metrics, source paths, and anomalies.
4. Build the complete planned-condition skeleton before joining observed runs.
5. Left-join observed runs so unexecuted, failed, invalid, missing, and insufficient-repeat combinations remain represented. Record declared and observed join cardinality and row counts before and after each join.
6. Compute metrics within the TODO-defined independent unit before summarizing across repeats; paired designs compute effects within pairs first.
7. Build `aggregate_full` with exactly one row per planned task-variable and required-control combination.
8. Build one logical `condition_merged` table per experiment class. It may be one file or a partitioned dataset, but it must contain the complete applicable data and stable source identifiers needed by Work.
9. Write tables in bulk. Prefer Parquet for large or multi-file tables; use CSV only for small interchange outputs written in one or a few bulk operations.
10. Write a machine-readable aggregation manifest with formulas, keys, versions, coverage, file paths, and hashes.
11. Write `aggregation-validation.json`. Run the mandatory checks plus only the additional risk-driven checks that apply to this data shape and claim.
12. Block aggregate publication when the validation reports a source, grain, coverage, join, denominator, or calculation problem that makes the result unsafe to use.
13. Update only the Codex result and condition-merged-table path values in the TODO.

## Concise example

If the plan contains two conditions and three independent repeats per condition, `runs` represents all six planned run identities. If one run fails, `aggregate_full` still contains both condition rows; the affected row reports `n_planned: 3`, `n_valid: 2`, and one failure rather than dropping the failed run or the condition.

## Mandatory validations

- every planned combination is present in `aggregate_full`;
- `n_planned`, `n_valid`, and status counts agree with `runs`;
- each raw run contributes at most once;
- no averaging crosses incompatible controls;
- no undeclared row filter exists;
- every aggregate row traces to source runs;
- every condition-merged row retains stable IDs and provenance;
- failed, missing, invalid, incomplete, and incomparable combinations are preserved;
- raw outputs remain immutable;
- manifest paths and hashes exist;
- a partitioned logical table has one stable schema across partitions.

Also select applicable risk-driven checks rather than running a fixed checklist mechanically:

- compare row counts and distinct stable keys before and after joins to detect join expansion;
- recompute important rates from raw numerators and denominators and reject zero or shifted denominators;
- reconstruct weighted estimates from component numerators and denominators instead of averaging precomputed averages;
- compare equal time windows and record timezone and cutoff rules;
- check whether filtering, unavailable records, or outcome-defined groups create selection bias;
- compare robust summaries or leave-one-out results when outliers could drive the stated result.

## I/O requirements

- Do not build outputs by reopening CSV for every row.
- In Python under a documented exception, accumulate records or Arrow record batches and write chunk/partition files; avoid repeated `pd.concat` in loops.
- In MATLAB, preallocate/collect table chunks and use `parquetwrite`, `writetable`, or MAT/HDF5 output at batch boundaries rather than per row.
- Merge worker outputs once after execution or use a partitioned dataset with independent files.

## Guardrails

- Do not aggregate only successful or favorable runs.
- Do not pool lower-level observations to inflate independent sample size unless the TODO explicitly defines that estimator.
- Do not substitute a best seed, best subject, or best parameter for the complete combination summary.
- Do not change failure or exclusion rules after viewing the result direction.
- Do not hide coverage or dispersion fields.
- Describe joins, grouping, and aggregation with standard database and statistical terms; do not invent a label for an ordinary sequence of operations.

## Output contract

Produce under the result directory:

1. `runs` table or dataset;
2. `aggregate_full` table or dataset;
3. `condition_merged` table(s) or dataset directory;
4. aggregation manifest;
5. `aggregation-validation.json` with source resolution, planned-versus-observed coverage, check results, issue impact, calculation spot checks, and evidence paths;
6. failure, missingness, incomparability, and insufficient-repeat counts.

Return the exact paths and update only the corresponding TODO path values.
