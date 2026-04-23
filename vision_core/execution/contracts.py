from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ExecutionPlan:
    mission_id: str
    target_file: str
    operations: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class ExecutionReceipt:
    mission_id: str
    target_file: str
    status: str
    changed: bool
    applied_operations: int
    details: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
