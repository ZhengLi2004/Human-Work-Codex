# Task-State File Contract

## Contents

- [Location](#location)
- [Authority](#authority)
- [Rule-set version](#rule-set-version)
- [TODO fingerprint](#todo-fingerprint)
- [TODO change events](#todo-change-events)
- [Status values](#status-values)
- [Predicate results](#predicate-results)
- [Eligibility truth model](#eligibility-truth-model)
- [Evaluated rules and eligible transitions](#evaluated-rules-and-eligible-transitions)
- [Human selection](#human-selection)
- [Atomic update](#atomic-update)
- [Transition history](#transition-history)

## Location

Use the policy path pattern, normally:

```text
results/{todo_id}/task-state.yaml
```

The path is derived from the TODO identifier and result root. Do not add a task-state path field to the TODO.

## Authority

- The TODO is authoritative for scientific meaning.
- The shared state machine is authoritative for allowed lifecycle rules.
- The task-state file is authoritative for the current machine lifecycle state and confirmed transition history.
- The current human instruction is authoritative for approval.

A state file never overrides the TODO.

## Rule-set version

The task-state file stores `state_machine_rule_set_version`. Every evaluation also stores `transition_review.based_on_rule_set_version`.

- Increment `rule_set_version` in the shared state machine whenever predicate semantics, eligibility logic, or transition rules change.
- Do not apply a pending review when its rule-set version differs from the current shared version.
- Evaluate mode may adopt the current version only by clearing any stale pending review and recomputing every outgoing rule. Apply mode never adopts a new version implicitly.

## TODO fingerprint

Store the SHA-256 digest of the complete TODO bytes:

```yaml
todo_fingerprint:
  algorithm: sha256
  value: 0123456789abcdef...
  synchronized_at: 2026-07-28T12:00:00+08:00
```

Every evaluation stores the same digest in `transition_review.based_on_todo_fingerprint`. Recompute it before Evaluate and Apply. A mismatch invalidates the pending review and blocks transition application; do not silently accept an edited scientific contract.

## TODO change events

Every authorized edit changes the complete-file digest. Codex increments state revision, refreshes the fingerprint, and records machine metadata for either an Output References path update or a verified-parameter rewrite. Path changes may be batched before transition evaluation and do not require scientific approval. A verified-parameter rewrite requires complete evidence, explicit researcher selection, and Work authorship at a decision boundary.

An unexplained mismatch is not an authorized edit. If it is rejected, restore the exact approved TODO bytes from version control or another researcher-verified source; the stored hash alone cannot reconstruct content. Then increment revision and append a `rejected_unapproved_edit_restoration` event with the observed mismatching digest. This makes the old review stale even though the restored digest equals the stored approved digest. If exact restoration is unavailable, remain blocked. Any approved scientific change outside the predefined verified-parameter rule starts a new versioned TODO and a new task-state file at `todo_ready`.

```yaml
todo_change_events:
  - state_revision: 2
    change_type: output_reference_path_update
    prior_fingerprint: 123456...
    current_fingerprint: abcdef...
    changed_by: codex
    approval_ref: null
    evidence_refs:
      - results/TODO-004/tables/condition-merged.parquet
    changed_at: 2026-07-28T11:50:00+08:00
  - state_revision: 3
    change_type: verified_hyperparameter_selection
    prior_fingerprint: abcdef...
    current_fingerprint: 012345...
    changed_by: work
    approval_ref: conversation-2026-07-28
    evidence_refs:
      - results/TODO-004/tables/pilot-parameter-selection.parquet
      - results/TODO-004/pilot/selection-rule.json
    changed_at: 2026-07-28T12:00:00+08:00
  - state_revision: 4
    change_type: rejected_unapproved_edit_restoration
    prior_fingerprint: 012345...
    current_fingerprint: 012345...
    observed_unapproved_fingerprint: fedcba...
    changed_by: codex
    approval_ref: conversation-2026-07-28-reject-edit
    evidence_refs:
      - conversation:metric-edit-rejected-2026-07-28
    changed_at: 2026-07-28T12:10:00+08:00
```

Each event proves edit scope and traceability without duplicating TODO values. Rejected candidates, obsolete designs, and comparison narrative stay in immutable technical evidence, not in the rewritten TODO or this event. Clear any prior review and evaluate again against the new fingerprint.

## Status values

`current.status`:

- `ready`
- `running`
- `awaiting_transition_evaluation`
- `awaiting_human_transition`
- `blocked`
- `terminal`

`execution.status`:

- `not_started`
- `running`
- `completed`
- `partial`
- `failed`
- `blocked`

`execution.decision_boundary_reached`:

- `false` while the current execution must resume before lifecycle rules are evaluated;
- `true` when the current attempt has produced enough auditable evidence to evaluate every outgoing rule, even if the attempt is partial, failed, or blocked.

A restricted long-run launch gate normally leaves this field `false` because the state itself has not ended.

`transition_review.status`:

- `not_evaluated`
- `evaluation_required`
- `awaiting_human`

After a state reaches a decision boundary, set `transition_review.status: evaluation_required`. Codex changes it to `awaiting_human` only after evaluating the shared rules.

## Predicate results

Store each predicate under `execution.predicate_results`:

```yaml
predicate_results:
  implementation_matches_todo:
    value: true
    evidence_refs:
      - results/TODO-004/tests/scientific-contract.json
  no_critical_correctness_risk:
    value: unknown
    evidence_refs:
      - results/TODO-004/logs/open-risk.txt
```

Use `unknown` when evidence is absent, incomplete, or conflicting. Never treat missing evidence as proof of `false` or `true`.

For `figure_review`, reference the researcher's interactive output rather than copying its narrative into task state. For example:

```yaml
predicate_results:
  figure_recommendations_recorded:
    value: true
    evidence_refs:
      - conversation:figure-review-2026-07-19
  figure_recommendations_within_scope:
    value: true
    evidence_refs:
      - results/TODO-004/figures/figure-plan.json
      - conversation:figure-review-2026-07-19
```

The final figure notebook may consume the referenced output, but the task-state YAML stores only the predicate values and references.

For transition eligibility, an `unknown` in an `all`, unresolved `any`, or `none` clause makes the non-self rule ineligible. In particular, `unknown` in a `none` clause is not treated as `false`.

## Eligibility truth model

For a non-self rule:

- every predicate in `all` must be `true`;
- at least one predicate in `any` must be explicitly `true` when the clause is present;
- every predicate in `none` must be explicitly `false`;
- `unknown` never makes the rule eligible.

The exact self-transition remains eligible by definition.

## Evaluated rules and eligible transitions

Record every outgoing rule:

```yaml
evaluated_rules:
  - rule_id: development.self
    from: development
    target: development
    kind: self
    eligibility: eligible
    predicate_values: {}
    evidence_refs: []
  - rule_id: development.to_pilot
    from: development
    target: pilot
    kind: forward
    eligibility: ineligible
    predicate_values:
      implementation_matches_todo: true
      smoke_test_passed: false
    evidence_refs:
      - results/TODO-004/tests/smoke-test.json
```

Store the eligible paths explicitly:

```yaml
eligible_transitions:
  - rule_id: development.self
    from: development
    to: development
    kind: self
  - rule_id: development.to_pilot
    from: development
    to: pilot
    kind: forward
eligible_targets:
  - development
  - pilot
```

`eligible_targets` is a convenience index derived from `eligible_transitions`. It must contain unique state names. Every state defined by the shared state machine has an eligible self-transition.

## Human selection

The preferred approval form names the exact rule and target:

```text
Approve development.to_pilot (Development → Pilot).
```

A target-only instruction may be accepted only when exactly one eligible rule reaches that target. Otherwise block and ask for the exact `rule_id`.

The approval is read from the current interaction and persisted only when Apply mode atomically appends the transition history and updates state. Do not maintain a separate mutable approval field.

## Atomic update

For every write:

1. read the current revision and current shared rule-set version;
2. construct the complete next YAML in memory;
3. write a sibling temporary file;
4. read it back and verify required keys, revision, rule-set version, TODO fingerprint, and, when applicable, rule ID and selected-target consistency;
5. rename it atomically over the prior state file;
6. never perform row-wise or partial in-place YAML edits.

## Transition history

Append one history entry only after human approval. Preserve the logical basis of the decision, not merely the source and target:

```yaml
history:
  - revision: 1
    rule_set_version: 4
    from: development
    to: pilot
    rule_id: development.to_pilot
    approved_by: human
    approval_ref: conversation-2026-07-16
    decided_at: 2026-07-16T10:20:00-07:00
    evaluation_snapshot:
      todo_fingerprint: 0123456789abcdef...
      execution_id: development-001
      execution_status: completed
      predicate_results:
        implementation_matches_todo:
          value: true
          evidence_refs:
            - results/TODO-004/tests/scientific-contract.json
      evaluated_rules:
        - rule_id: development.self
          eligibility: eligible
        - rule_id: development.to_pilot
          eligibility: eligible
      eligible_transitions:
        - rule_id: development.self
          from: development
          to: development
          kind: self
        - rule_id: development.to_pilot
          from: development
          to: pilot
          kind: forward
      blockers: []
      codex_recommendation:
        target: pilot
        rule_id: development.to_pilot
        confidence: high
      evidence_refs:
        - results/TODO-004/development/manifest.json
```

Do not delete or rewrite prior history entries. Corrections require a new revision and an explicit human decision.
