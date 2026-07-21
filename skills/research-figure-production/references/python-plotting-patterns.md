# Python Plotting Patterns

## Contents

- [Purpose and boundaries](#purpose-and-boundaries)
- [Temporary diagnostic scripts](#temporary-diagnostic-scripts)
- [Precomputed point and interval estimates](#precomputed-point-and-interval-estimates)
- [Histogram sensitivity and empirical cumulative distribution](#histogram-sensitivity-and-empirical-cumulative-distribution)
- [Dense two-variable data](#dense-two-variable-data)
- [Ordered series and small multiples](#ordered-series-and-small-multiples)
- [Heatmap with explicit limits and missing cells](#heatmap-with-explicit-limits-and-missing-cells)
- [External example pages](#external-example-pages)

## Purpose and boundaries

Use `../assets/scientific_plot_patterns.py` as optional notebook boilerplate after chart selection. The helpers require SciencePlots, activate `science` plus `no-latex` on import, use pandas, NumPy, and Matplotlib, plot every supplied valid row, require explicit bins, intervals, color limits, or grid sizes where defaults can alter interpretation, and publish exported figures atomically.

They do not:

- choose TODO inclusion or exclusion rules;
- aggregate observations or calculate uncertainty;
- drop missing or failed rows;
- choose a chart on the basis of appearance;
- write coverage, planning, or integrity manifests.

Copy the helper beside the task notebook when used. Record its path, function, arguments that affect interpretation, and repository revision in the figure manifest. Adapt titles, labels, units, scales, palettes, and output paths to the TODO.

The import activates `("science", "no-latex")`. When a tested output requirement needs an additional SciencePlots style, call `activate_scienceplots_style(extra_styles=("STYLE_NAME",))` before creating any axes and record the returned stack. Use `use_latex=True` only after the execution environment proves the required LaTeX and fonts are available.

## Temporary diagnostic scripts

Use a standalone `.py` file only to inspect metadata or provisional layout, style, legend, scale, density, or another visual cue. Allocate a directory below the platform temp root first, put the script there, and write every image beside it. Do not write a probe into the repository, result root, notebook directory, `draft/`, or `final/`.

Use clearly synthetic non-result values for metadata-only layout or style probes. Use the complete validated source for density, overlap, missingness, failure-state, or condition-cardinality probes; never select a convenient or favorable subset after inspection. Retain a cue only because it improves intended-size legibility, complete coverage, or caveat compliance.

Minimal probe skeleton:

```python
from pathlib import Path
import tempfile

import matplotlib.pyplot as plt
import scienceplots  # registers the styles

SYSTEM_TEMP = Path(tempfile.gettempdir()).resolve()
PROBE_DIR = Path(__file__).resolve().parent
if PROBE_DIR != SYSTEM_TEMP and SYSTEM_TEMP not in PROBE_DIR.parents:
    raise RuntimeError("Run this diagnostic script from a directory under the platform temp root")

STYLE_STACK = ["science", "no-latex"]
def render_layout_probe(preview_frame):
    with plt.style.context(STYLE_STACK):
        fig, ax = plt.subplots(figsize=(4.0, 2.5), constrained_layout=True)
        ax.plot(preview_frame["x"], preview_frame["y"], label="layout probe")
        ax.legend()
        output = PROBE_DIR / "layout-probe.png"
        fig.savefig(output, dpi=150, bbox_inches="tight")
        plt.close(fig)
    return output
```

Inspect the temporary image, then remove the probe directory when it is no longer needed. The script and image are not research artifacts or evidence. If the choice is retained, reimplement the encoding and layout in the executed notebook against the governed source, then record the notebook export and style stack; do not copy the preview image or require pixel identity.

## Precomputed point and interval estimates

Use when the aggregation table already contains the TODO-defined estimate and interval. The helper rejects incomplete category/group grids and intervals that do not contain the estimate.

```python
from scientific_plot_patterns import plot_interval_estimates, save_figure

fig, ax = plot_interval_estimates(
    summary,
    category="method",
    estimate="mean_accuracy",
    lower="ci95_low",
    upper="ci95_high",
    group="noise_level",
    category_order=METHOD_ORDER,
)
ax.set(
    title="Accuracy by method and noise level",
    xlabel="Accuracy (proportion)",
    ylabel="Method",
)
paths = save_figure(fig, final_dir / "accuracy-by-method")
```

Do not substitute a plotting-library confidence interval for the supplied interval.

## Histogram sensitivity and empirical cumulative distribution

Use common explicit bin edges for group comparisons. During planning, compare a small number of defensible bin choices and record them; do not retain only the one that supports a preferred interpretation. An empirical cumulative distribution is a useful unsmoothed companion.

```python
from scientific_plot_patterns import plot_ecdf, plot_histogram

fig_hist, ax_hist, edges = plot_histogram(
    valid_runs,
    value="latency_ms",
    group="method",
    bins=20,
    density=False,
)
ax_hist.set(xlabel="Latency (ms)", ylabel="Independent-run count")

fig_ecdf, ax_ecdf = plot_ecdf(valid_runs, value="latency_ms", group="method")
ax_ecdf.set(xlabel="Latency (ms)", ylabel="Empirical cumulative proportion")
```

Failed or missing runs must remain visible in a companion coverage element and the manifest; do not silently pass only successful rows without documenting the TODO-defined status handling.

## Dense two-variable data

Start with all points using size and transparency. If the rendered preview remains saturated, use an explicit hexagonal grid rather than favorable sampling.

```python
from scientific_plot_patterns import plot_hexbin, plot_scatter

fig_points, ax_points = plot_scatter(
    observations,
    x="signal_db",
    y="error_rate",
    group="method",
    alpha=0.25,
    marker_area=10,
)

fig_density, ax_density = plot_hexbin(
    observations,
    x="signal_db",
    y="error_rate",
    gridsize=35,
)
```

The hexbin view encodes counts, not individual identity. Keep stable-key coverage in `figure-coverage.json`.

## Ordered series and small multiples

The helper rejects duplicate x/group rows so that aggregation cannot occur implicitly. When many series form a spaghetti plot, create panels under a complete, predefined facet variable.

```python
from scientific_plot_patterns import plot_series

fig, axes = plt.subplots(1, len(DATASET_ORDER), sharex=True, sharey=True, constrained_layout=True)
for ax, dataset in zip(axes, DATASET_ORDER, strict=True):
    panel = summary.loc[summary["dataset"] == dataset]
    plot_series(
        panel,
        x="noise_level",
        y="mean_accuracy",
        group="method",
        lower="ci95_low",
        upper="ci95_high",
        group_order=METHOD_ORDER,
        ax=ax,
    )
    ax.set_title(str(dataset))
```

Use common limits when cross-panel magnitude comparison is intended. If free limits are necessary, disclose them on the figure and in the audit.

## Heatmap with explicit limits and missing cells

Pivot only after validating that the row/column keys are unique. Choose normalization, ordering, `vmin`, `vmax`, and any midpoint from scientific meaning or a predefined rule.

```python
from scientific_plot_patterns import plot_heatmap

matrix = complete_table.pivot(index="method", columns="noise_level", values="mean_accuracy")
fig, ax = plot_heatmap(
    matrix,
    vmin=0.0,
    vmax=1.0,
    cmap="viridis",
    colorbar_label="Accuracy (proportion)",
    annotate=True,
)
ax.set(xlabel="Noise level (dB)", ylabel="Method")
```

The missing-cell color is not a numerical value. Define it in the legend or caption and reconcile it to coverage and failure states.

## External example pages

After choosing a chart, use the exact Python Gallery link in `chart-selection-guide.md` for syntax or composition ideas. Reimplement the pattern against the task's validated tables and mandatory SciencePlots style stack. Do not copy example data, estimators, claims, or unexplained visual settings.
