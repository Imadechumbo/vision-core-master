from __future__ import annotations
from vision_core.execution.contracts import FileDiff


class DiffService:
    def build_payload(self, diffs: list[FileDiff]) -> list[dict[str, str]]:
        payload: list[dict[str, str]] = []
        for item in diffs:
            payload.append({
                "target_file": item.target_file,
                "diff_text": item.diff_text,
            })
        return payload
