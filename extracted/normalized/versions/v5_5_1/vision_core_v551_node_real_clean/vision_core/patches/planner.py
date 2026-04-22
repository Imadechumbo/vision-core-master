from pathlib import Path
from vision_core.utils import utc_now_iso, utc_stamp
from vision_core.adapters.detect import detect_adapter
from vision_core.adapters.node_adapter import inspect_node_project

def _build_node_vision_null_guard(root: Path, failure_type: str):
    node_info = inspect_node_project(str(root))
    candidates = []
    ft = failure_type.lower()
    for rel in node_info.get("mimetype_usages", []):
        candidates.append(rel)
    if not candidates:
        for rel in node_info.get("vision_candidates", []):
            candidates.append(rel)
    # prefer route files
    ranked = sorted(set(candidates), key=lambda x: (0 if "/routes/" in x else 1, x))
    ops = []
    for rel in ranked:
        p = root / rel
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "req.file.mimetype" in text:
            ops.append({
                "type": "insert_guard_before_pattern",
                "file": rel,
                "pattern": "req.file.mimetype",
                "guard": "if (!req.file) {\n  return res.status(400).json({ ok: false, error: 'file_required' });\n}\n\n",
                "reason": "Prevent null access before req.file.mimetype",
            })
            break
    risk = "medium" if ops else "low"
    return node_info, ops, risk

def build_patch_plan(project_root, failure_type, profile="auto"):
    root = Path(project_root)
    if not root.exists() or not root.is_dir():
        return {
            "ok": False,
            "error": "invalid_project_root",
            "project_root": str(root),
            "profile": profile,
        }

    detection = detect_adapter(str(root), profile)
    adapter = detection.get("selected_adapter")
    analysis = detection.get(adapter or "node") if adapter in ("node", "python") else detection

    operations = []
    risk = "low"
    if adapter == "node":
        node_info, operations, risk = _build_node_vision_null_guard(root, failure_type)
        analysis = node_info
    elif adapter == "python":
        analysis = detection.get("python", {})
    return {
        "ok": True,
        "plan_id": f"plan_{utc_stamp()}",
        "created_at": utc_now_iso(),
        "project_root": str(root),
        "profile": profile,
        "failure_type": failure_type,
        "adapter": adapter,
        "analysis": analysis,
        "operations": operations,
        "risk": risk,
        "requires_pass_gold": True,
        "rollback_mode": "snapshot_multi_file",
    }
