# Figure Data Contract

## Sources

A figure may use complete valid raw results, complete condition-merged tables, validated row/key-preserving curated tables, or an explicit combination. Require a passing `aggregation-validation.json` for the same TODO fingerprint, analysis grain, and source hashes.

Record each source path, hash, stable key, selected columns, predefined filters, statistical unit, coverage counts, and display-only reshaping.

For statistical results, apply the [statistical evidence contract](../../research-statistical-analysis/references/statistical-evidence-contract.md). Map each panel and annotation to produced analysis IDs. Captions identify exact per-group n and what it counts, replicate/dependence structure, summaries, interval/error-bar type, and applicable comparison, test, sidedness, and adjustment method. Link complete numerical results when they cannot fit the caption. SD, SEM, confidence, prediction, and credible intervals retain their distinct meanings. Significance symbols require a declared threshold and traceable produced value.

## Plotting-script boundary

The durable rendering source is an executed `.py` script under `TODO_###/exp/figures/`. Keep it separate from MATLAB computation code; store rendered artifacts under `TODO_###/data/figures/`.

The plotting script may validate, order, pivot, melt, facet, or reshape complete rows for presentation. It may not be the only production source for preprocessing, TODO metrics, inferential statistics, model fitting, exclusions, or aggregation. Produce any new scientific quantity in MATLAB and publish it in a complete table before plotting.

Every script imports `scienceplots` and uses `science` as the base style. Seaborn may provide semantic plotting or post-render conveniences when it does not add an implicit estimate or replace that base.

## Rendering and publication style

Map every scientific field, metric, planned condition, coverage state, missing or failed state, and applicable nonstandard-parameter sensitivity to a figure/panel or an explicit coverage entry. Use facets, small multiples, separate figures, or a coverage panel when one chart would obscure information.

Render this complete mapping before publication styling. Then apply the chosen profile from `journal-figure-style.md` to the whole figure. The post-render pass may set physical size, typography, non-data strokes, panel labels, shared labels, legend placement, spacing, and export properties; it may not change data, estimates, filters, scientifically chosen limits, or coverage.

The plan records the official profile sources and check date, final width and height, panel grid and reading order, font and line ranges, title policy, and export formats. Put the figure title in the caption or legend. Record any necessary facet heading as a data label.

## Planning and researcher feedback

Within `figure_review`, create the curated tables, plan, coverage manifest, plotting script, and complete drafts. Present all drafts as thumbnails with links to full-resolution exports and their source, statistical unit, method basis, profile, and coverage. Record researcher requests to retain, exclude, revise, split, combine, or add a labeled schematic.

The first presentation sets `milestones.governed_figures_presented_at`. A later scientific TODO revision uses a versioned TODO derived from the current implementation.

## Final integrity

Check every final figure using data, metadata, and programmatic evidence first; open thumbnails only when necessary. Full-resolution exports remain deliverables, not routine inspection inputs. Record the method used and unresolved limitations; a thumbnail alone does not establish fine-detail readability. Check for:

- source, stable-key, condition, metric, coverage, and sensitivity completeness;
- correct grouping, statistical unit, estimate, and uncertainty;
- per-analysis sample counts, complete comparison coverage, and traceable statistical annotations/captions;
- caption-based figure title and only planned in-artwork headings;
- final physical size, aspect ratio, panel order and alignment, shared labels and legends, whitespace, fonts, strokes, and export resolution;
- supported axes, units, scales, and reference marks;
- labels for every curve, color, marker, band, and panel;
- visible or documented missing, failed, invalid, and incomparable conditions;
- faithful researcher-feedback implementation;
- separation of quantitative figures and labeled schematics;
- script, input, output, style, and environment traceability;
- intended-size readability and unclipped content.

Write `pass`, `fail`, or `not_applicable` with evidence for each applicable chart caveat. A blocking failure prevents completion.

## Manifest fields

For each figure record its identifier, stage, kind, files, question, source class and hash, stable key, conditions, filters, display shaping, statistical unit, coverage, method basis, chart choice, caveats, plotting script and hash, command and times, TODO fingerprint, task-state revision, Git revision, packages, style stack, publication profile, post-render style audit, exported hashes, researcher feedback, and labels.

The profile contains its name, source URLs and check date, final dimensions, font family and size, line width, panel-label style, raster DPI, and export formats. The style audit has this compact shape; detailed evidence stays in `figure_integrity_audit.json`:

```json
{
  "applied_after_data_rendering": true,
  "scienceplots_base_preserved": true,
  "figure_title_inside_artwork": false,
  "profile_match_checked": true,
  "layout_checked": true,
  "final_size_readable": true
}
```

Keep plotting scripts in `exp/figures/` and drafts, final exports, plans, coverage manifests, and audits in `data/figures/`. Create no Markdown result handoff.
