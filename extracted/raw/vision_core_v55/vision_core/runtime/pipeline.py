from __future__ import annotations
from typing import Any, Dict
from vision_core.adapters.python import detect_python_project
from vision_core.patches.planner import generate_patch_plan
from vision_core.patches.apply import apply_patch_plan
from vision_core.gates.basic import run_default_gates
from vision_core.policy.engine import evaluate_promotion
from vision_core.incidents.store import count_open_incidents
from vision_core.utils.time import utc_now_iso

def run_pipeline(project_root: str, mission: str, data_dir: str, profile: str = "python-service") -> Dict[str, Any]:
    adapter_info = detect_python_project(project_root)
    plan = generate_patch_plan(project_root, failure_type=mission, profile=profile)
    apply_receipt = apply_patch_plan(project_root, plan, data_dir) if plan.get("operations") else {
        "ok": True, "applied": [], "snapshot_id": None, "plan_id": plan["plan_id"]
    }
    gates = run_default_gates(project_root)
    policy = evaluate_promotion(
        pass_gold=gates.get("ok", False),
        gates=gates,
        patch_plan=plan,
        codex_review_requested=True,
        incidents_open=count_open_incidents(data_dir),
    )
    return {
        "ok": True,
        "ran_at": utc_now_iso(),
        "mission": mission,
        "adapter_info": adapter_info,
        "plan": plan,
        "apply_receipt": apply_receipt,
        "gates": gates,
        "policy": policy,
    }
