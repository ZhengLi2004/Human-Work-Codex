"""Tests for governed plotting-script validation."""

from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "validate_figure_script.py"
SPEC = importlib.util.spec_from_file_location("validate_figure_script", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def digest(path: Path) -> str:
    """Return a test file's SHA-256 digest.

    Args:
        path: File to hash.

    Returns:
        Hexadecimal digest.
    """
    return hashlib.sha256(path.read_bytes()).hexdigest()


class FigureScriptValidationTests(unittest.TestCase):
    """Validate passing and failing figure-script fixtures."""

    def setUp(self) -> None:
        """Create a valid temporary plotting fixture."""
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.script = self.root / "plot.py"
        self.input = self.root / "input.csv"
        self.output = self.root / "figure.png"
        self.manifest = self.root / "manifest.json"
        self.report = self.root / "validation.json"

        self.script.write_text(
            "import scienceplots\n"
            "import matplotlib.pyplot as plt\n"
            "plt.style.use([\"science\", \"no-latex\"])\n",
            encoding="utf-8",
        )
        self.input.write_text("x,y\n1,2\n", encoding="utf-8")
        self.output.write_bytes(b"figure")
        self.write_manifest()

    def tearDown(self) -> None:
        """Remove the temporary fixture."""
        self.temporary.cleanup()

    def write_manifest(self) -> None:
        """Write a valid figure manifest for the current files."""
        payload = {
            "plotting_script": {"path": self.script.name, "sha256": digest(self.script)},
            "inputs": [{"path": self.input.name, "sha256": digest(self.input)}],
            "outputs": [{"path": self.output.name, "sha256": digest(self.output)}],
            "style_stack": ["science", "no-latex"],
            "execution": {
                "command": "python plot.py",
                "started_at_utc": "2026-08-23T00:00:00Z",
                "finished_at_utc": "2026-08-23T00:00:01Z",
                "status": "completed",
            },
            "todo_fingerprint": "abc",
            "task_state_revision": 1,
            "git_revision": "def",
            "package_versions": {"matplotlib": "3"},
            "data_quality_results": {"passed": True},
            "figure_data_sufficiency": {"passed": True},
        }
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")

    def test_valid_fixture_passes(self) -> None:
        """Accept a complete script and matching manifest."""
        report = MODULE.validate(self.script, self.manifest, "planning")
        self.assertTrue(report["passed"])

    def test_missing_scienceplots_import_fails(self) -> None:
        """Reject a script without the required style registration import."""
        self.script.write_text("import matplotlib.pyplot as plt\n", encoding="utf-8")
        self.write_manifest()
        report = MODULE.validate(self.script, self.manifest, "planning")
        self.assertIn("scienceplots_import", report["failed_checks"])

    def test_wrong_style_stack_fails(self) -> None:
        """Reject a manifest whose base style is not science."""
        payload = json.loads(self.manifest.read_text(encoding="utf-8"))
        payload["style_stack"] = ["default"]
        self.manifest.write_text(json.dumps(payload), encoding="utf-8")
        report = MODULE.validate(self.script, self.manifest, "planning")
        self.assertIn("science_style_stack", report["failed_checks"])

    def test_changed_output_hash_fails(self) -> None:
        """Reject an export that changed after manifest creation."""
        self.output.write_bytes(b"changed")
        report = MODULE.validate(self.script, self.manifest, "planning")
        self.assertIn("output_0_hash", report["failed_checks"])

    def test_final_mode_merges_validation(self) -> None:
        """Merge a passing final validation into the integrity audit."""
        self.report.write_text(json.dumps({"passed": True, "coverage": "pass"}), encoding="utf-8")
        report = MODULE.validate(self.script, self.manifest, "final")
        MODULE.write_validation(self.report, report, "final")
        audit = json.loads(self.report.read_text(encoding="utf-8"))
        self.assertTrue(audit["passed"])
        self.assertIn("plot_script_validation", audit)


if __name__ == "__main__":
    unittest.main()
