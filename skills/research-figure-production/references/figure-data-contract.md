# Figure Data Contract

## Logical source classes

1. **Raw computation results**: immutable per-run/per-task numerical outputs and their index.
2. **Condition-merged tables**: Codex-produced tables that align metrics and controls across complete condition keys.
3. **Curated tables**: Work-produced, row/key-preserving presentation tables.

A logical source may be one file or a partitioned dataset directory.

## Completeness rule

Each figure must use all applicable records from at least one of the first two logical source classes—raw computation results or condition-merged tables—under the TODO-defined inclusion/exclusion rules. A figure may combine them when raw detail and condition-level structure are both needed. A curated table may be auxiliary, but it cannot be the sole source that satisfies this rule. The workflow may not select a favorable file, partition, seed, subject, session, or condition merely for presentation.

Display-only operations such as axis limits, ordering, jitter, or label shortening must not alter the measured population. Any scientific filter must already be defined by the TODO.

## Statistical-unit rule

The notebook must identify:

- the basic observation unit;
- the independent uncertainty/inference unit;
- grouping and pairing keys;
- the estimate and interval/error representation;
- whether plotted points are raw units, repeats, condition aggregates, or summaries.

Compute the estimate explicitly when seaborn or another high-level plotting function would aggregate at the wrong level.

## Traceability

For every exported figure, `figure_manifest.json` records:

- figure identifier and files;
- scientific question/TODO metric;
- source path(s) and logical source class;
- source file list or dataset fingerprint;
- stable key and selected columns;
- predefined filters and display-only operations;
- transformation/aggregation function;
- sample/coverage counts;
- export dimensions and formats;
- notebook path and execution timestamp.

## Outputs

Keep one executed notebook, the manifest, and all exported figures in the single directory recorded in the TODO as `Work figure directory`. Do not add a Markdown figure report.
