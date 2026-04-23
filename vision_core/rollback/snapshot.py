from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


class SnapshotManager:
    def __init__(self, vault_root: str) -> None:
        self.vault_root = Path(vault_root)
        self.vault_root.mkdir(parents=True, exist_ok=True)

    def create_snapshot(self, mission_id: str, target_file: str) -> str:
        snapshot_id = f"snap-{uuid4().hex[:12]}"
        snapshot_dir = self.vault_root / snapshot_id
        snapshot_dir.mkdir(parents=True, exist_ok=True)

        target = Path(target_file)
        exists = target.exists()

        if exists:
            shutil.copy2(target, snapshot_dir / target.name)

        manifest = {
            "snapshot_id": snapshot_id,
            "mission_id": mission_id,
            "target_file": str(target),
            "file_name": target.name,
            "source_existed": exists,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        (snapshot_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return snapshot_id
