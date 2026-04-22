from __future__ import annotations
from typing import Any, Dict

def evaluate_promotion(pass_gold: bool, gates: Dict[str, Any], patch_plan: Dict[str, Any], codex_review_requested: bool = False, incidents_open: int = 0) -> Dict[str, Any]:
    reasons = []
    promote = True

    if not pass_gold:
        promote = False
        reasons.append("PASS_GOLD_REQUIRED")

    if not gates.get("ok", False):
        promote = False
        reasons.append("GATES_FAILED")

    if patch_plan.get("risk") == "high":
        promote = False
        reasons.append("HIGH_RISK_PLAN")

    if incidents_open > 0:
        promote = False
        reasons.append("OPEN_INCIDENTS")

    action = "promote" if promote else "hold"
    next_steps = []
    if not promote:
        next_steps = [
            "corrigir gates ou incidentes",
            "solicitar review adicional",
            "reexecutar validacao",
        ]
    else:
        next_steps = ["permitir merge", "gerar snapshot gold"]

    return {
        "ok": True,
        "action": action,
        "promote": promote,
        "reasons": reasons,
        "policy": {
            "pass_gold_required": True,
            "codex_review_requested": codex_review_requested,
            "incidents_open": incidents_open,
        },
        "next_steps": next_steps,
    }
