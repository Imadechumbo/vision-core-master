from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SnapshotRecord:
    mission_id: str
    snapshot_id: str
    snapshot_dir: str
    files: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class RestoreResult:
    mission_id: str
    snapshot_id: str
    restored: bool
    restored_files: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
