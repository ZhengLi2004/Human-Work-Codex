---
name: research-pilot
description: Execute the recorded Pilot state over the complete approved Pilot condition grid and independent repeats to evaluate behavior, stability, parameter marginal value, failures, and cost. Use only when task-state current.state is pilot. Do not cherry-pick results or choose the next state directly.
---

# Research Pilot

## Objective

Run the smallest controlled experiment that is complete enough to judge method behavior and whether the TODO should continue, return for rework, enter bounded Diagnosis, freeze Confirmation, or hand results to Work under the shared rules.

## Required inputs

- complete TODO;
- task-state YAML with `current.state: pilot`;
- reviewed Development implementation or equivalent existing evidence;
- complete Pilot combination set;
- repeat rules, metrics, controls, allowed flexibility, and resource policy.

## Workflow

1. Complete one combination and one repeat end to end.
2. Verify parameter enumeration, independent-repeat generation, metric meaning, storage, and aggregation.
3. Test interruption and resume on a small set when batch execution is applicable.
4. Freeze the Pilot task manifest before inspecting result trends.
5. Use `$research-computing-implementation` for language-specific performance and storage choices.
6. Use `$research-batch-execution` for multiple recoverable units, material I/O, concurrency, or long runtime.
7. Execute all approved combinations under the same repeat rule and preserve immutable raw outputs.
8. Use `$research-evidence-aggregation` to produce complete `runs`, `aggregate_full`, and condition-merged tables.
9. Reconcile every planned combination, including failed, missing, invalid, insufficient-repeat, and incomparable states.
10. Report quality, dispersion, coverage, runtime, memory, GPU memory, I/O behavior, and parameter marginal value.
11. Record execution status, artifact references, and applicable predicate results in task state.
12. Return control to `$research-todo-executor` for rule evaluation.

## Parameter evidence

Report the complete approved range rather than only an optimum:

- central estimate and dispersion for every combination;
- `n_planned`, `n_valid`, and coverage state;
- quality-cost relationship;
- marginal gains, plateau regions, and failure regions;
- all incomplete and incomparable combinations.

## I/O requirements

- Do not append one CSV row per repeat or condition.
- Prefer immutable per-task files plus one bulk merge, or buffered Parquet/array chunks.
- Keep progress/log writes separate from numerical result writes.
- If I/O dominates preflight, change chunk or task granularity before the full Pilot while preserving the planned combination set.

## Predicate evidence

Evaluate applicable predicates such as:

- `current_scope_executed`;
- `required_artifacts_complete`;
- `pilot_grid_complete`;
- `pilot_evidence_supports_confirmation`;
- `confirmation_spec_frozen`;
- `implementation_rework_needed`;
- `bounded_diagnosis_needed`;
- `diagnostic_scope_ready`;
- `no_critical_correctness_risk`;
- `no_scope_change_required`;
- `same_state_work_remaining`;
- `todo_completion_evidence_satisfied`;
- `codex_outputs_ready_for_work`;
- `continuation_warranted`;
- `stop_warranted`.

## Boundaries

- Do not expand or remove combinations after seeing results.
- Do not call a parameter value “best” unless the TODO defines that decision rule.
- Do not present Pilot results as Confirmation.
- Do not choose or apply a next state.
- Do not update the TODO beyond allowed output paths.

## Output contract

Return the frozen Pilot manifest, commands, raw-result path, complete table paths, coverage reconciliation, performance/I/O measurements, failures, limiting evidence, and predicate results with evidence references.
