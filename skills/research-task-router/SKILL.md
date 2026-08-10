---
name: research-task-router
description: Route TODO-centered research using the task-state YAML and rule-driven lifecycle. Use for TODO authoring, state initialization/evaluation/application, execution of the current state, Work table and figure planning, researcher figure review, final figure production, or post-report assessment. Do not execute work or infer a state outside the recorded rules.
---

# Research Task Router

## Objective

Use this Skill as the single entry router. Resolve the TODO, task-state YAML, current human instruction, and applicable rules; then select the smallest sufficient Work or Codex Skill set.

Classify and validate the request, then delegate the selected operation to the owning Skill.

Read `references/routing-table.md` when two routes overlap, a state-specific handoff is unclear, or the route must be checked against the full matrix.
Read `references/worked-examples.md` when a concrete route example would clarify a fragile boundary; do not load examples merely to restate an obvious route.

## Related Skills

| Workflow | Skill |
|---|---|
| Create or rewrite current-action TODOs | `$research-report-to-todos` |
| Execute the current Codex-owned state | `$research-todo-executor` plus the recorded state Skill |
| Initialize, synchronize a verified-parameter rewrite, evaluate, or apply lifecycle state | `$research-state-transition` |
| Curate completed result tables | `$publication-table-curation` |
| Plan draft figures or produce reviewed final figures | `$research-figure-production` in the mode fixed by current state |
| Request researcher review of draft figures | `$human-research-review-gate` figure-review procedure |
| Request a blocking human decision | `$human-research-review-gate` |
| Assess the next action after a human report | `$post-report-assessment` |

## Resolve the task and state

Locate the control artifacts in this order:

1. the TODO path explicitly provided by the human;
2. the task-state YAML derived from the TODO identifier and result root;
3. result paths recorded in the TODO;
4. the applicable `AGENTS.md`, shared state machine, policy, pipeline, selected Skills, repository code, and technical artifacts required by the route.

When located sources conflict, apply the authority order in `AGENTS.md`: current human instruction, TODO scientific meaning, task-state lifecycle facts, `AGENTS.md`, shared state-machine rules, policy, selected Skills, then existing engineering conventions. Treat `.research/workflow/pipeline.yaml` as routing guidance that must not override a higher-authority source.

If the TODO remains unresolved, block. Do not guess a task identifier.

If the task-state file is absent and the request concerns execution or lifecycle state, route to `$research-state-transition` in Initialize mode. Initialization creates `todo_ready`; it must not infer the first executable state.

## Classify the request

Choose one primary route:

| Request | Primary route |
|---|---|
| Create, revise, or split a task specification from research material | `$research-report-to-todos` |
| Initialize a missing task-state YAML | `$research-state-transition` Initialize |
| Record an authorized Output References edit, approved Work parameter rewrite, or exact restoration after rejecting an unapproved edit | `$research-state-transition` Synchronize TODO |
| Evaluate outgoing rules after a state | `$research-state-transition` Evaluate |
| Apply a human-confirmed eligible rule path | `$research-state-transition` Apply |
| Execute `exploration`, `development`, `pilot`, `confirmation`, or `ablation_diagnosis` recorded in task state | `$research-todo-executor` plus exactly one state Skill |
| Execute `work_postprocessing` | `$publication-table-curation`, then `$research-figure-production` Planning mode |
| Execute `figure_review` | `$human-research-review-gate` figure-review procedure; wait for the researcher's output |
| Execute `figure_production` | `$research-figure-production` Final mode |
| Aggregate completed runs without a broader state request | `$research-evidence-aggregation` |
| Assess information gain after the human report | `$post-report-assessment` |
| Check routing only | Return a route diagnosis |

Return `no_system_route` for general research questions, formula tutoring, literature explanation, or ordinary software work that is not governed by a Research Task System TODO.

## Resolve lifecycle control

Use `current.state`, `current.status`, `transition_review.status`, `revision`, and the stored TODO SHA-256 fingerprint from the task-state YAML. Recompute the TODO digest before routing lifecycle work. An unexplained mismatch is a blocker.

If the human rejects an unexplained edit, route exact restoration through `$research-state-transition` Synchronize TODO to invalidate the old review before reevaluation. If the human approves a scientific change outside the predefined verified-parameter procedure, route Work to a new versioned TODO and initialize its lifecycle at `todo_ready`; do not synchronize the changed scientific content into the active task.

### Pending transition review

When `transition_review.status` is `awaiting_human`:

- if the human explicitly selects an eligible rule ID and target, route to `$research-state-transition` Apply;
- if the human names only a target, resolve it only when exactly one eligible rule reaches that target;
- if the human asks for explanation or comparison, route to `$human-research-review-gate` without changing state;
- otherwise block execution and request one eligible rule path.

Do not rerun the current state while a transition decision is pending unless the human first confirms the self-transition rule.

### Evaluation-required state

When `current.status` is `awaiting_transition_evaluation` or `transition_review.status` is `evaluation_required`:

- route to `$research-state-transition` Evaluate before any execution, Work action, or transition application;
- exception: when an authorized TODO path edit or a complete evidence-backed Work parameter rewrite has not yet been synchronized, route first to `$research-state-transition` Synchronize TODO; a parameter rewrite routes through `$research-report-to-todos` before synchronization. Only then Evaluate;
- require `execution.decision_boundary_reached: true`, except for `todo_ready`;
- do not ask the human to choose a path until Codex has recorded the complete eligible rule set and one recommendation.

### Ready state

When `current.status` is `ready`:

- route a Codex-owned state to `$research-todo-executor` only when the human requests execution of the recorded current state;
- route `work_postprocessing` to Work table curation and figure planning/drafts;
- route `figure_review` to the human gate and stop until the researcher supplies recommendations;
- route `figure_production` to final figure production and integrity QA;
- do not execute terminal states.

If the human names a target different from `current.state`, require a recorded eligible transition and explicit confirmation before routing execution.

### Running or blocked state

- Resume a running state only when the request matches the same state and resume contract.
- For a blocked state, route to the blocker-specific Skill or human gate; do not silently change state.

## Select the minimum capability set

For Codex state execution, add only capabilities required by the TODO and current state:

- `$research-computing-implementation` for MATLAB-first non-plotting code, a documented Python-only exception, Python plotting, numerical optimization, parallel/GPU execution, or storage-boundary changes.
- `$research-agile-testing` for formulas, data semantics, controls, metrics, randomness, recovery, or implementation behavior.
- `$research-evidence-aggregation` for repeated metrics, complete run tables, aggregate tables, or condition-merged tables.
- `$research-batch-execution` for multiple recoverable units, material I/O, checkpoint/resume, concurrency, or long runtime.
- `$research-state-transition` after the state reaches a decision boundary.
- `$human-research-review-gate` for a pending transition, semantic change, long-run launch, completion, stop, or redesign.

Do not load every Skill preemptively. Preserve causal order:

```text
state resolution
→ state execution
→ risk-matched testing
→ formal execution when applicable
→ aggregation
→ evidence-backed human hyperparameter selection and Work TODO rewrite when defined
→ TODO fingerprint synchronization
→ transition rule evaluation
→ human confirmation
→ transition application
```

For Work:

```text
work_postprocessing state
→ publication-table-curation
→ research-figure-production Planning mode
→ mark the planning decision boundary
→ Codex research-state-transition Evaluate
→ human confirmation of figure_review
→ figure_review state
→ present drafts and coverage of all applicable data
→ wait for researcher recommendations
→ mark the review decision boundary
→ Codex research-state-transition Evaluate
→ human confirmation of figure_production
→ research-figure-production Final mode
→ figure integrity and traceability audit
→ mark the final-production decision boundary
→ Codex research-state-transition Evaluate
→ human confirmation of completion or rework
```

## Routing gates

Check in order:

1. **Authority gate:** Is the human authorizing execution, transition application, semantic change, or long-run launch as required?
2. **TODO gate:** Does the TODO define only the current scientific action without invention, status history, rejected candidates, or obsolete-design prose? Are experimentally selected fixed values verified and approved?
3. **State gate:** Does the task-state file exist, match the TODO identifier and SHA-256 fingerprint, and permit this action at its current revision?
4. **Transition gate:** Is the exact rule path recorded as eligible and explicitly confirmed?
5. **Scope gate:** Is the work inside the TODO rather than a hidden new scientific question?
6. **Artifact gate:** Are the implementation inputs or result paths required by the selected Skill available? For Work table or figure routes, does a passing `aggregation-validation.json` trace to the controlling sources and TODO fingerprint?
7. **Integrity gate:** Are failed results, complete combinations, independent repeats, predefined metrics, analysis grain, stable keys, source hashes, and applicable join or denominator checks preserved?
8. **I/O gate:** Does execution avoid row-at-a-time scientific result writes?
9. **Figure-stage gate:** Is the requested action planning, researcher review, or final production, and does it match `current.state`?
10. **Communication gate:** Are established technical terms used, local labels defined operationally, and evaluative claims tied to explicit evidence?

If any gate fails, return a blocking diagnosis instead of invoking an execution Skill.

## Output contract

Return:

1. `classification`;
2. `resolved_todo`;
3. `resolved_state_file`;
4. `todo_fingerprint_match` and authorized change class when applicable;
5. `state_revision`;
6. `current_state` and status;
7. `execution_status` and `decision_boundary_reached`;
8. `transition_review_status`;
9. `requested_action`;
10. `selected_skills` in call order;
11. `excluded_skills` most likely to be confused with the route;
12. `blocking_issues`;
13. `route_result`: `ready`, `blocked`, or `no_system_route`;
14. `next_action`.

## Hard rules

- Do not infer the current state from old chat text or result-directory contents.
- Do not apply a transition during evaluation.
- Do not treat a Codex recommendation as human approval.
- Do not execute a newly applied state unless the human explicitly authorizes execution.
- Do not omit the self-transition rule from a pending state decision.
- Do not create a parallel scientific handoff document.
- Do not route Work figure production to Codex experiment execution.
- Do not route final figure production directly from `work_postprocessing`; `figure_review` and its recorded output are mandatory.
- Do not treat a generalized schematic as a substitute for complete quantitative figures.
- Do not route Codex aggregation to Work table curation.
- Do not route derived tables to Work curation or figure production when controlling sources conflict or `aggregation-validation.json` has a blocking failure.
- Do not let a figure notebook become the only implementation of production preprocessing, metrics, statistical tests, model fitting, exclusions, or aggregation.
- Do not allow row-wise CSV updates, repeated DataFrame concatenation in result loops, or per-row MATLAB `writetable` calls.
- Do not route unexplained TODO edits past the fingerprint gate or reuse a transition review after a TODO rewrite.
- Do not route a broader approved scientific redesign through Synchronize TODO; create a new versioned TODO and initialize it at `todo_ready`.
- Do not route non-plotting Python merely for convenience; require the computing Skill's documented exception.
- Do not coin terminology when an established technical term or a concrete sequence of operations is clearer.
