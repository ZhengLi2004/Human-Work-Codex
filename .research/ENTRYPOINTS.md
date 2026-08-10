# Entry Prompts

Use `$research-task-router` for broad Research Task System requests. Internal Skills are selected by the router.

## 1. Work: create a TODO

```text
Use $research-task-router to process this research material: [path].

Create one or more complete TODOs. Each TODO must contain the full task definition, mathematical formulas, variables, controls, metrics, repeats, statistical question, required outputs, and completion criteria.

Describe only the current work and fixed current decisions. If a hyperparameter requires experimental selection, make that verification the current task; do not write a provisional downstream value. Do not retain progress notes, rejected candidates, obsolete designs, or old-versus-new comparisons.

Do not create workflow Markdown, an evidence ledger, a review packet, or a result package. Do not add lifecycle state fields to the TODO. Do not start implementation.
```

Expected route: `$research-report-to-todos`.

Codex initializes task state when lifecycle work first begins.

## 2. Codex: initialize lifecycle and evaluate initial paths

```text
Use $research-task-router for [TODO path].

Initialize its task-state YAML and TODO SHA-256 fingerprint if missing. Evaluate every outgoing rule from todo_ready, including todo_ready.self. Show each eligible rule_id, source, target, and kind. Recommend one path, but do not apply it until I confirm.
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

For implementation, use MATLAB for non-plotting computation unless a required Python-only package or measured MATLAB infeasibility is documented. Follow "Make it work, make it right, make it fast": run an efficient scaffold, implement and self-check the TODO faithfully, then profile and optimize with before/after benchmarks and equivalence tests.

Before publishing aggregate tables, resolve the controlling sources in this order: TODO; task-state and frozen task manifest; raw-result index and immutable raw outputs; derived tables. Write aggregation-validation.json with the applicable grain, schema, stable-key, duplicate, missingness, status-count, range, time-coverage, join-cardinality, denominator, weighted-aggregation, coverage, and calculation spot checks. Block on a missing controlling source, incompatible grain, unresolved conflict, or other finding that makes the aggregate unsafe to use.
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

## 6. Work: curate tables and prepare drafts covering all applicable data

Use after the human has confirmed `work_postprocessing`:

```text
Use $research-task-router for [TODO path].

Confirm current.state is work_postprocessing. Curate the complete Codex tables without changing rows or stable keys. Then use $research-figure-production in Planning mode.

Use complete raw results, complete condition-merged tables, or validated row/key-preserving Work tables. Inspect relevant paper figures when available, choose established graphical methods, map all scientific table information and planned conditions to an efficient draft set, and write the plan and coverage manifests. Generate governed drafts from an executed Jupyter notebook and apply the SciencePlots `science` + `no-latex` style stack. A standalone Python preview and every image it creates belong only in the platform temporary directory and must not become a draft. Do not call drafts final.

The notebook may validate, sort, pivot, or reshape the complete tables only for figure presentation. It must not become the only production implementation of preprocessing, metrics, statistical tests, model fitting, exclusion rules, or aggregation. If a figure needs a new scientific quantity, return it to the MATLAB result path first. Execute the notebook from a clean kernel, top to bottom, then run:

`python skills/research-figure-production/scripts/validate_figure_notebook.py --notebook [executed notebook] --manifest [draft-figure-manifest.json] --mode planning --output [notebook-validation.json]`

When planning finishes, record the Work predicates, set decision_boundary_reached true and transition_review.status to evaluation_required, return the tables and drafts, and do not recommend or apply a transition.
```

Expected route: `$publication-table-curation`, then `$research-figure-production` Planning mode.

## 7. Researcher: review the draft figure set

Use after the human has confirmed and executed `work_postprocessing.to_figure_review`:

```text
Use $research-task-router for [TODO path].

Confirm current.state is figure_review. Present every draft figure with its question, source, graphical-method basis, statistical unit, and condition-coverage summary. Ask which figures to retain, exclude, revise, split, combine, or supplement with a labeled schematic. Wait for my output; do not infer preferences from silence.
```

Expected route: `$human-research-review-gate` figure-review procedure.

Example researcher output:

```text
Retain F1. Split F2 by dataset so all conditions remain readable. Exclude F3 because it duplicates F1, but keep its condition coverage in F1. Add a labeled pipeline schematic that is clearly separate from the data figures.
```

After the output is referenced, mark the `figure_review` decision boundary and require Codex rule evaluation. Require a separate explicit human rule-path selection for transition approval.

## 8. Work: produce and audit final figures

Use after the human has confirmed and authorized `figure_review.to_figure_production`:

```text
Use $research-task-router for [TODO path].

Confirm current.state is figure_production. Use $research-figure-production in Final mode. Implement the recorded researcher recommendations faithfully, execute the notebook from a clean kernel, export the final figures with a recorded SciencePlots style stack based on `science`, and write figure_manifest.json and figure_integrity_audit.json.

Audit source and condition coverage, statistical units, aggregation, titles, axes, scales, units, legends, every curve or mark, missingness, failure states, schematic labeling, and recommendation traceability. If any check fails, record revision or misleading-risk predicates and do not make completion eligible.

Run `python skills/research-figure-production/scripts/validate_figure_notebook.py --notebook [executed notebook] --manifest [figure_manifest.json] --mode final --output [figure_integrity_audit.json]`. The command merges its result into the existing JSON audit.
```

Expected route: `$research-figure-production` Final mode.

## 9. Codex: evaluate closure or rework after final figures

```text
Use $research-task-router for [TODO path].

The final figure execution has reached its decision boundary. Evaluate every outgoing figure_production rule, including figure_production.self. Show all eligible rule paths, recommend one, and stop for my decision.
```

Expected route: `$research-state-transition` Evaluate + human gate.

Human completion example:

```text
Approve figure_production.to_completed (Figure Production → Completed).
```

## 10. Post-report assessment

```text
Use $research-task-router to assess the next research action after my report: [report path].

Use the original TODO and complete result tables as factual sources. Treat my report as the source of scientific interpretation. Recommend continue, targeted follow-up, redesign, stop, or a new TODO, but do not automatically create or start the next task.
```

Expected route: `$post-report-assessment`.

## 11. Work and Codex: record a verified hyperparameter

Use after a complete TODO-defined selection experiment reaches a decision boundary and the researcher approves the rule-supported value:

```text
Use $research-task-router for [TODO path].

The complete parameter evidence is at [paths], and I approve [parameter] = [value] under the predefined selection rule. Have Work rewrite the TODO so this value is fixed and only remaining actions are described. Remove completed selection instructions, rejected candidates, obsolete designs, status prose, and old-versus-new comparisons from the active TODO, but preserve all technical evidence.

Then have Codex synchronize the TODO SHA-256 fingerprint, increment task-state revision, invalidate any pending transition review, evaluate every outgoing rule again, and stop for my transition decision.
```

Expected route: `$research-report-to-todos`, then `$research-state-transition` Synchronize TODO, then a separate Evaluate operation and human gate.
