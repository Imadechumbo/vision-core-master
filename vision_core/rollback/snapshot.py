from __future__ import annotations
import json, shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4
from vision_core.execution.contracts import ExecutionPlan

class SnapshotManager:
    def __init__(self, vault_root: str) -> None:
        self.vault_root = Path(vault_root)
        self.vault_root.mkdir(parents=True, exist_ok=True)

    def create_snapshot(self, mission_id: str, plan: ExecutionPlan) -> str:
        snapshot_id = f"snap-{uuid4().hex[:12]}"
        snapshot_dir = self.vault_root / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        files = []
        for op in plan.operations:
            target = Path(op.target_file)
            file_meta = {
                "target_file": str(target),
                "file_name": target.name,
                "source_existed": target.exists(),
            }
            if target.exists():
                backup_dir = snapshot_dir / "files"
                backup_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup_dir / target.name)
            files.append(file_meta)

        manifest = {
            "snapshot_id": snapshot_id,
            "mission_id": mission_id,
            "files": files,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        (snapshot_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return snapshot_id
