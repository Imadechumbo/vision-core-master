from pathlib import Path
from vision_core.adapters.detect import detect_adapter
from vision_core.patches.planner import build_patch_plan
from vision_core.patches.apply import apply_plan
from vision_core.gates.engine import run_gates
from vision_core.policy.engine import evaluate_policy
from vision_core.utils import utc_now_iso

def run_mission(project_root, mission, profile="auto"):
    root = Path(project_root)
    if not root.exists() or not root.is_dir():
        return {
            "ok": False,
            "error": "invalid_project_root",
            "project_root": str(root),
            "mission": mission,
        }

    detection = detect_adapter(str(root), profile)
    if not detection.get("ok") or not detection.get("selected_adapter"):
        return {
            "ok": False,
            "error": "adapter_not_detected",
            "project_root": str(root),
            "mission": mission,
            "detection": detection,
        }

    plan = build_patch_plan(str(root), mission, profile)
    apply_receipt = apply_plan(str(root), plan) if plan.get("operations") else {
        "ok": False,
        "error": "empty_plan",
        "applied": [],
        "snapshot_id": None,
        "plan_id": plan.get("plan_id"),
    }
    gates = run_gates(str(root), profile)
    policy = evaluate_policy(
        pass_gold=(gates.get("ok", False) and bool(plan.get("operations")) and apply_receipt.get("ok", False)),
        gates=gates,
        patch_plan=plan,
        codex_review_requested=True,
        incidents_open=0,
    )
    return {
        "ok": True,
        "ran_at": utc_now_iso(),
        "mission": mission,
        "adapter_info": detection,
        "plan": plan,
        "apply_receipt": apply_receipt,
        "gates": gates,
        "policy": policy,
    }
