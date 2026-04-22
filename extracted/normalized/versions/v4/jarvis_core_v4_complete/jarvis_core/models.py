from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass
class Mission:
    raw: str
    normalized: str
    intent: str


@dataclass
class PatchOperation:
    file: str
    op_type: str
    target: str
    content: str
    reason: str = ''


@dataclass
class StructuredPatch:
    operations: List[PatchOperation] = field(default_factory=list)
    risk_level: str = 'medium'
    summary: str = ''

    def to_dict(self):
        return {
            'operations': [asdict(op) for op in self.operations],
            'risk_level': self.risk_level,
            'summary': self.summary,
        }


@dataclass
class RCAResult:
    root_cause: str
    cause_chain: List[str]
    confidence: str = 'medium'
    evidence: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
