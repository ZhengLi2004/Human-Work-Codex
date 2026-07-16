---
name: publication-table-curation
description: Curate Codex-completed result tables during work_postprocessing using row-preserving, key-preserving column and presentation transformations. Use only after complete result paths exist in the TODO. Do not recompute metrics, filter rows, select best conditions, or create a Markdown handoff.
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

Block and return the issue to Codex if required complete tables, coverage states, or provenance are absent. Work does not repair missing experimental facts.

## Data quality checks

For each logical table:

- validate the expected row skeleton or planned-combination count;
- validate stable keys are unique where required;
- preserve `n_planned`, `n_valid`, dispersion, failure, missingness, invalidity, and coverage fields;
- ensure no averaging crosses controls;
- ensure every row traces to runs and raw outputs;
- validate file paths, schemas, and manifests.

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
8. When task state is available, append curated-table artifact references and record `work_tables_complete` as `true`, `false`, or `unknown` with evidence. Do not change `current.state`.
9. Hand the paths to `$research-figure-production`.

## Output contract

Produce curated table file(s) or dataset directory and a machine-readable transformation manifest. Return input/output validation results and task-state evidence updates in chat. On normal success, continue to `$research-figure-production` without evaluating transitions. If curation reaches an auditable failure or blocker that prevents figure production, set the Work execution to a decision boundary (`execution.decision_boundary_reached: true`, `current.status: awaiting_transition_evaluation`, `transition_review.status: evaluation_required`) and return control for Codex rule evaluation. Do not create a Markdown result package or recommend a lifecycle transition.
