from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BaseProjectAdapter:
    project_id: str

    def detect_stack(self) -> dict:
        raise NotImplementedError

    def get_required_gates(self) -> list[str]:
        raise NotImplementedError

    def describe(self) -> dict:
        return {
            "project_id": self.project_id,
            "stack": self.detect_stack(),
            "required_gates": self.get_required_gates(),
        }
