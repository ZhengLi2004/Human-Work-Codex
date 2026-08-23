# TODO_001: [research task title]

> **Objective:** [State what will be implemented or tested, under which conditions, and which research decision the result informs.]
>
> **Authoring rule:** Keep only current actions and fixed decisions. Add a requirement only when the research question, an identified failure mode, or measured evidence supports it.

## 1. Research Definition

- Source material: [path, version, and section]
- Research question: [exact question]
- Pre-specified hypothesis: [hypothesis or `None`]
- Scope: [project, dataset, method, and experimental object]
- Dependencies: [TODO_### identifiers or `None`]

## 2. Method and Mathematical Specification

### 2.1 Project-object mapping

[Map research objects, inputs, outputs, controls, and evaluation targets to repository modules and data.]

### 2.2 Inputs, outputs, and analysis units

- Inputs: [fields, units, shapes, time range, and sample scope]
- Outputs: [model outputs, quantities, and tables]
- Basic analysis unit: [trial / session / subject / seed / sample / other]
- Independent statistical unit: [unit used for uncertainty and inference]
- Pairing, blocking, or stratification: [definition or `None`]

### 2.3 Mathematical definitions

Write every expression on one line between single-dollar delimiters. Example: $\hat{\theta}=\arg\min_{\theta\in\Theta}\mathcal{L}(X,Y;\theta)$, where $X$, $Y$, $\theta$, and $\mathcal{L}$ are defined below.

- $X$: [definition]
- $Y$: [definition]
- $\theta$: [definition]
- $\mathcal{L}$: [definition and evaluation domain]

### 2.4 Variables and parameters

| Variable or parameter | Research meaning | Complete values or rule | Role |
|---|---|---|---|
| [name] | [meaning] | [range or fixed value] | [comparison / control / parameter selection / stratification] |

For every nonstandard parameter without established methodological or prior empirical support, define:

- measurable selection criterion: [metric, direction, feasibility rule, and tie rule];
- sensitivity exploration: [values around the candidate or selected value and the quantity compared];
- sensitivity figure requirement: [figure question and conditions].

Do not state an experimentally selected value as fixed until complete evidence exists and the researcher approves it.

### 2.5 Controls and comparability

| Control | Fixed rule | Reason | Action if violated |
|---|---|---|---|
| [condition] | [value or rule] | [reason] | [group separately / mark incomparable / request approval] |

### 2.6 Metrics, repeats, and statistical question

| Metric | Research meaning | Definition or source | Repeats per combination |
|---|---|---|---|
| [metric] | [question answered] | [one-line formula, direction, or source] | [number or rule] |

- Complete planned combinations: [Cartesian product or explicit list]
- Independent repeat mechanism: [seed, initialization, independent sample, or other]
- Aggregation level: [within-repeat calculation and across-repeat summary]
- Primary comparison or statistical test: [null hypothesis, effect size, interval, or decision rule]
- Failure, missingness, invalidation, and exclusion rules: [predefined rules]

### 2.7 Fixed decisions and approved flexibility

**Fixed without further researcher approval:**

- [scientific method, metric, scope, parameter, or comparison]

**Adjustable within current scope:**

- [engineering choice or Pilot range]

Avoid architecture, gates, or thresholds that are not needed to answer the task or manage an observed risk.

## 3. Required Outputs and Completion

### 3.1 Technical artifacts

- [implementation and correctness evidence]
- [complete valid raw results and invalidation records]
- [run-level, aggregate, and condition-merged tables]
- [`aggregation-validation.json` with source, grain, schema, key, coverage, and applicable calculation checks]
- [configuration, command, checkpoint, progress, log, and version information needed for reproduction]
- [scientific fields, conditions, coverage states, and parameter sensitivities the figures must show]
- [relevant paper figures or established graphics conventions, or `None`]

### 3.2 Questions the outputs answer

1. [primary technical or experimental question]
2. [question explicitly marked unanswerable when evidence is insufficient]

### 3.3 Completion criteria

The task can close with a positive, negative, or inconclusive result when:

- the specification is implemented faithfully or an auditable blocker is established;
- required tests and experiments finish, or every incomplete unit has an auditable cause;
- every planned combination has an accounted-for state;
- applicable nonstandard-parameter sensitivity evidence and figures are complete;
- the referenced outputs answer Section 3.2 or establish why the design cannot answer it;
- the researcher approves completion or termination.

## 4. Output References

> Keep this section path-only. Use the task's `TODO_###` directory.

- Task directory: [TODO_###/]
- Method/framework code directory: [TODO_###/code/ or `None`]
- Experiment code directory: [TODO_###/exp/]
- Data directory: [TODO_###/data/]
