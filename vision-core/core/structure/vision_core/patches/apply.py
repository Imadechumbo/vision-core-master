from pathlib import Path
import shutil
from vision_core.utils import utc_now_iso, utc_stamp, ensure_dir, write_json

def _insert_guard_before_pattern(file_path: Path, pattern: str, guard: str):
    original = file_path.read_text(encoding="utf-8", errors="ignore")
    idx = original.find(pattern)
    if idx < 0:
        return False, "pattern_not_found"
    # prevent duplicate insertion
    if guard.strip() in original:
        return False, "guard_already_present"
    updated = original[:idx] + guard + original[idx:]
    file_path.write_text(updated, encoding="utf-8")
    return True, "guard_inserted"

def apply_plan(project_root, plan):
    root = Path(project_root)
    if not root.exists() or not root.is_dir():
        return {"ok": False, "error": "invalid_project_root", "project_root": str(root)}
    ops = plan.get("operations", [])
    if not ops:
        return {
            "ok": False,
            "error": "empty_plan",
            "applied_at": utc_now_iso(),
            "snapshot_id": None,
            "plan_id": plan.get("plan_id"),
            "applied": [],
        }

    snapshot_id = f"snap_{utc_stamp()}"
    snap_root = ensure_dir(root / ".vision_core" / "snapshots" / snapshot_id)
    backups = []
    applied = []
    for op in ops:
        rel = op["file"]
        src = root / rel
        if not src.exists():
            applied.append({"file": rel, "ok": False, "reason": "file_not_found"})
            continue
        dest = snap_root / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        backups.append(rel)

        if op["type"] == "insert_guard_before_pattern":
            ok, reason = _insert_guard_before_pattern(src, op["pattern"], op["guard"])
            applied.append({"file": rel, "ok": ok, "reason": reason, "type": op["type"]})
        else:
            applied.append({"file": rel, "ok": False, "reason": "unknown_operation", "type": op["type"]})

    manifest = {
        "snapshot_id": snapshot_id,
        "created_at": utc_now_iso(),
        "project_root": str(root),
        "backups": backups,
        "plan_id": plan.get("plan_id"),
    }
    write_json(snap_root / "manifest.json", manifest)
    return {
        "ok": any(item["ok"] for item in applied),
        "applied_at": utc_now_iso(),
        "snapshot_id": snapshot_id,
        "plan_id": plan.get("plan_id"),
        "applied": applied,
    }
