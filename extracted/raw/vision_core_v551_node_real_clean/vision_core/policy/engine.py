from vision_core.utils import utc_now_iso

def evaluate_policy(pass_gold, gates, patch_plan, codex_review_requested=False, incidents_open=0):
    reasons = []
    promote = True

    if not pass_gold:
        promote = False
        reasons.append("PASS_GOLD_REQUIRED")

    if not gates.get("ok", False):
        promote = False
        reasons.append("GATES_FAILED")

    operations = patch_plan.get("operations", [])
    if patch_plan.get("ok") and len(operations) == 0:
        promote = False
        reasons.append("EMPTY_PLAN")

    if patch_plan.get("ok") is False:
        promote = False
        reasons.append("PATCH_PLAN_INVALID")

    if incidents_open > 0:
        promote = False
        reasons.append("INCIDENTS_OPEN")

    return {
        "ok": True,
        "checked_at": utc_now_iso(),
        "action": "promote" if promote else "hold",
        "promote": promote,
        "reasons": reasons,
        "policy": {
            "pass_gold_required": True,
            "codex_review_requested": codex_review_requested,
            "incidents_open": incidents_open,
        },
        "next_steps": (
            ["permitir merge", "gerar snapshot gold"] if promote else
            ["corrigir gates, plano ou incidentes", "reexecutar validação"]
        ),
    }
