from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Any
import uuid


@dataclass
class Mission:
    raw_mission: str
    project_id: str
    intent: str
    project_root: str | None = None
    risk_profile: str = "medium"
    targets: list[str] = field(default_factory=list)
    artifacts: list[dict[str, Any]] = field(default_factory=list)
    constraints: dict[str, Any] = field(default_factory=lambda: {
        "require_pass_gold": True,
        "allow_production": False,
        "allow_autopatch": False,
        "allow_external_api": "fallback_only",
    })
    mission_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
