from __future__ import annotations
import pathlib
from typing import Any, Dict, List
from vision_core.snapshots.manager import create_snapshot
from vision_core.utils.io import write_text, read_json, write_json
from vision_core.utils.time import utc_now_iso

def apply_patch_plan(project_root: str, plan: Dict[str, Any], data_dir: str) -> Dict[str, Any]:
    operations = plan.get("operations", [])
    rel_paths = sorted({op["target"] for op in operations})
    snapshot = create_snapshot(project_root, rel_paths, data_dir)

    applied = []
    project = pathlib.Path(project_root)
    for op in operations:
        target = project / op["target"]
        if op["op"] in {"replace_file", "create_file"}:
            write_text(target, op["content"])
            applied.append({"target": op["target"], "op": op["op"], "reason": op["reason"]})
        else:
            raise ValueError(f"unsupported operation: {op['op']}")

    receipt = {
        "ok": True,
        "applied_at": utc_now_iso(),
        "snapshot_id": snapshot["snapshot_id"],
        "plan_id": plan.get("plan_id"),
        "applied": applied,
    }
    write_json(pathlib.Path(data_dir) / "last_apply_receipt.json", receipt)
    return receipt
