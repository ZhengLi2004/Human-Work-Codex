---
name: research-report-to-todos
description: Author or revise a concise current-action research TODO from researcher material and repository context.
---

# Research Report to TODOs

Create one executable scientific handoff without inventing meaning. Split TODOs only when objectives, primary measurements, data scopes, statistical units, dependencies, or closure decisions differ materially.

## Authoring

Use approved source material and repository interfaces to produce the current scientific specification in an unused `TODO_###` with `exp/`, `data/`, and optional `code/`. Adapt the template to the task: preserve enough definition of question, units, inputs/outputs, controls, comparisons, metrics, failure behavior, and completion evidence to make execution unambiguous.

Define the tractable core problem first, then primary metrics and justified guardrail bounds, then the framework and its validation criterion, and finally parameters. Explain the phenomenon each primary metric measures and the tradeoffs accepted in baseline comparisons; avoid unrelated metrics or an all-metrics-win objective.

Use `$research-statistical-analysis` for sample-size rationale, dependence, uncertainty, and inferential choices. Distinguish established decisions from proposals that need approval. For each unsupported nonstandard parameter, define a measurable selection criterion, sensitivity exploration, and figure requirement. Keep engineering discretion explicit without inventing scientific requirements.

Write each mathematical expression on one line between `$` delimiters. Keep Output References path-only and preserve only current actions and decisions; progress and superseded designs belong in technical history.

## Revisions

- Before figure presentation, synchronize an approved scientific change in place and preserve parameter evidence outside the TODO.
- After presentation, create a versioned TODO from the current implementation. Path-only updates remain in place.

## Output

Produce the TODO and its directories; summarize source mapping and unresolved scientific decisions. TODO authoring ends at the handoff to lifecycle initialization; implementation uses its approved state. Never fix an experimentally selected value before complete evidence and approval.
