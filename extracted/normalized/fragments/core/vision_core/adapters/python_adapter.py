from pathlib import Path
import re

def inspect_python_project(project_root):
    root = Path(project_root)
    exists = root.exists() and root.is_dir()
    info = {
        "root_exists": exists,
        "root": str(root),
        "is_python_project": False,
        "frameworks": [],
        "entry_candidates": [],
        "has_requirements_txt": False,
        "has_pyproject_toml": False,
        "detected_ports": [],
        "sample_files": [],
    }
    if not exists:
        return info

    req = root / "requirements.txt"
    pyproject = root / "pyproject.toml"
    info["has_requirements_txt"] = req.exists()
    info["has_pyproject_toml"] = pyproject.exists()

    candidates = []
    for p in list(root.rglob("*.py"))[:60]:
        rel = p.relative_to(root).as_posix()
        info["sample_files"].append(rel)
        if p.name in {"app.py", "main.py", "server.py", "wsgi.py"}:
            candidates.append(rel)

        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if "FastAPI(" in text and "fastapi" not in info["frameworks"]:
            info["frameworks"].append("FastAPI")
        if "Flask(" in text and "Flask" not in info["frameworks"]:
            info["frameworks"].append("Flask")
        if "django" in text.lower() and "Django" not in info["frameworks"]:
            info["frameworks"].append("Django")
        for m in re.findall(r"port\s*=\s*(\d{2,5})", text, flags=re.I):
            if m not in info["detected_ports"]:
                info["detected_ports"].append(m)
    info["entry_candidates"] = candidates
    info["is_python_project"] = info["has_requirements_txt"] or info["has_pyproject_toml"] or bool(info["sample_files"])
    return info
