---
name: research-exploration
description: Execute the recorded Exploration state to resolve project mappings, data semantics, feasibility, and bounded uncertainties with minimal decisive probes. Use only when task-state current.state is exploration. Do not build a full system or choose the next state directly.
---

# Research Exploration

## Objective

Resolve only the uncertainties that prevent faithful implementation or a justified lifecycle decision. Exploration is not Confirmation and should use the smallest evidence that can distinguish the approved possibilities.

## Required inputs

- complete TODO;
- task-state YAML with `current.state: exploration`;
- the requested same-state execution scope;
- repository modules, data interfaces, prior artifacts, and policies relevant to the uncertainty;
- explicit bounds on what Exploration may and may not change.

## Workflow

1. Restate each unresolved mapping, semantic assumption, or feasibility question from the TODO and current execution scope.
2. Inspect real repository code, data schemas, representative records, and prior artifacts before hypothesizing.
3. Distinguish verified facts from assumptions and unknowns.
4. Design the smallest probe that can resolve each material uncertainty.
5. Use `$research-agile-testing` for schema, unit, shape, label, formula, and invariant checks.
6. Use `$research-computing-implementation` only when a small Python or MATLAB probe is necessary.
7. Preserve probe outputs under the result root and label them as Exploration evidence.
8. Stop when the bounded questions are resolved as far as the available design permits.
9. Record execution status, artifact references, and applicable predicate results in task state.
10. Return control to `$research-todo-executor` for rule evaluation.

## Predicate evidence

Evaluate applicable predicates such as:

- `current_scope_executed`;
- `required_artifacts_complete`;
- `mapping_or_semantics_unresolved`;
- `mapping_and_semantics_resolved`;
- `implementation_work_needed`;
- `existing_implementation_pilot_ready`;
- `pilot_scope_defined`;
- `no_critical_correctness_risk`;
- `no_scope_change_required`;
- `same_state_work_remaining`;
- `todo_completion_evidence_satisfied`;
- `codex_outputs_ready_for_work`;
- `continuation_warranted`;
- `stop_warranted`.

Use `unknown` when the probe does not decide a predicate.

## Boundaries

- Do not turn Exploration into full Development or an open-ended search.
- Do not change TODO formulas, metrics, data meaning, or scope.
- Do not treat exploratory observations as formal evidence.
- Do not choose or apply a next state inside this Skill.
- Do not update the TODO beyond allowed output paths.

## Output contract

Return:

- questions investigated;
- repository and data facts verified;
- assumptions resolved, contradicted, or still unknown;
- probes, commands, and tests actually run;
- artifact paths;
- predicate results with evidence references;
- unresolved blockers.
