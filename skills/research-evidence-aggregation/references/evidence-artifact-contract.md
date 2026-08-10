# Evidence Artifact Contract

All artifacts live below the result directory referenced by the TODO. They are technical evidence, not additional handoff documents.

## Required logical artifacts

### Raw-output index

Maps every stable task/repeat ID to immutable raw artifacts, input identifiers, configuration/code/data fingerprints, state, and failure information.

### Complete run-level table

Contains one planned row per independent run or an explicit state row for every planned task. It preserves failures, missingness, invalidity, retry attempts, and provenance.

### `aggregate_full`

Aggregates only across the independent repeat unit defined in the TODO. Every condition/control combination remains present, including combinations with no valid runs. Include at least:

- stable condition key;
- `n_planned` and `n_valid`;
- estimate and uncertainty/dispersion fields defined by the TODO;
- completeness/comparability state;
- failure/missing/invalid counts;
- traceability to run rows.

### Condition-merged table

Joins all condition-level metrics and controls needed for downstream Work curation and figures. It must:

- preserve the complete condition skeleton;
- use explicit validated join keys and cardinality;
- expose coverage and comparability fields;
- never drop a condition because one metric is missing;
- retain paths or stable IDs that trace back to raw and run-level evidence.

A logical table may be a partitioned dataset composed of multiple physical files.

## I/O requirements

- Write tables in bulk, normally as Parquet datasets.
- Do not append one row at a time to CSV/XLSX or repeatedly concatenate a growing DataFrame/table.
- Use worker-isolated or chunk-isolated outputs and one final merge/scan.
- Use temporary paths and atomic publish for completed chunks.
- Record schema, row counts, key checks, file list, and hashes in a machine-readable manifest.

## Validation

Reconcile:

- planned task count;
- run-state counts;
- raw-artifact count;
- aggregate condition count;
- condition-merged row/key skeleton;
- duplicate/missing keys;
- metric validity and coverage fields;
- joins against the TODO-defined controls.

Do not interpret scientific meaning during aggregation. Preserve enough information for Work to curate tables and produce figures without rereading operational logs.

## `aggregation-validation.json`

Write this file beside the aggregation manifest. It is the fixed machine-readable validation output; do not replace it with prose or a notebook. Include:

- `schema_version`, `todo_fingerprint`, `task_state_revision`, and `generated_at_utc`;
- `controlling_sources` in the order TODO, task-state and frozen task manifest, raw-result index and immutable raw outputs, then derived tables, with path, SHA-256, revision when available, expected grain, and resolution status;
- `analysis_grain`, stable condition keys, stable run keys, statistical unit, time range, timezone, and declared filters;
- `planned_coverage` and `observed_coverage`, including planned runs, observed runs, every run status, planned conditions, aggregate conditions, and missing keys;
- `checks`, each with a stable check ID, `status: pass|fail|not_applicable`, concrete observed values, expected rule, impact on use, and evidence paths;
- `calculation_spot_checks`, with the source values, independently recomputed value, reported value, tolerance or exact rule, and status;
- `blocking_findings`, `non_blocking_findings`, and top-level `passed`.

At minimum, record checks for source availability and agreement, intended grain, schema, stable-key uniqueness, missing planned keys, status-count reconciliation, range validity, time coverage when time is used, declared-versus-observed join cardinality, aggregate row count, and traceability. Record denominator, weighted-average, period-alignment, timezone, selection-bias, and outlier-influence checks only when the metric or design makes them applicable; use `not_applicable` with a short reason when the applicability decision itself matters.

Set `passed: false` when any finding means the aggregate is unsafe for the TODO-defined use. Keep the derived files for diagnosis, but do not advertise them as validated evidence and do not let Work use them as a complete figure source.
