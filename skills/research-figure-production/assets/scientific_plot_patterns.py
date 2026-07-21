"""Reusable plotting patterns for governed research figures.

These functions are original repository helpers informed by the chart-selection
and caveat references in ``../references``. They accept already validated raw
or precomputed tables. They do not choose scientific filters, aggregate
observations, estimate uncertainty, or replace figure coverage checks.

Copy this file beside an executed figure notebook when a matching pattern is
useful, then record the copied path and function name in the figure manifest.
Importing this module activates the required SciencePlots ``science`` and
``no-latex`` style stack.
"""

from __future__ import annotations

import os
import tempfile
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

try:
    import scienceplots  # noqa: F401; registers SciencePlots styles
except ImportError as exc:
    raise ImportError(
        "SciencePlots is required for every chart in this repository. "
        "Install the repository requirements instead of using a fallback style."
    ) from exc


SCIENCEPLOTS_BASE_STYLE = "science"
SCIENCEPLOTS_DEFAULT_STYLE_STACK = (SCIENCEPLOTS_BASE_STYLE, "no-latex")
_active_scienceplots_style_stack = SCIENCEPLOTS_DEFAULT_STYLE_STACK


DEFAULT_COLORS = (
    "#0072B2",  # blue
    "#D55E00",  # vermillion
    "#009E73",  # bluish green
    "#CC79A7",  # reddish purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
    "#000000",  # black
)


def activate_scienceplots_style(
    extra_styles: Sequence[str] = (),
    *,
    use_latex: bool = False,
) -> tuple[str, ...]:
    """Activate and return a SciencePlots stack whose base is always ``science``."""

    extras = tuple(str(style).strip() for style in extra_styles)
    if any(not style for style in extras):
        raise ValueError("SciencePlots style names must be non-empty")
    if SCIENCEPLOTS_BASE_STYLE in extras or "no-latex" in extras:
        raise ValueError("Pass only additional styles; science and no-latex are managed here")
    stack = (SCIENCEPLOTS_BASE_STYLE, *extras)
    if not use_latex:
        stack = (*stack, "no-latex")
    unavailable = [style for style in stack if style not in plt.style.available]
    if unavailable:
        raise RuntimeError(f"Requested SciencePlots styles are unavailable: {unavailable}")
    plt.style.use(list(stack))
    global _active_scienceplots_style_stack
    _active_scienceplots_style_stack = stack
    return stack


def current_scienceplots_style() -> tuple[str, ...]:
    """Return the style stack that plotting helpers reapply before rendering."""

    return _active_scienceplots_style_stack


def _new_axes(ax: Axes | None, figsize: tuple[float, float]) -> tuple[Figure, Axes]:
    plt.style.use(list(_active_scienceplots_style_stack))
    if ax is None:
        fig, created_ax = plt.subplots(figsize=figsize, constrained_layout=True)
        return fig, created_ax
    return ax.figure, ax


activate_scienceplots_style()


def _require_columns(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [column for column in columns if column not in frame.columns]
    if missing:
        raise KeyError(f"Missing plotting columns: {missing}")


def _require_rows(frame: pd.DataFrame) -> None:
    if frame.empty:
        raise ValueError("Plot input must contain at least one row")


def _require_labels(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    missing = [column for column in columns if frame[column].isna().any()]
    if missing:
        raise ValueError(
            f"Grouping or category columns contain missing labels: {missing}. "
            "Represent missingness explicitly before plotting."
        )


def _require_colors(colors: Sequence[str]) -> None:
    if not colors:
        raise ValueError("At least one color is required")


def _require_finite(frame: pd.DataFrame, columns: Iterable[str]) -> None:
    for column in columns:
        values = pd.to_numeric(frame[column], errors="coerce").to_numpy(dtype=float)
        if not np.isfinite(values).all():
            raise ValueError(
                f"{column!r} contains missing or non-finite values. Handle failures and "
                "missingness explicitly before plotting; do not let the helper drop rows."
            )


def _levels(series: pd.Series, requested: Sequence[Any] | None) -> list[Any]:
    observed = list(pd.unique(series))
    if requested is None:
        return observed
    levels = list(requested)
    missing = [value for value in observed if value not in levels]
    unknown = [value for value in levels if value not in observed]
    if missing or unknown:
        raise ValueError(
            f"Requested order does not match observed levels; missing={missing}, unknown={unknown}"
        )
    return levels


def save_figure(
    fig: Figure,
    output_stem: str | Path,
    *,
    formats: Sequence[str] = ("pdf", "svg", "png"),
    raster_dpi: int = 300,
) -> list[Path]:
    """Atomically save one figure to vector and raster formats using one stem."""

    plt.style.use(list(_active_scienceplots_style_stack))
    stem = Path(output_stem)
    stem.parent.mkdir(parents=True, exist_ok=True)
    if not formats:
        raise ValueError("At least one output format is required")
    if raster_dpi <= 0:
        raise ValueError("raster_dpi must be positive")
    written: list[Path] = []
    for format_name in formats:
        normalized = format_name.lower().lstrip(".")
        if not normalized or "/" in normalized or "\\" in normalized:
            raise ValueError(f"Invalid output format: {format_name!r}")
        target = stem.parent / f"{stem.name}.{normalized}"
        kwargs: dict[str, Any] = {"bbox_inches": "tight"}
        if normalized in {"png", "jpg", "jpeg", "tif", "tiff"}:
            kwargs["dpi"] = raster_dpi
        with tempfile.NamedTemporaryFile(
            dir=target.parent,
            prefix=f".{target.name}.",
            suffix=f".{normalized}",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
        try:
            fig.savefig(temporary, format=normalized, **kwargs)
            os.replace(temporary, target)
        except Exception:
            temporary.unlink(missing_ok=True)
            raise
        written.append(target)
    return written


def bubble_areas(
    values: Sequence[float] | pd.Series,
    *,
    max_area: float = 360.0,
) -> np.ndarray:
    """Map nonnegative values proportionally to marker *area* for ``scatter(s=...)``."""

    data = np.asarray(values, dtype=float)
    if not np.isfinite(data).all() or (data < 0).any():
        raise ValueError("Bubble values must be finite and nonnegative")
    if not np.isfinite(max_area) or max_area <= 0:
        raise ValueError("max_area must be finite and positive")
    if data.size == 0:
        return data
    value_max = float(data.max())
    if value_max == 0:
        return np.zeros_like(data)
    return data / value_max * max_area


def plot_interval_estimates(
    frame: pd.DataFrame,
    *,
    category: str,
    estimate: str,
    lower: str,
    upper: str,
    group: str | None = None,
    category_order: Sequence[Any] | None = None,
    group_order: Sequence[Any] | None = None,
    orientation: str = "horizontal",
    colors: Sequence[str] = DEFAULT_COLORS,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot caller-supplied estimates and intervals without computing either."""

    columns = [category, estimate, lower, upper] + ([group] if group else [])
    _require_columns(frame, columns)
    _require_rows(frame)
    _require_labels(frame, [category] + ([group] if group else []))
    _require_finite(frame, [estimate, lower, upper])
    if orientation not in {"horizontal", "vertical"}:
        raise ValueError("orientation must be 'horizontal' or 'vertical'")
    _require_colors(colors)

    data = frame.loc[:, columns].copy()
    if (data[lower] > data[estimate]).any() or (data[estimate] > data[upper]).any():
        raise ValueError("Each interval must satisfy lower <= estimate <= upper")

    categories = _levels(data[category], category_order)
    groups = [None] if group is None else _levels(data[group], group_order)
    key_columns = [category] + ([group] if group else [])
    if data.duplicated(key_columns).any():
        raise ValueError(f"Interval input has duplicate rows for keys {key_columns}")
    expected_rows = len(categories) * len(groups)
    if len(data) != expected_rows:
        raise ValueError(
            "Interval input is not a complete category/group grid. Represent missing or "
            "failed combinations explicitly instead of silently omitting them."
        )

    fig, ax = _new_axes(ax, (6.4, max(3.2, 0.38 * len(categories) + 1.5)))
    base = np.arange(len(categories), dtype=float)
    offsets = np.zeros(1) if len(groups) == 1 else np.linspace(-0.28, 0.28, len(groups))

    for index, level in enumerate(groups):
        subset = data if group is None else data.loc[data[group] == level]
        subset = subset.set_index(category).reindex(categories)
        estimates = subset[estimate].to_numpy(dtype=float)
        low_error = estimates - subset[lower].to_numpy(dtype=float)
        high_error = subset[upper].to_numpy(dtype=float) - estimates
        positions = base + offsets[index]
        label = None if level is None else str(level)
        color = colors[index % len(colors)]
        if orientation == "horizontal":
            ax.errorbar(
                estimates,
                positions,
                xerr=np.vstack([low_error, high_error]),
                fmt="o",
                capsize=3,
                color=color,
                label=label,
            )
        else:
            ax.errorbar(
                positions,
                estimates,
                yerr=np.vstack([low_error, high_error]),
                fmt="o",
                capsize=3,
                color=color,
                label=label,
            )

    if orientation == "horizontal":
        ax.set_yticks(base, [str(value) for value in categories])
        ax.invert_yaxis()
    else:
        ax.set_xticks(base, [str(value) for value in categories])
    if group is not None:
        ax.legend(title=group, frameon=False)
    return fig, ax


def plot_histogram(
    frame: pd.DataFrame,
    *,
    value: str,
    bins: int | Sequence[float],
    group: str | None = None,
    density: bool = False,
    colors: Sequence[str] = DEFAULT_COLORS,
    ax: Axes | None = None,
) -> tuple[Figure, Axes, np.ndarray]:
    """Plot complete distributions with shared, explicit bin edges."""

    columns = [value] + ([group] if group else [])
    _require_columns(frame, columns)
    _require_rows(frame)
    _require_labels(frame, [group] if group else [])
    _require_finite(frame, [value])
    _require_colors(colors)
    values = frame[value].to_numpy(dtype=float)
    edges = np.histogram_bin_edges(values, bins=bins)
    fig, ax = _new_axes(ax, (6.4, 4.2))
    groups = [None] if group is None else list(pd.unique(frame[group]))
    for index, level in enumerate(groups):
        subset = frame if group is None else frame.loc[frame[group] == level]
        ax.hist(
            subset[value].to_numpy(dtype=float),
            bins=edges,
            density=density,
            histtype="step",
            linewidth=1.6,
            color=colors[index % len(colors)],
            label=None if level is None else str(level),
        )
    if group is not None:
        ax.legend(title=group, frameon=False)
    return fig, ax, edges


def plot_ecdf(
    frame: pd.DataFrame,
    *,
    value: str,
    group: str | None = None,
    colors: Sequence[str] = DEFAULT_COLORS,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot empirical cumulative distributions without smoothing."""

    columns = [value] + ([group] if group else [])
    _require_columns(frame, columns)
    _require_rows(frame)
    _require_labels(frame, [group] if group else [])
    _require_finite(frame, [value])
    _require_colors(colors)
    fig, ax = _new_axes(ax, (6.4, 4.2))
    groups = [None] if group is None else list(pd.unique(frame[group]))
    for index, level in enumerate(groups):
        subset = frame if group is None else frame.loc[frame[group] == level]
        x = np.sort(subset[value].to_numpy(dtype=float))
        y = np.arange(1, len(x) + 1, dtype=float) / len(x)
        ax.step(
            x,
            y,
            where="post",
            color=colors[index % len(colors)],
            label=None if level is None else str(level),
        )
    ax.set_ylim(0.0, 1.0)
    if group is not None:
        ax.legend(title=group, frameon=False)
    return fig, ax


def plot_scatter(
    frame: pd.DataFrame,
    *,
    x: str,
    y: str,
    group: str | None = None,
    alpha: float = 0.55,
    marker_area: float = 18.0,
    colors: Sequence[str] = DEFAULT_COLORS,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot all supplied points; use ``plot_hexbin`` when overlap remains severe."""

    columns = [x, y] + ([group] if group else [])
    _require_columns(frame, columns)
    _require_rows(frame)
    _require_labels(frame, [group] if group else [])
    _require_finite(frame, [x, y])
    _require_colors(colors)
    if not 0 < alpha <= 1 or marker_area <= 0:
        raise ValueError("Require 0 < alpha <= 1 and marker_area > 0")
    fig, ax = _new_axes(ax, (6.4, 4.8))
    groups = [None] if group is None else list(pd.unique(frame[group]))
    for index, level in enumerate(groups):
        subset = frame if group is None else frame.loc[frame[group] == level]
        ax.scatter(
            subset[x],
            subset[y],
            s=marker_area,
            alpha=alpha,
            color=colors[index % len(colors)],
            linewidths=0,
            rasterized=len(subset) > 5000,
            label=None if level is None else str(level),
        )
    if group is not None:
        ax.legend(title=group, frameon=False)
    return fig, ax


def plot_hexbin(
    frame: pd.DataFrame,
    *,
    x: str,
    y: str,
    gridsize: int,
    cmap: str = "viridis",
    min_count: int = 1,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot counts for all supplied points on an explicit hexagonal grid."""

    _require_columns(frame, [x, y])
    _require_rows(frame)
    _require_finite(frame, [x, y])
    if gridsize <= 1 or min_count != 1:
        raise ValueError("Require gridsize > 1 and min_count == 1 so low-count cells remain visible")
    fig, ax = _new_axes(ax, (6.4, 4.8))
    collection = ax.hexbin(
        frame[x].to_numpy(dtype=float),
        frame[y].to_numpy(dtype=float),
        gridsize=gridsize,
        mincnt=min_count,
        cmap=cmap,
    )
    colorbar = fig.colorbar(collection, ax=ax)
    colorbar.set_label("Observation count")
    return fig, ax


def plot_series(
    frame: pd.DataFrame,
    *,
    x: str,
    y: str,
    group: str | None = None,
    lower: str | None = None,
    upper: str | None = None,
    group_order: Sequence[Any] | None = None,
    colors: Sequence[str] = DEFAULT_COLORS,
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot ordered series and optional caller-supplied uncertainty bands."""

    if (lower is None) != (upper is None):
        raise ValueError("Provide both lower and upper, or neither")
    columns = [x, y] + ([group] if group else []) + ([lower, upper] if lower else [])
    _require_columns(frame, columns)
    _require_rows(frame)
    _require_labels(frame, [group] if group else [])
    _require_finite(frame, [x, y] + ([lower, upper] if lower else []))
    _require_colors(colors)
    key_columns = [x] + ([group] if group else [])
    if frame.duplicated(key_columns).any():
        raise ValueError(
            f"Series input has duplicate rows for {key_columns}; aggregate explicitly at the TODO-defined unit"
        )
    if lower and ((frame[lower] > frame[y]).any() or (frame[y] > frame[upper]).any()):
        raise ValueError("Each uncertainty band must satisfy lower <= y <= upper")

    fig, ax = _new_axes(ax, (6.4, 4.2))
    groups = [None] if group is None else _levels(frame[group], group_order)
    for index, level in enumerate(groups):
        subset = frame if group is None else frame.loc[frame[group] == level]
        subset = subset.sort_values(x)
        color = colors[index % len(colors)]
        label = None if level is None else str(level)
        ax.plot(subset[x], subset[y], marker="o", color=color, label=label)
        if lower:
            ax.fill_between(
                subset[x],
                subset[lower],
                subset[upper],
                color=color,
                alpha=0.18,
                linewidth=0,
            )
    if group is not None:
        ax.legend(title=group, frameon=False)
    return fig, ax


def plot_heatmap(
    matrix: pd.DataFrame,
    *,
    vmin: float,
    vmax: float,
    cmap: str = "viridis",
    colorbar_label: str,
    missing_color: str = "#D9D9D9",
    annotate: bool = False,
    value_format: str = ".2g",
    ax: Axes | None = None,
) -> tuple[Figure, Axes]:
    """Plot a labeled numeric matrix with explicit color limits and missing cells."""

    if not isinstance(matrix, pd.DataFrame) or matrix.empty:
        raise ValueError("matrix must be a non-empty pandas DataFrame")
    if not np.isfinite([vmin, vmax]).all() or vmax <= vmin:
        raise ValueError("Require finite color limits with vmax > vmin")
    numeric_frame = matrix.apply(pd.to_numeric, errors="coerce")
    invalid = matrix.notna() & numeric_frame.isna()
    if invalid.to_numpy().any():
        locations = list(zip(*np.where(invalid.to_numpy())))
        raise ValueError(
            f"Heatmap contains nonnumeric values at row/column offsets {locations[:8]}"
        )
    numeric = numeric_frame.to_numpy(dtype=float)
    masked = np.ma.masked_invalid(numeric)
    palette = plt.get_cmap(cmap).copy()
    palette.set_bad(missing_color)
    fig, ax = _new_axes(ax, (6.4, 4.8))
    image = ax.imshow(masked, aspect="auto", cmap=palette, vmin=vmin, vmax=vmax)
    ax.set_xticks(np.arange(matrix.shape[1]), [str(value) for value in matrix.columns])
    ax.set_yticks(np.arange(matrix.shape[0]), [str(value) for value in matrix.index])
    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label(colorbar_label)
    if annotate:
        for row in range(matrix.shape[0]):
            for column in range(matrix.shape[1]):
                value = numeric[row, column]
                label = "NA" if not np.isfinite(value) else format(value, value_format)
                ax.text(column, row, label, ha="center", va="center", fontsize=8)
    return fig, ax


__all__ = [
    "DEFAULT_COLORS",
    "SCIENCEPLOTS_BASE_STYLE",
    "SCIENCEPLOTS_DEFAULT_STYLE_STACK",
    "activate_scienceplots_style",
    "bubble_areas",
    "current_scienceplots_style",
    "plot_ecdf",
    "plot_heatmap",
    "plot_hexbin",
    "plot_histogram",
    "plot_interval_estimates",
    "plot_scatter",
    "plot_series",
    "save_figure",
]
