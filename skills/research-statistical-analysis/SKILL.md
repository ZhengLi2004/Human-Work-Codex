---
name: research-statistical-analysis
description: Specify, implement, or audit statistical design, uncertainty, comparisons, and reporting within a research task's approved stage. Use for inferential claims and statistical figure annotations.
---

# Research Statistical Analysis

Make each statistical claim traceable to an approved question, identifiable independent units, an appropriate estimator, and complete evidence. This is a capability within the recorded stage, not a new lifecycle state or permission to redesign a study.

Read [CNS reporting sources](references/cns-statistical-reporting.md) when planning the reporting requirements or checking a named journal. Read [the evidence contract](references/statistical-evidence-contract.md) when producing or auditing tables, validation, or figure annotations. Use the relevant requirements; a deterministic task or descriptive result needs no invented hypothesis test.

## Design in the TODO

Recover the scientific question and existing approvals first. Make the target quantity and population, independent unit, replicate hierarchy, sample-size rationale, allocation/blinding, comparisons, exclusions/missingness, and uncertainty method explicit to the extent needed by that question. Report when randomization, blinding, or prospective sample-size calculation was not performed; never reconstruct them as if they occurred.

For inference, propose a justified model or test, its assumptions and diagnostics, effect-size definition, interval method/level, and applicable sidedness, alpha, covariates, and multiplicity family. For Bayesian work, specify priors and computational diagnostics instead of adding frequentist requirements mechanically. For resampling, specify the independent resampling unit and dependence-preserving scheme. An unspecified scientific choice stays a proposal for researcher approval, not a default filled in by the implementation.

Separate primary, secondary, and exploratory analyses. Freeze the approved analysis, stopping rules, and allowed responses to failed assumptions before Confirmation. Pilot may inform a proposed sample size or parameter choice; preserve that provenance. A few random seeds measure algorithmic variability only over the approved seed-generating process, not population generalization by themselves.

## Execution and evidence

Implement the approved quantities through `$research-computing-implementation`, using MATLAB unless a documented exception applies. Validate the analysis against an independent reference or audited case that exercises its actual risk: pairing, nesting, denominators, multiplicity, interval construction, or degenerate data. Use `$research-evidence-aggregation` to retain all planned comparisons and their statuses.

Check assumptions relevant to the estimator and design. A normality-test result alone does not select a test or establish independence. If the frozen analysis fails, apply only a preapproved fallback; otherwise report the limitation and request a scientific revision. Preserve failed/undefined estimates with a reason instead of manufacturing a zero, interval, or P value. New post-result analyses remain exploratory and require approval when they change the TODO.

## Reporting

Carry sample counts, unit definitions, effect estimates, uncertainty, and applicable test/model details into complete production tables. Provide enough detail to reproduce complex analyses, including software versions and resampling or Bayesian settings. Plotting consumes these quantities; captions identify the displayed observations, summaries, intervals, comparisons, and adjustment method.

Record checks and limitations in the existing aggregation validation and figure audit using the evidence contract. A small P value does not establish scientific importance; a non-significant result does not establish equivalence. Report what the design and interval support, leaving scientific interpretation to the researcher.

Return the approved design references, produced artifacts, supported scope of inference, unresolved findings, and any required scientific decision. Apply the stage's normal outgoing-rule preparation.
