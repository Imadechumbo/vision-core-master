from __future__ import annotations

from pathlib import Path
from core.mission.schema import Mission


def collect_evidence(mission: Mission, adapter) -> dict:
    project_root_exists = bool(mission.project_root and Path(mission.project_root).exists())
    return {
        "intent": mission.intent,
        "project_root": mission.project_root,
        "project_root_exists": project_root_exists,
        "adapter_project": adapter.project_id,
        "signals": _derive_signals(mission),
    }


def _derive_signals(mission: Mission) -> list[str]:
    text = mission.raw_mission.lower()
    signals: list[str] = []
    if "vision" in text:
        signals.append("vision_requested")
    if "zip" in text:
        signals.append("zip_requested")
    if "print" in text or "imagem" in text:
        signals.append("image_requested")
    if mission.project_root:
        signals.append("local_project_mode")
    return signals
