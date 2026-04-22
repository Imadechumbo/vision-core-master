from __future__ import annotations
from pathlib import Path
import shutil
from jarvis_v5.memory_plane.patch_registry import PatchRegistry

def rollback_patch(storage_dir: str, project: str, patch_id: str, target_root: str | None = None) -> dict:
    registry = PatchRegistry(storage_dir)
    record = registry.get(patch_id)
    if not record:
        return {"ok": False, "error": "patch-id não encontrado"}

    backup_file = record.get("backup_file")
    target_file = record.get("target_file")
    if target_root and target_file:
        target_file = str(Path(target_root) / Path(target_file).name)

    if not backup_file or not Path(backup_file).exists():
        return {"ok": False, "error": "backup_file ausente"}
    if not target_file:
        return {"ok": False, "error": "target_file ausente"}

    Path(target_file).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_file, target_file)
    return {
        "ok": True,
        "project": project,
        "patch_id": patch_id,
        "restored_to": str(target_file),
        "backup_file": str(backup_file),
    }
