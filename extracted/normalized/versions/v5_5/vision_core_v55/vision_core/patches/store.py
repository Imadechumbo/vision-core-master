from __future__ import annotations
import pathlib
from typing import Any, Dict
from vision_core.utils.io import write_json, read_json, ensure_dir

def save_plan(data_dir: str, plan: Dict[str, Any], filename: str | None = None) -> str:
    plans_dir = ensure_dir(pathlib.Path(data_dir) / "plans")
    name = filename or f"{plan['plan_id']}.json"
    path = plans_dir / name
    write_json(path, plan)
    return str(path)

def load_plan(path: str) -> Dict[str, Any]:
    plan = read_json(path)
    if not isinstance(plan, dict):
        raise ValueError("invalid_plan_json")
    return plan
