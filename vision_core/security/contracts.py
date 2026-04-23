from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class SecurityDecision:
    mission_id: str
    allowed: bool
    requires_gold: bool
    promotion_allowed: bool
    reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
