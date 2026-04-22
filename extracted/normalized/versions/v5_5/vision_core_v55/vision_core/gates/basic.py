from __future__ import annotations
import pathlib, py_compile
from typing import Any, Dict, List

def run_python_syntax_gate(project_root: str) -> Dict[str, Any]:
    root = pathlib.Path(project_root)
    checked, errors = [], []
    for py in root.rglob("*.py"):
        try:
            py_compile.compile(str(py), doraise=True)
            checked.append(str(py.relative_to(root)).replace("\\", "/"))
        except Exception as exc:
            errors.append({"file": str(py.relative_to(root)).replace("\\", "/"), "error": str(exc)})
    return {"gate": "python_syntax", "ok": not errors, "checked": checked[:200], "errors": errors[:50]}

def run_default_gates(project_root: str) -> Dict[str, Any]:
    syntax = run_python_syntax_gate(project_root)
    overall = syntax["ok"]
    return {"ok": overall, "results": [syntax]}
