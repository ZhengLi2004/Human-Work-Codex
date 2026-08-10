---
name: publication-table-curation
description: Curate Codex-completed result tables during work_postprocessing using row-preserving, key-preserving column and presentation transformations, and prepare validated curated tables for figure planning that covers all applicable data. Use only after complete result paths exist in the TODO. Do not recompute metrics, filter rows, select best conditions, or create a Markdown handoff.
---

# Publication Table Curation

## Objective

Convert complete Codex tables into human-readable Work tables while preserving every experimental combination, failure state, negative result, and stable source key.

## Entry gates

Resolve:

- the complete TODO;
- task-state YAML with `current.state: work_postprocessing`;
- Codex result directory;
- raw-result index or directory;
- condition-merged table paths;
- complete `runs` and `aggregate_full` tables when required;
- stable combination keys and provenance fields.
- the passing `aggregation-validation.json` and its controlling-source references.

Resolve scientific meaning from the TODO, lifecycle and planned work from task-state plus the frozen task manifest, observed facts from the raw-result index plus immutable raw outputs, and derived values from the validated aggregate tables, in that order. Block and return the issue to Codex if sources conflict, the analysis grain differs, `aggregation-validation.json` fails, or required complete tables, coverage states, or provenance are absent. Work must not repair missing experimental facts or substitute a weaker source.

## Data quality checks

For each logical table:

- validate the expected row skeleton or planned-combination count;
- validate stable keys are unique where required;
- preserve `n_planned`, `n_valid`, dispersion, failure, missingness, invalidity, and coverage fields;
- ensure no averaging crosses controls;
- ensure every row traces to runs and raw outputs;
- validate file paths, schemas, and manifests.
- verify source hashes match the passing aggregation validation and its creation revision remains traceable in task-state history;
- review only the risk-driven checks applicable to the intended table use instead of adding unmotivated transformations or checks.

## Allowed transformations

- remove purely operational columns not needed for display;
- reorder columns;
- rename internal columns to human-readable names;
- map enumerated labels;
- combine one-to-one display columns while preserving traceability;
- select TODO-required metric columns while retaining coverage and limiting fields;
- apply documented display rounding;
- sort deterministically by task variables.

## Forbidden transformations

- filter, delete, duplicate, merge, deduplicate, or re-aggregate rows;
- keep only the best parameter, seed, subject, session, or supportive condition;
- hide failures, missingness, negative results, or coverage status;
- recompute metrics, impute values, or change the statistical unit;
- infer scientific priority from display order.

## Workflow

1. Load each logical input table completely or through a partition-aware scan.
2. Record input row count, stable-key set, schema, and hashes in a machine-readable transformation manifest.
3. Apply only allowed column-level and presentation transformations.
4. Validate output row count equals input row count and stable-key sets are identical.
5. Write curated tables in Parquet by default; write CSV only when small and required for interchange.
6. Save the transformation manifest beside the curated tables.
7. Update only the `Work curated table(s)` path value in the TODO.
8. Record that the TODO path changed and require Codex to invoke `$research-state-transition` in Synchronize TODO mode before transition evaluation.
9. When task state is available, append curated-table artifact references and record `work_tables_complete` as `true`, `false`, or `unknown` with evidence. Do not change `current.state`.
10. Hand the paths and transformation manifest to `$research-figure-production` in Planning mode. The curated table may serve as a figure source when the manifest proves row and stable-key preservation and the table retains all fields required by that figure.

## Concise example

Allowed: rename `snr_db` to `SNR (dB)`, reorder columns, round display values, and retain every stable condition key plus `n_planned`, `n_valid`, and failure counts.

Forbidden: keep only the SNR values with the highest mean score or delete failed conditions to make the table and later figures easier to read.

## Output contract

Produce curated table file(s) or dataset directory and a machine-readable transformation manifest. Return input/output validation results and task-state evidence updates in chat. On normal success, continue to `$research-figure-production` Planning mode without evaluating transitions; the curated-table and figure-directory path changes may be synchronized together, but Codex must synchronize them before evaluation. If curation reaches an auditable failure or blocker that prevents figure planning, synchronize any path change, set the Work execution to a decision boundary (`execution.decision_boundary_reached: true`, `current.status: awaiting_transition_evaluation`, `transition_review.status: evaluation_required`), and return control for Codex rule evaluation. Do not create a Markdown result package or recommend a lifecycle transition.
