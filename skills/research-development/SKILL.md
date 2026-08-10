---
name: research-development
description: Execute the recorded Development state under the MATLAB-first policy and the ordered make-it-work, make-it-right, make-it-fast gates. Use only when task-state current.state is development. Build a runnable scaffold, implement and self-check the TODO faithfully, then optimize measured bottlenecks without running an unapproved Pilot or choosing the next state.
---

# Research Development

## Objective

Convert the TODO's scientific specification into a credible executable vertical slice while preserving formulas, data semantics, controls, metrics, and output meaning. Complete **“Make it work, make it right, make it fast”** in order and keep separate evidence for each gate.

## Required inputs

- complete TODO;
- task-state YAML with `current.state: development`;
- the requested same-state execution scope;
- existing Python/MATLAB code and data interfaces;
- project policy and prior Exploration artifacts when applicable.

## Workflow

1. Map every scientific input, transformation, control, metric, and output to concrete code and data objects; inspect the existing implementation and environment before editing.
2. Invoke `$research-computing-implementation`. Use MATLAB for non-plotting computation unless its documented exception test is satisfied; keep governed plotting in Python/Jupyter.
3. **Make it work:** build and run a minimal current-environment scaffold with realistic interfaces, shapes, efficient bulk I/O, logs, recovery boundaries, and one representative task path. Label placeholder kernels; correctness evidence requires the implemented algorithm and its checks.
4. **Make it right:** implement a clear small-case reference and then the TODO's exact algorithm. Self-check formulas, data contracts, controls, units, randomness, metrics, and outputs against the strongest available oracle.
5. Use `$research-agile-testing` for invariants, leakage, indexing, numerical equivalence, and regression risk. Complete one representative combination and one independent repeat end to end.
6. **Make it fast:** profile the representative workload, then consider redundant-work removal, algorithmic changes, memory layout/preallocation, measured vectorization and JIT-friendly MATLAB, optimized built-ins, MEX or generated code, parallel computing, GPU acceleration, and I/O/task partitioning in that order of escalating cost.
7. Keep the correctness reference, run equivalence tests after every material optimization, and record before/after runtime and resource measurements. A profile showing no worthwhile safe optimization may close this gate when the evidence and remaining cost are recorded.
8. Add checkpoint, resume, progress, and isolated worker outputs when batch behavior is material. Do not write numerical results row by row.
9. Preserve scaffold, correctness, smoke-test, profile, and benchmark artifacts separately from Pilot and Confirmation outputs.
10. Record execution status, artifact references, and applicable predicate results in task state.
11. Return control to `$research-todo-executor` for rule evaluation.

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
- `implementation_scaffold_validated`;
- `implementation_matches_todo`;
- `risk_matched_tests_sufficient`;
- `smoke_test_passed`;
- `performance_optimization_complete`;
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
- Do not introduce a general framework beyond the TODO requirements.
- Do not optimize a scientific kernel before the runnable scaffold and correctness reference exist.
- Do not replace MATLAB with Python for implementation convenience; record the required package/interface or measured infeasibility that justifies any non-plotting Python component.
- Do not choose or apply a next state.
- Do not update the TODO except allowed output paths.

## Output contract

Return:

- implementation files and language/package choices;
- tests and commands actually run;
- smoke-test and benchmark paths;
- scaffold, correctness-reference, self-check, profile, before/after benchmark, and equivalence evidence;
- I/O and recovery design;
- limitations and unresolved risks;
- predicate results with evidence references.
