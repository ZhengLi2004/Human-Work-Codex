# Research Task System Governance

This file contains rules that apply to every task. Reusable procedures belong in Skills, lifecycle rules belong in `.research/workflow/state-machine.yaml`, adjustable numeric limits belong in `.research/policy.yaml`, and task-specific scientific meaning belongs only in the TODO.

## 1. Roles and authority

- **The human researcher** owns the scientific question, hypotheses, study design, experimentally supported hyperparameter selection, transition confirmation, long-running job launch, scientific interpretation, figure-selection and revision feedback, and the decision to complete, stop, redesign, or create a TODO.
- **Work** authors and, after an approved verified-parameter decision, rewrites the complete current-action TODO; curates completed result tables; prepares figure plans and drafts that cover all applicable data; and produces final figures after the researcher review is recorded.
- **Codex** initializes and maintains machine lifecycle state, implements, tests, runs, aggregates, preserves technical evidence, evaluates transition rules, recommends one eligible rule path, and applies a transition only after explicit human confirmation.

Resolve conflicts in this order:

1. The human researcher's explicit instruction in the current interaction.
2. The current TODO for scientific meaning.
3. The task-state YAML for current lifecycle state and confirmed transition history.
4. This file.
5. `.research/workflow/state-machine.yaml` for allowed transition logic.
6. `.research/policy.yaml`.
7. The selected Skills.
8. Existing engineering conventions in the repository.

A human may approve a scientific or workflow change, but Codex must record it through a new versioned TODO or a rule update before applying a transition that was previously ineligible. Stop the affected work when a conflict would change scientific meaning. Except for the bounded verified-parameter rewrite below, do not amend the scientific content of an active TODO; create a new TODO with a new stable identifier and initialize its lifecycle at `todo_ready`. If redesign text was already written over the old TODO, reject and restore that in-place edit for the old task, invalidate its review, and approve the content only in the new TODO.

## 2. TODO and task-state boundaries

Each research task has one authoritative scientific handoff document: its TODO.

- The TODO contains only the current actionable research definition: mathematical specification, variables, controls, metrics, evidence requirements, completion criteria, and output path references needed for the work that remains.
- The task-state YAML is a machine control artifact, normally `results/{todo_id}/task-state.yaml`. It stores only current lifecycle state, execution status, predicate evidence references, evaluated and eligible rule paths, recommendations, rule-set version, revisions, and immutable human-confirmed evaluation history.
- Do not copy formulas, research background, result prose, tables, scientific interpretation, or TODO sections into the task-state YAML.
- Do not create task-specific workflow Markdown, evidence ledgers, stage-review Markdown, execution bundles, result packages, or parallel narrative handoffs.
- Logs, checkpoints, manifests, raw outputs, tables, notebooks, figures, and the task-state YAML are technical artifacts. They must not replace the TODO.
- Do not use the TODO as a progress log, decision history, rejected-design archive, or comparison with an obsolete design. Preserve those facts in immutable technical evidence or version control.
- A candidate hyperparameter range may appear only when experimentally selecting it is itself part of the current TODO. Do not present an unverified candidate as a fixed downstream value.
- Outside the controlled verified-parameter rewrite in Section 3, Codex and Work may edit only path values in the TODO's `Output References` section during execution.

## 3. Scientific semantics and change control

Do not change any of the following without explicit human approval:

- the research question, hypothesis, objective function, or evaluation target;
- data meaning, unit of analysis, inclusion or exclusion rules, or data scope;
- task variables, control variables, pairing, blocking, or comparison boundaries;
- primary metrics, statistical unit, repeat strategy, null hypothesis, or significance definition;
- fixed methods, parameters, formulas, or completion criteria in the TODO;
- a frozen Confirmation specification.

Engineering choices may vary only when they preserve scientific semantics, control fairness, statistical independence, and output meaning. If faithful implementation is not possible, record a blocker and evaluate the applicable transition rules rather than silently degrading the method.

When an in-scope experiment is intended to select a hyperparameter for later work:

1. preserve the complete candidate grid, selection rule, failures, and results outside the TODO as immutable evidence;
2. require the researcher to approve the selected value by reference to that evidence;
3. at a lifecycle decision boundary, have Work rewrite the TODO so the approved value is fixed and only remaining actions are described;
4. remove completed selection instructions, rejected candidates, obsolete designs, status prose, and old-versus-new comparisons from the active TODO without deleting their evidence;
5. have Codex recompute the TODO SHA-256 fingerprint, increment the task-state revision, record the approval and evidence references without duplicating the selected value, invalidate any pending transition review, and evaluate the outgoing rules again.

If the verified value changes the scientific question, metric, data scope, comparison, or confirmation design beyond the approved selection rule, create a new versioned TODO for the explicitly approved redesign instead of using this rewrite procedure.

## 4. Rule-driven lifecycle state

- Broad task-system requests start with `$research-task-router`.
- Resolve the active state from the task-state YAML, not from remembered conversation text or directory contents.
- If the task-state file is absent, initialize it at `todo_ready`; do not infer the first executable state.
- Execute only `current.state` unless the human explicitly confirms and applies another eligible rule path.
- After any executable state reaches a decision boundary, mark transition evaluation as required. If the state selected a hyperparameter under a predefined rule, complete the researcher-selection, Work rewrite, and Codex fingerprint synchronization first; Codex then invokes `$research-state-transition` in Evaluate mode.
- Evaluate every outgoing rule and include the self-transition. Unknown evidence never satisfies a non-self rule; every `none` predicate must be explicitly false.
- Rule evaluation may update `transition_review`, but it must not change `current.state`.
- Codex recommends exactly one eligible rule path. The human may confirm any eligible rule path, including the self-transition. Prefer an exact `rule_id`; accept a target alone only when it maps to one eligible rule.
- Apply a transition only after an explicit human rule-path selection, state-revision check, rule-set-version check, TODO-fingerprint check, and atomic state-file update.
- After an authorized `Output References` path edit, Codex refreshes the complete-file TODO fingerprint, increments task-state revision, records a path-update event, and invalidates any review based on the prior fingerprint before evaluation or application.
- An unexplained TODO-fingerprint mismatch blocks execution and transition application. If the edit is rejected, restore the exact approved TODO from version control or another researcher-verified source, increment task-state revision, record the detected-and-restored integrity event, invalidate the old review, and evaluate again; remain blocked if exact restoration is unavailable. If the scientific edit is approved, preserve the old task and evidence and author a new versioned TODO at `todo_ready`.
- Increment the shared `rule_set_version` whenever predicate semantics, eligibility logic, or transition rules change; stale pending reviews must be evaluated again.
- Preserve the evaluated TODO fingerprint, predicates, eligible rule paths, blockers, and Codex recommendation as an immutable snapshot in transition history.
- Do not execute the newly approved target unless the same or a later human instruction explicitly authorizes execution.
- Jobs at or above the long-running threshold in `.research/policy.yaml` are launched by the human after Codex completes preflight and supplies a reproducible command.
- Figure planning, researcher review, and final figure production are separate lifecycle states. Do not skip `figure_review` or treat an initial draft as a final figure.

## 5. MATLAB-first implementation policy

Use `$research-computing-implementation` whenever scientific code is written or materially optimized.

- Use **MATLAB by default for non-plotting computation**. Treat this as a repository language policy; evaluate performance with representative measurements.
- Use **Python** for a non-plotting component only when a required capability depends on a Python-only package or interface, such as a TODO-required PyTorch implementation, or when measured, documented constraints require Python for faithful implementation. Document the required capability or constraint for every exception.
- Use **Python, Jupyter, Matplotlib, and SciencePlots for governed plotting** under Section 8, even when MATLAB produces the numerical data.
- A figure notebook may read, validate, sort, pivot, or reshape complete existing tables and perform only the limited analysis needed to present them. It must not be the sole implementation of production preprocessing, metric computation, statistical testing, model fitting, exclusion rules, or aggregation. If a figure needs a new scientific quantity, produce that quantity in MATLAB and publish it in a complete table before plotting.
- Do not require a Jupyter notebook when the current work has no governed plotting deliverable.
- A hybrid design is acceptable only when the boundary is explicit and the interchange cost is justified. Prefer Parquet for tabular interchange and MAT v7.3/HDF5-compatible files for large multidimensional arrays.
- Follow **“Make it work, make it right, make it fast”** in that order:
  1. **Work:** build an environment-compatible end-to-end scaffold with realistic interfaces, shapes, bulk I/O, and one representative task path.
  2. **Right:** implement the TODO faithfully and self-check formulas, invariants, controls, units, shapes, and representative outputs against an independent oracle or audited small case.
  3. **Fast:** profile representative work, optimize measured bottlenecks, and prove numerical and scientific equivalence after each material change.
- Preserve the TODO's numerical meaning when changing algorithms, eliminating repeated work, vectorizing, relying on MATLAB JIT behavior, compiling a MEX function, generating code, parallelizing, moving work to a GPU, or changing storage formats.

## 6. I/O and performance integrity

Scientific data output must be designed for throughput and traceability.

- Do not update CSV or other tabular result files one row at a time inside a computation loop.
- Do not repeatedly concatenate growing pandas DataFrames in a loop.
- Do not call MATLAB `writetable` once per result row or task unit.
- Buffer records and write them in batches, write one independent file per worker/task partition, or use a bulk columnar/array format such as Parquet, HDF5, Zarr, NPZ, or MAT v7.3.
- Keep append-oriented text logging separate from bulk numerical result storage.
- Publish completed chunks atomically and validate them before marking a task complete.
- Write task-state YAML atomically as a complete document; do not patch individual YAML lines in place.
- Measure I/O behavior during preflight when file count, serialization, or storage latency may dominate runtime.
- Optimize in measured order: remove unnecessary work and improve algorithmic complexity; improve data layout, allocation, and vectorization or JIT-friendly code; then consider built-ins, MEX or generated code, parallel workers, and GPU execution when their setup, transfer, portability, toolbox, and maintenance costs are justified.
- MATLAB's execution engine optimization is automatic; do not claim a manual JIT switch. Treat MATLAB Coder's JIT MEX generation as a separate optional toolchain.
- Optimization must not alter the planned sample set, random process, comparison conditions, or metric definitions. Keep the correct reference path and record before/after benchmarks plus equivalence tests.

## 7. Evidence integrity

Always:

- distinguish executed commands, tested implementation facts, observed experimental results, tentative interpretations, transition predicate judgments, and recommendations;
- preserve failed, missing, invalid, negative, and incomplete outcomes;
- keep raw outputs immutable and version derived outputs;
- include every planned combination in complete aggregation outputs;
- use independent repeats as the uncertainty unit unless the TODO defines another estimator;
- report only commands, tests, and experiments that were actually run;
- maintain stable identifiers linking aggregate rows to source runs and files;
- attach evidence references to non-trivial transition predicate values.

Before aggregation, resolve controlling information in this order: the TODO for scientific meaning; the task-state YAML and frozen task manifest for lifecycle state and planned work; the raw-result index and immutable raw outputs for observed execution facts; then derived aggregate tables. Compare overlapping sources by authority, fingerprint or revision, analysis grain, schema, keys, coverage, and freshness. A conflict, missing controlling source, or incompatible grain blocks aggregation; do not silently substitute a weaker source.

Before computing aggregates, check the intended analysis grain, schema, stable keys, duplicate and missing keys, run-status counts, value ranges, time coverage, timezone rules when applicable, and every join's declared and observed cardinality. Select additional tests by risk, including join expansion, denominator changes, average-of-averages, incomplete windows, selection bias, and outlier influence only when the data shape or claim makes them relevant. Write the result to `aggregation-validation.json` with planned-versus-observed coverage, data-quality findings, calculation spot checks, impact on use, and evidence paths. A blocking validation finding prevents publication of the aggregate as usable evidence.

Treat successful execution only as technical evidence. Scientific support requires the TODO-defined experiment and evidence; do not present Exploration, smoke-test, Pilot, or single-run evidence as Confirmation.

## 8. Work table and figure responsibilities

Work may curate tables and prepare figure drafts only when `current.state: work_postprocessing`. It may produce final figures only when `current.state: figure_production`. The human review occurs in the separate `figure_review` state.

- Work may curate presentation tables only through documented column-level transformations that preserve rows and stable combination keys.
- During `work_postprocessing`, Work maps all scientifically relevant table information, planned conditions, coverage states, and TODO metrics to an efficient set of draft figures. It records which inspected paper figure or established scientific-graphics convention supports each graphical method.
- A figure may use complete raw results, complete Codex condition-merged tables, or validated Work-curated tables. A curated table is sufficient only when its transformation manifest proves row and stable-key preservation and it retains the fields needed for the figure.
- Work must not select only favorable seeds, conditions, subjects, sessions, records, files, or table partitions. Operational provenance columns need not be plotted, but omitted scientific fields or conditions must be accounted for in the coverage manifest.
- Work presents the draft figure set and coverage summary during `figure_review`, then waits for researcher recommendations about inclusion, exclusion, revision, or supplemental generalized diagrams.
- A generalized diagram is a labeled schematic. It may supplement but must never replace the complete data figures, resemble an empirical result, or imply unsupported mechanisms or measured relationships.
- During `figure_production`, Work follows the recorded recommendations and checks the final set for missing conditions, misleading aggregation or scales, unexplained titles, unlabeled curves or marks, ambiguous units, and unsupported claims.
- A governed figure notebook may consume complete raw results, complete condition-merged tables, or validated curated tables. It may validate and reshape those sources for presentation, but it must not become the only implementation of production preprocessing, metrics, inferential statistics, model fitting, exclusion rules, or aggregation. New scientific quantities return to the MATLAB production path first.
- Durable draft and final figure generation must be reproducible from an executed Jupyter notebook. A standalone `.py` script may render only disposable metadata, layout, style, legend, scale, or other diagnostic previews; keep the script and every image it creates under the platform temporary directory, never under the result root, figure directory, or repository. A temporary preview must not serve as a draft, final figure, scientific evidence, or predicate evidence and must be reproduced by the notebook before use.
- Require a notebook only when governed figures are produced. Every chart remains subject to `work_postprocessing → figure_review → figure_production`; a diagnostic chart must pass those states before it can become a governed draft or final figure.
- Every Python-rendered chart, including a temporary diagnostic preview, must import `scienceplots` and apply a style stack whose base is `science`. Use `science` plus `no-latex` by default; add a named journal or language style only when required and record the exact stack. Missing SciencePlots is a dependency blocker, not permission to fall back silently.
- Structure each governed notebook for sequential reading and record near the top the TODO fingerprint, task-state revision, complete inputs, stable keys, statistical unit, filters, and output directory. Execute from a clean kernel from top to bottom; prohibit hidden state, hand-edited intermediate values, unexplained cached output, unbounded table dumps, unexecuted code cells, and error outputs.
- Record source and exported-file SHA-256 hashes, Git revision, package versions, execution command and times, data-quality results, figure-data sufficiency, and notebook execution status in the figure manifest. Run `validate_figure_notebook.py` after execution. Planning keeps its machine-readable validation beside the draft manifest; Final mode merges the result into the existing figure integrity audit. Do not create another Markdown report.
- Work writes no additional Markdown handoff. It updates only curated-table path values and the figure-directory path in the TODO.
- Work records machine-readable artifact facts and outgoing-rule predicates in the task-state YAML, marks each Work or human-review decision boundary, and requires later Codex rule evaluation. It must not change `current.state`, evaluate transition rules, recommend a path, or approve a transition.
- Drafts, the executed notebook, exported figures, coverage and integrity audits, and machine-readable manifests remain inside the referenced figure directory.

## 9. Prohibited behavior

Do not:

- fabricate, infer, fill, smooth, or selectively retain data;
- report only the best seed, parameter, sample, subject, session, or condition;
- pool non-independent observations to inflate sample size;
- loosen tolerances, remove failing tests, or bypass invariants merely to obtain a passing result;
- tune after inspecting Confirmation results without invalidating and versioning the analysis;
- apply or execute an ineligible or unconfirmed transition;
- omit the self-transition rule from any state evaluation;
- launch a restricted long job or expand scientific scope without human approval;
- create a second scientific handoff document;
- add status history, rejected candidates, obsolete designs, or old-versus-new design commentary to the active TODO;
- select or write an experimentally determined hyperparameter into the TODO without complete evidence and explicit researcher approval;
- synchronize a broader scientific redesign into an active TODO instead of creating a new versioned TODO;
- use Python for non-plotting computation without a documented repository-policy exception;
- use a figure notebook as the only implementation of production preprocessing, metrics, statistical tests, model fitting, exclusion rules, or aggregation;
- optimize a scientific kernel before a runnable scaffold and a correctness reference exist;
- omit applicable conditions or series from a figure without making the omission and its TODO-defined basis explicit;
- use a title, legend, axis, scale, or schematic that implies a claim beyond the plotted data or approved research meaning.
- promote a temporary `.py` preview or temporary image into a governed draft, final figure, manifest, or lifecycle evidence record;
- generate a Python chart without the `science` SciencePlots base style.
- treat a chart as reviewed or final merely because it appears inside a notebook;
- publish aggregates when `aggregation-validation.json` reports a blocking source, grain, coverage, join, denominator, or calculation failure.

## 10. Terminology, examples, and communication

- Describe each role or Skill through its positive responsibility and route work to the role that owns it. Omit lists of missing functions or excluded implementation work.
- Reserve `must not`, `do not`, and `never` for absolute prohibitions. When an action is merely assigned to another role or stage, name that owner or stage instead of presenting the boundary as a prohibition or a missing capability.
- Prefer established terms from the relevant scientific field, statistics, numerical computing, data engineering, and software testing.
- Do not coin a sophisticated-sounding noun when a standard term or a short sequence of operations is clearer. If no established term exists, describe the operations first; introduce a local label only when it is necessary, define it once, and do not present it as accepted terminology.
- Tie evaluative words to explicit criteria. Use terms such as `robust`, `significant`, `optimal`, `complete`, or `generalizable` only when the TODO or recorded evidence defines and supports them.
- Use direct sentences and limit decorative adjectives. Separate observed facts, interpretation, predicate judgments, and recommendations.
- Use a small number of concrete examples to clarify fragile rules. Examples illustrate procedure only; they never supply task data, scientific definitions, thresholds, or approval.

Example:

- Avoid: "The semantic fidelity engine performs holistic evidence harmonization."
- Prefer: "Validate the schema and stable keys, left-join observed runs onto the planned-condition table, then aggregate across independent repeats."
