---
name: research-figure-production
description: Produce figures during work_postprocessing using a Jupyter notebook and complete applicable data from Codex raw results, condition-merged tables, or both. Use NumPy/SciPy/pandas with Matplotlib, SciencePlots, and seaborn. Do not create Markdown, cherry-pick rows, or change lifecycle state.
---

# Research Figure Production

## Overview

Use this Skill only when Codex result paths exist in the TODO and task state is `work_postprocessing`. Create a reproducible `.ipynb` that loads complete data, performs transparent transformations, generates the requested figures, and exports them into one figure directory.

Read `references/figure-data-contract.md`. Start from `assets/research_figures_template.ipynb` when useful.

## Required inputs

- the complete TODO, including metric and inclusion definitions;
- task-state YAML with `current.state: work_postprocessing`;
- Codex raw-result path(s);
- Codex condition-merged table path(s);
- Work curated table path(s), when available;
- the human's requested figure set or the figures directly implied by the TODO.

A logical table may span multiple physical files. Load the full logical dataset rather than one convenient partition.

## Source selection for each figure

For every figure:

1. state in the notebook which scientific question or TODO metric it visualizes;
2. choose raw results, condition-merged tables, or both as the scientific source;
3. use all applicable records from at least one of those selected logical sources under the TODO's predefined inclusion and exclusion rules;
4. use both raw and merged data when one supplies detail and the other supplies condition-level structure;
5. use a curated table only as an auxiliary display mapping or cross-check, never as the sole source that satisfies the completeness rule;
6. preserve stable IDs so plotted values can be traced to source rows or files;
7. never select rows because they make the figure cleaner or more supportive.

Any filter must come from the TODO or be a display-only operation that does not alter the measured population. Record transformations in notebook code and in a machine-readable figure manifest.

## Preferred stack

Use Python in the notebook:

- data processing: `numpy`, `scipy`, `pandas`;
- plotting: `matplotlib` as the primary plotting API, `SciencePlots` for scientific style contexts, and `seaborn` where its statistical or semantic plotting interface is appropriate;
- tabular I/O: pandas/PyArrow for Parquet and CSV;
- array I/O: NumPy, SciPy, h5py, or compatible readers as required by the Codex output.

Import `scienceplots` before selecting its styles. Prefer a `science` + `no-latex` context unless the environment and required fonts/LaTeX are explicitly available.

## Notebook workflow

1. Create or copy the notebook into the target figure directory.
2. Define all input and output paths at the top.
3. Load complete logical sources and validate schema, row count, stable IDs, conditions, and coverage fields.
4. Reproduce only transformations needed for the requested figures; do not silently re-run the scientific aggregation.
5. Use explicit grouping and uncertainty units from the TODO.
6. Generate one figure object at a time with clear labels, units, legends, and sample/coverage information when relevant.
7. Avoid defaults that silently aggregate at the wrong statistical level; compute the intended estimate explicitly when necessary.
8. Export vector output (`.pdf` or `.svg`) and a raster preview (`.png`) when practical.
9. Close figures after saving to avoid memory accumulation.
10. Write `figure_manifest.json` mapping each figure to source paths, selected columns, predefined filters, transformation functions, and exported files.
11. Execute the notebook end to end from a clean kernel and verify every declared figure file exists.
12. Update only the final `Work figure directory` path in the TODO.
13. Append notebook/figure artifact references and record `work_tables_complete`, `work_figures_complete`, `work_outputs_traceable`, `work_revision_needed`, `codex_output_defect_found`, `formal_output_gap_found`, `no_critical_correctness_risk`, `no_scope_change_required`, and other applicable outgoing-rule predicates as `true`, `false`, or `unknown` with evidence.
14. Record the Work execution as `completed`, `partial`, `failed`, or `blocked`; set `execution.decision_boundary_reached: true`, `current.status: awaiting_transition_evaluation`, and `transition_review.status: evaluation_required`.
15. Do not change `current.state`, evaluate rules, or recommend a transition. Return the figures to the human and state that Codex transition evaluation is the mandatory next lifecycle action.

## Figure integrity rules

- Do not drop failed, missing, invalid, negative, or low-performing conditions unless the figure explicitly visualizes a TODO-defined valid subset and the omission is visible in the notebook/manifest.
- Do not pool trials, sessions, subjects, or seeds in a way that changes the independent unit.
- Do not use seaborn's implicit estimator when it conflicts with the TODO-defined aggregation.
- Do not treat a Work-curated table as the only scientific source when raw or condition-merged data are required and available.
- Do not recompute a new primary metric during plotting.
- Do not create a Markdown result or figure report.
- Keep the notebook, manifest, and all figures inside the single referenced figure directory.

## Output contract

Produce:

- one executed `.ipynb`;
- exported figure files;
- `figure_manifest.json`;
- validation evidence in notebook outputs or chat.

Update only the `Work figure directory` path in the TODO. Return the task-state path, Work execution status, recorded predicate evidence, and the mandatory next action: Codex must invoke `$research-state-transition` in Evaluate mode before any further lifecycle action.
