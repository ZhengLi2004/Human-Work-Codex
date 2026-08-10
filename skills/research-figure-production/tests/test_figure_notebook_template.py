"""Integration tests for the governed figure notebook template."""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import nbformat

SKILL_DIRECTORY = Path(__file__).parents[1]
REPOSITORY_ROOT = Path(__file__).parents[3]
TEMPLATE_PATH = SKILL_DIRECTORY / "assets" / "research_figures_template.ipynb"
VALIDATOR_PATH = SKILL_DIRECTORY / "scripts" / "validate_figure_notebook.py"


class FigureNotebookTemplateTests(unittest.TestCase):
    """Exercise planning and final notebook execution from a clean kernel."""

    def test_template_executes_cleanly_and_validates(self) -> None:
        """Execute configured planning and final notebooks and validate artifacts."""

        with tempfile.TemporaryDirectory() as temporary_name:
            root = Path(temporary_name)
            input_path = root / "complete-table.csv"

            input_path.write_text(
                "condition,x,value\nA,1,0.2\nB,2,0.5\nC,3,0.7\n", encoding="utf-8"
            )

            aggregation_validation_path = root / "aggregation-validation.json"

            aggregation_validation_path.write_text(
                json.dumps(
                    {
                        "schema_version": 1,
                        "passed": True,
                        "todo_fingerprint": "a" * 64,
                        "task_state_revision": 6,
                    }
                ),
                encoding="utf-8",
            )

            output_directory = root / "figures"
            output_directory.mkdir()
            notebook_path = root / "configured-figures.ipynb"
            notebook = nbformat.read(TEMPLATE_PATH, as_version=4)

            replacements = {
                "REPLACE_MODE": "planning",
                "REPLACE_TODO_SHA256": "a" * 64,
                "REPLACE_TASK_STATE_REVISION": "7",
                "REPLACE_EXECUTED_NOTEBOOK_PATH": str(notebook_path),
                "REPLACE_COMPLETE_INPUT_PATH": str(input_path),
                "REPLACE_AGGREGATION_VALIDATION_PATH": str(aggregation_validation_path),
                "REPLACE_GIT_REPOSITORY_DIRECTORY": str(REPOSITORY_ROOT),
                "REPLACE_FIGURE_DIRECTORY": str(output_directory),
                "REPLACE_STABLE_KEY": "condition",
                "REPLACE_STATISTICAL_UNIT": "independent repeat",
                "REPLACE_EXECUTION_COMMAND": "python -m jupyter nbconvert --execute --to notebook --inplace configured-figures.ipynb",
                "REPLACE_CHART_KIND": "line",
                "REPLACE_X_COLUMN": "x",
                "REPLACE_Y_COLUMN": "value",
                "REPLACE_FIGURE_TITLE": "Synthetic value by condition",
                "REPLACE_X_LABEL": "Condition index",
                "REPLACE_Y_LABEL": "Synthetic value",
                "REPLACE_MIN_OBSERVATIONS": "3",
                "REPLACE_GRAPHICAL_METHOD_BASIS": "Established ordered-series convention for the synthetic test",
            }

            for cell in notebook.cells:
                source = cell.source

                for placeholder, value in replacements.items():
                    source = source.replace(placeholder, value)

                cell.source = source

            nbformat.write(notebook, notebook_path)
            environment = os.environ.copy()

            environment["PATH"] = (
                str(Path(sys.executable).parent) + os.pathsep + environment["PATH"]
            )

            execute = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jupyter",
                    "nbconvert",
                    "--execute",
                    "--to",
                    "notebook",
                    "--inplace",
                    str(notebook_path),
                    "--ExecutePreprocessor.timeout=120",
                ],
                cwd=REPOSITORY_ROOT,
                env=environment,
                capture_output=True,
                text=True,
                timeout=180,
            )

            self.assertEqual(execute.returncode, 0, execute.stdout + execute.stderr)
            manifest_path = output_directory / "draft-figure-manifest.json"
            validation_path = output_directory / "notebook-validation.json"

            validate = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    "--notebook",
                    str(notebook_path),
                    "--manifest",
                    str(manifest_path),
                    "--mode",
                    "planning",
                    "--output",
                    str(validation_path),
                ],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                text=True,
                timeout=60,
            )

            validation_detail = (
                validation_path.read_text(encoding="utf-8")
                if validation_path.exists()
                else ""
            )

            self.assertEqual(
                validate.returncode,
                0,
                validate.stdout + validate.stderr + validation_detail,
            )

            report = json.loads(validation_path.read_text(encoding="utf-8"))
            self.assertTrue(report["passed"])
            self.assertTrue((output_directory / "draft" / "F1.pdf").is_file())
            self.assertTrue((output_directory / "draft" / "F1.png").is_file())
            self.assertTrue((output_directory / "figure-plan.json").is_file())
            self.assertTrue((output_directory / "figure-coverage.json").is_file())
            final_notebook_path = root / "configured-final-figures.ipynb"
            final_replacements = dict(replacements)

            final_replacements.update(
                {
                    "REPLACE_MODE": "final",
                    "REPLACE_TASK_STATE_REVISION": "8",
                    "REPLACE_EXECUTED_NOTEBOOK_PATH": str(final_notebook_path),
                    "REPLACE_EXECUTION_COMMAND": "python -m jupyter nbconvert --execute --to notebook --inplace configured-final-figures.ipynb",
                }
            )

            final_notebook = nbformat.read(TEMPLATE_PATH, as_version=4)

            for cell in final_notebook.cells:
                source = cell.source

                for placeholder, value in final_replacements.items():
                    source = source.replace(placeholder, value)

                source = source.replace(
                    "RESEARCHER_RECOMMENDATION_REFERENCE = None",
                    'RESEARCHER_RECOMMENDATION_REFERENCE = "synthetic-review-reference"',
                )

                source = source.replace(
                    "FIGURE_PLAN_PATH = None",
                    f'FIGURE_PLAN_PATH = Path(r"{output_directory / "figure-plan.json"}")',
                )

                source = source.replace(
                    "FIGURE_COVERAGE_PATH = None",
                    f'FIGURE_COVERAGE_PATH = Path(r"{output_directory / "figure-coverage.json"}")',
                )

                cell.source = source

            nbformat.write(final_notebook, final_notebook_path)

            execute_final = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "jupyter",
                    "nbconvert",
                    "--execute",
                    "--to",
                    "notebook",
                    "--inplace",
                    str(final_notebook_path),
                    "--ExecutePreprocessor.timeout=120",
                ],
                cwd=REPOSITORY_ROOT,
                env=environment,
                capture_output=True,
                text=True,
                timeout=180,
            )

            self.assertEqual(
                execute_final.returncode, 0, execute_final.stdout + execute_final.stderr
            )

            final_manifest_path = output_directory / "figure_manifest.json"
            audit_path = output_directory / "figure_integrity_audit.json"

            validate_final = subprocess.run(
                [
                    sys.executable,
                    str(VALIDATOR_PATH),
                    "--notebook",
                    str(final_notebook_path),
                    "--manifest",
                    str(final_manifest_path),
                    "--mode",
                    "final",
                    "--output",
                    str(audit_path),
                ],
                cwd=REPOSITORY_ROOT,
                capture_output=True,
                text=True,
                timeout=60,
            )

            final_audit_detail = (
                audit_path.read_text(encoding="utf-8") if audit_path.exists() else ""
            )

            self.assertEqual(
                validate_final.returncode,
                0,
                validate_final.stdout + validate_final.stderr + final_audit_detail,
            )

            final_audit = json.loads(final_audit_detail)
            self.assertTrue(final_audit["passed"])
            self.assertTrue(final_audit["notebook_validation"]["passed"])
            self.assertTrue((output_directory / "final" / "F1.pdf").is_file())
            self.assertTrue((output_directory / "final" / "F1.png").is_file())
            self.assertTrue((output_directory / "final-figure-coverage.json").is_file())


if __name__ == "__main__":
    unittest.main()
