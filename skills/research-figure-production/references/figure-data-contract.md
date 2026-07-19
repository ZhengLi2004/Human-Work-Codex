# Figure Data Contract

## Logical source classes

1. **Raw computation results**: immutable per-run or per-task numerical outputs and their index.
2. **Condition-merged tables**: Codex-produced tables that align metrics and controls across complete condition keys.
3. **Validated curated tables**: Work-produced presentation tables whose transformation manifest proves row-count and stable-key preservation.

A logical source may be one file or a partitioned dataset directory. A figure may use any one class or an explicit combination. A curated table is a sufficient source only when it retains the metrics, conditions, coverage fields, and uncertainty fields required by the figure.

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
- clear separation of data figures from schematics.
- visual inspection of each rendered export for clipping, unreadable labels, overlapping marks, and ambiguous color encoding.

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
- applicable researcher recommendation reference;
- title, axes, units, legend or direct-label specification;
- notebook path and execution timestamp.

## Two worked examples

**Factorial result table:** A table contains method, noise level, repeat, accuracy, interval, and failure count. Use small multiples or a heatmap plus coverage panel so every method and noise level remains visible. A line plot containing only low-noise conditions is incomplete even if its trend is clearer.

**Requested generalized diagram:** The researcher asks for a pipeline overview after reviewing the data plots. Add a visibly labeled schematic and record `figure_kind: schematic`. Keep the full quantitative condition plots; do not draw a smooth curve in the schematic that could be mistaken for a measured trend.

## Outputs

Keep planning and final notebooks, drafts, final exports, coverage manifests, figure manifests, and integrity audits inside the single directory recorded in the TODO as `Work figure directory`. Do not add a Markdown figure report.
