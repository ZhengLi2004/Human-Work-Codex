# Research Task System Governance

Reusable procedures belong in Skills, lifecycle rules in `.research/workflow/state-machine.yaml`, adjustable limits in `.research/policy.yaml`, and task-specific scientific meaning only in the TODO.

## 1. Roles and authority

- **The human researcher** owns the scientific question, hypotheses, study design, experimentally supported parameter choices, lifecycle decisions, scientific interpretation, figure feedback, and the decision to complete, stop, redesign, or create a TODO. The researcher runs any script whose estimated minimum runtime exceeds three hours.
- **Codex** performs every agent-side stage in one shared task context: TODO authoring and revision, lifecycle control, implementation, testing, short execution, aggregation, table curation, figure planning, figure production, and technical evidence maintenance.

TODO authoring, implementation, aggregation, curation, and figure production remain distinct workflow stages inside that shared context.

### Research priorities

Work from **problem → metrics → framework → parameters**. Learn through bounded experiments and revisit upstream choices when evidence challenges them. Extract the main unresolved phenomenon and its tractable core before broadening scope. Use only metrics that measure that core; state essential tradeoffs. Secondary measures are justified guardrails against unacceptable behavior, not optimization targets once within bounds. Fair baseline comparisons assess the primary problem under comparable conditions; universal superiority is not the objective.

Use 80/20 as an effort heuristic: concentrate on modeling, derivation, and analysis; reserve refinement for a framework already supported on the primary problem. Before substantial tuning or patching, validate the framework against TODO-defined primary criteria and relevant baselines. If it underperforms, check implementation correctness, then prioritize reassessing or replacing the framework over further tuning. Scientific revisions still require researcher approval; numerical speed optimization does not substitute for framework validation.

### Working discretion

Work toward the approved stage outcome using the repository's contracts as constraints. Choose implementation details, tools, and focused checks from the actual problem; procedure lists describe dependencies and evidence needs rather than a script to recite. Reuse trustworthy evidence when its inputs and scope still match. Continue authorized work through its decision boundary without requesting the same approval again.

Resolve routine engineering ambiguity from repository context and record consequential assumptions. Ask a focused question when missing information changes scientific meaning, authorized scope, or a lifecycle decision; continue independent work meanwhile. When a rule blocks progress, cite the exact rule, affected action, and evidence needed to resolve it. Model capability does not replace researcher authority or observed evidence.

Keep detailed evidence in artifacts. User-facing updates should explain the outcome, material uncertainty, and next decision; use tables or lists where they aid comparison. Scale verification to the scientific and engineering risks, and stop extending it once the relevant checks pass unless new evidence warrants more work.

Resolve conflicts in this order:

1. the researcher's current explicit instruction;
2. the current TODO for scientific meaning;
3. task-state YAML for lifecycle facts;
4. this file;
5. the shared state machine;
6. policy;
7. selected Skills;
8. repository engineering conventions.

## 2. TODO and task-state boundaries

Each task has one scientific handoff: its TODO.

- The TODO contains only current actionable definitions, variables, controls, metrics, evidence requirements, completion criteria, and output paths.
- Task state stores lifecycle state, execution facts, TODO fingerprint, rule evidence, eligible paths, recommendations, and confirmed history.
- Logs, checkpoints, manifests, raw outputs, tables, plotting scripts, figures, and task state are technical artifacts; they do not replace the TODO.
- Keep progress, rejected designs, obsolete alternatives, and old-versus-new commentary outside the active TODO.
- Candidate ranges belong in the TODO only when their experimental selection is current work.
- Use valid Markdown. Write each mathematical expression on one line between `$` delimiters; do not use `\(...\)` or `\[...\]` in TODO files.
- Add only requirements supported by the scientific question, a known failure mode, or measured evidence. Avoid speculative architecture and arbitrary quality thresholds.

### Task directory

Each task uses one repository-root directory named `TODO_###`, where `###` is three digits:

```text
TODO_001/
├── TODO.md
├── task-state.yaml
├── code/        # optional method/framework implementation
├── exp/         # experiment, metric, aggregation, and plotting code
└── data/        # inputs, outputs, tables, checkpoints, logs, and figures
```

`code/` is optional; `exp/` and `data/` are required. Keep every task artifact inside this directory and do not create parallel `TODO/` or `results/` trees.

Code under `code/` uses cohesive modules, explicit interfaces, Google-style Python docstrings, MATLAB help comments, and avoids known code smells. Code under `exp/` has no prescribed architecture or documentation style; it only needs to complete the required experiment.

## 3. TODO revision and debugging

Scientific changes always require explicit researcher approval.

Before the first governed draft figures are presented, an approved TODO revision may be made in place. Codex then refreshes the complete-file SHA-256 fingerprint, increments task-state revision, records the change reference, invalidates a pending decision, and prepares fresh lifecycle options.

After governed draft figures have been presented, a scientific TODO revision requires a new versioned TODO with a new stable identifier. Base it on the current TODO, code, data interfaces, and artifacts; reuse and modify the existing implementation instead of rebuilding it. Path-only output-reference updates remain in place.

After an evidence-backed parameter selection, Codex may rewrite the current TODO in place before figure presentation so the approved value is fixed and only remaining actions remain. Preserve the complete candidate and sensitivity evidence outside the TODO.

During Development, Pilot, and Confirmation debugging, Codex may edit code and data in the existing task directory. It may delete or replace artifacts proven invalid by an implementation or data-pipeline defect when it records the reason and affected stable identifiers, removes dependent derived artifacts, and regenerates the relevant indexes and checks. Preserve valid observations and never delete data because of result direction. A corrected formal run must again satisfy the frozen Confirmation specification.

An unexplained TODO fingerprint mismatch blocks execution. Resolve it as an approved in-place revision before figure presentation, an exact restoration, or a new versioned TODO after figure presentation.

## 4. Lifecycle control

- Resolve `current.state` from task state, not chat memory or directory names.
- Initialization creates `todo_ready`, resolves bounded project mappings, data meaning, and feasibility, then prepares its outgoing rules. There is no separate Exploration or Evaluate stage.
- At every executable decision boundary, record evidence and prepare all outgoing rules, including the self-transition, as part of that stage execution.
- Unknown evidence never satisfies a non-self rule; every `none` predicate must be explicitly false.
- Codex recommends exactly one eligible rule path. The researcher may select any eligible path.
- A researcher-approved transition also authorizes immediate execution of its target. Applying a self-transition starts another pass of the same state. Terminal targets only update state.
- Verify state revision, rule-set version, TODO fingerprint, and exact eligible rule path before applying a decision atomically.
- Increment `rule_set_version` whenever predicate meaning, eligibility, or topology changes.
- `figure_review` combines table curation, figure planning, draft rendering, presentation, and researcher feedback. `figure_production` implements the recorded feedback and performs final integrity checks.

## 5. Implementation and performance

Use `$research-computing-implementation` for scientific code.

- Use MATLAB by default for non-plotting computation. A Python exception requires a Python-only capability or measured implementation constraint.
- Use separate Python scripts with Matplotlib and SciencePlots for governed plotting. Plotting scripts consume complete produced data and do not contain the sole production implementation of preprocessing, metrics, tests, fitting, exclusions, or aggregation.
- Follow **Make it work, make it right, make it fast** in order:
  1. **Work:** build a runnable environment-compatible vertical slice with realistic interfaces and bulk I/O.
  2. **Right:** implement the TODO faithfully and check formulas, units, controls, shapes, randomness, and outputs against an independent oracle or audited small case.
  3. **Fast:** profile measured bottlenecks, optimize them, and prove equivalence after material changes.
- Fast-phase benchmarks use a representative medium-sized dataset: large enough that warm-up, setup, serialization, and fixed I/O do not dominate, but small enough for repeated iteration. Record its size and fixed costs; check scaling at an additional larger size when batch-size behavior can change the conclusion.
- Preserve numerical and scientific meaning when changing algorithms, allocation, vectorization, MEX/code generation, parallelism, GPU use, or storage.

## 6. Batch execution and I/O

- Buffer scientific records or write independent task/chunk files; do not write result tables one row at a time.
- Keep logs separate from numerical results, publish completed chunks atomically, and validate them before completion.
- Write task-state YAML atomically as a complete document.
- Derive concurrency from measured CPU, memory, GPU memory, runtime, and I/O.
- When a script's estimated minimum runtime exceeds three hours, Codex completes preflight and provides the researcher a resumable script or command with batching, checkpoints, progress, logs, working directory, expected outputs, resource estimate, completion criteria, and failure criteria. Codex does not launch that formal run.

## 7. Evidence and parameters

- Distinguish commands run, tested implementation facts, observed results, interpretation, rule judgments, and recommendations.
- Account for every planned combination and preserve failed, missing, negative, and incomplete outcomes unless a documented debug defect invalidates the artifact under Section 3.
- Aggregate across independent repeats unless the TODO defines another unit.
- Resolve controlling sources in this order: TODO; task state and frozen task manifest; raw-result index and valid raw outputs; derived tables.
- Before aggregation, check grain, schema, stable keys, duplicates, missing keys, status counts, value ranges, time coverage when applicable, and join cardinality. Add only risk-relevant checks such as denominator consistency, average-of-averages, selection bias, or outlier influence.
- Write `aggregation-validation.json`; blocking source, grain, coverage, join, denominator, or calculation failures prevent publication.
- A nonstandard parameter without established methodological or prior empirical support requires both selection by a measurable TODO-defined criterion and a sensitivity exploration around the selected value. Preserve the full results and include the sensitivity result in governed figures.
- Treat successful execution as technical evidence. Confirmation support requires the TODO-defined confirmatory experiment.

### Statistical design and reporting

Use `$research-statistical-analysis` when a task estimates uncertainty, compares conditions, fits inferential models, or reports statistical claims. Its source reference distinguishes Nature, Cell, and Science guidance from repository conventions; apply the relevant journal and study context.

The TODO owns the estimand, independent unit, sample-size rationale, design, comparisons, uncertainty method, and applicable decision rules. Freeze these before Confirmation. Engineering repeat defaults do not justify scientific sample sizes. Codex may propose a defensible analysis; the researcher approves new or changed scientific choices.

Preserve exact sample counts and their meaning, replicate/dependence structure, exclusions and missingness, effect estimates, uncertainty, and applicable test details through produced tables and figure captions. Distinguish descriptive spread from uncertainty and exploratory results from confirmatory evidence. Record applicability and statistical checks inside `aggregation-validation.json`; a structural validator alone does not establish inferential validity. Unsupported inference blocks its publication, while negative or inconclusive results remain valid outcomes.

## 8. Tables and figures

During `figure_review`, Codex:

1. curates complete presentation tables through documented row- and key-preserving transformations;
2. maps all scientific fields, metrics, conditions, coverage states, and applicable parameter sensitivities to an efficient draft set;
3. records the relevant paper figure or established graphics convention supporting each method;
4. renders drafts from a dedicated `.py` plotting script using complete validated sources;
5. applies the target-journal profile to the complete figure after data rendering, without changing scientific semantics;
6. presents every draft and its coverage summary, then waits for researcher recommendations.

During `figure_production`, Codex implements the recorded recommendations and checks source coverage, statistical units, aggregation, titles, axes, units, scales, legends, missingness, failures, schematics, sensitivity results, and readability.

- Inspect images only when needed to resolve a specific question, and use thumbnails only. Prefer data, metadata, and programmatic checks; retain full-resolution exports for delivery. Record unresolved visual limits rather than claiming an unchecked property.
- Keep computation and plotting code in separate files.
- Every Python-rendered chart imports `scienceplots` and uses a style stack whose base is `science`; default to `science` plus `no-latex`.
- Record plotting-script and input/output SHA-256 hashes, Git revision, package versions, execution command and times, data-quality results, style stack, and figure-data sufficiency in the manifest.
- A plotting script may validate, sort, pivot, or reshape complete tables for presentation. New scientific quantities return to the MATLAB production path first.
- Account for all applicable conditions; never select favorable seeds, subjects, sessions, records, or partitions.
- A generalized diagram is visibly labeled as a schematic and supplements rather than replaces quantitative figures.
- Keep plotting scripts in `exp/figures/` and their exports, plans, manifests, and audits in `data/figures/`. Do not create a parallel Markdown handoff.

## 9. Absolute prohibitions

Do not:

- fabricate, infer, fill, smooth, or selectively retain data;
- pool non-independent observations to inflate sample size;
- loosen tolerances, remove failing tests, or bypass invariants to obtain a passing result;
- tune after viewing Confirmation results without invalidating the analysis and obtaining approval;
- apply an ineligible or unconfirmed rule path, or omit the self-transition;
- expand scientific scope or change fixed semantics without researcher approval;
- use Python for non-plotting computation without a documented exception;
- optimize before a runnable scaffold and correctness reference exist;
- generate a Python chart without the `science` SciencePlots base style;
- publish an aggregate or final figure with a blocking integrity finding.

## 10. Communication

- Describe responsibilities positively and route work to the owning stage.
- Reserve `must not`, `do not`, and `never` for absolute prohibitions.
- Prefer established scientific and engineering terms. Describe operations before defining a necessary local label.
- Tie words such as `robust`, `significant`, `optimal`, `complete`, and `generalizable` to explicit criteria and evidence.
- Use direct sentences, few adjectives, and only enough examples to clarify a fragile rule.

Example:

- Avoid: "The semantic fidelity engine performs holistic evidence harmonization."
- Prefer: "Validate the schema and stable keys, join observed runs to the planned-condition table, then aggregate across independent repeats."
