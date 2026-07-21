---
name: research-figure-production
description: Plan complete draft figures in work_postprocessing or produce researcher-reviewed final figures in figure_production. Use validated complete sources, executed Jupyter notebooks, mandatory SciencePlots styling, chart-selection and caveat references, coverage manifests, and final integrity audits. Use only the mode fixed by current.state; do not replace figure_review, promote temporary Python previews, cherry-pick data, or change lifecycle state.
---

# Research Figure Production

## Objective

Turn complete scientific tables or raw results into figures through three governed steps:

1. Planning mode selects graphical methods, maps all scientific table information to drafts, and prepares researcher-review material.
2. The separate `figure_review` state obtains interactive researcher recommendations.
3. Final mode implements those recommendations and checks that the final set is complete, traceable, and not misleading.

Read `references/figure-data-contract.md` before either mode. In Planning mode, read `references/chart-selection-guide.md` before selecting chart types and use `references/chart-caveat-checklist.md` to attach applicable caveat IDs. In Final mode, read `references/chart-caveat-checklist.md` before the integrity audit. Read `references/python-plotting-patterns.md` and copy or adapt `assets/scientific_plot_patterns.py` only when a matching implementation pattern is useful. Start from `assets/research_figures_template.ipynb` when useful.

## Rendering artifact boundary

- Generate every governed draft, final data figure, and retained schematic from an executed `.ipynb`. The executed notebook is the durable rendering source.
- Use a standalone `.py` script only for disposable metadata checks or provisional layout, style, legend, scale, density, or other visual cues. Create the script and all of its images under the platform temporary directory. Do not place them in the repository, result root, or figure directory.
- For a metadata-only probe, use clearly synthetic values that cannot be mistaken for task results. For an overlap, density, missingness, or condition-cardinality probe, use the complete validated source. Never choose an inspected subset because it produces a cleaner preview, and choose retained cues by intended-size legibility and caveat compliance rather than aesthetic preference.
- A repository or task-local `.py` helper may expose reusable functions imported and called by notebook cells. It must not be launched independently to create governed exports; the executed notebook owns the rendering call, configuration, outputs, and manifest record. Any image created by executing the helper as a standalone process is a temporary preview.
- Never promote a temporary preview. Reproduce any retained choice in the executed notebook before review, manifesting, auditing, or predicate evaluation. Reproduction means recreating the retained encoding and layout in notebook-executed code against the governed source, not copying the temporary image or requiring pixel identity.
- Import `scienceplots` and apply a stack based on `science` for every chart, including temporary previews. Default to `science` plus `no-latex`; record the exact stack for governed figures. Stop on a missing dependency rather than falling back silently.

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
4. Classify variable roles, data shape, analytical task, statistical unit, density, ordering, and group cardinality. Use `references/chart-selection-guide.md` to generate feasible candidates, not to override the TODO or a justified paper convention.
5. Compare candidates against complete coverage and the applicable checks in `references/chart-caveat-checklist.md`. Record rejected candidates and reasons. Do not choose a chart only because a Python example is available.
6. Build `figure-plan.json`, mapping each scientific field, TODO metric, planned condition, failure or missingness state, and research question to a proposed figure or panel. For each figure, record `data_shape`, `analytical_task`, `candidate_charts`, `selected_chart`, `selection_reason`, `rejected_chart_reasons`, `method_sources`, `python_reference_url`, `helper_reference`, `style_stack`, `applicable_caveat_ids`, and `coverage_strategy`.
7. Build `figure-coverage.json`, reconciling the planned condition skeleton and stable keys against the proposed set.
8. Create and execute the planning notebook from a clean kernel and export the complete draft figure set under `draft/`. Adapt gallery or helper code to the validated source and compute no hidden estimator, interval, filter, or model fit. Temporary `.py` previews do not count as drafts.
9. Write `draft-figure-manifest.json` with executed-notebook provenance, the exact SciencePlots style stack, method basis, chart-selection record, source classes, stable keys, statistical units, transformations, titles, axes, units, series labels, applicable caveat IDs, and coverage counts.
10. Update only the `Work figure directory` path in the TODO.
11. Record applicable predicates, including `figure_plan_complete`, `figure_method_basis_recorded`, `draft_figures_complete`, `figure_source_coverage_complete`, `figure_review_material_ready`, `work_outputs_traceable`, and risks or revision needs.
12. Mark the `work_postprocessing` decision boundary and return control for Codex transition evaluation. The eligible forward target is `figure_review`, not completion.

## Researcher-review material

Present, through `$human-research-review-gate` after the approved transition to `figure_review`:

- every draft figure and its intended question;
- the table-to-figure and condition-coverage summary;
- the graphical-method basis and any unavailable paper source;
- the selected chart, plausible rejected alternatives, inspected example links, and applicable chart-specific caveats;
- known tradeoffs, such as using facets instead of one crowded plot;
- a direct request to include, exclude, revise, or add figures, including optional generalized diagrams.

Wait for the researcher's output. Do not infer approval from silence.

## Final workflow

1. Verify `current.state: figure_production` and resolve the exact researcher recommendation reference.
2. Classify each recommendation as presentation-only, ambiguous, or a scientific-semantic change. Stop for clarification or semantic approval when needed.
3. Implement every in-scope recommendation. A clear presentation-only recommendation may change the planned chart or layout: preserve the original plan and record the plan-to-final change plus recommendation reference in the final manifest. Set `figure_plan_revision_needed` only when the table-to-figure mapping or draft set must return to Planning mode before faithful production can continue. Record any recommendation that cannot be followed and why; do not silently omit it.
4. Keep data-derived figures and generalized diagrams distinct. Mark generalized diagrams as `figure_kind: schematic`, label them visibly, and do not let them replace complete data figures.
5. Use explicit grouping and uncertainty units from the TODO. Do not rely on an implicit plotting-library estimator when it would change the statistical unit.
6. Use clear descriptive titles, axis labels with units, declared scales, and a legend or direct label for every visual series or reference mark. Apply and record a SciencePlots stack based on `science`; use `science` plus `no-latex` by default.
7. Export vector output (`.pdf` or `.svg`) and a raster preview (`.png`) when practical.
8. Write `figure_manifest.json`, linking every final figure to the executed notebook, execution timestamp, Python and plotting-package versions, exact SciencePlots style stack, sources, plan entries, chart-selection rationale, applicable caveat IDs, coverage, and researcher recommendations.
9. Execute the notebook from a clean kernel and verify every declared output.
10. Open and visually inspect every exported preview at its intended reading size; a manifest-only check cannot detect clipping, unreadable labels, overlapping marks, or ambiguous color encoding.
11. Write `figure_integrity_audit.json` and check executed-notebook provenance, the `science`-based SciencePlots stack, coverage, statistical units, aggregation, titles, axes, units, scales, legends, marks, missingness, failure states, schematics, recommendation traceability, rendered legibility, and every applicable `DTV-Cxx` entry. Record `pass`, `fail`, or `not_applicable` with evidence; unresolved integrity or readability failures prevent an audit pass.
12. Record `work_figures_complete`, `work_outputs_traceable`, `figure_source_coverage_complete`, `figure_integrity_audit_passed`, `figure_revision_needed`, `misleading_figure_risk_found`, and other applicable predicates with evidence.
13. Mark the `figure_production` decision boundary and return control for Codex transition evaluation.

## Preferred stack

Use Python in the notebook:

- processing: `numpy`, `scipy`, `pandas`;
- plotting: `matplotlib` as the primary API, mandatory `SciencePlots` with `science` as the base style, and `seaborn` only when its estimator and semantic mapping match the TODO;
- tabular I/O: pandas and PyArrow for Parquet or CSV;
- array I/O: NumPy, SciPy, h5py, or compatible readers as required.

Use `assets/scientific_plot_patterns.py` as optional boilerplate for explicit point-and-interval, histogram, empirical cumulative distribution, scatter, hexbin, ordered-series, heatmap, bubble-area, and export patterns. It plots supplied values and deliberately refuses common forms of silent row loss or implicit aggregation. Copy the helper beside the task notebook when used and record its repository revision; do not import it as an untracked external dependency.

The helper asset is a module imported and called by the executed notebook, not an alternative rendering document. Its `.py` extension does not permit governed figures to bypass notebook execution or delegate the only rendering call to a separately launched process.

Import `scienceplots` before selecting its styles. Apply `plt.style.use(["science", "no-latex"])` before creating axes, or keep figure creation, plotting, and export inside the equivalent style context. A tested journal, presentation, color-cycle, or language style may extend the stack, but it must retain `science` as the base and be recorded in the manifest.

## Integrity rules

- Do not hide failed, missing, invalid, negative, low-performing, or inconvenient conditions.
- Do not pool trials, sessions, subjects, or seeds in a way that changes the independent unit.
- Do not recompute a new primary metric while plotting.
- Do not inherit an example dataset, implicit estimator, confidence interval, binning rule, palette, title, annotation, or scientific claim from Data-to-Viz or a Python Gallery page.
- Do not save standalone `.py` previews under the repository or result tree, cite them as evidence, or copy them into `draft/` or `final/`.
- Do not render a chart without SciencePlots or silently use a fallback style when the package or requested style is unavailable.
- Do not mark a triggered caveat as inapplicable merely because the draft omitted the affected conditions or marks.
- Do not use titles such as "robust", "optimal", or "generalizable" unless the TODO defines the criterion and the plotted evidence supports it.
- Do not leave curves, bands, markers, colors, panels, or reference lines unexplained.
- Do not create a Markdown result or figure report.
- Keep all planning and final artifacts inside the referenced figure directory.

## Output contract

Planning mode produces an executed planning notebook, draft figures, `figure-plan.json`, `figure-coverage.json`, and `draft-figure-manifest.json`. Each planned figure includes its candidate/selection record, source links actually inspected, Python or copied-helper reference when used, applicable caveat IDs, and exact SciencePlots style stack.

Final mode produces an executed final notebook, final exported figures, `figure_manifest.json`, and `figure_integrity_audit.json`. The manifest records the notebook and exact SciencePlots style stack; the audit records those checks plus status and evidence for every applicable chart caveat.

Return the task-state path, mode, execution status, source and coverage results, recorded predicates, failures or ambiguities, and the mandatory next action: Codex must invoke `$research-state-transition` in Evaluate mode before any later lifecycle action.
