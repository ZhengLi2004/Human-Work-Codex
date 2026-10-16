# Statistical evidence contract

The TODO is the sole scientific specification. Manifests, tables, and checks under `TODO_###/data/` record execution and evidence; do not create a parallel analysis-plan handoff. Freeze an execution snapshot of the approved statistical definitions with the Confirmation manifest.

## Produced evidence

Use existing tables where their grain fits. When contrasts or model coefficients have a different grain, produce a separate complete table in `data/tables/`, keyed by stable analysis/comparison ID and linked condition IDs. Validate that join explicitly; a many-row contrast table cannot silently expand a condition summary.

For each applicable analysis retain:

- The TODO definition, confirmatory/secondary/exploratory role, compared conditions, response, estimand, and target population.
- Exact n per group and per analysis, what n counts, independent-unit IDs or their traceable index, technical/biological repeats, pairing/blocking/nesting, and planned versus observed coverage. Operational `n_valid` is not automatically the inferential sample size. Bootstrap draws and cross-validation folds do not create independent subjects.
- Estimate/effect size with definition and units; center and spread definitions; interval bounds, type, level, method, and resampling unit/settings when used. Distinguish SD, SEM, confidence intervals, prediction intervals, and credible intervals.
- Applicable model/test, formula and covariates, assumptions and diagnostics, statistic, degrees of freedom, sidedness, alpha, exact numeric P value, multiplicity family/method, and adjusted P or q values when produced. Preserve numerical precision; report computational limits rather than a literal P = 0. Bayesian analyses instead retain priors, likelihood, posterior summaries, computation settings, convergence evidence, and relevant sensitivity.
- Included/excluded/missing counts with reasons, predefined transformations and analysis filters, method/software versions, command, code/input/output hashes, and a status/reason for unsupported or undefined quantities.

Retain every planned comparison, including undefined or failed results. Use null plus a reason for unavailable quantities; zero is an observed value. Descriptive analyses require counts and summary definitions, not artificial P values or confidence intervals. Respect the repository prohibition on filling missing observations; disclosure requirements do not authorize imputation.

## Validation in the existing artifact

Extend `aggregation-validation.json.checks` with applicable statistical checks, using its existing `pass|fail|not_applicable` status, expected rule, observed evidence, and impact fields. Use stable IDs such as `statistical_unit`, `analysis_sample_counts`, `design_and_assumptions`, `effect_and_interval`, `multiplicity`, `frozen_analysis`, and `statistical_reporting`. Record why inference is inapplicable for a deterministic/descriptive task instead of demanding a test. Missing required evidence is a failure, not `not_applicable`.

Check counts against the actual analysis population; verify paired/hierarchical handling and resampling units; audit the estimator/interval against a reference; reconcile all planned contrasts and multiplicity families; compare the executed analysis with the frozen specification. Check only applicable assumptions, including Bayesian computational diagnostics when relevant.

The supplied aggregation helper validates structural contracts. Its `passed` value alone does not certify this contract: the stage executor integrates statistical checks and recomputes the final result. If a finding makes the TODO-defined use unsafe, set top-level `passed: false`, retain the artifacts for diagnosis, and identify the affected analyses. Lack of significance alone is not an integrity finding.

## Figures and lifecycle

Store panel-to-analysis IDs and caption details in the existing figure plan/manifest. Report exact n and its unit for each group, represented observations/repeats, summary and error-bar definitions, applicable comparison/test/sidedness and adjustment, and the location of complete numerical results. Every significance symbol maps to produced evidence and a defined threshold. Render precomputed intervals and annotations; plotting never chooses a test or computes new inferential quantities.

Include statistical evidence in `results_ready_for_figures` and `figure_integrity_audit_passed`; design readiness also contributes to `todo_definition_complete` and `confirmation_prerequisites_ready` under the current rule set. A not-applicable determination with a reason satisfies only the statistical component of those predicates. It does not satisfy their other requirements. Incomplete design or unsupported inference follows the existing revision/self-transition paths; no additional approval stage is introduced.
