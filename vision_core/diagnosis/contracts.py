from dataclasses import dataclass, field
from typing import Any

@dataclass(slots=True)
class EvidenceItem:
    kind: str
    value: str

@dataclass(slots=True)
class DiagnosisResult:
    mission_id: str
    summary: str
    root_cause: str
    confidence: float
    strategy: str
    source: str
    evidence: list[EvidenceItem] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
