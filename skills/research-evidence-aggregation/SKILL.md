---
name: research-evidence-aggregation
description: Convert immutable scientific runs into complete traceable run-level, aggregate, and condition-merged tables while preserving every planned combination, repeat, failure, and source path. Do not filter unfavorable rows or infer grouping rules from results.
---

# Research Evidence Aggregation

## Overview

Create the complete factual tables required by the TODO and by downstream Work figure production. The aggregation must be reproducible from immutable raw outputs and must retain failed, missing, invalid, and incomplete combinations.

Read `references/evidence-artifact-contract.md` for schemas.

## Entry requirements

Before aggregation, resolve from the TODO:

- every task variable and planned value;
- control variables and comparability rules;
- complete planned combination set;
- independent-repeat unit and required repeat count;
- metric definitions and direction;
- failure, missingness, exclusion, invalidation, and incomparability rules;
- raw-result index and code/data/config versions.

Stop when a missing definition would change grouping or statistical meaning.

## Workflow

1. Validate the raw-result index and task manifest.
2. Build `runs` with one row per independent run, including all variables, controls, repeat IDs, statuses, metrics, source paths, and anomalies.
3. Build the complete planned-condition skeleton before joining observed runs.
4. Left-join observed runs so unexecuted, failed, invalid, missing, and insufficient-repeat combinations remain represented.
5. Compute metrics within the TODO-defined independent unit before summarizing across repeats; paired designs compute effects within pairs first.
6. Build `aggregate_full` with exactly one row per planned task-variable and required-control combination.
7. Build one logical `condition_merged` table per experiment class. It may be one file or a partitioned dataset, but it must contain the complete applicable data and stable source identifiers needed by Work.
8. Write tables in bulk. Prefer Parquet for large or multi-file tables; use CSV only for small interchange outputs written in one or a few bulk operations.
9. Write a machine-readable aggregation manifest with formulas, keys, versions, coverage, file paths, and validations.
10. Validate uniqueness, completeness, comparability, traceability, and row counts.
11. Update only the Codex result and condition-merged-table path values in the TODO.

## Mandatory validations

- every planned combination is present in `aggregate_full`;
- `n_planned`, `n_valid`, and status counts agree with `runs`;
- each raw run contributes at most once;
- no averaging crosses incompatible controls;
- no undeclared row filter exists;
- every aggregate row traces to source runs;
- every condition-merged row retains stable IDs and provenance;
- failed, missing, invalid, incomplete, and incomparable combinations are preserved;
- raw outputs are not overwritten;
- manifest paths and hashes exist;
- a partitioned logical table has one stable schema across partitions.

## I/O requirements

- Do not build outputs by reopening CSV for every row.
- In Python, accumulate records or Arrow record batches and write chunk/partition files; avoid repeated `pd.concat` in loops.
- In MATLAB, preallocate/collect table chunks and use `parquetwrite`, `writetable`, or MAT/HDF5 output at batch boundaries rather than per row.
- Merge worker outputs once after execution or use a partitioned dataset with independent files.

## Guardrails

- Do not aggregate only successful or favorable runs.
- Do not pool lower-level observations to inflate independent sample size unless the TODO explicitly defines that estimator.
- Do not substitute a best seed, best subject, or best parameter for the complete combination summary.
- Do not change failure or exclusion rules after viewing the result direction.
- Do not hide coverage or dispersion fields.

## Output contract

Produce under the result directory:

1. `runs` table or dataset;
2. `aggregate_full` table or dataset;
3. `condition_merged` table(s) or dataset directory;
4. aggregation manifest;
5. automated validation results;
6. failure, missingness, incomparability, and insufficient-repeat counts.

Return the exact paths and update only the corresponding TODO path values.
