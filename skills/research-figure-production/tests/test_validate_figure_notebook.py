"""Unit tests for deterministic figure notebook validation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import nbformat

SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_figure_notebook.py"
SPEC = importlib.util.spec_from_file_location("validate_figure_notebook", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def sha256(path: Path) -> str:
    """Compute a file SHA-256 digest for fixture manifests.

    Args:
        path: Fixture file to hash.

    Returns:
        The lowercase hexadecimal digest.
    """

    return hashlib.sha256(path.read_bytes()).hexdigest()


class FigureNotebookValidatorTests(unittest.TestCase):
    """Validate notebook, manifest, and final-audit failure modes."""

    def setUp(self) -> None:
        """Create a valid notebook, manifest, export, and artifact fixture."""
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.input_path = self.root / "input.csv"
        self.input_path.write_text("condition,value\nA,1\nB,2\n", encoding="utf-8")
        self.export_path = self.root / "figure.png"
        self.export_path.write_bytes(b"synthetic image bytes")
        self.artifact_path = self.root / "figure-plan.json"
        self.artifact_path.write_text('{"schema_version": 1}', encoding="utf-8")
        self.notebook_path = self.root / "figures.ipynb"
        self.manifest_path = self.root / "draft-figure-manifest.json"
        self.write_notebook()
        self.write_manifest()

    def tearDown(self) -> None:
        """Remove the temporary fixture directory."""

        self.temporary.cleanup()

    def write_notebook(self, mutate=None) -> None:
        """Write a valid executed notebook with an optional mutation.

        Args:
            mutate: Optional callable that mutates the notebook before writing.
        """

        cells = []

        for heading in MODULE.REQUIRED_SECTIONS:
            cells.append(
                nbformat.v4.new_markdown_cell(f"{heading}\n\nReader-facing content.")
            )

            if heading == "## Sources and environment":
                cells.append(
                    nbformat.v4.new_code_cell(
                        "import scienceplots\nimport matplotlib.pyplot as plt",
                        execution_count=1,
                        outputs=[],
                    )
                )

            if heading == "## Rendering":
                cells.append(
                    nbformat.v4.new_code_cell(
                        'plt.style.use(["science", "no-latex"])',
                        execution_count=2,
                        outputs=[],
                    )
                )

        notebook = nbformat.v4.new_notebook(cells=cells)

        notebook.metadata.kernelspec = {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3",
        }

        if mutate:
            mutate(notebook)

        nbformat.write(notebook, self.notebook_path)

    def base_manifest(self) -> dict:
        """Build a valid planning manifest.

        Returns:
            A fresh manifest mapping linked to the current fixture paths.
        """

        return {
            "schema_version": 1,
            "mode": "planning",
            "todo_fingerprint": "a" * 64,
            "task_state_revision": 3,
            "notebook": {"path": str(self.notebook_path)},
            "execution": {
                "command": "python -m jupyter nbconvert --execute --to notebook --inplace figures.ipynb",
                "started_at_utc": "2026-08-10T00:00:00Z",
                "finished_at_utc": "2026-08-10T00:01:00Z",
                "clean_kernel": True,
                "status": "completed",
            },
            "git_revision": "515036f",
            "package_versions": {
                "python": "3.12",
                "nbformat": "5.10",
                "ipykernel": "6.29",
                "matplotlib": "3.9",
                "scienceplots": "2.1",
            },
            "inputs": [
                {"path": str(self.input_path), "sha256": sha256(self.input_path)}
            ],
            "stable_keys": ["condition"],
            "statistical_unit": "independent repeat",
            "filters": [],
            "output_directory": str(self.root),
            "data_quality": [{"id": "stable_keys", "status": "pass"}],
            "figure_data_sufficiency": [{"figure_id": "F1", "status": "pass"}],
            "style_stack": ["science", "no-latex"],
            "exports": [
                {"path": str(self.export_path), "sha256": sha256(self.export_path)}
            ],
            "artifacts": [
                {"path": str(self.artifact_path), "sha256": sha256(self.artifact_path)}
            ],
        }

    def write_manifest(self, mutate=None) -> None:
        """Write a valid manifest with an optional mutation.

        Args:
            mutate: Optional callable that mutates the manifest before writing.
        """

        manifest = self.base_manifest()

        if mutate:
            mutate(manifest)

        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

    def validate(self):
        """Validate the current planning fixture.

        Returns:
            The validator report mapping.
        """

        return MODULE.validate(self.notebook_path, self.manifest_path, "planning")

    def assert_fails(self, check_id: str) -> None:
        """Assert that API and CLI validation fail on a specific check.

        Args:
            check_id: Expected failed-check identifier.
        """

        report = self.validate()
        self.assertFalse(report["passed"])
        self.assertIn(check_id, report["failures"])
        output_path = self.root / "validation.json"

        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPT_PATH),
                "--notebook",
                str(self.notebook_path),
                "--manifest",
                str(self.manifest_path),
                "--mode",
                "planning",
                "--output",
                str(output_path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        self.assertEqual(completed.returncode, 1, completed.stdout + completed.stderr)

        self.assertIn(
            check_id, json.loads(output_path.read_text(encoding="utf-8"))["failures"]
        )

    def test_valid_notebook_passes(self) -> None:
        """Accept a complete valid planning notebook and manifest."""

        self.assertTrue(self.validate()["passed"])

    def test_unexecuted_cell_fails(self) -> None:
        """Reject an unexecuted code cell."""

        self.write_notebook(lambda nb: setattr(nb.cells[3], "execution_count", None))
        self.assert_fails("all_code_cells_executed")

    def test_error_output_fails(self) -> None:
        """Reject a code cell containing an error output."""

        def mutate(notebook):
            """Insert a synthetic error output.

            Args:
                notebook: Notebook fixture to mutate.
            """

            notebook.cells[3].outputs = [
                nbformat.v4.new_output(
                    "error",
                    ename="RuntimeError",
                    evalue="failure",
                    traceback=["failure"],
                )
            ]

        self.write_notebook(mutate)
        self.assert_fails("no_error_outputs")

    def test_placeholder_fails(self) -> None:
        """Reject an unresolved template placeholder."""

        self.write_notebook(
            lambda nb: nb.cells.append(nbformat.v4.new_markdown_cell("REPLACE_VALUE"))
        )

        self.assert_fails("no_notebook_placeholders")

    def test_missing_required_section_fails(self) -> None:
        """Reject a notebook missing a required section."""

        self.write_notebook(lambda nb: nb.cells.pop(0))
        self.assert_fails("required_section_order")

    def test_missing_source_hash_fails(self) -> None:
        """Reject an input record without a source hash."""

        self.write_manifest(lambda manifest: manifest["inputs"][0].pop("sha256"))
        self.assert_fails("input_files_and_hashes")

    def test_wrong_style_fails(self) -> None:
        """Reject a style stack whose base differs from SciencePlots science."""

        self.write_manifest(
            lambda manifest: manifest.__setitem__("style_stack", ["ggplot"])
        )

        self.assert_fails("scienceplots_style_stack")

    def test_failing_data_quality_fails(self) -> None:
        """Reject a manifest containing a failed data-quality check."""

        self.write_manifest(
            lambda manifest: manifest.__setitem__(
                "data_quality", [{"id": "stable_keys", "status": "fail"}]
            )
        )

        self.assert_fails("data_quality_recorded_and_passing")

    def test_insufficient_figure_data_fails(self) -> None:
        """Reject a manifest containing insufficient figure data."""

        self.write_manifest(
            lambda manifest: manifest.__setitem__(
                "figure_data_sufficiency", [{"figure_id": "F1", "status": "fail"}]
            )
        )

        self.assert_fails("figure_data_sufficiency_recorded_and_passing")

    def test_missing_export_fails(self) -> None:
        """Reject a declared export that is missing from disk."""

        self.export_path.unlink()
        self.assert_fails("export_files_and_hashes")

    def test_missing_declared_artifact_fails(self) -> None:
        """Reject a declared supporting artifact that is missing from disk."""

        self.artifact_path.unlink()
        self.assert_fails("artifact_files_and_hashes")

    def test_final_mode_merges_existing_audit(self) -> None:
        """Merge passing final validation into an existing integrity audit."""

        manifest = self.base_manifest()
        manifest["mode"] = "final"
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        audit_path = self.root / "figure_integrity_audit.json"

        audit_path.write_text(
            json.dumps(
                {"schema_version": 1, "passed": True, "checks": {"coverage": "pass"}}
            ),
            encoding="utf-8",
        )

        report = MODULE.validate(self.notebook_path, self.manifest_path, "final")
        MODULE.write_validation(report, audit_path, "final")
        merged = json.loads(audit_path.read_text(encoding="utf-8"))
        self.assertTrue(merged["passed"])
        self.assertIn("notebook_validation", merged)
        self.assertEqual(merged["checks"], {"coverage": "pass"})

    def test_final_mode_can_recover_from_prior_notebook_failure(self) -> None:
        """Clear a prior notebook failure after a passing final validation."""

        manifest = self.base_manifest()
        manifest["mode"] = "final"
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        audit_path = self.root / "figure_integrity_audit.json"

        audit_path.write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "passed": False,
                    "failed_checks": ["notebook_reproducibility"],
                    "checks": [{"id": "coverage", "status": "pass"}],
                    "notebook_validation": {"passed": False},
                }
            ),
            encoding="utf-8",
        )

        report = MODULE.validate(self.notebook_path, self.manifest_path, "final")
        MODULE.write_validation(report, audit_path, "final")
        merged = json.loads(audit_path.read_text(encoding="utf-8"))
        self.assertTrue(merged["passed"])
        self.assertEqual(merged["failed_checks"], [])


if __name__ == "__main__":
    unittest.main()
