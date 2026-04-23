from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from vision_core.integration.contracts import CodexExportResult


class CodexBridge:
    def __init__(self, export_root: str | Path):
        self.export_root = Path(export_root)
        self.export_root.mkdir(parents=True, exist_ok=True)

    def export(self, data: dict) -> CodexExportResult:
        mission_id = data["mission_id"]
        bundle = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "mission_id": mission_id,
            "mission": data["mission"],
            "decision": data["decision"],
            "root_cause": data["diagnosis"].root_cause,
            "strategy": data["diagnosis"].strategy,
            "validation": {
                "outcome": data["validation"].outcome,
                "pass_gold": data["validation"].pass_gold,
                "gates": data["validation"].gates,
                "findings": data["validation"].findings,
            },
            "security": {
                "promotion_allowed": data["security"].promotion_allowed,
                "reasons": data["security"].reasons,
            },
            "execution": {
                "applied_files": data["execution_receipt"].applied_files,
                "details": data["execution_receipt"].details,
                "diffs": [
                    {
                        "target_file": item.target_file,
                        "diff_text": item.diff_text,
                    }
                    for item in data["execution_receipt"].diffs
                ],
            },
            "snapshot_id": data["snapshot_id"],
        }

        path = self.export_root / f"{mission_id}_codex_bundle.json"
        path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False), encoding="utf-8")

        return CodexExportResult(
            status="exported",
            bundle_path=str(path),
            files_exported=len(bundle["execution"]["diffs"]),
            metadata={"engine": "CodexBridge"},
        )
