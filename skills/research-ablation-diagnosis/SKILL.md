---
name: research-ablation-diagnosis
description: Execute the recorded Ablation/Diagnosis state to isolate bounded component contributions, implementation faults, or predefined candidate explanations. Use only when task-state current.state is ablation_diagnosis. Do not expand into a new scientific question or choose the next state directly.
---

# Research Ablation and Diagnosis

## Objective

Distinguish a finite approved set of candidate explanations or failure causes while changing only the target factor under test.

## Required inputs

- complete TODO;
- task-state YAML with `current.state: ablation_diagnosis`;
- defined candidate explanations or components;
- exact intervention and control definitions;
- evidence that motivated Diagnosis;
- approved metrics and stopping boundary.

## Workflow

1. State each candidate explanation and the observation that would strengthen or weaken it.
2. Design the smallest intervention or diagnostic that distinguishes candidates.
3. Prove that the intervention changes only the intended factor.
4. Use `$research-computing-implementation` for language-specific implementation and performance choices.
5. Use `$research-agile-testing` for intervention isolation, invariants, and regression protection.
6. Use `$research-batch-execution` and `$research-evidence-aggregation` when repeated or multi-condition evidence is required.
7. Preserve all null, contradictory, failed, and unresolved outcomes.
8. Stop when the approved candidates are distinguished as far as the design permits.
9. Record execution status, artifact references, and applicable predicate results in task state.
10. Return control to `$research-todo-executor` for rule evaluation.

## Predicate evidence

Evaluate applicable predicates such as:

- `current_scope_executed`;
- `required_artifacts_complete`;
- `same_state_work_remaining`;
- `diagnosis_supports_development`;
- `diagnosis_supports_pilot`;
- `diagnosis_supports_confirmation`;
- `pilot_scope_defined`;
- `confirmation_spec_frozen`;
- `no_critical_correctness_risk`;
- `no_scope_change_required`;
- `todo_completion_evidence_satisfied`;
- `codex_outputs_ready_for_work`;
- `continuation_warranted`;
- `stop_warranted`.

## Boundaries

- Do not allow Diagnosis to become an unlimited search for a favorable explanation.
- Do not introduce a new dataset, brain region, behavior variable, objective, or primary metric without a new approval or TODO.
- Do not treat implementation debugging as mechanism evidence.
- Do not choose or apply a next state.
- Do not update the TODO beyond allowed output paths.

## Output contract

Return tested candidates, exact interventions, tests and commands, observed facts, explanations weakened or unresolved, artifacts, and predicate results with evidence references.
