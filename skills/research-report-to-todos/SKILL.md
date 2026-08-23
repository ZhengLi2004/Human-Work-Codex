---
name: research-report-to-todos
description: Author or revise a concise current-action research TODO from researcher material and repository context.
---

# Research Report to TODOs

Create one executable scientific handoff without inventing meaning. Split TODOs only when objectives, primary measurements, data scopes, statistical units, dependencies, or closure decisions differ materially.

## Authoring

1. Select an unused `TODO_###`; create `TODO.md`, `exp/`, `data/`, and optional method `code/`.
2. Read the approved source material and repository interfaces.
3. Define the question, hypothesis, inputs/outputs, analysis and uncertainty units, controls, combinations, repeats, metrics, comparisons, failure rules, and completion evidence.
4. Put each mathematical expression on one line between `$` delimiters.
5. Separate fixed scientific decisions from bounded engineering choices; add requirements only when justified by the question, a known failure mode, or measurement.
6. For each unsupported nonstandard parameter, define a measurable selection rule, sensitivity range, and sensitivity figure.
7. Keep Output References path-only and omit progress, completed work, rejected candidates, and obsolete designs.

## Revisions

- Before figure presentation, synchronize an approved scientific change in place and preserve parameter evidence outside the TODO.
- After presentation, create a versioned TODO from the current implementation. Path-only updates remain in place.

Example: replace `test several settings and make a good plot` with `evaluate every approved setting under the defined repeat rule, preserve failures in coverage, apply the stated selection criterion, and plot the complete sensitivity range`.

## Output

Produce `TODO_###/TODO.md` and its directories; return source mapping and unresolved scientific ambiguities. Create no parallel handoff, begin no implementation, and never fix an experimentally selected value before complete evidence and approval.
