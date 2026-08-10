# Figure Notebook Reproducibility Contract

Use this contract for every governed planning or final figure notebook. Treat the notebook as a reader-facing rendering artifact over complete validated data. It must not replace the production pipeline.

## Required section order

Use these exact level-two headings so a reader and the validator can follow the notebook from top to bottom:

1. `## Execution summary`
2. `## Scope and parameters`
3. `## Sources and environment`
4. `## Data quality`
5. `## Figure contract`
6. `## Rendering`
7. `## Coverage and integrity`
8. `## Observed facts and limitations`

Put the TODO fingerprint, task-state revision, mode, complete input paths, stable keys, statistical unit, declared filters, output directory, and execution command near the top. Keep observed facts separate from interpretation and do not put unexecuted conclusions in the execution summary.

## Computation boundary

The notebook may:

- load complete raw, condition-merged, or validated curated tables;
- verify schemas, source hashes, stable keys, planned coverage, statuses, units, and figure-data sufficiency;
- sort, pivot, melt, facet, or otherwise reshape complete rows for presentation;
- compute display coordinates and other limited quantities that do not change scientific meaning.

The notebook must not be the only implementation of production preprocessing, TODO metrics, inferential statistics, model fitting, exclusion rules, or aggregation. If a proposed figure needs a new estimator, fitted parameter, test result, exclusion, or scientific quantity, stop and add it to the MATLAB-produced complete tables through the governed lifecycle first.

## Clean execution

Execute from a fresh kernel, top to bottom. Every nonempty code cell must have an execution count, execution counts must increase, and no code cell may contain an error output. Do not depend on variables created outside the notebook, hand-edit intermediate values, retain unexplained cached output, or hide a failed cell. Keep previews bounded with explicit `head`, row limits, selected columns, or summarized validation output; never dump an unrestricted large table.

Use this command or an equivalent clean-kernel executor and record the exact command:

```bash
python -m jupyter nbconvert --execute --to notebook --inplace path/to/notebook.ipynb
```

## Manifest contract

The planning manifest is `draft-figure-manifest.json`; the final manifest is `figure_manifest.json`. Both include:

- `schema_version`, `mode`, `todo_fingerprint`, and `task_state_revision`;
- `notebook.path`;
- `execution.command`, `execution.started_at_utc`, `execution.finished_at_utc`, `execution.clean_kernel`, and `execution.status`;
- `git_revision` and package versions for Python, Jupyter execution packages, NumPy, pandas, Matplotlib, and SciencePlots;
- every complete input path, SHA-256, source class, row count, stable-key fields, and schema;
- data-quality check IDs, status, observed values, expected rule, and evidence;
- figure-data sufficiency for every planned chart, including row count, observation grain, category or temporal point count when applicable, and honest fallback;
- exact style stack beginning with `science`;
- every exported figure path, SHA-256, figure ID, and format, plus path and SHA-256 for plan, coverage, and other declared machine-readable artifacts;
- notebook execution status and the plan, coverage, caveat, and researcher-recommendation references required by the selected mode.

Use UTC ISO 8601 timestamps. Resolve paths consistently and hash file bytes with SHA-256 after atomic publication. Do not use a directory mtime or file name as a content fingerprint.

## Deterministic validation

After clean execution, run:

```bash
python skills/research-figure-production/scripts/validate_figure_notebook.py \
  --notebook PATH --manifest PATH --mode planning|final --output PATH
```

The validator fails on an invalid notebook, missing required section, unresolved `REPLACE_*` or `TODO-XXX` placeholder, unexecuted code cell, error output, non-increasing execution counts, missing source hash, a style stack whose first entry differs from `science`, an incomplete execution record, or a declared export whose file or SHA-256 differs from the manifest. It writes deterministic JSON atomically.

In Final mode, pass the existing `figure_integrity_audit.json` as `--output`; the validator preserves the existing audit and adds `notebook_validation`. Set the audit's top-level pass to false whenever notebook validation fails. In Planning mode, write a machine-readable notebook-validation JSON beside the planning manifest; do not create a parallel Markdown report.
