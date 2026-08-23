"""Tests for the governed plotting-script template."""

from __future__ import annotations

import ast
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).parents[1]
TEMPLATE = SKILL_ROOT / "assets" / "research_figure_template.py"


class FigureScriptTemplateTests(unittest.TestCase):
    """Check the direct-script plotting boundary."""

    def test_template_uses_scienceplots_script(self) -> None:
        """Require SciencePlots and a dedicated render function."""
        source = TEMPLATE.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(TEMPLATE))
        function_names = {
            node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
        }
        self.assertIn("import scienceplots", source)
        self.assertIn('STYLE_STACK = ["science", "no-latex"]', source)
        self.assertIn("render_figure", function_names)

    def test_skill_contains_no_notebook_assets(self) -> None:
        """Keep governed figure assets free of Jupyter notebooks."""
        self.assertEqual([], list(SKILL_ROOT.rglob("*.ipynb")))


if __name__ == "__main__":
    unittest.main()
