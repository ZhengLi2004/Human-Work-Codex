"""Structure a governed SciencePlots rendering script over complete table data."""

from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import scienceplots  # noqa: F401  Registers the SciencePlots styles.


STYLE_STACK = ["science", "no-latex"]


def parse_args() -> argparse.Namespace:
    """Parse plotting input and output paths.

    Returns:
        Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


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


def render_figure(table: pd.DataFrame) -> plt.Figure:
    """Render the TODO-defined figure from supplied production quantities.

    Args:
        table: Complete table already containing every scientific quantity.

    Returns:
        Matplotlib figure.

    Raises:
        NotImplementedError: Until adapted to the selected chart contract.
    """
    raise NotImplementedError(
        "Adapt render_figure to the approved figure plan; keep production calculations in MATLAB."
    )


def save_figure_atomic(figure: plt.Figure, output_path: Path) -> None:
    """Save a figure through an atomic same-directory replacement.

    Args:
        figure: Figure to export.
        output_path: Final export path.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(
        suffix=output_path.suffix,
        dir=output_path.parent,
        delete=False,
    ) as stream:
        temporary_path = Path(stream.name)

    try:
        figure.savefig(temporary_path, bbox_inches="tight")
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

    with plt.style.context(STYLE_STACK):
        figure = render_figure(table)

    save_figure_atomic(figure, args.output)
    plt.close(figure)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
