---
name: research-state-transition
description: Evaluate or apply rule-based lifecycle transitions for a research TODO using its task-state YAML and the shared state-machine rules. Use after any executable state reaches a decision boundary, when initializing state, or when the human confirms an eligible rule path. Do not execute a next state or change current.state without explicit human approval.
---

# Research State Transition

## Objective

Maintain durable task lifecycle state without duplicating the TODO. Evaluate every outgoing rule after the current state, include the explicit self-transition, recommend one eligible rule path, and leave the current state unchanged until the human confirms a path.

Read `references/state-file-contract.md` before editing a task-state file.

## Modes

Use exactly one mode:

- **Initialize**: create the task-state file from the template when none exists.
- **Evaluate**: evaluate outgoing transition rules after the current state reaches a decision boundary.
- **Apply**: apply one explicitly human-confirmed eligible rule path.

Do not combine Evaluate and Apply unless the human's current instruction explicitly selects the rule path and authorizes applying it. Do not execute the target state unless the same instruction also explicitly authorizes execution.

## Artifact resolution

1. Resolve the TODO and extract its stable identifier from the heading.
2. Resolve the result root from the TODO when present; otherwise use `.research/policy.yaml`.
3. Resolve the task-state file as `results/{todo_id}/task-state.yaml` unless policy specifies another path.
4. Read `.research/workflow/state-machine.yaml` and its `rule_set_version`.
5. Treat the TODO as the scientific contract and the task-state YAML as machine lifecycle control only.

## Initialize mode

1. Verify that the TODO exists and has a stable identifier.
2. Create the result root if needed.
3. Copy the state template and replace `todo_id` and `todo_path`.
4. Store the shared state machine's `rule_set_version` as `state_machine_rule_set_version`.
5. Set `current.state` and `execution.state` to `todo_ready`.
6. Set `revision` to `0`, `current.status` to `ready`, and `current.approved_by` to `system_initialization`.
7. Do not infer the first executable state.
8. Continue in Evaluate mode for `todo_ready` when the human asks to see initial paths. Apply one only after explicit approval.

## Evaluate mode

1. Verify that the file revision, TODO identity, `current.state`, and `execution.state` are internally consistent.
2. Compare `state_machine_rule_set_version` with the current shared `rule_set_version`. If they differ, discard any stale pending review, update the stored version, and perform a fresh evaluation. Never reuse eligibility computed under an older rule set.
3. For `todo_ready`, evaluate directly. For every other executable state, require `execution.decision_boundary_reached: true` and `transition_review.status` equal to `evaluation_required` or `not_evaluated`.
4. Collect predicate evidence from the TODO, commands, tests, manifests, logs, raw outputs, complete tables, Work artifacts, the referenced researcher figure-review output, and the current execution record as applicable.
5. Record every predicate used by an outgoing rule as `true`, `false`, or `unknown` with evidence references. Do not convert missing evidence into `false`.
6. Evaluate every outgoing rule for `current.state` using the shared truth model.
7. Include the exact self-transition rule as eligible, including for terminal states.
8. Mark a non-self rule eligible only when every `all` predicate is true, at least one `any` predicate is explicitly true when that clause is present, and every `none` predicate is explicitly false. Unknown evidence never satisfies a non-self rule.
9. Record all evaluated rules, explicit `eligible_transitions`, derived unique `eligible_targets`, blockers, and evidence references in `transition_review`. Set `based_on_revision` to the current revision, `based_on_rule_set_version` to the current rule-set version, and `from_state` to `current.state`.
10. Evaluate each eligible rule's optional `recommend_when` clause using the same truth model. Treat it as recommendation evidence, not as eligibility.
11. Select exactly one Codex recommendation identified by both `rule_id` and target. Prefer scientific validity and the smallest sufficient next scope over speed or a favorable result direction; prefer self when non-self evidence is unknown or materially conflicting.
12. Write the recommendation with a concise rationale, confidence level, and evidence references.
13. Set `transition_review.status` to `awaiting_human` and `current.status` to `awaiting_human_transition`.
14. Do not change `current.state` or append transition history.
15. Invoke `$human-research-review-gate` with the complete eligible rule-path set, including self.

## Recommendation policy

Recommend:

- the self-transition when current-state work remains, evidence is incomplete, or no non-self rule is eligible;
- a backward transition when a reproducible correctness, mapping, or implementation defect requires it;
- a forward transition only when every entry predicate is supported;
- `work_postprocessing` only when complete Codex outputs satisfy the Work input contract;
- `figure_review` only after curated tables, drafts covering all applicable data, graphical-method basis, and source coverage are ready;
- `figure_production` only after explicit in-scope researcher recommendations are recorded;
- `completed` only from `figure_production`, after final tables and figures are complete, traceable, and pass the integrity audit;
- `stopped` only when stopping is warranted and human confirmation is required.

Do not recommend a new state merely because its result would be desirable.

## Apply mode

1. Require an explicit human selection in the current interaction.
2. Verify that `transition_review.status` is `awaiting_human`.
3. Verify that `transition_review.based_on_revision` equals the current `revision`, `transition_review.based_on_rule_set_version` equals the current shared rule-set version, and `from_state` still equals `current.state`.
4. Resolve the selected path by exact `rule_id`. Accept a target-only instruction only when exactly one eligible rule reaches that target.
5. Verify that the selected rule ID and target match one entry in `eligible_transitions`.
6. If the selected path is ineligible or ambiguous, block and state the missing, contradicted, or ambiguous conditions. Do not force the transition.
7. Append a history entry containing the new revision, from, to, rule ID, human approval reference, decision time, and an immutable evaluation snapshot: execution identity/status, predicate results, evaluated rules, eligible transitions, blockers, Codex recommendation, and evidence references.
8. Increment `revision` by one.
9. Set `current.state` to the approved target, set `current.status` to `terminal` for terminal states or `ready` otherwise, and update `entered_at`, `approved_by`, and `approval_ref`.
10. Reset `execution` for a new pass in the target state, including when the target equals the source state: set the target state, `not_started`, `decision_boundary_reached: false`, null timestamps/identifier, and empty artifact/predicate collections.
11. Reset `transition_review` to `not_evaluated`, set `based_on_revision` to the new revision and `from_state` to the target, clear `based_on_rule_set_version`, rules, paths, blockers, and recommendation, and preserve the prior decision only in history.
12. Write the complete YAML to a temporary file, verify it can be read back, then atomically replace the state file.
13. Return to `$research-task-router`. Execute the new state only when the human explicitly authorized both transition and execution.

## Write boundaries

The task-state file may contain only:

- lifecycle state and execution status;
- rule predicate values and evidence references;
- evaluated rules, eligible rule paths, and the Codex recommendation;
- explicit human transition decisions;
- revision and transition history.

Do not copy formulas, research background, result prose, tables, scientific interpretations, or TODO sections into the state file.

## Output contract

Return:

- `mode`;
- `todo`;
- `state_file`;
- `revision`;
- `current_state`;
- `rule_set_version`;
- `eligible_transitions` with rule IDs, source, target, and kind;
- `recommended_transition` with rule ID and target;
- `blockers`;
- `human_decision_required`;
- `state_changed`: `true` or `false`;
- `next_action`.

## Hard rules

- Evaluation never changes `current.state`.
- Every state evaluation includes an eligible self-transition.
- A recommendation is not approval.
- Only an explicit human decision applies a transition.
- A pending evaluation cannot be applied after its rule-set version or state revision changes; it must be evaluated again.
- Do not execute a newly approved state unless execution is also explicitly authorized.
- Do not use the task-state YAML as a second scientific handoff document.
- Do not skip the `figure_review` state or infer researcher figure preferences from silence.
- Use established technical terms in predicate rationales; describe concrete operations instead of inventing labels.
