# Task-State File Contract

## Authority and location

Store task state at `TODO_###/task-state.yaml` beside `TODO.md`. The TODO owns scientific meaning, the shared state machine owns rule definitions, task state owns current lifecycle facts, and the current researcher instruction owns approval.

## Fingerprints and revisions

Hash the complete TODO bytes with SHA-256. Store the current state-machine `rule_set_version`. A synchronized TODO change increments revision, records prior/current fingerprints and evidence, invalidates a pending decision, and prepares fresh rules when the stage is at a boundary.

Rule-set migration preserves the prior state and evidence unless that state no longer exists. Version 6 maps the removed `exploration` state to `todo_ready`, records the migration, and retains valid probe references.

Version 7 preserves all states and execution artifacts and adds statistical evidence to four existing predicates. Apply migrations in source-to-target version order (5 to 6 to 7 when needed), independent of their list order. In one atomic update, increment task-state revision, store the new rule-set version, record the migration in history, and invalidate the pending review, eligible paths, and recommendation. Clear each `invalidate_predicate_results` entry to `unknown` in current execution evidence; retain its historical evidence for re-evaluation. At an executable boundary, recompute affected predicates and all outgoing rules before accepting a decision. Historical approvals and terminal states stay recorded; migration neither reopens a terminal task nor retroactively certifies its statistics. The TODO and fingerprint change only through their existing revision procedure.

Version 8 uses the same atomic migration procedure for its listed predicates, preserving evidence and terminal states. Re-evaluate problem/metric alignment, framework-validation readiness, and figure-audit evidence; do not fabricate retrospective design approval or visual inspection. Apply the full migration chain to the current rule-set version.

Before governed figures are presented, an approved scientific change can synchronize in place. After the presentation milestone, a scientific change creates a new versioned TODO based on the current implementation. Path-only changes remain in place.

## Status

`current.status` uses `ready`, `running`, `awaiting_human_transition`, `blocked`, or `terminal`.

`execution.status` uses `not_started`, `running`, `completed`, `partial`, `failed`, or `blocked`.

`transition_review.status` uses `not_prepared` or `awaiting_human`. `todo_ready` includes bounded exploration and initial decision preparation; there is no separate Exploration, Evaluate stage, or `evaluation_required` status.

`milestones.governed_figures_presented_at` and its reference define the TODO-versioning boundary.

## Predicate and eligibility records

Store only `true`, `false`, or `unknown` with evidence references. Every self-transition is eligible. A non-self rule requires every `all` predicate true, one `any` predicate true when present, and every `none` predicate false.

Record every outgoing rule, explicit eligible paths, unique targets, blockers, and exactly one recommendation. Keep researcher figure feedback as an external reference rather than narrative in task state.

## Confirmation and execution

The researcher selects an exact eligible rule ID. A target-only reply is valid only when one eligible rule reaches that target. Confirmation appends the decision snapshot, updates `current.state`, resets execution, writes the YAML atomically, and immediately begins the target. Terminal targets only update state.

## Atomic update

Construct the complete next YAML in memory, write a sibling temporary file, parse and verify it, then atomically replace the prior file. Preserve prior history entries unchanged.
