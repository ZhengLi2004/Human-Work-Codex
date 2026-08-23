---
name: research-task-router
description: Route a TODO through its recorded research lifecycle. Use for TODO changes, stage execution, lifecycle decisions, figures, aggregation, or post-report assessment.
---

# Research Task Router

Resolve `TODO_###/TODO.md`, sibling task state, current instruction, and fingerprint. Read repository governance before routing; initialize missing state through `$research-state-transition`. Require `exp/` and `data/`; `code/` is optional.

## Routes

| Request or state | Skill |
|---|---|
| Author or revise a TODO | `$research-report-to-todos` |
| Initialize, synchronize, prepare, or confirm lifecycle state | `$research-state-transition` |
| `todo_ready` | Resolve bounded project/data questions, then `$research-state-transition` Prepare |
| `development` | `$research-development` |
| `pilot` | `$research-pilot` |
| `confirmation` | `$research-confirmation` |
| `ablation_diagnosis` | `$research-ablation-diagnosis` |
| `figure_review` | `$research-figure-production` Planning, then `$human-research-review-gate` |
| `figure_production` | `$research-figure-production` Final |
| Aggregate results | `$research-evidence-aggregation` |
| Assess a human report | `$post-report-assessment` |

Add capability Skills only when the selected stage needs them.

## `todo_ready`

Resolve project mappings, data meaning, and feasibility from valid evidence or the smallest decisive probe. Record the resolved/unresolved predicate with evidence and prepare outgoing rules; probes are not Confirmation evidence.

## Boundaries

- Execute only the recorded state; confirmation begins an eligible target immediately.
- `figure_review` includes table curation, draft planning/rendering, presentation, and feedback.
- Return `no_system_route` for unrelated work.

## Output

Return paths, fingerprint/revision, state, selected Skills in call order, blockers, route, and next action.
