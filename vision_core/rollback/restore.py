from __future__ import annotations

import json
import shutil
from pathlib import Path


class RestoreManager:
    def __init__(self, vault_root: str) -> None:
        self.vault_root = Path(vault_root)

    def restore_snapshot(self, snapshot_id: str) -> dict:
        snapshot_dir = self.vault_root / snapshot_id
        manifest_file = snapshot_dir / "manifest.json"
        if not manifest_file.exists():
            raise FileNotFoundError(f"snapshot manifest not found: {snapshot_id}")

        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        target = Path(manifest["target_file"])
        backup_file = snapshot_dir / manifest["file_name"]

        if manifest["source_existed"]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_file, target)
            action = "restored_previous_file"
        else:
            if target.exists():
                target.unlink()
            action = "removed_created_file"

        return {
            "snapshot_id": snapshot_id,
            "target_file": str(target),
            "action": action,
        }
