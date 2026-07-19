---
name: research-figure-production
description: Plan draft figures covering all applicable data during work_postprocessing or produce reviewed final figures during figure_production using executed Jupyter notebooks, validated raw or tabular sources, explicit researcher recommendations, and a figure integrity audit. Use Planning mode only when current.state is work_postprocessing and Final mode only when current.state is figure_production. Do not skip figure_review, cherry-pick data, invent graphical terminology, or change lifecycle state.
---

# Research Figure Production

## Objective

Turn complete scientific tables or raw results into figures through three governed steps:

1. Planning mode selects graphical methods, maps all scientific table information to drafts, and prepares researcher-review material.
2. The separate `figure_review` state obtains interactive researcher recommendations.
3. Final mode implements those recommendations and checks that the final set is complete, traceable, and not misleading.

Read `references/figure-data-contract.md` before either mode. Start from `assets/research_figures_template.ipynb` when useful.

## Select exactly one mode

### Planning mode

Require `current.state: work_postprocessing`. Use after `$publication-table-curation` when curated tables are available, or use complete raw or condition-merged sources directly when they are the clearer basis.

Produce drafts and review material. Do not call them final and do not evaluate a path directly to `completed`.

### Final mode

Require `current.state: figure_production` and a referenced researcher output from the completed `figure_review` state.

Produce the final figure set, the final manifest, and the integrity audit. Do not silently reinterpret an ambiguous recommendation; set `figure_review_clarification_needed` and return to rule evaluation.

## Required inputs

- complete TODO, including metrics, variables, controls, units, statistical units, and inclusion rules;
- task-state YAML and current revision;
- Codex raw-result and condition-merged paths;
- Work curated-table paths and transformation manifests when used;
- stable condition keys, complete planned-condition skeleton, coverage and failure fields;
- relevant papers or source sections named by the TODO, when available;
- in Final mode, the referenced researcher recommendations and planning artifacts.

A logical table may span multiple files. Load the full logical dataset rather than one convenient partition.

## Source selection

For each data figure, choose one or more complete logical sources:

- raw computation results;
- condition-merged tables;
- validated Work-curated tables.

A curated table may be the sole source when its manifest proves unchanged row count and stable-key set and it retains every field required by the figure. Preserve stable IDs and record source paths, selected columns, predefined filters, and transformations.

Never select records because they make a cleaner or more supportive figure. When complete information does not fit one plot, use multiple panels, facets, small multiples, separate figures, or an explicit coverage panel.

## Planning workflow

1. Load and validate complete sources, schemas, row counts, stable keys, conditions, metrics, units, uncertainty fields, and coverage states.
2. Inventory the scientific information in each source. Distinguish it from operational provenance that belongs only in a manifest.
3. Inspect graphical methods in relevant papers when they are accessible. Record exact paper and figure references and the method borrowed; do not invent citations or claim inspection when access failed.
4. Otherwise select an established plot type and name it directly. Match visual encodings to variable types, comparison structure, statistical unit, and data density.
5. Build `figure-plan.json`, mapping each scientific field, TODO metric, planned condition, failure or missingness state, and research question to a proposed figure or panel.
6. Build `figure-coverage.json`, reconciling the planned condition skeleton and stable keys against the proposed set.
7. Create an executed planning notebook and export the complete draft figure set under `draft/`.
8. Write `draft-figure-manifest.json` with method basis, source classes, stable keys, statistical units, transformations, titles, axes, units, series labels, and coverage counts.
9. Update only the `Work figure directory` path in the TODO.
10. Record applicable predicates, including `figure_plan_complete`, `figure_method_basis_recorded`, `draft_figures_complete`, `figure_source_coverage_complete`, `figure_review_material_ready`, `work_outputs_traceable`, and risks or revision needs.
11. Mark the `work_postprocessing` decision boundary and return control for Codex transition evaluation. The eligible forward target is `figure_review`, not completion.

## Researcher-review material

Present, through `$human-research-review-gate` after the approved transition to `figure_review`:

- every draft figure and its intended question;
- the table-to-figure and condition-coverage summary;
- the graphical-method basis and any unavailable paper source;
- known tradeoffs, such as using facets instead of one crowded plot;
- a direct request to include, exclude, revise, or add figures, including optional generalized diagrams.

Wait for the researcher's output. Do not infer approval from silence.

## Final workflow

1. Verify `current.state: figure_production` and resolve the exact researcher recommendation reference.
2. Classify each recommendation as presentation-only, ambiguous, or a scientific-semantic change. Stop for clarification or semantic approval when needed.
3. Implement every in-scope recommendation. Record any recommendation that cannot be followed and why; do not silently omit it.
4. Keep data-derived figures and generalized diagrams distinct. Mark generalized diagrams as `figure_kind: schematic`, label them visibly, and do not let them replace complete data figures.
5. Use explicit grouping and uncertainty units from the TODO. Do not rely on an implicit plotting-library estimator when it would change the statistical unit.
6. Use clear descriptive titles, axis labels with units, declared scales, and a legend or direct label for every visual series or reference mark.
7. Export vector output (`.pdf` or `.svg`) and a raster preview (`.png`) when practical.
8. Write `figure_manifest.json`, linking every final figure to sources, plan entries, coverage, and researcher recommendations.
9. Execute the notebook from a clean kernel and verify every declared output.
10. Open and visually inspect every exported preview at its intended reading size; a manifest-only check cannot detect clipping, unreadable labels, overlapping marks, or ambiguous color encoding.
11. Write `figure_integrity_audit.json` and check coverage, statistical units, aggregation, titles, axes, units, scales, legends, marks, missingness, failure states, schematics, recommendation traceability, and rendered legibility.
12. Record `work_figures_complete`, `work_outputs_traceable`, `figure_source_coverage_complete`, `figure_integrity_audit_passed`, `figure_revision_needed`, `misleading_figure_risk_found`, and other applicable predicates with evidence.
13. Mark the `figure_production` decision boundary and return control for Codex transition evaluation.

## Preferred stack

Use Python in the notebook:

- processing: `numpy`, `scipy`, `pandas`;
- plotting: `matplotlib` as the primary API, `SciencePlots` for style contexts, and `seaborn` when its estimator and semantic mapping match the TODO;
- tabular I/O: pandas and PyArrow for Parquet or CSV;
- array I/O: NumPy, SciPy, h5py, or compatible readers as required.

Import `scienceplots` before selecting its styles. Prefer a `science` and `no-latex` context unless the environment explicitly supports the required fonts and LaTeX.

## Integrity rules

- Do not hide failed, missing, invalid, negative, low-performing, or inconvenient conditions.
- Do not pool trials, sessions, subjects, or seeds in a way that changes the independent unit.
- Do not recompute a new primary metric while plotting.
- Do not use titles such as "robust", "optimal", or "generalizable" unless the TODO defines the criterion and the plotted evidence supports it.
- Do not leave curves, bands, markers, colors, panels, or reference lines unexplained.
- Do not create a Markdown result or figure report.
- Keep all planning and final artifacts inside the referenced figure directory.

## Output contract

Planning mode produces an executed planning notebook, draft figures, `figure-plan.json`, `figure-coverage.json`, and `draft-figure-manifest.json`.

Final mode produces an executed final notebook, final exported figures, `figure_manifest.json`, and `figure_integrity_audit.json`.

Return the task-state path, mode, execution status, source and coverage results, recorded predicates, failures or ambiguities, and the mandatory next action: Codex must invoke `$research-state-transition` in Evaluate mode before any later lifecycle action.
