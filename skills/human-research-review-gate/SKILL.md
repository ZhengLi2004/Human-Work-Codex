---
name: human-research-review-gate
description: Present a blocking human decision for eligible lifecycle transitions, semantic changes, restricted long-run launch, completion, stop, or redesign. Use after factual evidence or transition evaluation is ready. Do not approve, apply, or persist the decision yourself.
---

# Human Research Review Gate

## Objective

Stop execution at a governance boundary and request one explicit human decision in the conversation. Do not create a review packet or change lifecycle state.

## Use this gate for

- selecting one eligible transition rule path, including the self-transition;
- approving a fixed-method, metric, control, data-scope, or completion-criterion change;
- launching a restricted long-running job;
- accepting incomplete or incomparable evidence;
- completing, stopping, or redesigning a TODO;
- separating a new scientific question into another TODO.

## Transition decision procedure

When a transition review is pending:

1. State the TODO, task-state path, revision, current state, and execution status.
2. Separate verified facts, predicate judgments, and tentative interpretation.
3. List every eligible transition exactly as recorded, including `rule_id`, source, target, kind, and the self-transition.
4. Give the Codex-recommended rule ID, target, confidence, and concise rationale.
5. Explain material alternatives and the consequences of selecting each.
6. Identify notable ineligible paths only when their missing or contradicted predicates clarify the decision.
7. Ask the human to select exactly one eligible `rule_id` and target. A target-only response is acceptable only when one eligible rule reaches that target.
8. State that selecting a path approves the transition only; execution requires explicit authorization unless the human says to approve and execute.
9. Stop.

After the human responds, route the selection to `$research-state-transition` Apply. Do not edit the state file in this Skill.

## Semantic-change procedure

1. State the current TODO and lifecycle state.
2. Identify the exact fixed definition that would change.
3. Explain how the change affects interpretation, comparability, or prior artifacts.
4. Give the smallest safe options: reject, amend the TODO, create a new TODO, or invalidate/version prior evidence.
5. Request one explicit decision and stop.

## Long-run request fields

Include:

- reproducible command;
- working directory;
- frozen configuration or manifest path;
- expected result directory;
- measured preflight runtime and resources;
- estimated formal runtime and resources;
- checkpoint and resume behavior;
- progress and log paths;
- completion and failure criteria.

A long-run launch decision does not itself change lifecycle state.

## Output contract

Return:

- `decision_type`;
- `todo`;
- `state_file` and revision when applicable;
- `current_state`;
- `verified_facts`;
- `predicate_summary` when applicable;
- `eligible_transitions` including the self rule when applicable;
- `recommended_transition` with rule ID and target;
- `alternatives`;
- `explicit_human_decision_requested`;
- `execution_requires_separate_authorization`.

## Hard rules

- Do not interpret silence, a positive result, or a prior stage name as approval.
- Do not apply a transition or edit `current.state`.
- Do not omit an eligible self-transition or its rule ID.
- Do not write approval into the TODO.
- Do not create a stage-review, workflow, gate, or result-summary Markdown file.
- Do not weaken the proposed scope to avoid asking for approval.
