"""Render complete table data, then apply one publication-style pass."""

from __future__ import annotations

import argparse
import os
import tempfile
from dataclasses import dataclass
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import scienceplots  # noqa: F401  Registers the SciencePlots styles.
import seaborn as sns


STYLE_STACK = ["science", "no-latex"]
MM_PER_INCH = 25.4


@dataclass(frozen=True)
class PublicationProfile:
    """Final-size settings taken from the selected journal profile."""

    name: str
    width_mm: float
    height_mm: float
    font_family: str
    font_size_pt: float
    line_width_pt: float
    raster_dpi: int

    @property
    def size_inches(self) -> tuple[float, float]:
        """Return final width and height in inches.

        Returns:
            Final canvas size accepted by Matplotlib.
        """
        return self.width_mm / MM_PER_INCH, self.height_mm / MM_PER_INCH


def parse_args() -> argparse.Namespace:
    """Parse plotting input and output paths.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--profile-name", required=True)
    parser.add_argument("--width-mm", required=True, type=float)
    parser.add_argument("--height-mm", required=True, type=float)
    parser.add_argument("--font-family", default="Arial")
    parser.add_argument("--font-size-pt", default=7.0, type=float)
    parser.add_argument("--line-width-pt", default=0.75, type=float)
    parser.add_argument("--raster-dpi", default=300, type=int)
    parser.add_argument("--allowed-panel-heading", action="append", default=[])
    parser.add_argument("--despine", action="store_true")
    return parser.parse_args()


def profile_from_args(args: argparse.Namespace) -> PublicationProfile:
    """Build the recorded publication profile from command-line arguments.

    Args:
        args: Parsed command-line arguments.

    Returns:
        Immutable publication profile.

    Raises:
        ValueError: If any profile field is empty or numerically invalid.
    """
    numeric = {
        "width_mm": args.width_mm,
        "height_mm": args.height_mm,
        "font_size_pt": args.font_size_pt,
        "line_width_pt": args.line_width_pt,
        "raster_dpi": args.raster_dpi,
    }
    invalid = [
        name
        for name, value in numeric.items()
        if isinstance(value, bool) or not 0 < float(value) < float("inf")
    ]

    if invalid:
        raise ValueError(f"Profile values must be positive and finite: {invalid}")

    if not args.profile_name.strip() or not args.font_family.strip():
        raise ValueError("Profile name and font family must be non-empty")

    return PublicationProfile(
        name=args.profile_name,
        width_mm=args.width_mm,
        height_mm=args.height_mm,
        font_family=args.font_family,
        font_size_pt=args.font_size_pt,
        line_width_pt=args.line_width_pt,
        raster_dpi=args.raster_dpi,
    )


def read_complete_table(path: Path) -> pd.DataFrame:
    """Read a complete CSV or Parquet table.

    Args:
        path: Validated complete input table.

    Returns:
        Loaded table without filtering or aggregation.

    Raises:
        ValueError: If the file format is unsupported.
    """
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)

    if path.suffix.lower() == ".csv":
        return pd.read_csv(path)

    raise ValueError(f"Unsupported table format: {path.suffix}")


def render_figure(
    table: pd.DataFrame,
    profile: PublicationProfile,
) -> plt.Figure:
    """Render the TODO-defined figure from supplied production quantities.

    Args:
        table: Complete table already containing every scientific quantity.
        profile: Selected final-size journal profile.

    Returns:
        Matplotlib figure.

    Raises:
        NotImplementedError: Until adapted to the selected chart contract.
    """
    raise NotImplementedError(
        "Adapt render_figure to the approved figure plan; keep production calculations in MATLAB."
    )


def apply_publication_style(
    figure: plt.Figure,
    profile: PublicationProfile,
    allowed_panel_headings: set[str],
    despine: bool = False,
) -> None:
    """Apply layout-only styling after every data artist has been drawn.

    Args:
        figure: Complete figure whose scientific content is already fixed.
        profile: Selected final-size journal profile.
        allowed_panel_headings: Planned facet headings that identify data.
        despine: Whether the selected chart benefits from Seaborn despining.

    Raises:
        ValueError: If an unexplained title remains inside the artwork.
    """
    figure.set_size_inches(*profile.size_inches, forward=True)
    super_title = getattr(figure, "_suptitle", None)

    if super_title is not None and super_title.get_text().strip():
        raise ValueError("Move the figure title to the manuscript caption or legend")

    unexpected_headings = [
        axes.get_title().strip()
        for axes in figure.axes
        if axes.get_title().strip()
        and axes.get_title().strip() not in allowed_panel_headings
    ]

    if unexpected_headings:
        raise ValueError(
            "Unplanned in-artwork headings must move to the caption or be recorded "
            f"as facet labels: {unexpected_headings}"
        )

    for axes in figure.axes:
        if despine and axes.name == "rectilinear":
            sns.despine(ax=axes)

        axes.tick_params(
            axis="both",
            which="both",
            labelsize=profile.font_size_pt,
            width=profile.line_width_pt,
        )

        for label in (
            axes.xaxis.label,
            axes.yaxis.label,
            axes.title,
            *axes.get_xticklabels(),
            *axes.get_yticklabels(),
        ):
            label.set_fontfamily(profile.font_family)
            label.set_fontsize(profile.font_size_pt)

        for spine in axes.spines.values():
            spine.set_linewidth(profile.line_width_pt)

        legend = axes.get_legend()

        if legend is not None:
            legend.set_frame_on(False)

            for label in (*legend.get_texts(), legend.get_title()):
                label.set_fontfamily(profile.font_family)
                label.set_fontsize(profile.font_size_pt)

        for label in axes.texts:
            label.set_fontfamily(profile.font_family)

    for label in figure.texts:
        label.set_fontfamily(profile.font_family)

    figure.align_xlabels()
    figure.align_ylabels()


def save_figure_atomic(
    figure: plt.Figure,
    output_path: Path,
    raster_dpi: int,
) -> None:
    """Save a figure through an atomic same-directory replacement.

    Args:
        figure: Figure to export.
        output_path: Final export path.
        raster_dpi: Effective resolution for rasterized content.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=output_path.suffix,
        dir=output_path.parent,
        delete=False,
    ) as stream:
        temporary_path = Path(stream.name)

    try:
        figure.savefig(temporary_path, dpi=raster_dpi)
        os.replace(temporary_path, output_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def main() -> int:
    """Load complete data, render with SciencePlots, and export atomically.

    Returns:
        Process exit status.
    """
    args = parse_args()
    table = read_complete_table(args.input)
    profile = profile_from_args(args)

    with plt.style.context(STYLE_STACK):
        figure = render_figure(table, profile)
        apply_publication_style(
            figure,
            profile,
            set(args.allowed_panel_heading),
            despine=args.despine,
        )

    save_figure_atomic(figure, args.output, profile.raster_dpi)
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
