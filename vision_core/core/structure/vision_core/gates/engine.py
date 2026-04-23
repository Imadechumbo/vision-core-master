import py_compile
import shutil
import subprocess
from pathlib import Path
from vision_core.adapters.detect import detect_adapter

def _run_node_check(file_path):
    node = shutil.which("node")
    if not node:
        return {"ok": None, "skipped": True, "reason": "node_not_found", "file": str(file_path)}
    proc = subprocess.run([node, "--check", str(file_path)], capture_output=True, text=True)
    return {
        "ok": proc.returncode == 0,
        "skipped": False,
        "file": str(file_path),
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }

def run_gates(project_root, profile="auto"):
    detection = detect_adapter(project_root, profile)
    if not detection.get("ok"):
        return {"ok": False, "error": "invalid_project_root", "details": detection}

    selected = detection.get("selected_adapter")
    results = []
    overall = True

    root = Path(project_root)
    if selected == "node":
        checked = []
        errors = []
        for p in list(root.rglob("*.js"))[:120]:
            checked.append(str(p.relative_to(root)).replace("\\", "/"))
            out = _run_node_check(p)
            if out["ok"] is False:
                overall = False
                errors.append(out)
        results.append({
            "gate": "node_syntax",
            "ok": len(errors) == 0,
            "checked": checked,
            "errors": errors,
        })
    elif selected == "python":
        checked = []
        errors = []
        for p in list(root.rglob("*.py"))[:120]:
            rel = str(p.relative_to(root)).replace("\\", "/")
            checked.append(rel)
            try:
                py_compile.compile(str(p), doraise=True)
            except Exception as exc:
                overall = False
                errors.append({"file": rel, "error": str(exc)})
        results.append({
            "gate": "python_syntax",
            "ok": len(errors) == 0,
            "checked": checked,
            "errors": errors,
        })
    else:
        overall = False
        results.append({"gate": "adapter_detected", "ok": False, "checked": [], "errors": [{"error": "no_adapter_selected"}]})

    return {
        "ok": overall,
        "selected_adapter": selected,
        "results": results,
    }
