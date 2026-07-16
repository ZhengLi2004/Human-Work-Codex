# Entry Prompts

Use `$research-task-router` for broad Research Task System requests. Internal Skills are selected by the router.

## 1. Work: create a TODO

```text
Use $research-task-router to process this research material: [path].

Create one or more complete TODOs. Each TODO must contain the full task definition, mathematical formulas, variables, controls, metrics, repeats, statistical question, required outputs, and completion criteria.

Do not create workflow Markdown, an evidence ledger, a review packet, or a result package. Do not add lifecycle state fields to the TODO. Do not start implementation.
```

Expected route: `$research-report-to-todos`.

Codex initializes task state when lifecycle work first begins.

## 2. Codex: initialize lifecycle and evaluate initial paths

```text
Use $research-task-router for [TODO path].

Initialize its task-state YAML if missing. Evaluate every outgoing rule from todo_ready, including todo_ready.self. Show each eligible rule_id, source, target, and kind. Recommend one path, but do not apply it until I confirm.
```

Expected route: `$research-state-transition` Initialize, then Evaluate.

Human response example:

```text
Approve todo_ready.to_development (TODO Ready → Development) and execute Development.
```

Expected route: `$research-state-transition` Apply, then `$research-todo-executor` + `$research-development`.

## 3. Codex: execute the recorded current state

```text
Use $research-task-router to execute the current state for [TODO path].

Read current.state from task-state.yaml. Do not infer or replace it. Use the minimum required implementation, testing, batch, and aggregation Skills. At the decision boundary, record predicate evidence, mark transition evaluation as required, evaluate every outgoing rule including self, recommend one eligible rule path, and stop for my decision.
```

Expected route: `$research-todo-executor` + exactly one recorded state Skill + minimum capability Skills + `$research-state-transition` Evaluate + human gate.

## 4. Human: confirm a transition path

Apply only:

```text
Approve development.to_pilot (Development → Pilot).
```

Apply and execute:

```text
Approve development.to_pilot (Development → Pilot) and execute Pilot.
```

Expected route: `$research-state-transition` Apply. Execution occurs only in the second form.

The human may select the self-transition:

```text
Approve pilot.self (Pilot → Pilot) and execute another Pilot pass with the approved remaining scope.
```

A target-only response is accepted only when exactly one eligible rule reaches that target.

## 5. Codex: prepare a restricted long-running run

```text
Use $research-task-router to prepare the current-state run for [TODO path].

Before handing the command to me:
- run risk-matched tests;
- complete one combination and one repeat end to end;
- validate buffered/batched I/O, checkpointing, resume, progress, logging, and aggregation;
- measure single-task resource and material I/O cost;
- provide one reproducible command, working directory, expected result directory, completion criteria, and failure criteria;
- do not launch the formal run;
- keep decision_boundary_reached false until the current state actually ends.
```

## 6. Work: curate tables and produce figures

Use after the human has confirmed `work_postprocessing`:

```text
Use $research-task-router for [TODO path].

Confirm current.state is work_postprocessing. Curate the complete Codex tables without changing rows or stable keys, then create the required figures in an executed ipynb. Each figure must use complete applicable raw results, condition-merged tables, or both. Update only the Work table paths and figure-directory path in the TODO. Create no Markdown handoff.

When Work finishes, record the Work rule predicates, set decision_boundary_reached true and transition_review.status to evaluation_required, return the tables and figures to me, and do not recommend or apply a transition.
```

Expected route: `$publication-table-curation`, then `$research-figure-production`.

## 7. Codex: evaluate closure or rework after Work

```text
Use $research-task-router for [TODO path].

The Work execution has reached its decision boundary. Evaluate every outgoing work_postprocessing rule, including work_postprocessing.self. Show all eligible rule paths, recommend one, and stop for my decision.
```

Expected route: `$research-state-transition` Evaluate + human gate.

Human completion example:

```text
Approve work_postprocessing.to_completed (Work Postprocessing → Completed).
```

## 8. Post-report assessment

```text
Use $research-task-router to assess the next research action after my report: [report path].

Use the original TODO and complete result tables as factual sources. Treat my report as the source of scientific interpretation. Recommend continue, targeted follow-up, redesign, stop, or a new TODO, but do not automatically create or start the next task.
```

Expected route: `$post-report-assessment`.
