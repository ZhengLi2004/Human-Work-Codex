#!/usr/bin/env python3
"""Deterministically validate an executed governed figure notebook and manifest."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

import nbformat

REQUIRED_SECTIONS = [
    "## Execution summary",
    "## Scope and parameters",
    "## Sources and environment",
    "## Data quality",
    "## Figure contract",
    "## Rendering",
    "## Coverage and integrity",
    "## Observed facts and limitations",
]

PLACEHOLDER_PATTERN = re.compile(
    r"\b(?:REPLACE_[A-Z0-9_]+|TODO-(?:X{2,}|REPLACE[A-Z0-9_-]*))\b"
)

SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


def parse_args() -> argparse.Namespace:
    """Parse validator command-line arguments.

    Returns:
        The validated command-line namespace.
    """

    parser = argparse.ArgumentParser(
        description="Validate an executed research-figure notebook and its manifest."
    )

    parser.add_argument("--notebook", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("planning", "final"))
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    """Compute a file SHA-256 digest.

    Args:
        path: File whose bytes are hashed.

    Returns:
        The lowercase hexadecimal digest.
    """

    digest = hashlib.sha256()

    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)

    return digest.hexdigest()


def resolve_record_path(raw_path: Any, manifest_path: Path) -> Path:
    """Resolve a manifest artifact path.

    Args:
        raw_path: Absolute path or path relative to the manifest directory.
        manifest_path: Manifest that owns the path record.

    Returns:
        The resolved absolute artifact path.
    """

    path = Path(str(raw_path))

    if not path.is_absolute():
        path = manifest_path.parent / path

    return path.resolve()


def check(check_id: str, passed: bool, evidence: Any) -> dict[str, Any]:
    """Create one deterministic validation check record.

    Args:
        check_id: Stable validation-check identifier.
        passed: Whether the check passed.
        evidence: Machine-readable evidence for the result.

    Returns:
        A normalized check record.
    """

    return {
        "id": check_id,
        "status": "pass" if passed else "fail",
        "evidence": evidence,
    }


def walk_strings(value: Any) -> Iterator[str]:
    """Yield every string key and value in a nested JSON-like object.

    Args:
        value: Scalar, mapping, or list to traverse.

    Yields:
        String values and mapping keys in traversal order.
    """

    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, child in value.items():
            yield str(key)
            yield from walk_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_strings(child)


def validate_hash_records(
    records: Any, manifest_path: Path, record_kind: str
) -> tuple[bool, list[dict[str, Any]]]:
    """Validate recorded paths and SHA-256 digests.

    Args:
        records: Manifest records to validate.
        manifest_path: Manifest used to resolve relative paths.
        record_kind: Human-readable record category for error evidence.

    Returns:
        A pass flag and per-record validation details.
    """

    details: list[dict[str, Any]] = []

    if not isinstance(records, list) or not records:
        return False, [{"error": f"{record_kind} must be a non-empty list"}]

    all_valid = True

    for index, record in enumerate(records):
        detail: dict[str, Any] = {"index": index}

        if not isinstance(record, dict) or not record.get("path"):
            detail["error"] = "missing path"
            details.append(detail)
            all_valid = False
            continue

        path = resolve_record_path(record["path"], manifest_path)
        recorded_hash = str(record.get("sha256", "")).lower()
        detail.update({"path": str(path), "recorded_sha256": recorded_hash})

        if not path.is_file():
            detail["error"] = "file does not exist"
            details.append(detail)
            all_valid = False
            continue

        actual_hash = sha256_file(path)
        detail["actual_sha256"] = actual_hash

        valid_hash = (
            bool(SHA256_PATTERN.fullmatch(recorded_hash))
            and recorded_hash == actual_hash
        )

        detail["hash_matches"] = valid_hash
        all_valid = all_valid and valid_hash
        details.append(detail)

    return all_valid, details


def validate(notebook_path: Path, manifest_path: Path, mode: str) -> dict[str, Any]:
    """Validate a governed figure notebook and its manifest.

    Args:
        notebook_path: Executed notebook to inspect.
        manifest_path: Planning or final figure manifest.
        mode: Validation mode, either ``planning`` or ``final``.

    Returns:
        Deterministic validation report containing every check and failure ID.
    """

    notebook_path = notebook_path.resolve()
    manifest_path = manifest_path.resolve()
    checks: list[dict[str, Any]] = []

    try:
        with notebook_path.open("r", encoding="utf-8") as handle:
            notebook = nbformat.read(handle, as_version=4)

        nbformat.validate(notebook)
        notebook_valid = True
        notebook_error = None
    except (
        Exception
    ) as exc:  # pragma: no cover - exact parser text is version-dependent
        notebook = None
        notebook_valid = False
        notebook_error = f"{type(exc).__name__}: {exc}"

    checks.append(
        check("notebook_format", notebook_valid, notebook_error or str(notebook_path))
    )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest_valid = isinstance(manifest, dict)
        manifest_error = None if manifest_valid else "manifest root is not an object"
    except Exception as exc:
        manifest = {}
        manifest_valid = False
        manifest_error = f"{type(exc).__name__}: {exc}"

    checks.append(
        check("manifest_json", manifest_valid, manifest_error or str(manifest_path))
    )

    if notebook is not None:
        headings: list[str] = []
        notebook_text: list[str] = []
        code_text: list[str] = []
        execution_counts: list[int] = []
        unexecuted_cells: list[int] = []
        error_outputs: list[dict[str, Any]] = []

        for cell_index, cell in enumerate(notebook.cells):
            source = str(cell.get("source", ""))
            notebook_text.append(source)

            if cell.cell_type == "markdown":
                headings.extend(
                    line.strip()
                    for line in source.splitlines()
                    if line.startswith("## ")
                )

            if cell.cell_type == "code" and source.strip():
                code_text.append(source)
                count = cell.get("execution_count")

                if not isinstance(count, int):
                    unexecuted_cells.append(cell_index)
                else:
                    execution_counts.append(count)

                for output_index, output in enumerate(cell.get("outputs", [])):
                    if output.get("output_type") == "error":
                        error_outputs.append(
                            {
                                "cell_index": cell_index,
                                "output_index": output_index,
                                "ename": output.get("ename"),
                                "evalue": output.get("evalue"),
                            }
                        )

        positions = []

        for section in REQUIRED_SECTIONS:
            positions.append(
                headings.index(section) if headings.count(section) == 1 else -1
            )

        sections_valid = all(
            position >= 0 for position in positions
        ) and positions == sorted(positions)

        checks.append(
            check(
                "required_section_order",
                sections_valid,
                {"required": REQUIRED_SECTIONS, "observed": headings},
            )
        )

        checks.append(
            check("all_code_cells_executed", not unexecuted_cells, unexecuted_cells)
        )

        strictly_increasing = all(
            current > previous
            for previous, current in zip(execution_counts, execution_counts[1:])
        )

        checks.append(
            check(
                "execution_counts_increase",
                strictly_increasing and not unexecuted_cells,
                execution_counts,
            )
        )

        checks.append(check("no_error_outputs", not error_outputs, error_outputs))

        placeholders = sorted(
            set(PLACEHOLDER_PATTERN.findall("\n".join(notebook_text)))
        )

        checks.append(check("no_notebook_placeholders", not placeholders, placeholders))
        combined_code = "\n".join(code_text)

        checks.append(
            check(
                "scienceplots_imported",
                bool(
                    re.search(
                        r"(^|\n)\s*(?:import\s+scienceplots|from\s+scienceplots\s+import)",
                        combined_code,
                    )
                ),
                "Notebook code must import scienceplots explicitly.",
            )
        )

        checks.append(
            check(
                "matplotlib_style_applied",
                "style.use" in combined_code or "style.context" in combined_code,
                "Notebook code must apply its declared style stack.",
            )
        )

    manifest_placeholders = sorted(
        set(PLACEHOLDER_PATTERN.findall("\n".join(walk_strings(manifest))))
    )

    checks.append(
        check(
            "no_manifest_placeholders", not manifest_placeholders, manifest_placeholders
        )
    )

    checks.append(
        check("manifest_mode", manifest.get("mode") == mode, manifest.get("mode"))
    )

    fingerprint = str(manifest.get("todo_fingerprint", "")).lower()

    checks.append(
        check(
            "todo_fingerprint", bool(SHA256_PATTERN.fullmatch(fingerprint)), fingerprint
        )
    )

    revision = manifest.get("task_state_revision")

    checks.append(
        check(
            "task_state_revision", isinstance(revision, int) and revision >= 0, revision
        )
    )

    notebook_record = manifest.get("notebook", {})

    notebook_record_valid = isinstance(notebook_record, dict) and bool(
        notebook_record.get("path")
    )

    notebook_record_path = None

    if notebook_record_valid:
        notebook_record_path = resolve_record_path(
            notebook_record["path"], manifest_path
        )

        notebook_record_valid = notebook_record_path == notebook_path

    checks.append(
        check(
            "manifest_notebook_path",
            notebook_record_valid,
            str(notebook_record_path) if notebook_record_path else notebook_record,
        )
    )

    execution = manifest.get("execution", {})

    required_execution = (
        isinstance(execution, dict)
        and execution.get("status") == "completed"
        and execution.get("clean_kernel") is True
        and bool(execution.get("command"))
        and bool(execution.get("started_at_utc"))
        and bool(execution.get("finished_at_utc"))
    )

    checks.append(check("clean_execution_record", required_execution, execution))
    style_stack = manifest.get("style_stack")

    valid_style = (
        isinstance(style_stack, list)
        and bool(style_stack)
        and style_stack[0] == "science"
    )

    checks.append(check("scienceplots_style_stack", valid_style, style_stack))

    required_context = {
        "stable_keys": manifest.get("stable_keys"),
        "statistical_unit": manifest.get("statistical_unit"),
        "filters": manifest.get("filters"),
        "output_directory": manifest.get("output_directory"),
    }

    context_valid = (
        isinstance(required_context["stable_keys"], list)
        and bool(required_context["stable_keys"])
        and bool(required_context["statistical_unit"])
        and isinstance(required_context["filters"], list)
        and bool(required_context["output_directory"])
    )

    checks.append(check("analysis_context_recorded", context_valid, required_context))
    git_revision = manifest.get("git_revision")

    git_revision_valid = isinstance(git_revision, str) and bool(
        re.fullmatch(r"[0-9a-fA-F]{7,64}", git_revision.strip())
    )

    checks.append(check("git_revision_recorded", git_revision_valid, git_revision))
    package_versions = manifest.get("package_versions")

    required_packages = {
        "python",
        "nbformat",
        "ipykernel",
        "matplotlib",
        "scienceplots",
    }

    package_valid = (
        isinstance(package_versions, dict)
        and required_packages.issubset(package_versions)
        and all(
            bool(str(package_versions[name]).strip())
            and str(package_versions[name]).lower() not in {"unknown", "unavailable"}
            for name in required_packages
        )
    )

    checks.append(check("package_versions_recorded", package_valid, package_versions))
    data_quality = manifest.get("data_quality")

    data_quality_valid = (
        isinstance(data_quality, list)
        and bool(data_quality)
        and all(
            isinstance(item, dict) and item.get("status") in {"pass", "not_applicable"}
            for item in data_quality
        )
    )

    checks.append(
        check("data_quality_recorded_and_passing", data_quality_valid, data_quality)
    )

    sufficiency = manifest.get("figure_data_sufficiency")

    sufficiency_valid = (
        isinstance(sufficiency, list)
        and bool(sufficiency)
        and all(
            isinstance(item, dict) and item.get("status") == "pass"
            for item in sufficiency
        )
    )

    checks.append(
        check(
            "figure_data_sufficiency_recorded_and_passing",
            sufficiency_valid,
            sufficiency,
        )
    )

    input_valid, input_details = validate_hash_records(
        manifest.get("inputs"), manifest_path, "inputs"
    )

    checks.append(check("input_files_and_hashes", input_valid, input_details))

    export_valid, export_details = validate_hash_records(
        manifest.get("exports"), manifest_path, "exports"
    )

    checks.append(check("export_files_and_hashes", export_valid, export_details))

    artifact_valid, artifact_details = validate_hash_records(
        manifest.get("artifacts"), manifest_path, "artifacts"
    )

    checks.append(check("artifact_files_and_hashes", artifact_valid, artifact_details))
    failures = [item["id"] for item in checks if item["status"] == "fail"]

    return {
        "schema_version": 1,
        "validator": "validate_figure_notebook.py",
        "mode": mode,
        "passed": not failures,
        "notebook": str(notebook_path),
        "manifest": str(manifest_path),
        "checks": checks,
        "failures": failures,
    }


def atomic_write_json(path: Path, value: dict[str, Any]) -> None:
    """Write a JSON object atomically in deterministic form.

    Args:
        path: Final JSON output path.
        value: JSON-compatible mapping to serialize.
    """

    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )

    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, sort_keys=True, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())

        os.replace(temporary_path, path)
    finally:
        if temporary_path.exists():
            temporary_path.unlink()


def write_validation(report: dict[str, Any], output_path: Path, mode: str) -> None:
    """Write a planning report or merge final validation into an audit.

    Args:
        report: Notebook validation report.
        output_path: Planning report path or final integrity-audit path.
        mode: Validation mode, either ``planning`` or ``final``.
    """

    existing: dict[str, Any] | None = None

    if output_path.exists():
        try:
            candidate = json.loads(output_path.read_text(encoding="utf-8"))

            if isinstance(candidate, dict):
                existing = candidate
        except (OSError, json.JSONDecodeError):
            existing = None

    is_standalone_prior_report = (
        existing and existing.get("validator") == report["validator"]
    )

    if mode == "final" and existing and not is_standalone_prior_report:
        merged = dict(existing)
        merged["notebook_validation"] = report

        failed_checks = [
            item
            for item in existing.get("failed_checks", [])
            if item != "notebook_reproducibility"
        ]

        audit_checks = existing.get("checks", [])

        if isinstance(audit_checks, dict):
            audit_check_values = audit_checks.values()
        elif isinstance(audit_checks, list):
            audit_check_values = audit_checks
        else:
            audit_check_values = []

        other_check_failed = any(
            (isinstance(item, dict) and item.get("status") == "fail") or item == "fail"
            for item in audit_check_values
        )

        if not report["passed"] and "notebook_reproducibility" not in failed_checks:
            failed_checks.append("notebook_reproducibility")

        merged["failed_checks"] = failed_checks

        merged["passed"] = (
            not failed_checks and not other_check_failed and report["passed"]
        )

        atomic_write_json(output_path, merged)
    elif mode == "final":
        atomic_write_json(
            output_path,
            {
                "schema_version": 1,
                "passed": report["passed"],
                "failed_checks": []
                if report["passed"]
                else ["notebook_reproducibility"],
                "notebook_validation": report,
            },
        )
    else:
        atomic_write_json(output_path, report)


def main() -> int:
    """Run command-line validation.

    Returns:
        Zero when validation passes; otherwise one.
    """
    args = parse_args()
    report = validate(args.notebook, args.manifest, args.mode)
    write_validation(report, args.output, args.mode)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
