from pathlib import Path
import shutil
import json
from vision_core.utils import utc_now_iso

def rollback_snapshot(project_root, snapshot_id):
    root = Path(project_root)
    snap_root = root / ".vision_core" / "snapshots" / snapshot_id
    manifest = snap_root / "manifest.json"
    if not manifest.exists():
        return {"ok": False, "error": "snapshot_not_found", "snapshot_id": snapshot_id}
    data = json.loads(manifest.read_text(encoding="utf-8"))
    restored = []
    for rel in data.get("backups", []):
        src = snap_root / rel
        dest = root / rel
        if src.exists():
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            restored.append(rel)
    return {
        "ok": True,
        "rolled_back_at": utc_now_iso(),
        "snapshot_id": snapshot_id,
        "restored": restored,
    }
