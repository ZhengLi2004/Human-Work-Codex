"""Template: buffered, atomic scientific result writes.

Adapt the schema and compute function to the TODO. Scientific records are
written in Parquet chunks; logs/checkpoints remain separate.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable, Mapping

import pandas as pd


@dataclass
class ParquetResultBuffer:
    output_dir: Path
    schema_columns: tuple[str, ...]
    flush_rows: int = 10_000
    prefix: str = "part"
    _records: list[dict[str, Any]] = field(default_factory=list, init=False)
    _part_index: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        if self.flush_rows < 1:
            raise ValueError("flush_rows must be positive")
        if not self.schema_columns:
            raise ValueError("schema_columns must not be empty")

        # A task-level resume layer must skip records already completed. Starting
        # after existing immutable parts prevents accidental overwrite here.
        existing = sorted(self.output_dir.glob(f"{self.prefix}-*.parquet"))
        if existing:
            indices = [int(path.stem.rsplit("-", 1)[1]) for path in existing]
            self._part_index = max(indices) + 1

    def add(self, record: Mapping[str, Any]) -> None:
        missing = set(self.schema_columns) - set(record)
        extra = set(record) - set(self.schema_columns)
        if missing or extra:
            raise ValueError(f"Schema mismatch: missing={sorted(missing)}, extra={sorted(extra)}")
        self._records.append(dict(record))
        if len(self._records) >= self.flush_rows:
            self.flush()

    def flush(self) -> Path | None:
        if not self._records:
            return None

        frame = pd.DataFrame.from_records(self._records, columns=self.schema_columns)
        final_path = self.output_dir / f"{self.prefix}-{self._part_index:06d}.parquet"
        temp_path = final_path.with_suffix(".parquet.tmp")

        if final_path.exists():
            raise FileExistsError(f"Refusing to overwrite immutable result part: {final_path}")

        # Use one bulk serialization. The temporary file is on the same filesystem.
        frame.to_parquet(temp_path, index=False, engine="pyarrow")
        if len(pd.read_parquet(temp_path, columns=[self.schema_columns[0]])) != len(frame):
            temp_path.unlink(missing_ok=True)
            raise RuntimeError(f"Row-count validation failed for {temp_path}")
        os.replace(temp_path, final_path)

        self._records.clear()
        self._part_index += 1
        return final_path

    def close(self) -> None:
        self.flush()


def run_tasks(tasks: Iterable[Mapping[str, Any]], output_dir: Path) -> None:
    columns = ("task_id", "condition", "repeat", "metric", "state", "error")
    buffer = ParquetResultBuffer(output_dir=output_dir, schema_columns=columns)

    try:
        for task in tasks:
            task_id = str(task["task_id"])
            try:
                # Replace with the TODO-defined computation.
                metric = float(task["value"])
                record = {
                    "task_id": task_id,
                    "condition": task["condition"],
                    "repeat": int(task["repeat"]),
                    "metric": metric,
                    "state": "complete",
                    "error": None,
                }
            except Exception as exc:  # preserve failure evidence
                record = {
                    "task_id": task_id,
                    "condition": task.get("condition"),
                    "repeat": task.get("repeat"),
                    "metric": None,
                    "state": "failed",
                    "error": repr(exc),
                }
            buffer.add(record)
    finally:
        buffer.close()

    manifest = {
        "format": "partitioned-parquet",
        "directory": str(output_dir),
        "schema_columns": list(columns),
        "parts": sorted(path.name for path in output_dir.glob("part-*.parquet")),
    }
    manifest_path = output_dir / "manifest.json.tmp"
    manifest_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    os.replace(manifest_path, output_dir / "manifest.json")
