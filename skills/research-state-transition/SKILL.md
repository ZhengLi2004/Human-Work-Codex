---
name: research-state-transition
description: Initialize, synchronize, evaluate, or apply rule-based lifecycle control for a research TODO using its SHA-256 fingerprint, task-state YAML, and shared state-machine rules. Use after an authorized Output References path edit, after an approved verified-parameter TODO rewrite, after an executable state reaches a decision boundary, or when the human confirms an eligible rule path. Do not execute a next state or change current.state without explicit human approval.
---

# Research State Transition

## Objective

Maintain durable task lifecycle state without duplicating the TODO. Evaluate every outgoing rule after the current state, include the explicit self-transition, recommend one eligible rule path, and leave the current state unchanged until the human confirms a path.

Read `references/state-file-contract.md` before editing a task-state file.

## Modes

Use exactly one mode:

- **Initialize**: create the task-state file from the template when none exists.
- **Synchronize TODO**: record an authorized Output References path edit, an approved Work rewrite after verified parameter selection, or exact restoration after rejecting an unapproved edit; invalidate stale transition evaluation.
- **Evaluate**: evaluate outgoing transition rules after the current state reaches a decision boundary.
- **Apply**: apply one explicitly human-confirmed eligible rule path.

Do not combine Evaluate and Apply unless the human's current instruction explicitly selects the rule path and authorizes applying it. Do not execute the target state unless the same instruction also explicitly authorizes execution.

## Artifact resolution

1. Resolve the TODO and extract its stable identifier from the heading.
2. Resolve the result root from the TODO when present; otherwise use `.research/policy.yaml`.
3. Resolve the task-state file as `results/{todo_id}/task-state.yaml` unless policy specifies another path.
4. Read `.research/workflow/state-machine.yaml` and its `rule_set_version`.
5. Treat the TODO as the scientific contract and the task-state YAML as machine lifecycle control only.
6. Compute the SHA-256 digest from the complete TODO bytes; do not normalize, omit, or reorder content before hashing.

## Initialize mode

1. Verify that the TODO exists and has a stable identifier.
2. Create the result root if needed.
3. Copy the state template and replace `todo_id` and `todo_path`.
4. Store the shared state machine's `rule_set_version` as `state_machine_rule_set_version`.
5. Store the TODO digest and synchronization time under `todo_fingerprint`.
6. Set `current.state` and `execution.state` to `todo_ready`.
7. Set `revision` to `0`, `current.status` to `ready`, and `current.approved_by` to `system_initialization`.
8. Do not infer the first executable state.
9. End Initialize, then use a separate Evaluate operation for `todo_ready` when the human asks to see initial paths. Apply one only after explicit approval.

## Synchronize TODO mode

Use this mode only for one of three governed cases:

- **Output References path update:** Codex or Work changed only existing path values allowed by governance. Verify the Markdown diff is limited to those values, reference the created artifacts, and synchronize the authorized path change.
- **Verified hyperparameter selection:** at a lifecycle decision boundary, complete candidate, failure, selection-rule, and result evidence exists; the researcher explicitly approved the selected value; and Work rewrote the scientific TODO.
- **Rejected unapproved edit restoration:** an unexplained fingerprint mismatch was detected, the edit was rejected, and the exact previously approved TODO bytes were restored from version control or another researcher-verified source. A hash supplies identity only; restoration requires the exact approved bytes. Record the observed mismatching digest and the rejection/restoration evidence; do not adopt the unapproved digest.

For a verified-parameter rewrite, verify that the TODO fixes the approved value, contains only remaining actions, and omits completed selection instructions, rejected candidates, obsolete designs, progress prose, and old-versus-new comparisons. Reject the mode if the change exceeds the predefined selection rule or changes another scientific definition; route that case to the semantic-change procedure.

For any other approved scientific change, do not synchronize the changed content into the active TODO. If it was written over the old file, treat that in-place mutation as rejected for the old task, restore and record it through the restoration case, and approve the scientific content only for a new versioned TODO. Preserve the old task's state and evidence, have Work author the new TODO with a new stable identifier, and initialize that task at `todo_ready`.

Then:

1. Compute the current SHA-256 digest. Require it to differ from the stored digest for an authorized path or parameter change. For a rejected edit, require the restored digest to equal the stored digest and require the separately recorded observed mismatch digest to differ.
2. Increment `revision` and append a `todo_change_events` entry containing the new state revision, `change_type`, prior and current approved fingerprints, actor, timestamp, and evidence references. For verified selection, also include the approval reference; for a rejected edit, include `observed_unapproved_fingerprint`. Do not duplicate scientific values in task state.
3. Store the current approved fingerprint and synchronization time. Preserve `current.state` and existing execution evidence.
4. Clear evaluated rules, eligible paths, blockers, and recommendation; set `based_on_revision` to the new revision, `based_on_rule_set_version` and `based_on_todo_fingerprint` to null, and `from_state` to `current.state`.
5. If `execution.decision_boundary_reached` is true, set `transition_review.status: evaluation_required` and `current.status: awaiting_transition_evaluation`. Otherwise set the review to `not_evaluated` and preserve the valid running, ready, or blocked current status.
6. Write the complete task-state YAML atomically.
7. At a decision boundary, end this mode and invoke a separate fresh Evaluate operation. Never apply a rule path evaluated from the prior fingerprint.

## Evaluate mode

1. Verify that the file revision, TODO identity, `current.state`, and `execution.state` are internally consistent and that the current TODO digest matches `todo_fingerprint.value`. An unexplained mismatch blocks evaluation. Reject and restore it through Synchronize TODO before reevaluation, or create a new versioned TODO after an approved scientific redesign; never adopt the changed digest directly.
2. Compare `state_machine_rule_set_version` with the current shared `rule_set_version`. If they differ, discard any stale pending review, update the stored version, and perform a fresh evaluation. Never reuse eligibility computed under an older rule set.
3. For `todo_ready`, evaluate directly. For every other executable state, require `execution.decision_boundary_reached: true` and `transition_review.status` equal to `evaluation_required` or `not_evaluated`.
4. Collect predicate evidence from the TODO, commands, tests, manifests, logs, raw outputs, complete tables, Work artifacts, the referenced researcher figure-review output, and the current execution record as applicable.
5. Record every predicate used by an outgoing rule as `true`, `false`, or `unknown` with evidence references. Do not convert missing evidence into `false`.
6. Evaluate every outgoing rule for `current.state` using the shared truth model.
7. Include the exact self-transition rule as eligible, including for terminal states.
8. Mark a non-self rule eligible only when every `all` predicate is true, at least one `any` predicate is explicitly true when that clause is present, and every `none` predicate is explicitly false. Unknown evidence never satisfies a non-self rule.
9. Record all evaluated rules, explicit `eligible_transitions`, derived unique `eligible_targets`, blockers, and evidence references in `transition_review`. Set `based_on_revision` to the current revision, `based_on_rule_set_version` to the current rule-set version, `based_on_todo_fingerprint` to the current digest, and `from_state` to `current.state`.
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
3. Recompute the TODO digest and verify that `transition_review.based_on_revision` equals the current `revision`, `transition_review.based_on_rule_set_version` equals the current shared rule-set version, `transition_review.based_on_todo_fingerprint` equals both the stored and recomputed digest, and `from_state` still equals `current.state`.
4. Resolve the selected path by exact `rule_id`. Accept a target-only instruction only when exactly one eligible rule reaches that target.
5. Verify that the selected rule ID and target match one entry in `eligible_transitions`.
6. If the selected path is ineligible or ambiguous, block and state the missing, contradicted, or ambiguous conditions. Do not force the transition.
7. Append a history entry containing the new revision, from, to, rule ID, human approval reference, decision time, and an immutable evaluation snapshot: TODO fingerprint, execution identity/status, predicate results, evaluated rules, eligible transitions, blockers, Codex recommendation, and evidence references.
8. Increment `revision` by one.
9. Set `current.state` to the approved target, set `current.status` to `terminal` for terminal states or `ready` otherwise, and update `entered_at`, `approved_by`, and `approval_ref`.
10. Reset `execution` for a new pass in the target state, including when the target equals the source state: set the target state, `not_started`, `decision_boundary_reached: false`, null timestamps/identifier, and empty artifact/predicate collections.
11. Reset `transition_review` to `not_evaluated`, set `based_on_revision` to the new revision and `from_state` to the target, clear `based_on_rule_set_version`, `based_on_todo_fingerprint`, rules, paths, blockers, and recommendation, and preserve the prior decision only in history.
12. Write the complete YAML to a temporary file, verify it can be read back, then atomically replace the state file.
13. Return to `$research-task-router`. Execute the new state only when the human explicitly authorized both transition and execution.

## Write boundaries

The task-state file may contain only:

- lifecycle state and execution status;
- rule predicate values and evidence references;
- evaluated rules, eligible rule paths, and the Codex recommendation;
- explicit human transition decisions;
- TODO fingerprint and authorized TODO change event references;
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
- `todo_fingerprint`;
- `eligible_transitions` with rule IDs, source, target, and kind;
- `recommended_transition` with rule ID and target;
- `blockers`;
- `human_decision_required`;
- `state_changed`: `true` or `false`;
- `next_action`.

## Hard rules

- Evaluation never changes `current.state`.
- Every state evaluation includes an eligible self-transition.
- Require explicit human approval after making a recommendation.
- Only an explicit human decision applies a transition.
- A pending evaluation must not be applied after its rule-set version, state revision, or TODO fingerprint changes; evaluate it again.
- Never synchronize an unexplained TODO edit as an authorized path update or approved verified-parameter rewrite; only a verified exact restoration may record and invalidate it.
- Never synchronize a broader approved scientific redesign into the active task; initialize a new versioned TODO at `todo_ready`.
- Do not execute a newly approved state unless execution is also explicitly authorized.
- Do not use the task-state YAML as a second scientific handoff document.
- Do not skip the `figure_review` state or infer researcher figure preferences from silence.
- Use established technical terms in predicate rationales; describe concrete operations instead of inventing labels.
