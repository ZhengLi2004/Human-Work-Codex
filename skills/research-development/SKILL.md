---
name: research-development
description: Execute the recorded Development state to build and verify the minimum scientifically faithful Python or MATLAB implementation needed by the TODO. Use only when task-state current.state is development. Do not run an unapproved Pilot or choose the next state directly.
---

# Research Development

## Objective

Convert the TODO's scientific specification into a credible executable vertical slice while preserving formulas, data semantics, controls, metrics, and output meaning.

## Required inputs

- complete TODO;
- task-state YAML with `current.state: development`;
- the requested same-state execution scope;
- existing Python/MATLAB code and data interfaces;
- project policy and prior Exploration artifacts when applicable.

## Workflow

1. Map every scientific input, transformation, control, metric, and output to concrete code and data objects.
2. Inspect existing implementation before editing.
3. Choose Python, MATLAB, or a justified hybrid boundary through `$research-computing-implementation`.
4. Implement the smallest vertical slice that preserves the TODO.
5. Design throughput-aware storage; do not write numerical results row by row.
6. Use `$research-agile-testing` for formulas, data contracts, invariants, leakage, randomization, numerical equivalence, and regression risk.
7. Add checkpoint, resume, progress, and logs when batch behavior is material.
8. Complete one representative combination and one independent repeat end to end.
9. Measure representative runtime, memory, GPU memory, and material I/O cost.
10. Preserve smoke-test artifacts separately from Pilot and Confirmation outputs.
11. Record execution status, artifact references, and applicable predicate results in task state.
12. Return control to `$research-todo-executor` for rule evaluation.

## Required verification

Choose tests by risk:

- formulas and local algorithms: analytic, property, metamorphic, or differential checks;
- data interfaces: schema, dtype, unit, shape, label, and provenance checks;
- Python/MATLAB parity or optimization: justified numerical equivalence;
- module boundaries: focused integration tests;
- random behavior: fixed-seed implementation determinism;
- storage and resume: atomicity, idempotence, and corruption detection;
- full chain: one-combination one-repeat smoke test.

## Predicate evidence

Evaluate applicable predicates such as:

- `current_scope_executed`;
- `required_artifacts_complete`;
- `mapping_or_semantics_unresolved`;
- `implementation_work_needed`;
- `implementation_matches_todo`;
- `risk_matched_tests_sufficient`;
- `smoke_test_passed`;
- `pilot_scope_defined`;
- `implementation_rework_needed`;
- `no_critical_correctness_risk`;
- `no_scope_change_required`;
- `same_state_work_remaining`;
- `todo_completion_evidence_satisfied`;
- `codex_outputs_ready_for_work`;
- `continuation_warranted`;
- `stop_warranted`.

## Boundaries

- Do not change the TODO's mathematics, metrics, data scope, controls, or independent unit.
- Do not perform an unapproved Pilot or Confirmation run.
- Do not treat a smoke-test metric as research evidence.
- Do not introduce a general framework that this TODO does not require.
- Do not choose or apply a next state.
- Do not update the TODO except allowed output paths.

## Output contract

Return:

- implementation files and language/package choices;
- tests and commands actually run;
- smoke-test and benchmark paths;
- I/O and recovery design;
- limitations and unresolved risks;
- predicate results with evidence references.
