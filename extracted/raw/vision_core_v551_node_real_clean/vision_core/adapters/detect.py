from pathlib import Path
from vision_core.adapters.node_adapter import inspect_node_project
from vision_core.adapters.python_adapter import inspect_python_project

def detect_adapter(project_root, profile="auto"):
    root = Path(project_root)
    if not root.exists() or not root.is_dir():
        return {
            "ok": False,
            "error": "invalid_project_root",
            "project_root": str(root),
            "profile": profile,
            "selected_adapter": None,
        }
    node_info = inspect_node_project(project_root)
    py_info = inspect_python_project(project_root)

    selected = None
    reason = "no_match"
    if profile in {"node", "node-service"}:
        selected, reason = "node", "profile_forced"
    elif profile in {"python", "python-service"}:
        selected, reason = "python", "profile_forced"
    elif node_info.get("is_node_project"):
        selected, reason = "node", "package_json_detected"
    elif py_info.get("is_python_project"):
        selected, reason = "python", "python_markers_detected"

    return {
        "ok": True,
        "project_root": str(root),
        "profile": profile,
        "selected_adapter": selected,
        "reason": reason,
        "node": node_info,
        "python": py_info,
    }
