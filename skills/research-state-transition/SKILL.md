---
name: research-state-transition
description: Initialize, synchronize, prepare, or atomically execute a fingerprinted research lifecycle decision.
---

# Research State Transition

Keep lifecycle control in task-state YAML. Read `references/state-file-contract.md` before editing it.

## Initialize and prepare

Create `task-state.yaml` beside the TODO with the current rule set, complete TODO SHA-256, and `todo_ready`. Resolve bounded mapping, data meaning, and feasibility through `$research-task-router`, then prepare every outgoing rule including self.

## Synchronize TODO

Classify the change as a path update, approved pre-figure revision, verified-parameter rewrite, exact restoration, or post-presentation versioned TODO. For an in-place change, verify authority, refresh the digest/revision, record fingerprints and evidence, invalidate stale review, prepare fresh rules at a boundary, and replace YAML atomically.

Apply migrations exactly as defined in the state machine and file contract before another operation.

## Prepare a stage decision

Verify the revision, state, rule set, fingerprint, and boundary. Record evidence-backed predicates, evaluate every outgoing rule, store eligible paths and blockers, recommend exactly one, and request one rule ID. Self is always eligible; unknown cannot satisfy a non-self rule.

## Confirm and execute

Recheck the selected eligible rule against revision, rule set, fingerprint, and source state. Append the decision snapshot, update target and execution state atomically, then begin the target through `$research-task-router`; terminal targets only update state.

## Output

Return the operation, paths, revision, state, rule set, fingerprint, eligible paths, recommendation, blockers, state change, and action begun.
