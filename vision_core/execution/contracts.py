from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class FileOperation:
    target_file: str
    op: str
    content: str = ""


@dataclass(slots=True)
class ExecutionPlan:
    mission_id: str
    operations: list[FileOperation] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class FileDiff:
    target_file: str
    diff_text: str


@dataclass(slots=True)
class ExecutionReceipt:
    mission_id: str
    status: str
    applied_files: int
    details: list[str] = field(default_factory=list)
    diffs: list[FileDiff] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
