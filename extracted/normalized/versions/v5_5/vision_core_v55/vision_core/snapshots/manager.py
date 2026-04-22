from __future__ import annotations
import pathlib, shutil
from typing import Any, Dict, List
from vision_core.utils.io import ensure_dir, read_text, write_json, copy_file
from vision_core.utils.time import utc_now_iso, utc_stamp

def create_snapshot(project_root: str, rel_paths: List[str], data_dir: str) -> Dict[str, Any]:
    project = pathlib.Path(project_root)
    snapshots_dir = ensure_dir(pathlib.Path(data_dir) / "snapshots")
    snapshot_id = f"snap_{utc_stamp()}"
    snap_root = snapshots_dir / snapshot_id
    ensure_dir(snap_root / "files")

    items = []
    for rel in rel_paths:
        src = project / rel
        exists_before = src.exists()
        backup_target = snap_root / "files" / rel
        if exists_before:
            copy_file(src, backup_target)
        items.append({"path": rel, "exists_before": exists_before})

    manifest = {
        "snapshot_id": snapshot_id,
        "created_at": utc_now_iso(),
        "project_root": str(project),
        "items": items,
    }
    write_json(snap_root / "manifest.json", manifest)
    return manifest

def rollback_snapshot(project_root: str, data_dir: str, snapshot_id: str) -> Dict[str, Any]:
    project = pathlib.Path(project_root)
    snap_root = pathlib.Path(data_dir) / "snapshots" / snapshot_id
    manifest_path = snap_root / "manifest.json"
    if not manifest_path.exists():
        return {"ok": False, "error": "snapshot_not_found", "snapshot_id": snapshot_id}

    import json
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    restored = []
    removed = []
    for item in manifest["items"]:
        rel = item["path"]
        src_backup = snap_root / "files" / rel
        dst = project / rel
        if item["exists_before"]:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src_backup, dst)
            restored.append(rel)
        else:
            if dst.exists():
                dst.unlink()
                removed.append(rel)
    return {"ok": True, "snapshot_id": snapshot_id, "restored": restored, "removed": removed}
