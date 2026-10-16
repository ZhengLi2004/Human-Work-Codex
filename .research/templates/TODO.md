# TODO_001: [research task title]

> **Objective:** [State what will be implemented or tested, under which conditions, and which research decision the result informs.]
>
> **Authoring rule:** Keep only current actions and fixed decisions. Add a requirement only when the research question, an identified failure mode, or measured evidence supports it.

## 1. Research Definition

- Source material: [path, version, and section]
- Research question: [main unexplained phenomenon and tractable core; scope deliberately deferred]
- Pre-specified hypothesis: [hypothesis or `None`]
- Scope: [project, dataset, method, and experimental object]
- Dependencies: [TODO_### identifiers or `None`]

## 2. Method and Mathematical Specification

### 2.1 Problem, metrics, and framework

- Primary criteria: [minimal metrics tied to the core phenomenon; success criterion and essential tradeoffs]
- Guardrails: [secondary measures, justified acceptable bounds, and response to violations; not ranking objectives within bounds]
- Framework: [model assumptions and derivation explaining how it addresses the core problem]
- Validation before refinement: [relevant baselines, comparable conditions, minimal justified settings, and evidence needed before substantial tuning]
- Reconsideration rule: [evidence warranting framework revision rather than further tuning, after checking implementation correctness]

### Project-object mapping

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

| Metric and role | Research meaning | Definition or source | Repeats per combination |
|---|---|---|---|
| [metric; primary / guardrail] | [question answered] | [one-line formula, direction, or source] | [number or rule] |

- Complete planned combinations: [Cartesian product or explicit list]
- Independent repeat mechanism: [seed, initialization, independent sample, or other]
- Aggregation level: [within-repeat calculation and across-repeat summary]
- Primary comparison or estimand: [quantity, target population, contrast, and scientific interpretation of its units]
- Failure, missingness, invalidation, and exclusion rules: [predefined rules]

Statistical design, where relevant (retain applicable fields and briefly explain when inference is outside scope):

- Analysis role: [primary confirmatory / secondary / exploratory / descriptive]
- Sample size per condition and rationale: [power/precision inputs, prior evidence, or fixed available sample and limitations; distinguish technical from independent repeats]
- Allocation and blinding: [procedures and stages, or explicit explanation of what was not performed]
- Dependence: [repeated measures, nesting, clusters, pairing, and the unit used for estimation/resampling]
- Estimation and uncertainty: [estimator, effect-size definition, spread versus uncertainty, interval type/level/method]
- Inferential method, if used: [model/test, hypothesis, covariates, assumptions, diagnostics, and preapproved fallback]
- Testing decisions, if used: [sidedness and rationale, alpha, comparison family, multiplicity correction or justified absence]
- Bayesian/resampling details, if used: [priors and computation/diagnostics, or resampling scheme and settings]
- Stopping and analysis freeze: [collection/stopping rule, separation from Pilot, and definitions fixed before Confirmation]
- Reporting evidence: [exact n and its unit, estimates/intervals, applicable statistics/df/P or posterior results, software and caption mapping]

Do not substitute engineering repeat defaults for a scientific sample-size rationale. Unapproved scientific choices remain unresolved proposals.

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
