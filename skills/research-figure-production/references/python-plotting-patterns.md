# Python Plotting Patterns

After chart selection, copy only the needed helpers from `../assets/scientific_plot_patterns.py` into the task's `exp/figures/` plotting code. The helpers plot supplied production quantities without implicit aggregation and use `science` plus `no-latex` by default.

Copy only the needed helper code beside the task script. Record its repository revision, function, interpretation-affecting arguments, and exact SciencePlots stack. Keep the script separate from MATLAB computation.

## Precomputed estimates and intervals

Use the TODO-defined estimate and interval already present in the complete table.

```python
from scientific_plot_patterns import plot_interval_estimates, save_figure

figure, axes = plot_interval_estimates(
    summary,
    category="method",
    estimate="mean_accuracy",
    lower="ci95_low",
    upper="ci95_high",
    group="noise_level",
    category_order=METHOD_ORDER,
)
axes.set(xlabel="Accuracy (proportion)", ylabel="Method")
save_figure(figure, draft_dir / "accuracy-by-method")
```

Do not substitute a plotting-library interval for the supplied interval.

## Distribution and sensitivity

Use common explicit bin edges for group comparisons. Compare defensible bins rather than retaining only one supportive view; an empirical cumulative distribution is a useful companion.

```python
from scientific_plot_patterns import plot_ecdf, plot_histogram

histogram, hist_axes, edges = plot_histogram(
    valid_runs,
    value="latency_ms",
    group="method",
    bins=20,
    density=False,
)
ecdf, ecdf_axes = plot_ecdf(valid_runs, value="latency_ms", group="method")
```

For a nonstandard parameter, plot the complete tested sensitivity range and mark the approved value without hiding nearby failures or plateaus.

## Dense two-variable data

Start with all points. Use hexagonal bins instead of favorable sampling when saturation prevents reading.

```python
from scientific_plot_patterns import plot_hexbin, plot_scatter

points, point_axes = plot_scatter(
    observations,
    x="signal_db",
    y="error_rate",
    group="method",
    alpha=0.25,
    marker_area=10,
)
density, density_axes = plot_hexbin(
    observations,
    x="signal_db",
    y="error_rate",
    gridsize=35,
)
```

## Ordered series and panels

Reject duplicate x/group rows before plotting. Use panels under a predefined facet when many series become unreadable.

```python
from scientific_plot_patterns import plot_series

figure, axes = plt.subplots(1, len(DATASET_ORDER), sharex=True, sharey=True)
for axes_item, dataset in zip(axes, DATASET_ORDER, strict=True):
    panel = summary.loc[summary["dataset"] == dataset]
    plot_series(
        panel,
        x="noise_level",
        y="mean_accuracy",
        group="method",
        lower="ci95_low",
        upper="ci95_high",
        group_order=METHOD_ORDER,
        ax=axes_item,
    )
```

Use common limits for cross-panel magnitude comparisons or disclose free limits.

## Heatmaps

Pivot only after stable-key uniqueness is verified. Derive ordering and color limits from scientific meaning or a predefined rule.

```python
from scientific_plot_patterns import plot_heatmap

matrix = complete_table.pivot(
    index="method",
    columns="noise_level",
    values="mean_accuracy",
)
figure, axes = plot_heatmap(
    matrix,
    vmin=0.0,
    vmax=1.0,
    cmap="viridis",
    colorbar_label="Accuracy (proportion)",
    annotate=True,
)
```

Define missing-cell colors in the figure and reconcile them to coverage states.

## External examples

Use inspected gallery pages only for syntax or composition. Reimplement the pattern against validated task data and record the source. Do not copy example data, estimators, claims, or unexplained settings.
