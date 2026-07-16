---
name: research-report-to-todos
description: Convert human research material and project context into one or more complete TODO specifications. Use when Work must define tasks before Codex execution. Do not create workflow, ledger, review, bundle, or result-package documents and do not start coding.
---

# Research Report to TODOs

## Overview

Use this Skill to author complete, stable research TODOs from the researcher's material and the actual project context. Each TODO must be sufficient for later Codex and Work execution without another task-definition document.

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

1. Read the human research material and identify the exact source sections.
2. Inspect the repository and data interfaces needed to map research objects to project objects.
3. Preserve the human's scientific meaning; distinguish established facts from assumptions requiring Exploration.
4. Define inputs, outputs, basic and independent units, pairing, blocking, and stratification.
5. Write every mathematical formula, variable definition, objective, baseline, control, and metric that changes interpretation.
6. Define the complete planned combination set, repeat mechanism, aggregation level, primary statistical question, and failure/missingness rules.
7. Separate fixed scientific decisions from approved engineering or Pilot flexibility.
8. Define required technical artifacts and completion criteria that do not depend on a positive result.
9. Reserve the TODO `Output References` section for paths only.
10. Validate that Codex can execute the task and Work can later curate tables and produce figures using only the TODO plus referenced result files.

## Project-specific computing definition

When the implementation language matters, define the scientific interface rather than over-prescribing code structure. Record constraints that affect meaning, such as numerical precision, expected array shapes, GPU equivalence, or cross-language file compatibility. Leave language selection to `$research-computing-implementation` unless the research method or existing codebase requires one language.

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
