# Research Task System Governance

This file contains rules that apply to every task. Reusable procedures belong in Skills, lifecycle rules belong in `.research/workflow/state-machine.yaml`, adjustable numeric limits belong in `.research/policy.yaml`, and task-specific scientific meaning belongs only in the TODO.

## 1. Roles and authority

- **The human researcher** owns the scientific question, hypotheses, study design, transition confirmation, long-running job launch, scientific interpretation, and the decision to complete, stop, redesign, or create a TODO.
- **Work** authors the complete TODO, curates completed result tables, and produces figures after Codex outputs are ready.
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

A human may approve a scientific or workflow change, but Codex must record the change through the appropriate TODO or rule update before applying a transition that was previously ineligible. Stop the affected work when a conflict would change scientific meaning.

## 2. TODO and task-state boundaries

Each research task has one authoritative scientific handoff document: its TODO.

- The TODO contains the complete research definition, mathematical specification, variables, controls, metrics, evidence requirements, completion criteria, and output path references.
- The task-state YAML is a machine control artifact, normally `results/{todo_id}/task-state.yaml`. It stores only current lifecycle state, execution status, predicate evidence references, evaluated and eligible rule paths, recommendations, rule-set version, revisions, and immutable human-confirmed evaluation history.
- Do not copy formulas, research background, result prose, tables, scientific interpretation, or TODO sections into the task-state YAML.
- Do not create task-specific workflow Markdown, evidence ledgers, stage-review Markdown, execution bundles, result packages, or parallel narrative handoffs.
- Logs, checkpoints, manifests, raw outputs, tables, notebooks, figures, and the task-state YAML are technical artifacts. They do not replace the TODO.
- During execution, Codex and Work may edit only path values in the TODO's `Output References` section.

## 3. Scientific semantics and change control

Do not change any of the following without explicit human approval:

- the research question, hypothesis, objective function, or evaluation target;
- data meaning, unit of analysis, inclusion or exclusion rules, or data scope;
- task variables, control variables, pairing, blocking, or comparison boundaries;
- primary metrics, statistical unit, repeat strategy, null hypothesis, or significance definition;
- fixed methods, parameters, formulas, or completion criteria in the TODO;
- a frozen Confirmation specification.

Engineering choices may vary only when they preserve scientific semantics, control fairness, statistical independence, and output meaning. If faithful implementation is not possible, record a blocker and evaluate the applicable transition rules rather than silently degrading the method.

## 4. Rule-driven lifecycle state

- Broad task-system requests start with `$research-task-router`.
- Resolve the active state from the task-state YAML, not from remembered conversation text or directory contents.
- If the task-state file is absent, initialize it at `todo_ready`; do not infer the first executable state.
- Execute only `current.state` unless the human explicitly confirms and applies another eligible rule path.
- After any executable state reaches a decision boundary, mark transition evaluation as required. Codex then invokes `$research-state-transition` in Evaluate mode.
- Evaluate every outgoing rule and include the self-transition. Unknown evidence never satisfies a non-self rule; every `none` predicate must be explicitly false.
- Rule evaluation may update `transition_review`, but it must not change `current.state`.
- Codex recommends exactly one eligible rule path. The human may confirm any eligible rule path, including the self-transition. Prefer an exact `rule_id`; accept a target alone only when it maps to one eligible rule.
- Apply a transition only after an explicit human rule-path selection, state-revision check, rule-set-version check, and atomic state-file update.
- Increment the shared `rule_set_version` whenever predicate semantics, eligibility logic, or transition rules change; stale pending reviews must be evaluated again.
- Preserve the evaluated predicates, eligible rule paths, blockers, and Codex recommendation as an immutable snapshot in transition history.
- Do not execute the newly approved target unless the same or a later human instruction explicitly authorizes execution.
- Jobs at or above the long-running threshold in `.research/policy.yaml` are launched by the human after Codex completes preflight and supplies a reproducible command.

## 5. Python and MATLAB implementation policy

Use `$research-computing-implementation` whenever scientific code is written or materially optimized.

- Prefer **MATLAB** when the task is dominated by dense matrix algebra, vectorized numerical operations, established MATLAB signal-processing code, or MATLAB-specific toolboxes.
- Prefer **Python** when the task is dominated by large multi-file data processing, heterogeneous data pipelines, machine learning, deep neural networks, or integration with the Python scientific ecosystem.
- A hybrid design is acceptable only when the boundary is explicit and the interchange cost is justified. Prefer Parquet for tabular interchange and MAT v7.3/HDF5-compatible files for large multidimensional arrays.
- Preserve the TODO's numerical meaning when vectorizing, parallelizing, moving work to a GPU, or changing storage formats.

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
- Optimization must not alter the planned sample set, random process, comparison conditions, or metric definitions.

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

Do not treat successful execution as scientific support. Do not present Exploration, smoke-test, Pilot, or single-run evidence as Confirmation.

## 8. Work table and figure responsibilities

Work may operate only when the task-state YAML records `current.state: work_postprocessing` and that state is ready or validly resumed.

- Work may curate presentation tables only through documented column-level transformations that preserve rows and stable combination keys.
- Work produces figures in a Jupyter notebook using complete data from at least one of the following for each figure: raw computation results, Codex-generated condition-merged tables, or both.
- Work must not select only favorable seeds, conditions, subjects, sessions, or records.
- Work writes no additional Markdown handoff. It updates only curated-table path values and the final figure-directory path in the TODO.
- Work records machine-readable artifact facts and outgoing-rule predicates in the task-state YAML, marks the Work decision boundary, and requires later Codex rule evaluation. It must not change `current.state`, evaluate transition rules, recommend a path, or approve a transition.
- Figure notebooks, exported figures, and any machine-readable figure manifest remain inside the referenced figure directory.

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
- add narrative execution records to the TODO beyond file or directory paths in `Output References`.
