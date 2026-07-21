---
name: human-research-review-gate
description: Present a blocking human decision for eligible lifecycle transitions, semantic changes, restricted long-run launch, researcher review of draft figures, completion, stop, or redesign. Use after factual evidence, figure-review material, or transition evaluation is ready. Do not approve or apply a lifecycle transition yourself.
---

# Human Research Review Gate

## Objective

Stop execution at a governance boundary and request one explicit human decision in the conversation. Do not create a review packet or change lifecycle state.

## Use this gate for

- selecting one eligible transition rule path, including the self-transition;
- approving a fixed-method, metric, control, data-scope, or completion-criterion change;
- launching a restricted long-running job;
- obtaining interactive researcher recommendations on draft figures covering all applicable data during `figure_review`;
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

## Figure-review procedure

Use only when `current.state: figure_review` and the planning artifacts are ready.

1. State the TODO, task-state path, revision, and figure-directory path.
2. Show or link every governed draft figure. For each, state the executed notebook, SciencePlots style stack, question, source class, graphical method, statistical unit, and represented conditions. Do not present a temporary `.py` preview.
3. Summarize the table-to-figure coverage check, including missing, failed, invalid, or incomparable conditions. Do not overwhelm the researcher with operational provenance fields.
4. Identify which relevant paper figures were inspected, or state plainly that none were available and name the established plot convention used.
5. Summarize the selected chart, the plausible alternatives that were rejected, the selection reason, and the chart-specific caveats that the final audit will check. Link the exact Data-to-Viz or Python Gallery page only when it was actually inspected.
6. Ask for concrete recommendations: retain, exclude with reason, revise, split or combine, or add a supplemental generalized diagram.
7. State that a generalized diagram will be labeled as a schematic and cannot replace complete quantitative figures.
8. Flag any requested metric, inclusion-rule, condition-scope, statistical-unit, or scientific-claim change as a semantic change requiring separate approval.
9. Wait for the researcher's output. Do not infer approval or preferences from silence.
10. When output arrives, preserve its meaning and provide a concise action list plus an exact conversation reference for predicate evidence. Do not convert a suggestion into transition approval.
11. Mark the review execution decision boundary through the governing workflow and require `$research-state-transition` Evaluate before final production.

Example prompt:

> Draft F1 shows every method across all noise levels; F2 shows failure counts for the same condition keys. Please specify which figures to retain, exclude, or revise, and whether you want a supplemental schematic. Excluding a data figure does not permit its conditions to disappear from the final quantitative set.

Example response handling:

> Researcher request: retain F1, split F2 by dataset, and add a labeled pipeline schematic. These are presentation changes; no metric, condition, or inclusion rule changes were requested.

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
- `figure_review_material` and `coverage_summary` when applicable;
- `researcher_recommendations` and exact evidence reference after figure review output arrives;
- `explicit_human_decision_requested`;
- `execution_requires_separate_authorization`.

## Hard rules

- Do not interpret silence, a positive result, or a prior stage name as approval.
- Do not apply a transition or edit `current.state`.
- Do not omit an eligible self-transition or its rule ID.
- Do not write approval into the TODO.
- Do not create a stage-review, workflow, gate, or result-summary Markdown file.
- Do not weaken the proposed scope to avoid asking for approval.
- Do not omit drafts or conditions to shorten a figure-review prompt; summarize coverage and link the complete artifacts.
- Do not use invented technical labels or persuasive adjectives. Name established plot types and state evidence directly.
