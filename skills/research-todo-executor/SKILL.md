---
name: research-todo-executor
description: Execute the current Codex-owned lifecycle state recorded for a complete research TODO, coordinate the minimum implementation/testing/batch/aggregation Skills, and hand state evidence to rule-based transition evaluation. Do not infer, change, or automatically advance the state.
---

# Research TODO Executor

## Objective

Orchestrate one execution of the current Codex-owned state while preserving the TODO's scientific contract and the task-state YAML's lifecycle control.

This Skill does not create TODOs, choose another state, apply transitions, or create task-specific narrative handoffs.

## Required inputs

Read:

1. `AGENTS.md`;
2. `.research/policy.yaml`;
3. `.research/workflow/pipeline.yaml`;
4. `.research/workflow/state-machine.yaml`;
5. the complete TODO;
6. the task-state YAML;
7. relevant repository code, data interfaces, and existing result artifacts;
8. the human's requested execution scope for the recorded current state.

Require:

- `current.state` is one of `exploration`, `development`, `pilot`, `confirmation`, or `ablation_diagnosis`;
- `current.status` is `ready`, or a valid same-state resume is requested;
- `transition_review.status` is `not_evaluated`, unless a valid same-state resume is requested;
- the state-file TODO identifier and path match the resolved TODO;
- the human requested execution of the recorded state rather than a different target.

Stop if any condition fails.

## Build the execution contract

Extract from the TODO:

- objective and research question;
- included and excluded work;
- input/output definitions and analysis units;
- mathematical definitions;
- variables, controls, planned combinations, repeats, and metrics;
- fixed decisions and approved flexibility;
- required technical artifacts and completion criteria;
- result paths already present.

Extract from task state:

- current state and revision;
- current execution status and prior artifact references;
- confirmed transition history;
- any resume identifier or blocker.

Do not copy this contract into another handoff file.

## Execution workflow

1. Verify the state-file revision immediately before work begins.
2. Set `current.status` and `execution.status` to `running`; set the state, execution identifier, and start time.
3. Select exactly one state Skill matching `current.state`.
4. Select the minimum capability Skills required by the TODO and scope.
5. Inspect existing code and data boundaries before editing.
6. Implement the smallest scientifically faithful vertical slice.
7. Use `$research-computing-implementation` for Python/MATLAB choices, performance, and storage design.
8. Use `$research-agile-testing` after each high-risk slice.
9. When experimental metrics are produced, save immutable raw outputs and use `$research-evidence-aggregation`.
10. When multiple recoverable units, substantial I/O, concurrency, or long runtime are involved, use `$research-batch-execution`.
11. Store technical outputs under one result root, normally `results/{todo_id}/`.
12. Update only the relevant Codex path values in the TODO `Output References` section.
13. At the state decision boundary, record execution status, artifact references, and state-relevant predicate results in the task-state YAML.
14. Set `execution.decision_boundary_reached` to `true`, `current.status` to `awaiting_transition_evaluation`, and `transition_review.status` to `evaluation_required`.
15. Invoke `$research-state-transition` in Evaluate mode.
16. Invoke `$human-research-review-gate` with every eligible rule path and the Codex recommendation.
17. Stop. Do not apply or execute another state.

## Execution status

Use:

- `completed` when the approved state scope reached its decision boundary;
- `partial` when auditable work exists but additional same-state work remains;
- `failed` when the state execution failed without corrupting prior evidence;
- `blocked` when a human, dependency, resource, or semantic decision is required;
- `running` only while an execution or human-launched long run is actually active.

A `partial`, `failed`, or `blocked` outcome may still be evaluated. The self-transition must remain available.

## Predicate evidence

Record only predicates relevant to the current state and supported by evidence. Each value must be `true`, `false`, or `unknown` with artifact references.

Never set a favorable predicate merely to make a forward transition eligible. Missing or conflicting evidence is `unknown`.

## Result directory

Use a structure equivalent to:

```text
results/{todo_id}/
├── task-state.yaml
├── raw/
├── tables/
├── checkpoints/
├── logs/
└── figures/
```

A logical table may be a partitioned Parquet dataset rather than one physical file. Keep logs separate from bulk numerical output.

## TODO write boundary

During Codex execution, edit only these path values when the corresponding outputs exist:

- `Codex result directory`;
- `Codex raw-result index or directory`;
- `Codex condition-merged table(s)`.

Do not add implementation summaries, tests, state, decisions, or interpretations to the TODO.

## Long-running jobs

When estimated runtime reaches the policy threshold:

1. complete risk-matched tests;
2. complete one combination and one repeat end to end;
3. verify buffered or partitioned output, checkpointing, resume, progress, logging, and aggregation;
4. measure representative CPU, memory, GPU memory, runtime, and material I/O cost;
5. save the resumable execution record under the result root;
6. provide one reproducible command, working directory, output path, completion criteria, and failure criteria;
7. set execution status to `blocked`, keep `execution.decision_boundary_reached: false`, and attach the long-run gate artifact reference;
8. set `current.status: blocked` and invoke the human gate;
9. do not evaluate lifecycle transitions yet, because the current state has not reached its decision boundary;
10. do not launch the formal run.

## Output contract

At each pause or state decision boundary, return:

- TODO and task-state paths;
- current state, status, and revision;
- completed and incomplete work;
- files changed;
- commands and tests actually run;
- result paths;
- failures, missing items, anomalies, and untested risks;
- observed technical or experimental facts;
- predicate results and evidence references;
- eligible rule paths after rule evaluation;
- one Codex-recommended rule path;
- the explicit human decision required.

## Hard rules

- Do not create another scientific handoff document.
- Do not edit TODO content outside path values.
- Do not infer or change `current.state`.
- Do not present implementation success as scientific support.
- Do not present smoke-test, Exploration, or Pilot evidence as Confirmation.
- Do not silently change metrics, controls, data scope, combinations, or repeat rules.
- Do not delete failed, intermediate, negative, or contradictory results.
- Do not write scientific results one row at a time to CSV or another shared table.
- Do not apply or execute the transition recommended after this state.
- Report with established technical terms and direct evidence. Define any necessary local label operationally and avoid evaluative adjectives that are not tied to TODO criteria.
