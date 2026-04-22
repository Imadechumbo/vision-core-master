from __future__ import annotations

from core.mission.schema import Mission


def normalize_mission(raw_mission: str, project_id: str, project_root: str | None, intent: str) -> Mission:
    mission = Mission(
        raw_mission=raw_mission,
        project_id=project_id,
        project_root=project_root,
        intent=intent,
        targets=["backend", "frontend"] if "zip" in raw_mission.lower() or "print" in raw_mission.lower() else ["backend"],
        risk_profile="high" if any(k in raw_mission.lower() for k in ["deploy", "rollback", "production"]) else "medium",
    )
    return mission
