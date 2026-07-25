"""Lightweight guardrails for Onion Architecture dependency direction."""

import ast
from pathlib import Path
import unittest


SOURCE_ROOT = Path(__file__).resolve().parents[1] / "src"


def imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
    return modules


class ArchitectureBoundaryTests(unittest.TestCase):
    def test_domain_has_no_framework_or_infrastructure_dependencies(self):
        forbidden_roots = {"pandas", "pytz", "streamlit", "yfinance"}
        for path in (SOURCE_ROOT / "domain").rglob("*.py"):
            for module in imported_modules(path):
                self.assertNotIn(
                    module.split(".")[0],
                    forbidden_roots,
                    f"{path.relative_to(SOURCE_ROOT)} imports {module}",
                )

    def test_application_does_not_depend_on_outer_layers(self):
        forbidden_parts = {"infrastructure", "presentation"}
        forbidden_roots = {"pandas", "streamlit", "yfinance"}
        for path in (SOURCE_ROOT / "application").rglob("*.py"):
            for module in imported_modules(path):
                parts = set(module.split("."))
                self.assertFalse(
                    parts & forbidden_parts,
                    f"{path.relative_to(SOURCE_ROOT)} imports {module}",
                )
                self.assertNotIn(
                    module.split(".")[0],
                    forbidden_roots,
                    f"{path.relative_to(SOURCE_ROOT)} imports {module}",
                )


if __name__ == "__main__":
    unittest.main()
