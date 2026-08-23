"""Validate a governed scientific plotting script and its manifest."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed script, manifest, mode, and output paths.
    """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--script", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--mode", required=True, choices=("planning", "final"))
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def sha256_file(path: Path) -> str:
    """Return the SHA-256 digest of a file.

    Args:
        path: File to hash.

    Returns:
        Lowercase hexadecimal digest.
    """
    digest = hashlib.sha256()

    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)

    return digest.hexdigest()


def resolve_path(recorded: str, manifest_path: Path) -> Path:
    """Resolve a manifest path relative to its manifest.

    Args:
        recorded: Absolute or manifest-relative path.
        manifest_path: Manifest containing the path.

    Returns:
        Resolved path.
    """
    path = Path(recorded)
    return path if path.is_absolute() else manifest_path.parent / path


def add_check(
    checks: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    detail: str,
) -> None:
    """Append one deterministic validation result.

    Args:
        checks: Mutable result list.
        check_id: Stable check identifier.
        passed: Whether the check passed.
        detail: Concise evidence or failure detail.
    """
    checks.append({"id": check_id, "passed": bool(passed), "detail": detail})


def validate_hash_records(
    records: Any,
    label: str,
    manifest_path: Path,
    checks: list[dict[str, Any]],
) -> None:
    """Validate declared file paths and hashes.

    Args:
        records: List of objects containing ``path`` and ``sha256``.
        label: Check identifier prefix.
        manifest_path: Manifest used for relative paths.
        checks: Mutable validation results.
    """
    valid_shape = isinstance(records, list) and bool(records)
    add_check(checks, f"{label}_records_present", valid_shape, f"count={len(records) if isinstance(records, list) else 0}")

    if not valid_shape:
        return

    for index, record in enumerate(records):
        record_ok = isinstance(record, dict) and record.get("path") and record.get("sha256")
        add_check(checks, f"{label}_{index}_record_complete", bool(record_ok), "path and sha256 required")

        if not record_ok:
            continue

        path = resolve_path(str(record["path"]), manifest_path)
        exists = path.is_file()
        add_check(checks, f"{label}_{index}_exists", exists, str(path))

        if exists:
            actual = sha256_file(path)
            add_check(checks, f"{label}_{index}_hash", actual == record["sha256"], f"actual={actual}")


def validate(script_path: Path, manifest_path: Path, mode: str) -> dict[str, Any]:
    """Validate script syntax, style use, provenance, and exports.

    Args:
        script_path: Governed plotting script.
        manifest_path: Figure manifest JSON.
        mode: ``planning`` or ``final``.

    Returns:
        Deterministic validation report.
    """
    checks: list[dict[str, Any]] = []
    script_exists = script_path.is_file()
    manifest_exists = manifest_path.is_file()
    add_check(checks, "script_exists", script_exists, str(script_path))
    add_check(checks, "manifest_exists", manifest_exists, str(manifest_path))

    source = ""

    if script_exists:
        source = script_path.read_text(encoding="utf-8")

        try:
            tree = ast.parse(source, filename=str(script_path))
            add_check(checks, "script_syntax", True, "valid Python")
        except SyntaxError as error:
            tree = ast.parse("")
            add_check(checks, "script_syntax", False, str(error))

        imports_scienceplots = any(
            (isinstance(node, ast.Import) and any(alias.name == "scienceplots" for alias in node.names))
            or (isinstance(node, ast.ImportFrom) and node.module == "scienceplots")
            for node in ast.walk(tree)
        )
        add_check(checks, "scienceplots_import", imports_scienceplots, "import scienceplots required")
        style_call_present = "style.use" in source or "style.context" in source
        science_literal_present = '"science"' in source or "'science'" in source
        add_check(
            checks,
            "science_style_call",
            style_call_present and science_literal_present,
            "science style call required",
        )
        placeholders_absent = "REPLACE_" not in source and "TODO-XXX" not in source
        add_check(checks, "no_placeholders", placeholders_absent, "no unresolved placeholders")

    manifest: dict[str, Any] = {}

    if manifest_exists:
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            add_check(checks, "manifest_json", isinstance(manifest, dict), "JSON object required")
        except json.JSONDecodeError as error:
            add_check(checks, "manifest_json", False, str(error))

    if manifest:
        script_record = manifest.get("plotting_script", {})
        record_complete = isinstance(script_record, dict) and script_record.get("path") and script_record.get("sha256")
        add_check(checks, "script_record_complete", bool(record_complete), "plotting_script.path and sha256 required")

        if record_complete and script_exists:
            recorded_path = resolve_path(str(script_record["path"]), manifest_path).resolve()
            add_check(checks, "script_path_match", recorded_path == script_path.resolve(), str(recorded_path))
            add_check(checks, "script_hash_match", script_record["sha256"] == sha256_file(script_path), "script SHA-256")

        style_stack = manifest.get("style_stack")
        add_check(
            checks,
            "science_style_stack",
            isinstance(style_stack, list) and bool(style_stack) and style_stack[0] == "science",
            repr(style_stack),
        )
        execution = manifest.get("execution", {})
        execution_ok = all(execution.get(key) for key in ("command", "started_at_utc", "finished_at_utc")) and execution.get("status") == "completed"
        add_check(checks, "execution_complete", bool(execution_ok), "completed command and timestamps required")

        for key in ("todo_fingerprint", "task_state_revision", "git_revision", "package_versions", "data_quality_results", "figure_data_sufficiency"):
            add_check(checks, f"manifest_{key}", key in manifest and manifest[key] not in (None, "", {}), f"{key} required")

        validate_hash_records(manifest.get("inputs"), "input", manifest_path, checks)
        validate_hash_records(manifest.get("outputs"), "output", manifest_path, checks)

    passed = bool(checks) and all(check["passed"] for check in checks)
    return {
        "schema_version": 1,
        "mode": mode,
        "passed": passed,
        "script": str(script_path),
        "manifest": str(manifest_path),
        "checks": checks,
        "failed_checks": [check["id"] for check in checks if not check["passed"]],
    }


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    """Write JSON through an atomic same-directory replacement.

    Args:
        path: Destination JSON path.
        payload: Serializable mapping.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=path.parent, delete=False) as stream:
        json.dump(payload, stream, indent=2, sort_keys=True)
        stream.write("\n")
        temporary = Path(stream.name)

    os.replace(temporary, path)


def write_validation(output_path: Path, report: dict[str, Any], mode: str) -> None:
    """Write planning validation or merge final validation into an audit.

    Args:
        output_path: Planning report or final audit path.
        report: Validation report.
        mode: ``planning`` or ``final``.
    """
    if mode == "planning":
        atomic_write_json(output_path, report)
        return

    audit: dict[str, Any] = {}

    if output_path.is_file():
        audit = json.loads(output_path.read_text(encoding="utf-8"))

    audit["plot_script_validation"] = report
    audit["passed"] = bool(audit.get("passed", True) and report["passed"])
    atomic_write_json(output_path, audit)


def main() -> int:
    """Run command-line validation.

    Returns:
        Zero on success; one when any check fails.
    """
    args = parse_args()
    report = validate(args.script, args.manifest, args.mode)
    write_validation(args.output, report, args.mode)
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
