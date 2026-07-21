# Figure Data Contract

## Contents

- [Logical source classes](#logical-source-classes)
- [Rendering artifact classes](#rendering-artifact-classes)
- [Complete-information rule](#complete-information-rule)
- [Graphical-method basis](#graphical-method-basis)
- [Statistical-unit rule](#statistical-unit-rule)
- [Researcher review contract](#researcher-review-contract)
- [Final integrity audit](#final-integrity-audit)
- [Traceability](#traceability)
- [Two worked examples](#two-worked-examples)
- [Outputs](#outputs)

## Logical source classes

1. **Raw computation results**: immutable per-run or per-task numerical outputs and their index.
2. **Condition-merged tables**: Codex-produced tables that align metrics and controls across complete condition keys.
3. **Validated curated tables**: Work-produced presentation tables whose transformation manifest proves row-count and stable-key preservation.

A logical source may be one file or a partitioned dataset directory. A figure may use any one class or an explicit combination. A curated table is a sufficient source only when it retains the metrics, conditions, coverage fields, and uncertainty fields required by the figure.

## Rendering artifact classes

Distinguish two classes before writing plotting code:

1. **Governed figure artifacts**: drafts presented in `figure_review`, final figures, and any schematic included in the final set. Generate these from an executed `.ipynb`, preserve its outputs, and keep the notebook, exports, plans, manifests, and audits in the TODO-referenced figure directory.
2. **Temporary diagnostic previews**: metadata checks or provisional layout, style, legend, scale, density, or other visual cues used only to decide how to implement the notebook. A standalone `.py` script is allowed for this class only. Put the script and every image it creates under the platform temporary directory, such as the path returned by `tempfile.mkdtemp`; do not put them under the repository, result root, or figure directory.

A `.py` helper stored beside the notebook is not a standalone renderer when it only defines reusable functions that notebook cells import and call. The notebook must own the rendering call, configuration, output paths, and manifest record. Launching that helper as a separate process makes its images temporary previews, even if the same file can also be imported.

Use clearly synthetic non-result values for a metadata-only layout or style probe. Use the complete validated source for a density, overlap, missingness, failure-state, or condition-cardinality probe; do not select a favorable subset after inspection. Retain a visual choice only for intended-size legibility, complete coverage, or an applicable caveat check—not because the preview looks attractive or supports a preferred conclusion. Reproduce means reimplementing the retained encoding and layout in notebook-executed code against the governed source, not copying pixels from the preview.

A temporary preview is disposable and cannot satisfy `draft_figures_complete`, `work_figures_complete`, `figure_source_coverage_complete`, `figure_integrity_audit_passed`, or any other artifact predicate. Do not cite its path in task state or a figure manifest. Reproduce any retained design choice in the executed notebook against the validated complete source.

Every Python chart in both classes imports SciencePlots and uses a style stack based on `science`. Use `science` plus `no-latex` by default. Record the exact stack for governed figures; a named journal, presentation, color-cycle, or language style may extend the stack only when it preserves legibility and the intended encoding. Missing SciencePlots blocks rendering rather than authorizing a fallback style.

## Complete-information rule

Across the planned figure set, account for every scientifically relevant table field, TODO metric, planned condition, failure or missingness state, and comparability or coverage field. Operational fields such as hashes or worker paths may remain only in the manifest when they do not encode scientific information.

For each data figure, use all applicable records from its selected logical source under TODO-defined inclusion and exclusion rules. Do not select a favorable file, partition, seed, subject, session, condition, metric, or range merely for presentation. When one plot would be unreadable, use facets, small multiples, linked panels, separate figures, or a coverage panel instead of dropping information.

Write a machine-readable coverage manifest that maps:

- source paths and source class;
- stable keys and planned-condition skeleton;
- scientific columns and TODO metrics;
- each condition, coverage state, failure state, and missingness state;
- the figure and panel where each item appears, or the explicit reason it remains table-only.

Display-only operations such as ordering, jitter, label shortening, and transparent axis limits must not change the measured population. Any scientific filter must already be defined by the TODO.

## Graphical-method basis

During Planning mode, inspect graphical methods in relevant papers identified by the TODO or research material when they are available. Record the paper, exact figure or section, and the graphical method adopted or rejected. Do not claim to have inspected a paper that was unavailable.

When no relevant paper is available, name the established convention used, such as a scatter plot with uncertainty intervals, a small-multiple line plot, a heatmap, or an empirical cumulative distribution. Explain why the encoding matches the variable types and comparison. Do not invent a label for an ordinary plot type.

Use `chart-selection-guide.md` to classify the input-data roles and analytical task, generate feasible candidates, and record why the selected chart preserves the TODO's statistical unit and complete-information requirements. Data-to-Viz and its linked Python Gallery pages are implementation references, not scientific authorities. A gallery example cannot define task filters, estimators, uncertainty, scales, labels, or claims.

Each figure-plan entry records the data shape, analytical task, candidate charts, selected chart, rejected-candidate reasons, method sources actually inspected, exact Python reference URL when used, SciencePlots style stack, applicable `DTV-Cxx` caveat IDs, and coverage strategy.

## Statistical-unit rule

The notebook must identify:

- the basic observation unit;
- the independent uncertainty or inference unit;
- grouping and pairing keys;
- the estimate and interval or error representation;
- whether plotted points are raw units, repeats, condition aggregates, or summaries.

Compute the estimate explicitly when seaborn or another high-level plotting function would aggregate at the wrong level.

## Researcher review contract

Planning mode produces drafts, not final figures. Present the drafts together with the coverage summary and method basis in the separate `figure_review` state. Ask the researcher which figures to include, exclude, revise, or supplement with a generalized diagram, then wait for the output.

A request to change metrics, inclusion rules, condition scope, statistical units, or scientific claims is a semantic-change request rather than a presentation instruction.

A generalized diagram must be marked `figure_kind: schematic`, visibly labeled as a schematic, and traced to the researcher's request and supported concepts. It must not resemble an empirical plot, imply a measured relationship, or replace the quantitative figures required for complete data coverage.

## Final integrity audit

Final mode writes `figure_integrity_audit.json`. Check every final figure for:

- complete applicable source, stable-key, condition, metric, and coverage representation;
- correct statistical unit, grouping, pairing, estimate, and uncertainty;
- titles that describe the displayed quantities and conditions without unsupported conclusions;
- axis labels, units, scale type, disclosed truncation, and comparable limits where comparison requires them;
- a legend or direct label for every curve, color, marker, band, panel, and reference line;
- visible or explicitly documented missing, failed, invalid, or incomparable conditions;
- faithful implementation of the recorded researcher recommendations;
- clear separation of data figures from schematics;
- confirmed generation from the executed notebook rather than a temporary script;
- a recorded SciencePlots style stack whose base is `science`;
- visual inspection of each rendered export for clipping, unreadable labels, overlapping marks, and ambiguous color encoding;
- explicit `pass`, `fail`, or `not_applicable` results with evidence for every applicable chart-specific check from `chart-caveat-checklist.md`.

Set `figure_integrity_audit_passed: true` only when every check passes. Otherwise identify affected figure IDs, set the relevant revision or risk predicates, and do not evaluate completion as eligible.

## Traceability

For every draft or final figure, its manifest records:

- figure identifier, stage, kind, and files;
- scientific question or TODO metric;
- source path, logical source class, source file list or dataset fingerprint;
- stable key, selected columns, and complete condition counts;
- predefined filters and display-only operations;
- transformation or aggregation function and statistical unit;
- sample, failure, missingness, and coverage counts;
- graphical-method basis;
- data shape, analytical task, candidate charts, selection rationale, rejected-candidate reasons, and inspected source URLs;
- exact Python example or copied helper reference when used;
- executed notebook path, execution timestamp, Python and plotting-package versions, and a `science`-based SciencePlots style stack;
- applicable caveat IDs and their final audit evidence;
- applicable researcher recommendation reference;
- title, axes, units, legend or direct-label specification;
- execution timestamp.

## Two worked examples

**Factorial result table:** A table contains method, noise level, repeat, accuracy, interval, and failure count. Use small multiples or a heatmap plus coverage panel so every method and noise level remains visible. A line plot containing only low-noise conditions is incomplete even if its trend is clearer.

**Requested generalized diagram:** The researcher asks for a pipeline overview after reviewing the data plots. Add a visibly labeled schematic and record `figure_kind: schematic`. Keep the full quantitative condition plots; do not draw a smooth curve in the schematic that could be mistaken for a measured trend.

## Outputs

Keep planning and final notebooks, drafts, final exports, coverage manifests, figure manifests, and integrity audits inside the single directory recorded in the TODO as `Work figure directory`. Do not add a Markdown figure report.
