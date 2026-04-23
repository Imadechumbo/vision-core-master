from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timezone
from math import ceil
from pathlib import Path
from typing import Any

from vision_core.integration.codex.bridge import CodexBridge
from vision_core.integration.contracts import IntegrationResult
from vision_core.integration.github.bridge import GitHubBridge
from vision_core.integration.pr_validation import PRValidationService


class IntegrationOrchestrator:
    def __init__(self, runtime_root: str | Path, repository_root: str | Path | None = None):
        runtime_root = Path(runtime_root)
        self.runtime_root = runtime_root
        self.state_root = runtime_root / "integration"
        self.state_root.mkdir(parents=True, exist_ok=True)
        self.state_file = self.state_root / "last_integration.json"
        self.history_file = self.state_root / "history.json"
        self.codex = CodexBridge(runtime_root / "codex_exports")
        self.pr_validation = PRValidationService()
        self.github = GitHubBridge(repository_root=repository_root)

    def run(self, data: dict) -> IntegrationResult:
        codex_result = self.codex.export(data)
        pr_validation = self.pr_validation.validate(data)
        github_result = self.github.publish(data, pr_validation)

        if pr_validation.merge_allowed and github_result.status in {"completed", "skipped", "noop"}:
            status = "ready"
        elif pr_validation.merge_allowed:
            status = "partial"
        else:
            status = "blocked"

        result = IntegrationResult(
            mission_id=data["mission_id"],
            status=status,
            codex=codex_result,
            pr_validation=pr_validation,
            github=github_result,
            metadata={"engine": "IntegrationOrchestrator", "state_file": str(self.state_file), "history_file": str(self.history_file)},
        )
        self.persist_last(result, data)
        self.append_history(result, data)
        return result

    def persist_last(self, result: IntegrationResult, pipeline_data: dict) -> None:
        payload = self._build_payload(result, pipeline_data)
        self.state_file.write_text(json.dumps(self._jsonable(payload), indent=2, ensure_ascii=False), encoding="utf-8")

    def append_history(self, result: IntegrationResult, pipeline_data: dict) -> None:
        history = self.read_history()
        payload = self._build_payload(result, pipeline_data)
        history.insert(0, payload)
        history = history[:200]
        self.history_file.write_text(json.dumps(self._jsonable(history), indent=2, ensure_ascii=False), encoding="utf-8")

    def read_last(self) -> dict[str, Any]:
        if not self.state_file.exists():
            return {
                "status": "empty",
                "integration": None,
                "reason": "No integration run persisted yet.",
            }
        return json.loads(self.state_file.read_text(encoding="utf-8"))

    def read_history(self) -> list[dict[str, Any]]:
        if not self.history_file.exists():
            return []
        payload = json.loads(self.history_file.read_text(encoding="utf-8"))
        return payload if isinstance(payload, list) else []

    def read_history_page(self, page: int = 1, page_size: int = 10) -> dict[str, Any]:
        history = self.read_history()
        safe_page_size = max(1, min(int(page_size), 100))
        total_items = len(history)
        total_pages = max(1, ceil(total_items / safe_page_size)) if total_items else 1
        safe_page = max(1, min(int(page), total_pages))
        start = (safe_page - 1) * safe_page_size
        end = start + safe_page_size
        items = history[start:end]
        return {
            "items": items,
            "pagination": {
                "page": safe_page,
                "page_size": safe_page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_previous": safe_page > 1,
                "has_next": safe_page < total_pages,
                "next_page": safe_page + 1 if safe_page < total_pages else None,
                "previous_page": safe_page - 1 if safe_page > 1 else None,
            },
        }

    def _build_payload(self, result: IntegrationResult, pipeline_data: dict) -> dict[str, Any]:
        return {
            "recorded_at": datetime.now(timezone.utc).isoformat(),
            "mission_id": result.mission_id,
            "status": result.status,
            "integration": result.to_dict(),
            "summary": {
                "mission": pipeline_data.get("mission"),
                "decision": pipeline_data.get("decision"),
                "validation": getattr(pipeline_data.get("validation"), "outcome", None),
                "pass_gold": getattr(pipeline_data.get("validation"), "pass_gold", None),
                "promotion_allowed": getattr(pipeline_data.get("security"), "promotion_allowed", None),
                "applied_files": getattr(pipeline_data.get("execution_receipt"), "applied_files", None),
                "snapshot_id": pipeline_data.get("snapshot_id"),
            },
            "diffs": pipeline_data.get("diffs", []),
            "github_debug": self.github.get_debug_state(),
        }

    def _jsonable(self, value: Any) -> Any:
        if is_dataclass(value):
            return asdict(value)
        if isinstance(value, dict):
            return {k: self._jsonable(v) for k, v in value.items()}
        if isinstance(value, (list, tuple)):
            return [self._jsonable(v) for v in value]
        return value
