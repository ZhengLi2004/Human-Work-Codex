# Chart Selection Guide

This reference adapts the [Data-to-Viz decision approach](https://www.data-to-viz.com/) to the governed scientific-figure workflow in this repository. Data-to-Viz classifies charts by input-data format, proposes feasible chart families, and then uses context and caveats to choose among them. Its authors describe the catalog as a starting point rather than an exhaustive rule set. The source snapshot inspected for this reference was repository commit [`253d428`](https://github.com/holtzy/data_to_viz/commit/253d428fdc4dd04c20bce6c1828448f423d27c05), and the source repository is [MIT-licensed](https://github.com/holtzy/data_to_viz/blob/253d428fdc4dd04c20bce6c1828448f423d27c05/LICENSE).

Use this guide as a candidate generator. The TODO, statistical unit, complete-information rule, researcher instructions, and graphical methods in relevant papers take precedence. A gallery example is implementation guidance, not scientific evidence and not permission to copy its estimator, filters, labels, or claims.

## Contents

1. [Selection procedure](#selection-procedure)
2. [Data-shape decision matrix](#data-shape-decision-matrix)
3. [Chart catalog](#chart-catalog)
4. [Required planning record](#required-planning-record)

## Selection procedure

For each proposed figure or panel:

1. Resolve the complete logical source and TODO-defined inclusion rules before considering appearance.
2. Record each variable's role: quantitative, categorical, ordered, temporal, geographic, hierarchical, node, edge, weight, estimate, interval, coverage, or failure state.
3. Record the observation unit, independent uncertainty unit, pairing or blocking keys, number of groups, number of observations, and whether values are raw observations or precomputed summaries.
4. State the analytical task: inspect a distribution, compare magnitudes, show a relationship, show change over an ordered axis, show composition, show spatial variation, or show structure or flow.
5. Generate feasible candidates from the matrix and catalog below. Include an established chart used by a relevant paper even when it is absent from Data-to-Viz.
6. Reject candidates that obscure applicable conditions, require unsupported aggregation, depend on imprecise area or angle comparisons, or become illegible at the intended reading size.
7. Prefer the candidate that answers the question with the fewest encodings while preserving complete condition and failure coverage.
8. Record the selected chart, alternatives considered, reasons, source links, Python example or copied-helper reference when used, and applicable caveat IDs from `chart-caveat-checklist.md`.

Do not select a chart only because matching code is available. Do not import a gallery dataset, title, annotation, threshold, palette, model fit, or default confidence interval into the research figure.

## Data-shape decision matrix

| Input and task | Preferred starting points | Conditional choices | Usually reject or replace |
|---|---|---|---|
| One quantitative variable; show distribution | Histogram with explicit bins; empirical cumulative distribution; raw points when feasible | Density plot with recorded bandwidth | A boxplot alone when shape or sample size matters |
| Quantitative observations by category | Raw points plus box/violin summary; faceted histograms or empirical cumulative distributions | Ridgeline for many ordered groups with readable overlap | Bars of means without the observations or a defined interval |
| Precomputed estimate and interval by category | Point-and-interval plot; horizontal dot/lollipop plot | Grouped point-and-interval plot | An implicit plotting-library estimator; decorative bars when zero is not meaningful |
| Two quantitative variables | Scatter plot with subgroup encoding | Hexbin or 2D density for severe overlap | Sampling away records solely for appearance; an unexplained fitted line |
| Three quantitative variables | Facet one variable or use color with a declared scale | Bubble plot when approximate magnitude is sufficient and area is scaled correctly | Static 3D scatter for routine comparison |
| Several quantitative variables per observation | Heatmap, correlogram, selected pair plots | Parallel coordinates for a small readable set; dimensionality-reduction view as a secondary analysis | Radar chart when precise comparison matters |
| One ordered or temporal series | Line with observed points; point-and-interval series | Area chart when a meaningful baseline and magnitude are central | Connecting unordered categories; an undisclosed truncated axis |
| Several ordered or temporal series | Faceted lines or small multiples with common scales | A limited set of directly labeled lines | Spaghetti plots, dual axes, or stacked areas when individual trends matter |
| Composition at one or more conditions | Stacked bars for coarse composition; direct values or dot plots for precise comparison | Treemap for hierarchical overview | Pie/doughnut charts for close comparisons; 3D or radial bars |
| Hierarchy or clustering | Dendrogram with declared distance/linkage; heatmap plus dendrogram | Treemap, circle packing, or sunburst for overview | Area-based hierarchy when exact values must be compared |
| Set membership and intersections | Direct counts; an intersection matrix for many sets | Venn diagram for two or three sets | Venn diagrams with many sets |
| Geographic values | Choropleth of an appropriate normalized quantity; point or bubble map; small multiples | Hexbin map or cartogram with an explicit purpose | Raw regional counts when exposure or population differs; an undisclosed projection |
| Nodes, edges, or flows | Adjacency matrix, network, Sankey, or arc diagram selected to match the question | Chord or bundled edges for bounded overview | Hairball networks; dropping scientifically applicable edges only to declutter |

## Chart catalog

The categories and links below come from Data-to-Viz. “Conditional” means the chart can be useful only when its perceptual and coverage limitations do not conflict with the TODO. A dash means the inspected Data-to-Viz snapshot did not provide a chart-specific Python Gallery link.

### Distribution

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Violin | Compare distribution shape across groups; show sample size and raw points when feasible. | [Data-to-Viz](https://www.data-to-viz.com/graph/violin.html) · [Python](https://python-graph-gallery.com/violin-plot/) |
| Density | Show a smoothed distribution; record bandwidth and facet rather than overlaying many groups. | [Data-to-Viz](https://www.data-to-viz.com/graph/density.html) · [Python](https://python-graph-gallery.com/density-plot/) |
| Histogram | Show counts or density with explicit common bin edges; inspect bin sensitivity. | [Data-to-Viz](https://www.data-to-viz.com/graph/histogram.html) · [Python](https://python-graph-gallery.com/histogram/) |
| Boxplot | Compactly summarize quartiles; supplement it when distribution shape or group size matters. | [Data-to-Viz caveat](https://www.data-to-viz.com/caveat/boxplot.html) · [Python](https://python-graph-gallery.com/boxplot/) |
| Ridgeline | Compare many distributions on a shared scale; overlap can conceal tails and values. | [Data-to-Viz](https://www.data-to-viz.com/graph/ridgeline.html) · — |

### Relationship and correlation

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Scatter | Show two quantitative variables; preserve subgroups and address overplotting without favorable sampling. | [Data-to-Viz](https://www.data-to-viz.com/graph/scatter.html) · [Python](https://python-graph-gallery.com/scatter-plot/) |
| Heatmap | Encode a matrix by color; declare normalization, order, missing cells, palette, and color limits. | [Data-to-Viz](https://www.data-to-viz.com/graph/heatmap.html) · [Python](https://python-graph-gallery.com/heatmap/) |
| Correlogram | Summarize pairwise associations for a bounded variable set; state the correlation definition and sample basis. | [Data-to-Viz](https://www.data-to-viz.com/graph/correlogram.html) · [Python](https://python-graph-gallery.com/correlogram/) |
| Bubble | Add a third quantitative variable to a scatter plot; scale marker area, show a size legend, and retain overlap visibility. | [Data-to-Viz](https://www.data-to-viz.com/graph/bubble.html) · [Python](https://python-graph-gallery.com/bubble-plot/) |
| Connected scatter | Connect points only when the connection order is meaningful and visible. | [Data-to-Viz](https://www.data-to-viz.com/graph/connectedscatter.html) · [Python](https://python-graph-gallery.com/connected-scatter-plot/) |
| 2D density or hexbin | Show dense joint distributions using all records; record grid or bandwidth and color scale. | [Data-to-Viz](https://www.data-to-viz.com/graph/density2d.html) · [Python](https://python-graph-gallery.com/2d-density-plot/) |

### Ranking and multivariable profiles

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Bar | Compare magnitudes from zero; sort when order is not scientifically fixed and distinguish it from a histogram. | [Data-to-Viz](https://www.data-to-viz.com/graph/barplot.html) · [Python](https://python-graph-gallery.com/barplot/) |
| Radar or spider | Conditional overview for very few profiles on commensurate scales; prefer faceted bars or lines for precise comparison. | [Data-to-Viz caveat](https://www.data-to-viz.com/caveat/spider.html) · [Python](https://python-graph-gallery.com/radar-chart/) |
| Word cloud | Usually reject for scientific comparison because position and area do not support precise frequency reading. | [Data-to-Viz](https://www.data-to-viz.com/graph/wordcloud.html) · [Python](https://python-graph-gallery.com/wordcloud/) |
| Parallel coordinates | Compare multivariable profiles for a small set; declare per-axis scaling and address line crossings. | [Data-to-Viz](https://www.data-to-viz.com/graph/parallel.html) · [Python](https://python-graph-gallery.com/parallel-plot/) |
| Lollipop or Cleveland dot plot | Compare ranked magnitudes or paired values; use a horizontal layout for long labels. | [Data-to-Viz](https://www.data-to-viz.com/graph/lollipop.html) · [Python](https://python-graph-gallery.com/lollipop-plot/) |
| Circular bar | Usually replace with a Cartesian bar or dot plot; radial baselines distort length comparison. | [Data-to-Viz](https://www.data-to-viz.com/graph/circularbarplot.html) · — |

### Part-to-whole and hierarchy

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Treemap | Show hierarchical composition when space is limited; area is unsuitable for precise comparisons. | [Data-to-Viz](https://www.data-to-viz.com/graph/treemap.html) · [Python](https://python-graph-gallery.com/treemap/) |
| Venn | Show membership for two or three sets with explicit counts; use an intersection matrix for more sets. | [Data-to-Viz](https://www.data-to-viz.com/graph/venn.html) · [Python](https://python-graph-gallery.com/venn-diagram/) |
| Doughnut | Usually replace with bars or points; angle and area comparisons are imprecise. | [Data-to-Viz](https://www.data-to-viz.com/graph/donut.html) · [Python](https://python-graph-gallery.com/donut-plot/) |
| Pie | Usually replace with bars or points; never use 3D and verify that a claimed whole is valid. | [Data-to-Viz caveat](https://www.data-to-viz.com/caveat/pie.html) · [Python](https://python-graph-gallery.com/pie-plot/) |
| Dendrogram | Show a hierarchy or clustering; record distance, linkage, orientation, and cut rule. | [Data-to-Viz](https://www.data-to-viz.com/graph/dendrogram.html) · [Python](https://python-graph-gallery.com/dendrogram/) |
| Circle packing | Conditional hierarchy overview; do not use circle area for exact comparison. | [Data-to-Viz](https://www.data-to-viz.com/graph/circularpacking.html) · — |
| Sunburst | Conditional radial hierarchy overview; comparisons across rings are difficult. | [Data-to-Viz](https://www.data-to-viz.com/graph/sunburst.html) · — |

### Evolution over an ordered axis

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Line | Show change along a real order or time axis; avoid dual axes and facet when series become crowded. | [Data-to-Viz](https://www.data-to-viz.com/graph/line.html) · [Python](https://python-graph-gallery.com/line-chart/) |
| Area | Emphasize magnitude relative to a meaningful baseline; do not use fill to imply an unsupported whole. | [Data-to-Viz](https://www.data-to-viz.com/graph/area.html) · [Python](https://python-graph-gallery.com/area-plot/) |
| Stacked area | Show total and coarse composition; individual series above the baseline are hard to compare. | [Data-to-Viz](https://www.data-to-viz.com/graph/stackedarea.html) · [Python](https://python-graph-gallery.com/stacked-area-plot/) |
| Streamgraph | Use only for an overview of relative composition; it is poor for reading individual trajectories. | [Data-to-Viz](https://www.data-to-viz.com/graph/streamgraph.html) · [Python](https://python-graph-gallery.com/streamchart/) |

### Maps

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Background map | Provide geographic context; record projection, extent, boundary source, and coordinate system. | [Data-to-Viz](https://www.data-to-viz.com/graph/map.html) · [Python](https://python-graph-gallery.com/map/) |
| Choropleth | Map a defensible normalized regional quantity; disclose denominator, classification, missing regions, and palette. | [Data-to-Viz](https://www.data-to-viz.com/graph/choropleth.html) · [Python](https://python-graph-gallery.com/choropleth-map/) |
| Hexbin map | Reduce region-size bias with equal cells; retain enough geographic landmarks for interpretation. | [Data-to-Viz](https://www.data-to-viz.com/graph/hexbinmap.html) · [Python examples](https://python-graph-gallery.com/2d-density-plot/) |
| Cartogram | Distort geography to emphasize another quantity; use only when the distortion is part of the question and clearly explained. | [Data-to-Viz](https://www.data-to-viz.com/graph/cartogram.html) · — |
| Connection map | Show geographic links; disclose direction, weight, projection, and drawing order, and address overlap. | [Data-to-Viz catalog](https://www.data-to-viz.com/#connection) · [Python](https://python-graph-gallery.com/connection-map/) |
| Bubble map | Show magnitudes at locations; scale bubble area, provide a size legend, and handle overlap. | [Data-to-Viz](https://www.data-to-viz.com/graph/bubblemap.html) · [Python](https://python-graph-gallery.com/bubble-map/) |

### Networks and flows

| Chart | Use and repository-specific caution | Source and linked Python examples |
|---|---|---|
| Chord | Conditional overview of bounded flows; explain direction and width and minimize crossings. | [Data-to-Viz](https://www.data-to-viz.com/graph/chord.html) · [Python](https://python-graph-gallery.com/chord-diagram/) |
| Network | Show nodes and edges when topology is the question; disclose layout and prevent a hairball from hiding structure. | [Data-to-Viz](https://www.data-to-viz.com/graph/network.html) · [Python](https://python-graph-gallery.com/network-chart/) |
| Sankey or alluvial | Show conserved or staged flows; verify node/link arithmetic and minimize crossings. Do not remove applicable weak flows merely to improve appearance. | [Data-to-Viz](https://www.data-to-viz.com/graph/sankey.html) · [Python](https://python-graph-gallery.com/sankey-diagram/) |
| Arc | Show ordered nodes and edges; the node order determines which clusters or bridges appear. | [Data-to-Viz](https://www.data-to-viz.com/graph/arc.html) · [Python Gallery index](https://python-graph-gallery.com/) |
| Hierarchical edge bundling | Conditional hierarchy-and-edge overview; bundling can conceal individual paths and direction. | [Data-to-Viz](https://www.data-to-viz.com/graph/edge_bundling.html) · — |

## Required planning record

Add these fields to each `figure-plan.json` entry:

- `data_shape`: variable roles, cardinalities, density, order, and raw-versus-summary status;
- `analytical_task`;
- `statistical_unit` and `uncertainty_unit`;
- `candidate_charts`: feasible candidates actually considered;
- `selected_chart` and `selection_reason`;
- `rejected_chart_reasons`;
- `method_sources`: relevant-paper figure references and/or Data-to-Viz links actually inspected;
- `python_reference_url`: exact example page used, or `null`;
- `helper_reference`: copied helper path, function, and repository revision, or `null`;
- `style_stack`: exact SciencePlots stack beginning with `science`;
- `applicable_caveat_ids`: stable IDs from `chart-caveat-checklist.md`;
- `coverage_strategy`: panel, facet, series, missingness, and failure-state mapping.

Example:

```json
{
  "figure_id": "figure-02",
  "data_shape": "precomputed estimate and 95% interval by method and noise level",
  "analytical_task": "compare methods across every planned noise level",
  "statistical_unit": "independent repeat",
  "uncertainty_unit": "repeat-level estimate",
  "candidate_charts": ["grouped bar with intervals", "faceted point-and-interval plot"],
  "selected_chart": "faceted point-and-interval plot",
  "selection_reason": "shows each estimate and interval without a decorative bar baseline or crowded grouping",
  "rejected_chart_reasons": {
    "grouped bar with intervals": "requires dense grouping and makes interval endpoints harder to compare"
  },
  "method_sources": [
    "https://www.data-to-viz.com/caveat/error_bar.html"
  ],
  "python_reference_url": null,
  "helper_reference": "assets/scientific_plot_patterns.py::plot_interval_estimates at REPOSITORY_REVISION",
  "style_stack": ["science", "no-latex"],
  "applicable_caveat_ids": ["DTV-C07", "DTV-C11", "DTV-C28"],
  "coverage_strategy": "one panel per dataset; every method-noise combination and failed condition is accounted for"
}
```

This example illustrates the record shape only. It does not define a metric, interval, threshold, or chart for another TODO.
