from __future__ import annotations


def evaluate_policy(mission, root_cause):
    risk = 20
    if mission.risk_profile == "high":
        risk = 80
    if root_cause.get("root_cause_class") == "missing_project_root_or_invalid_path":
        risk = max(risk, 60)
    return {
        "engine": "aegis-lite",
        "risk_score": risk,
        "allow_shell": False,
        "allow_deploy": False,
        "require_human_approval": risk >= 70,
    }
