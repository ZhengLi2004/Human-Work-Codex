# Task-State File Contract

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
4. read it back and verify required keys, revision, rule-set version, rule ID, and selected target consistency;
5. rename it atomically over the prior state file;
6. never perform row-wise or partial in-place YAML edits.

## Transition history

Append one history entry only after human approval. Preserve the logical basis of the decision, not merely the source and target:

```yaml
history:
  - revision: 1
    rule_set_version: 2
    from: development
    to: pilot
    rule_id: development.to_pilot
    approved_by: human
    approval_ref: conversation-2026-07-16
    decided_at: 2026-07-16T10:20:00-07:00
    evaluation_snapshot:
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
