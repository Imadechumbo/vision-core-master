from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class ValidationResult:
    mission_id: str
    outcome: str
    pass_gold: bool
    findings: list[str] = field(default_factory=list)
    gates: dict[str, bool] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
