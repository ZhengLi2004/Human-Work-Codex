# Research Task Routing Table

The TODO is the only scientific handoff document. The task-state YAML stores machine lifecycle state, and the human confirms exact transition rule paths.

| Request or state | Required route | Optional capabilities | Blocking condition |
|---|---|---|---|
| Author or split complete TODOs | `research-report-to-todos` | None | Source meaning or metric definition cannot be resolved |
| Missing task state | `research-state-transition` Initialize | None | TODO identifier cannot be resolved |
| `evaluation_required` or `awaiting_transition_evaluation` | `research-state-transition` Evaluate | human gate | Decision boundary, evidence, or state revision is inconsistent |
| Apply transition | `research-state-transition` Apply | None | Rule path is not eligible, ambiguous, stale, or not human-confirmed |
| `exploration` | `research-todo-executor` + `research-exploration` | computing, testing | State not ready or TODO incomplete |
| `development` | `research-todo-executor` + `research-development` | computing, testing, batch | State not ready or TODO incomplete |
| `pilot` | `research-todo-executor` + `research-pilot` | computing, testing, batch, aggregation | Planned scope or repeats unclear |
| `confirmation` | `research-todo-executor` + `research-confirmation` | computing, testing, batch, aggregation | Frozen semantics or formal prerequisites absent |
| `ablation_diagnosis` | `research-todo-executor` + `research-ablation-diagnosis` | computing, testing, batch, aggregation | Candidate explanations or intervention scope unclear |
| `work_postprocessing` ready | `publication-table-curation` then `research-figure-production` | None | Codex source paths incomplete |
| Work decision boundary | `research-state-transition` Evaluate | human gate | Work predicates or artifacts are inconsistent |
| `completed` or `stopped` | no execution route | post-report assessment | Human requests work inside a terminal TODO |
| Aggregate completed runs | `research-evidence-aggregation` | batch when recomputation is needed | Manifest/raw evidence absent |
| Post-report next-step assessment | `post-report-assessment` | human gate | Human report absent |
| General explanation or code outside the TODO system | `no_system_route` | None | Not applicable |

## Capability triggers

- `research-computing-implementation`: Python/MATLAB code, numerical performance, parallel/GPU execution, or storage design.
- `research-agile-testing`: scientific invariants, formulas, metrics, control semantics, randomness, recovery, or regression risk.
- `research-batch-execution`: multiple recoverable units, checkpoint/resume, material I/O, concurrency, or long runtime.
- `research-evidence-aggregation`: run-level metrics, aggregate tables, or condition-merged tables.
- `research-state-transition`: initialization, post-state rule evaluation, or human-confirmed transition application.
- `human-research-review-gate`: transition choice, semantic change, restricted long run, completion, stop, or redesign.

## Transition routing

```text
state execution reaches decision boundary
    ↓
transition_review.status = evaluation_required
    ↓
research-state-transition Evaluate
    ↓
eligible_transitions includes the exact self rule
    ↓
Codex recommends one rule_id + target
    ↓
human selects one eligible rule path
    ↓
research-state-transition Apply
    ↓
router may execute the new state only when separately authorized
```

## Router output

Return:

- route result;
- resolved TODO and state-file paths;
- current state, execution status, decision-boundary flag, and revision;
- primary Skill and ordered loadout;
- pending eligible rule paths when applicable;
- blocking reason or human decision required;
- next permitted action.
