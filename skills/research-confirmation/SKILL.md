---
name: research-confirmation
description: Execute the recorded Confirmation state under a frozen specification, complete predefined condition set, fixed metrics, and fixed repeat/statistical rules. Use only when task-state current.state is confirmation. Do not tune after seeing results or choose the next state directly.
---

# Research Confirmation

## Objective

Produce complete, recoverable, and traceable formal evidence under the exact frozen specification associated with the current task state.

## Entry gates

All must hold:

- task state is `confirmation` and ready or validly resumed;
- the specification, code/config version, condition set, repeats, metrics, controls, failure rules, and output namespace are frozen;
- relevant regression and integration tests pass;
- no unresolved leakage, comparability, aggregation, or storage-integrity risk remains;
- formal outputs are distinct from preflight and Pilot outputs.

Do not fill missing formal definitions with defaults.

## Preflight

1. Compare the frozen configuration with the TODO.
2. Generate the complete immutable task manifest.
3. Run critical regression, contract, and integration tests.
4. Verify buffered/partitioned I/O, checkpointing, resume, logs, progress, and aggregation.
5. Complete one formal-configuration combination and one repeat in a separate preflight namespace.
6. Measure representative compute and I/O cost.
7. When the runtime threshold is reached, invoke the human long-run gate instead of launching the run; do not evaluate lifecycle transition yet.

## Formal execution

1. Use `$research-computing-implementation` for the approved Python or MATLAB boundary.
2. Use `$research-batch-execution` for the frozen task manifest.
3. Preserve raw artifacts immutably; reruns use new identifiers.
4. Do not change parameters, metrics, inclusion rules, conditions, or repeats in response to interim results.
5. Reconcile completed, failed, missing, duplicate, invalid, and incomparable units.
6. Use `$research-evidence-aggregation` to produce complete `runs`, `aggregate_full`, condition-merged tables, and manifests.
7. Record supporting, limiting, contradictory, negative, and anomalous facts.
8. Update only Codex result paths in the TODO.
9. Record execution status, artifact references, and applicable predicate results in task state.
10. Return control to `$research-todo-executor` for rule evaluation.

## Invalidating a run

Mark a run invalid only for a documented implementation error, data corruption, frozen-spec violation, or incomplete execution. Preserve the original output, state the exact reason, add regression protection, and rerun under a new version. Result direction is never an invalidation criterion.

## Predicate evidence

Evaluate applicable predicates such as:

- `current_scope_executed`;
- `required_artifacts_complete`;
- `formal_evidence_complete`;
- `formal_run_invalidated`;
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

- Do not tune, change metrics, or revise exclusions after viewing results.
- Keep new exploratory analyses separate from the predefined primary analysis.
- Do not interpret a non-significant result as proof of no effect.
- Do not write a formal scientific narrative.
- Do not choose or apply a next state.
- Do not create another handoff document.

## Output contract

Return the frozen specification identifier, formal command, task reconciliation, raw and table paths, complete supporting and limiting facts, invalid/missing items, and predicate results with evidence references.
