from __future__ import annotations
import json, shutil
from pathlib import Path

class RestoreManager:
    def __init__(self, vault_root: str) -> None:
        self.vault_root = Path(vault_root)

    @staticmethod
    def _normalize_path(value: str) -> str:
        return str(Path(value))

    def restore_snapshot(self, snapshot_id: str) -> dict:
        snapshot_dir = self.vault_root / snapshot_id
        manifest_file = snapshot_dir / "manifest.json"
        if not manifest_file.exists():
            raise FileNotFoundError(f"snapshot manifest not found: {snapshot_id}")

        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        restored = []

        for entry in manifest.get("files", []):
            target = Path(entry["target_file"])
            backup_file = snapshot_dir / "files" / entry["file_name"]

            if entry["source_existed"]:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(backup_file, target)
                restored.append({"target_file": str(target), "action": "restored_previous_file"})
            else:
                if target.exists():
                    target.unlink()
                restored.append({"target_file": str(target), "action": "removed_created_file"})

        return {"snapshot_id": snapshot_id, "restored": restored}

    def restore_file(self, snapshot_id: str, target_file: str) -> dict:
        snapshot_dir = self.vault_root / snapshot_id
        manifest_file = snapshot_dir / "manifest.json"
        if not manifest_file.exists():
            raise FileNotFoundError(f"snapshot manifest not found: {snapshot_id}")

        manifest = json.loads(manifest_file.read_text(encoding="utf-8"))
        requested = self._normalize_path(target_file)

        for entry in manifest.get("files", []):
            stored = self._normalize_path(entry["target_file"])
            if stored == requested:
                target = Path(entry["target_file"])
                backup_file = snapshot_dir / "files" / entry["file_name"]
                if entry["source_existed"]:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup_file, target)
                    return {"target_file": str(target), "action": "restored_previous_file"}
                else:
                    if target.exists():
                        target.unlink()
                    return {"target_file": str(target), "action": "removed_created_file"}

        raise FileNotFoundError(f"target file not found in snapshot: {target_file}")
