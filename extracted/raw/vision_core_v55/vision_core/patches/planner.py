from __future__ import annotations
import pathlib
from typing import Any, Dict, List
from vision_core.adapters.python import detect_python_project
from vision_core.utils.io import read_text
from vision_core.utils.time import utc_now_iso, utc_stamp

def _replace_or_append_env_fallback(content: str) -> str:
    if "PORT" in content and "os.getenv" in content:
        return content
    if "from os import getenv" in content:
        return content
    if "import os" not in content:
        content = "import os\n" + content
    return content

def _plan_fix_python_port(file_path: str, content: str) -> Dict[str, Any] | None:
    lower = content.lower()
    markers = ["app.run(", "uvicorn.run(", "runserver"]
    if not any(m in lower for m in markers):
        return None
    new_content = content
    changed = False

    if "app.run(" in content and "port=" not in content:
        new_content = new_content.replace("app.run(", "app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8000')), ")
        changed = True

    if "uvicorn.run(" in content and "port=" not in content:
        new_content = new_content.replace("uvicorn.run(", "uvicorn.run(port=int(os.getenv('PORT', '8000')), host='0.0.0.0', ")
        changed = True

    if changed:
        new_content = _replace_or_append_env_fallback(new_content)
        return {
            "op": "replace_file",
            "target": file_path,
            "reason": "fix_python_runtime_host_port",
            "content": new_content,
        }
    return None

def _plan_add_requirements(project_root: pathlib.Path, info: Dict[str, Any]) -> Dict[str, Any] | None:
    req = project_root / "requirements.txt"
    if req.exists():
        content = read_text(req)
        additions: List[str] = []
        if "fastapi" in info["frameworks"] and "fastapi" not in content.lower():
            additions.append("fastapi")
        if "fastapi" in info["frameworks"] and "uvicorn" not in content.lower():
            additions.append("uvicorn")
        if "flask" in info["frameworks"] and "flask" not in content.lower():
            additions.append("Flask")
        if "django" in info["frameworks"] and "django" not in content.lower():
            additions.append("Django")
        if not additions:
            return None
        new_content = content.rstrip() + "\n" + "\n".join(additions) + "\n"
        return {"op": "replace_file", "target": "requirements.txt", "reason": "sync_requirements", "content": new_content}

    if not info["frameworks"]:
        return None
    lines: List[str] = []
    if "fastapi" in info["frameworks"]:
        lines += ["fastapi", "uvicorn"]
    if "flask" in info["frameworks"]:
        lines += ["Flask"]
    if "django" in info["frameworks"]:
        lines += ["Django"]
    return {"op": "create_file", "target": "requirements.txt", "reason": "create_requirements", "content": "\n".join(lines) + "\n"}

def _plan_add_health_endpoint(file_path: str, content: str, framework: str) -> Dict[str, Any] | None:
    if "/health" in content or "health" in content.lower():
        return None
    if framework == "fastapi" and "FastAPI(" in content:
        new_content = content.rstrip() + "\n\n@app.get('/health')\ndef health():\n    return {'ok': True, 'service': 'python-service'}\n"
        return {"op": "replace_file", "target": file_path, "reason": "add_health_endpoint", "content": new_content}
    if framework == "flask" and "Flask(" in content:
        new_content = content.rstrip() + "\n\n@app.get('/health')\ndef health():\n    return {'ok': True, 'service': 'python-service'}\n"
        return {"op": "replace_file", "target": file_path, "reason": "add_health_endpoint", "content": new_content}
    return None

def generate_patch_plan(project_root: str, failure_type: str = "", profile: str = "python-service") -> Dict[str, Any]:
    root = pathlib.Path(project_root)
    info = detect_python_project(project_root)
    operations: List[Dict[str, Any]] = []

    candidates = info["entry_candidates"][:5]
    for rel in candidates:
        abs_path = root / rel
        content = read_text(abs_path)
        op = _plan_fix_python_port(rel, content)
        if op:
            operations.append(op)

        for fw in info["frameworks"]:
            op2 = _plan_add_health_endpoint(rel, content if not op else op["content"], fw)
            if op2:
                operations.append(op2)
                break

    req_op = _plan_add_requirements(root, info)
    if req_op:
        operations.append(req_op)

    dedup = []
    seen = set()
    for op in operations:
        key = (op["op"], op["target"], op["reason"])
        if key not in seen:
            dedup.append(op)
            seen.add(key)

    return {
        "plan_id": f"plan_{utc_stamp()}",
        "created_at": utc_now_iso(),
        "project_root": str(root),
        "profile": profile,
        "failure_type": failure_type,
        "adapter": "python",
        "analysis": info,
        "operations": dedup,
        "risk": "medium" if len(dedup) > 1 else "low",
        "requires_pass_gold": True,
        "rollback_mode": "snapshot_multi_file",
    }
