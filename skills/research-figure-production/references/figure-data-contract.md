# Figure Data Contract

## Sources

A figure may use complete valid raw results, complete condition-merged tables, validated row/key-preserving curated tables, or an explicit combination. Require a passing `aggregation-validation.json` for the same TODO fingerprint, analysis grain, and source hashes.

Record each source path, hash, stable key, selected columns, predefined filters, statistical unit, coverage counts, and display-only reshaping.

## Plotting-script boundary

The durable rendering source is an executed `.py` script under `TODO_###/exp/figures/`. Keep it separate from MATLAB computation code; store rendered artifacts under `TODO_###/data/figures/`.

The plotting script may validate, order, pivot, melt, facet, or reshape complete rows for presentation. It may not be the only production source for preprocessing, TODO metrics, inferential statistics, model fitting, exclusions, or aggregation. Produce any new scientific quantity in MATLAB and publish it in a complete table before plotting.

Every script imports `scienceplots` and uses `science` as the base style. Record the exact stack, script hash, execution command and times, Git revision, package versions, input/output hashes, data-quality result, and figure-data sufficiency.

## Complete information

Map every scientific field, metric, planned condition, coverage state, missing or failed state, and applicable nonstandard-parameter sensitivity to a figure/panel or an explicit coverage entry. Use facets, small multiples, separate figures, or a coverage panel when one chart would obscure information.

Operational provenance can remain in the manifest. Scientific omissions require the TODO-defined basis and researcher feedback.

## Planning and researcher feedback

Within `figure_review`, create the curated tables, plan, coverage manifest, plotting script, and complete drafts. Present all drafts with their source, statistical unit, method basis, style, and coverage. Record researcher requests to retain, exclude, revise, split, combine, or add a labeled schematic.

The first presentation sets `milestones.governed_figures_presented_at`. A later scientific TODO revision uses a versioned TODO derived from the current implementation.

## Final integrity

Check every final figure for:

- source, stable-key, condition, metric, coverage, and sensitivity completeness;
- correct grouping, statistical unit, estimate, and uncertainty;
- supported titles, axes, units, scales, and reference marks;
- labels for every curve, color, marker, band, and panel;
- visible or documented missing, failed, invalid, and incomparable conditions;
- faithful researcher-feedback implementation;
- separation of quantitative figures and labeled schematics;
- script, input, output, style, and environment traceability;
- intended-size readability.

Write `pass`, `fail`, or `not_applicable` with evidence for each applicable chart caveat. A blocking failure prevents completion.

## Manifest fields

For each figure record its identifier, stage, kind, files, question, source class and hash, stable key, conditions, filters, display shaping, statistical unit, coverage, method basis, chart choice, caveats, plotting script and hash, command and times, TODO fingerprint, task-state revision, Git revision, packages, style stack, exported hashes, researcher feedback, and labels.

Keep plotting scripts in `exp/figures/` and drafts, final exports, plans, coverage manifests, and audits in `data/figures/`. Create no Markdown result handoff.
