# Journal Figure Style

Use the current instructions for the named target journal. The profiles below are a checked snapshot from 2026-08-29; recheck the linked source before final export when the journal is known. Do not combine exact values from different profiles. For another journal, record its official source and use a custom profile.

## Two-pass workflow

These profiles govern presentation. Statistical design and reporting use [CNS statistical reporting sources](../../research-statistical-analysis/references/cns-statistical-reporting.md) and the statistical evidence contract; visual conformity alone does not establish statistical or submission compliance.

1. Complete the scientific rendering first: data, estimates, uncertainty, conditions, failures, scales, and panel mapping.
2. After all data artists exist, apply one publication-style pass to the whole figure. It may change canvas size, typography, non-data strokes, panel labels, legend placement, shared labels, spacing, and export settings. It may not change data, estimators, filters, limits chosen for scientific reasons, or coverage.
3. Check dimensions, typography, clipping, and layout from export metadata and renderer geometry. Inspect a thumbnail only if a visual ambiguity remains; record unresolved readability limits.

Keep the `science` SciencePlots style as the base. Seaborn may express semantic mappings during rendering and provides useful post-render operations such as `despine` and `move_legend`; do not let `set_theme` replace the SciencePlots base, and do not invoke implicit estimators. Figure titles belong in the manuscript caption or legend. A short facet heading that identifies a condition is a data label, not a figure title, and must be recorded in the plan.

For multi-panel figures, choose the final page slot before arranging panels. Export all panels as one figure file, follow the journal's label order, use shared axes or legends where they preserve meaning, and allocate panel area by content rather than forcing every panel to the same shape.

## Profiles

### Nature

- Main widths: 89 mm or 183 mm; maximum height: 170 mm.
- Arial or Helvetica, 5–7 pt for ordinary text; panel labels are bold upright lowercase letters at 8 pt.
- Final line weights: 0.25–1 pt. Keep graph text and line art editable and vector-based where possible.
- Arrange panels alphabetically, minimize unused space, and size each panel for its content and legibility.
- Use accessible colors; avoid red/green combinations, rainbow scales, colored text, and low-contrast text.

Sources: [Nature research figure guide](https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/) and [Nature final submission](https://www.nature.com/nature/for-authors/final-submission).

### Science

- Printed widths: 57 mm, 121 mm, or 184 mm for one, two, or three columns.
- Helvetica is preferred. Ordinary text should reduce to about 7 pt and never below 5 pt; panel labels are bold uppercase letters at 10 pt.
- Lines must remain at least 0.5 pt at final size. Prefer vector PDF, EPS, or AI; raster content must be at least 300 dpi at final size and must not be upsampled.
- Put the figure title at the start of the caption, not in the artwork. Set panels close together, avoid repeated common axis labels, and maximize space used for data.
- Use SI units and scale bars. Avoid unnecessary grid lines, minor ticks, similar hues, and red/green combinations.

Sources: [Science initial-manuscript instructions](https://www.science.org/content/page/instructions-preparing-initial-manuscript) and [Science revised-manuscript instructions](https://www.science.org/content/page/instructions-preparing-revised-manuscript).

### Cell and Cell Press

- For ordinary two-column articles, widths are 85 mm, 114 mm, or 174 mm; keep the figure on one page and normally no taller than 200 mm.
- Use Arial at 6–8 pt, uppercase panel labels, and 0.5–1.5 pt strokes.
- Upload every panel of a main figure together in one file. Keep the title and legend in the manuscript, not in the image, and minimize vertical gaps.
- Prefer PDF for vector or mixed content and TIFF for raster content. Minimum final-size resolution is 300 dpi for color or grayscale, 500 dpi for black-and-white, and 1,000 dpi for line art; use RGB.
- For quantitative graphs, show individual observations as well as the declared summary when applicable. Preserve original image data and disclose stitching or other permitted processing.

Sources: [Cell Press figure guidelines](https://www.cell.com/information-for-authors/figure-guidelines) and [Cell final-submission instructions](https://www.cell.com/cell/information-for-authors/final-submission#main-figures).

## Final-size audit

Record the profile name, official source URLs and check date, final width and height in millimetres, font and stroke choices, raster DPI when applicable, and export formats. The audit passes only when the figure has no unexplained in-artwork title, every panel is in the composite, text and lines remain readable at final size, and spacing does not distort the intended reading order.
