# TODO-[Work: identifier]: [Work: research task title]

> **Objective:** [Work: state exactly what will be implemented or tested, under which conditions, and which research judgment the result will inform.]
>
> **Authoring rule:** Describe only current work and the fixed decisions needed to perform it. Do not retain progress notes, completed selection instructions, rejected candidates, obsolete designs, or old-versus-new comparisons.

## 1. Research Definition

- Source research material: [path, version, and relevant section]
- Parent research question: [preserve the researcher's intended meaning]
- Current research question or decision: [state the exact question this work must answer]
- Current pre-specified hypothesis: [state the hypothesis tested by this work, or `None`]
- Role of this TODO: [state the current implementation or evidence closure]
- Project scope: [project, dataset, method, and experimental object]
- Dependencies: [other TODO identifiers, or `None`]

## 2. Method and Mathematical Specification

> This section defines what must be computed. Generic Exploration, Development, Pilot, Confirmation, testing, checkpointing, logging, and review procedures belong in Skills rather than in this TODO.

### 2.1 Project-object mapping

[Map the research objects, method components, inputs, outputs, controls, and evaluation targets needed by the current work to concrete repository modules and data. If verifying a mapping is the current task, state the probe and decision rule; do not preserve superseded mappings as background narrative.]

### 2.2 Inputs, outputs, and analysis units

- Inputs: [objects, fields, units, shapes, time range, and sample scope]
- Outputs: [model outputs, derived quantities, or result tables]
- Basic analysis unit: [trial / session / subject / seed / sample / other]
- Independent statistical unit: [unit used for uncertainty and inference]
- Pairing, blocking, or stratification: [definition, or `None`]

### 2.3 Mathematical and algorithmic definitions

[Specify every formula, variable, objective, transformation, estimator, baseline, and control that changes scientific meaning. Define every symbol.]

Example:

\[
\hat{\theta}=\arg\min_{\theta\in\Theta}\mathcal{L}(X,Y;\theta)
\]

where:

- \(X\): [definition]
- \(Y\): [definition]
- \(\theta\): [definition]
- \(\mathcal{L}\): [definition and evaluation domain]

### 2.4 Task variables

| Variable | Research meaning | Complete values or sampling rule | Role |
|---|---|---|---|
| [intentionally varied factor] | [meaning] | [complete range] | [primary comparison / experimentally verified parameter selection / stratification / other] |

If this TODO selects a hyperparameter experimentally, put the complete approved candidate range, decision metric, feasibility constraints, tie rule, stopping rule, and selection rule here. Do not also state a provisional downstream value. After verification and explicit researcher approval, Work rewrites the TODO to retain the approved value and remaining work; complete candidate evidence remains in the result artifacts.

### 2.5 Controls and comparability

| Control | Fixed rule | Reason | Action if violated |
|---|---|---|---|
| [comparability condition] | [value or rule] | [reason] | [promote to grouping key / mark incomparable / request approval] |

### 2.6 Metrics, repeats, and statistical question

| Metric | Research meaning | Mathematical definition, direction, or source | Repeats per combination |
|---|---|---|---|
| [metric] | [question answered] | [formula / direction / implementation source] | [number or rule] |

- Complete planned combination set: [Cartesian product or explicit list]
- Independent repeat mechanism: [seed, initialization, independent sample, or other]
- Aggregation level: [normally compute within each independent repeat, then summarize across repeats]
- Primary comparison or statistical test: [null hypothesis, effect size, interval, or decision rule]
- Failure, missingness, invalidation, and exclusion rules: [predefined rules]
- Incomplete or incomparable evidence rule: [predefined rule]

### 2.7 Fixed decisions and approved flexibility

**Fixed unless the human explicitly approves a change:**

- [methods, metrics, data scope, parameters, or comparison definitions]

**Adjustable within the approved scope:**

- [engineering or Pilot choices and their permitted bounds]

**Experimentally verified hyperparameters used by this current task:**

| Parameter | Fixed value | Applies to |
|---|---|---|
| [parameter, or `None`] | [fixed value] | [method, condition, or component] |

Include a row only after the verification experiment is complete and the researcher has approved the value. Keep approval and evidence references in the task-state change event and technical artifacts. Do not retain rejected values or obsolete designs in this TODO.

### 2.8 Scope

**Required:**

- [implementation, validation, and experiment work needed to answer the task]
- [raw outputs and complete evidence that must be produced]

**Excluded:**

- [mechanistic interpretation, expansion, or refactoring outside this TODO]
- [work that belongs to another TODO or to the human research report]

The excluded list defines current scope; it is not a history of abandoned work. Omit obsolete alternatives and comparisons with earlier designs.

## 3. Required Outputs and Completion Criteria

### 3.1 Required technical artifacts

- [implementation and correctness evidence]
- [immutable raw results]
- [complete run-level table, complete aggregate table, and condition-merged table]
- [failure, missingness, anomaly, and limitation records]
- [code, configuration, version, command, checkpoint, and log information needed for reproduction]
- [scientific fields, metrics, conditions, and coverage states that the figure set must communicate]
- [relevant paper figures whose graphical methods should be considered, or `None`]

### 3.2 Questions the outputs must answer

1. [technical or experimental question that must be answerable]
2. [question that must explicitly be marked unanswerable when evidence is insufficient]

### 3.3 Completion criteria

The TODO is complete whether the result is positive, negative, or inconclusive when:

- the specification has been implemented faithfully or shown to be infeasible for an auditable reason;
- required tests and experiments have completed, or every incomplete item has an auditable cause;
- every planned combination has a `complete`, `incomplete`, `failed`, `missing`, or `invalid` state in the result artifacts;
- the referenced outputs answer Section 3.2 or establish why the current design cannot answer it;
- the human approves completion or termination of the TODO.

## 4. Output References

> Outside the governed verified-parameter rewrite, Codex and Work may edit only the path values below. Do not add status fields, summaries, interpretations, stage records, or other narrative content.

- Codex result directory: [path]
- Codex raw-result index or directory: [path or paths]
- Codex condition-merged table(s): [path or paths]
- Work curated table(s): [path or paths]
- Work figure directory: [path]
