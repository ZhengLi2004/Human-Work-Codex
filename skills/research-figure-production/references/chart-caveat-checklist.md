# Chart Caveat Checklist

This checklist converts the [Data-to-Viz caveat collection](https://www.data-to-viz.com/caveats.html) into explicit planning and final-audit checks for this repository. The `DTV-Cxx` values are local stable identifiers for manifests; they are not names of new visualization concepts.

## Contents

1. [How to apply the checklist](#how-to-apply-the-checklist)
2. [Data, summaries, and uncertainty](#data-summaries-and-uncertainty)
3. [Axes and geometric encodings](#axes-and-geometric-encodings)
4. [Density, ordering, and clutter](#density-ordering-and-clutter)
5. [Color, labels, and consistency](#color-labels-and-consistency)
6. [Maps and terminology](#maps-and-terminology)
7. [Audit record](#audit-record)

## How to apply the checklist

During Planning mode:

1. Match every proposed figure to the trigger column below.
2. Add every matching ID to the figure plan and draft manifest.
3. Apply the check or select a lower-risk chart. Do not mark a caveat inapplicable merely because the current draft hides the condition that triggers it.

During Final mode:

1. Re-evaluate triggers against the rendered final figure, not only the plotting code.
2. Record `pass`, `fail`, or `not_applicable`, with evidence and a short reason.
3. Record `fail` when a triggered check was not performed or has no evidence; `unknown`, `pending`, and an empty evidence field cannot pass a final audit.
4. Treat an integrity failure as `figure_integrity_audit_passed: false`.
5. Treat a readability failure as revision-required unless the intended-size inspection demonstrates that the design remains unambiguous.
6. Preserve applicable data. A decluttering technique must not become an unapproved filter.

## Data, summaries, and uncertainty

| ID | Trigger | Required check or remedy | Effect if unresolved | Source |
|---|---|---|---|---|
| DTV-C05 | Histogram, density, violin, ridgeline, hexbin, or 2D density | Record bin edges, grid size, or bandwidth. Inspect reasonable alternatives during planning and do not select a setting only because it supports a preferred conclusion. | Integrity | [Bin size](https://www.data-to-viz.com/caveat/bin_size.html) |
| DTV-C06 | Boxplot or another compact distribution summary | Show or state group sample sizes and expose distribution shape with raw points, violin, raincloud, or a companion panel when shape matters. | Integrity | [Boxplot](https://www.data-to-viz.com/caveat/boxplot.html) |
| DTV-C07 | Error bar, ribbon, interval, or bar-plus-error display | Name the estimate and interval; compute them at the TODO-defined independent unit. Prefer points plus intervals and raw units when feasible. Do not leave SD, SE, CI, quantiles, or range ambiguous. | Integrity | [Error bars](https://www.data-to-viz.com/caveat/error_bar.html) |
| DTV-C14 | Labels, percentages, totals, compositions, node/link widths, or annotations contain calculated values | Reconcile displayed values to the source table; check totals, percentages, interval endpoints, and label-to-mark correspondence. | Integrity | [Calculation errors](https://www.data-to-viz.com/caveat/calculation_error.html) |
| DTV-C32 | Aggregate trend can differ across a grouping or control variable | Compare aggregate and relevant stratified views under the TODO's comparison boundaries. Do not pool away a reversal or confounder. | Integrity | [Simpson's paradox](https://www.data-to-viz.com/caveat/simpson.html) |

## Axes and geometric encodings

| ID | Trigger | Required check or remedy | Effect if unresolved | Source |
|---|---|---|---|---|
| DTV-C02 | Bar, area, line, or other magnitude comparison with a nonzero or truncated axis | Bars and filled magnitudes normally require a zero baseline. For lines, disclose truncation and choose limits that show variation without exaggerating it. Keep comparable panels on comparable scales unless the difference is explicit. | Integrity | [Y-axis baseline](https://www.data-to-viz.com/caveat/cut_y_axis.html) |
| DTV-C12 | Reversed axes, unusual direction, unfamiliar symbol meaning, or semantic colors | Follow field conventions unless the TODO or data require an exception; label the exception directly. | Integrity | [Counter-intuitive encodings](https://www.data-to-viz.com/caveat/counter_intuitive.html) |
| DTV-C13 | Two quantitative y-scales share one panel | Replace dual axes with aligned panels, indexing, normalization defined by the TODO, or separate plots. If unavoidable, record why scale choices cannot manufacture the apparent relationship. | Integrity | [Dual axes](https://www.datawrapper.de/blog/dualaxis) |
| DTV-C15 | Bars use polar or radial coordinates | Prefer Cartesian bars or dots. Radial distance and differing inner/outer widths must not distort magnitude. | Integrity | [Radial bars](https://www.data-to-viz.com/caveat/circular_barplot_accordeon.html) |
| DTV-C18 | Marker size encodes a quantitative value | Make marker area proportional to the value, reject negative inputs, and show a size legend with reference values. | Integrity | [Bubble area](https://www.data-to-viz.com/caveat/radius_or_area.html) |
| DTV-C20 | Circular bars are retained | Use a sufficiently large inner radius, repeat readable reference ticks, and verify that bar geometry still supports comparison. Prefer Cartesian alternatives. | Integrity | [Circular-bar distortion](https://www.data-to-viz.com/caveat/circular_bar_yaxis.html) |
| DTV-C21 | 3D bars, pies, scatter, or surfaces | Reject 3D bars and pies. Prefer 2D facets for scatter; use interactive 3D or a surface only when the third spatial dimension is essential and occlusion can be examined. | Integrity | [3D](https://www.data-to-viz.com/caveat/3d.html) |
| DTV-C22 | Line slope, geometric shape, or dense panel is sensitive to width/height | Inspect the intended output size and a reasonable aspect-ratio alternative. Avoid ratios that flatten, steepen, or hide patterns. | Integrity | [Aspect ratio](https://www.data-to-viz.com/caveat/aspect_ratio.html) |
| DTV-C23 | Bars, areas, or flows are stacked | Verify that the question concerns totals or composition. Provide a common-baseline alternative when individual groups must be compared; record stack order. | Integrity | [Stacking](https://www.data-to-viz.com/caveat/stacking.html) |
| DTV-C24 | Reader must subtract, sum, or compare displaced shapes to recover the intended quantity | Plot the derived comparison directly or add aligned labels/panels; do not require repeated mental arithmetic. | Readability | [Mental arithmetic](https://www.data-to-viz.com/caveat/mental_calculation.html) |
| DTV-C25 | Area represents a quantitative value | Prefer position or length for precise comparison. If area is necessary, state that it supports approximate magnitude and supply labels or a companion table. | Integrity | [Area perception](https://www.data-to-viz.com/caveat/area_hard.html) |
| DTV-C30 | Radar or spider chart | Keep groups and axes few, use commensurate and explicit scales, and compare against faceted bars, dots, or lines. Do not infer magnitude from polygon area. | Integrity | [Radar charts](https://www.data-to-viz.com/caveat/spider.html) |

## Density, ordering, and clutter

| ID | Trigger | Required check or remedy | Effect if unresolved | Source |
|---|---|---|---|---|
| DTV-C01 | Categories have no required scientific order | Use a meaningful order such as estimate, median, predefined sequence, or hierarchy and record it. Never reorder paired panels inconsistently. | Readability | [Ordering](https://www.data-to-viz.com/caveat/order_data.html) |
| DTV-C03 | Multiple lines become difficult to identify or compare at the intended reading size | Use small multiples, direct highlighting with complete context, or bounded subgroup panels. Do not delete applicable series. | Readability | [Spaghetti plots](https://www.data-to-viz.com/caveat/spaghetti.html) |
| DTV-C04 | Pie or doughnut chart | Prefer an ordered bar or dot plot. If retained for a simple whole, verify the denominator and 100% total, label slices directly, and never use 3D. | Integrity | [Pie charts](https://www.data-to-viz.com/caveat/pie.html) |
| DTV-C08 | Many distributions are overlaid | Use facets, violins, ridgelines, or a heatmap with common scales. Preserve all planned groups across the figure set. | Readability | [Multiple distributions](https://www.data-to-viz.com/caveat/multi_distribution.html) |
| DTV-C09 | Points or marks overlap | Reduce mark size, add transparency, use deterministic jitter for discrete coordinates, facet, or use hexbin/2D density. Sampling is allowed only when predefined and coverage remains explicit. | Integrity | [Overplotting](https://www.data-to-viz.com/caveat/overplotting.html) |
| DTV-C11 | Facets or small multiples are used | Choose rows/columns to fit labels and reading order; use common scales where comparison requires them and disclose free scales. | Readability | [Faceting](https://www.data-to-viz.com/caveat/small_multiple.html) |
| DTV-C16 | Points are connected | Confirm that the connection order is real—time, dose, rank, path, or another declared order. Do not connect independent unordered categories. | Integrity | [Connecting dots](https://www.data-to-viz.com/caveat/connect_your_dot.html) |
| DTV-C26 | Grouped bars or grouped marks | Keep marks from the same group visually adjacent and separate different groups; use consistent within-group order. | Readability | [Grouped bars](https://www.data-to-viz.com/caveat/grouped_bar.html) |
| DTV-C27 | Decorative elements, redundant encodings, heavy grids, or repeated labels compete with data | Remove non-informative elements while retaining units, uncertainty, coverage, missingness, failures, and reference marks needed for interpretation. | Readability | [Decluttering](https://www.data-to-viz.com/caveat/declutter.html) |
| DTV-C34 | Dense bars of similar length create a visual interference pattern | Try an ordered lollipop or dot plot, increase spacing, or split panels without removing categories. | Readability | [Data-to-Viz caveat index](https://www.data-to-viz.com/caveats.html) |

## Color, labels, and consistency

| ID | Trigger | Required check or remedy | Effect if unresolved | Source |
|---|---|---|---|---|
| DTV-C10 | Color encodes an ordered or continuous value | Use a perceptually ordered sequential or diverging palette with a meaningful midpoint; avoid rainbow palettes. Verify grayscale and common color-vision deficiencies when material. | Integrity | [Color palettes](https://www.datawrapper.de/blog/colors) |
| DTV-C17 | Multiple colors appear | Every color must encode a declared variable, status, emphasis, or uncertainty. Remove arbitrary categorical color changes. | Readability | [Meaningless color](https://www.data-to-viz.com/caveat/color_com_nothing.html) |
| DTV-C19 | Category labels are long or rotated | Prefer a horizontal plot, shorter defined labels, wrapping, or direct annotation. Preserve a mapping to full names. | Readability | [Long labels](https://www.data-to-viz.com/caveat/hard_label.html) |
| DTV-C28 | A legend or direct labels identify series, sizes, colors, bands, or marks | Explain every encoding and reference mark. Prefer direct labels when readable; otherwise keep legend order consistent with the plot. | Integrity | [Data-to-Viz caveat index](https://www.data-to-viz.com/caveats.html) |
| DTV-C29 | Several figures or panels reuse variables and groups | Keep color, marker, line style, ordering, units, and scale semantics consistent. Explicitly flag intentional changes. | Integrity | [Cross-chart consistency](https://www.data-to-viz.com/caveat/consistency.html) |
| DTV-C31 | Numerical heatmap or categorical status matrix | Declare row/column order. For numerical values, declare normalization, distance/clustering when used, color limits, midpoint, missing-cell encoding, and colorbar units. For status categories, use a discrete color or glyph mapping and define every state without a numerical colorbar. | Integrity | [Heatmap](https://www.data-to-viz.com/graph/heatmap.html) |
| DTV-C33 | Explanatory annotation is added | Tie annotations to displayed evidence, keep wording descriptive, and avoid unsupported causal or evaluative claims. | Integrity | [Annotation](https://www.data-to-viz.com/caveat/annotation.html) |

## Maps and terminology

| ID | Trigger | Required check or remedy | Effect if unresolved | Source |
|---|---|---|---|---|
| DTV-C35 | Choropleth or region-filled map | Use a defensible rate, proportion, density, or other normalized quantity when exposure differs. State the denominator and show missing or incomparable regions. | Integrity | [Data-to-Viz caveat index](https://www.data-to-viz.com/caveats.html) |
| DTV-C36 | Multiplicative change, broad orders of magnitude, or log axis | Use a log scale only when it matches the quantity and all values are valid. Label the scale and reference ratios; never conceal excluded zeros or negatives. | Integrity | [Log scales](https://www.datawrapper.de/blog/weeklychart-logscale3) |
| DTV-C37 | The chart or manifest names a choropleth | Spell and define `choropleth` correctly. This is terminology QA, not a scientific predicate. | Terminology | [Data-to-Viz caveat index](https://www.data-to-viz.com/caveats.html) |

## Audit record

For each final figure, include an entry like this in `figure_integrity_audit.json`:

```json
{
  "figure_id": "figure-02",
  "applicable_caveats": [
    {
      "id": "DTV-C07",
      "status": "pass",
      "evidence": "caption and legend define points as repeat means and whiskers as the TODO-defined 95% interval"
    },
    {
      "id": "DTV-C11",
      "status": "pass",
      "evidence": "one dataset per panel with common y limits and complete method-noise coverage"
    },
    {
      "id": "DTV-C28",
      "status": "pass",
      "evidence": "method colors are identified in display order and the failure marker is defined"
    }
  ],
  "failed_caveat_ids": [],
  "chart_specific_caveats_passed": true
}
```

Do not copy this evidence text into another task. Evidence must identify the rendered figure and its actual source, units, encodings, and inspection result.
