---
name: research-report-to-todos
description: Convert human research material and project context into current-action-only TODO specifications, or rewrite a TODO after an evidence-backed human-approved hyperparameter selection. Use when Work must define what remains to be done before Codex execution. Exclude progress history, rejected candidates, obsolete designs, and old-versus-new comparisons; do not start coding.
---

# Research Report to TODOs

## Overview

Use this Skill to author complete, stable research TODOs from the researcher's material and actual project context. Each TODO is a current to-do list: it must be sufficient for later Codex and Work execution without becoming a record of completed, rejected, or superseded work.

## When to split TODOs

Create separate TODOs when questions have different:

- scientific objectives or hypotheses;
- primary measurements or statistical units;
- data inclusion rules;
- implementation dependencies;
- evidence closure criteria;
- likely decisions after completion.

Do not split merely because a task has multiple implementation files or experiment conditions.

## Workflow

1. Read the human research material and identify the exact source sections that define the current approved work. Do not copy obsolete alternatives merely because they appear in the source.
2. Inspect the repository and data interfaces needed to map research objects to project objects.
3. Preserve the human's scientific meaning. If an unresolved mapping or parameter prevents a complete current task, define its verification as the current action or ask for a decision; do not mix a provisional choice into downstream work.
4. Define inputs, outputs, basic and independent units, pairing, blocking, and stratification.
5. Write every mathematical formula, variable definition, objective, baseline, control, and metric that changes interpretation.
6. Define the complete planned combination set, repeat mechanism, aggregation level, primary statistical question, and failure/missingness rules.
7. Separate fixed scientific decisions from approved engineering or Pilot flexibility. For a hyperparameter that requires experimental selection, define the complete candidates, decision metric, feasibility constraints, tie rule, stopping rule, and selection rule; fix a value only after complete verification evidence and researcher approval.
8. Define required technical artifacts and completion criteria that do not depend on a positive result.
9. Reserve the TODO `Output References` section for paths only.
10. Validate that Codex can execute the task and Work can later curate tables and produce figures using only the TODO plus referenced result files.
11. Remove status phrases, completed steps, rejected candidates, obsolete designs, and comparisons with earlier designs. Keep those records in source material, technical evidence, or version control.

## Concise example

Too vague: "Measure model robustness several times and make a good plot."

Sufficiently concrete: "For every model × noise-level combination, compute balanced accuracy within each independent seed, summarize across five seeds with the TODO-defined interval, retain failed seeds in coverage counts, and test the stated paired contrast."

The example illustrates specificity only. It does not define the metric, repeat count, or test for another TODO.

## Project-specific computing definition

When the implementation language matters, define the scientific interface rather than over-prescribing code structure. Record constraints that affect meaning, such as numerical precision, expected array shapes, GPU equivalence, or cross-language file compatibility. `$research-computing-implementation` applies the repository's MATLAB-first non-plotting policy and Python plotting boundary unless the research method requires a specific language.

## Verified-parameter rewrite

Use this procedure only at a lifecycle decision boundary after an in-scope experiment applied the TODO's predefined selection rule.

1. Require complete candidate-grid, failure, metric, and selection-rule evidence outside the TODO.
2. Require the researcher's explicit approval of the selected value.
3. Confirm that the value is within the approved candidate and selection scope; otherwise invoke the semantic-change gate.
4. Rewrite the TODO so the value is fixed where the remaining implementation or experiment needs it.
5. Delete completed selection instructions, rejected candidate values, obsolete designs, and old-versus-new discussion from the active TODO. Do not delete or narrow the underlying evidence.
6. Keep only current questions, current scope, current fixed values, required outputs, completion criteria, and output paths.
7. Hand the rewrite and its approval/evidence references to `$research-state-transition` in Synchronize TODO mode so Codex refreshes the fingerprint and invalidates stale transition evaluation.

Do not use this rewrite procedure for another scientific change. After explicit redesign approval, preserve the old task and evidence and author a new versioned TODO with a new stable identifier and a new task-state file initialized at `todo_ready`.

## Output contract

Produce:

- one TODO file per independent research closure;
- a chat summary mapping each TODO to the source research material;
- a chat list of unresolved scientific ambiguities or incompatible project facts requiring human approval.

Do not create any additional scientific handoff Markdown. Do not initialize task state; Codex creates it at `todo_ready` when lifecycle work first begins.

## Hard rules

- Do not omit metric definitions on the assumption that a later Skill will invent them.
- Do not place generic Pilot, Confirmation, testing, checkpoint, logging, or plotting procedures in the TODO.
- Do not start implementation or experimentation.
- Do not add lifecycle status, transition, or state fields to the TODO.
- Do not use the TODO as a progress report, change log, rejected-design archive, or literature/background summary.
- Do not state an experimentally selected hyperparameter as fixed before complete verification and explicit researcher approval.
- Do not retain the candidate grid in a downstream TODO after the selected value is fixed; preserve it in immutable technical evidence.
- Prefer established domain terms. When no standard term exists, describe the operations and define any necessary local label instead of presenting a coined term as established vocabulary.
