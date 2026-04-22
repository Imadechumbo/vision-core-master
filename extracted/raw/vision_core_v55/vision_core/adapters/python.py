from __future__ import annotations
import pathlib, re, json
from typing import Any, Dict, List
from vision_core.utils.io import read_text

FRAMEWORK_HINTS = {
    "fastapi": ["fastapi", "uvicorn", "APIRouter", "FastAPI("],
    "flask": ["flask", "Flask(", "Blueprint("],
    "django": ["django", "manage.py", "wsgi.py", "asgi.py"],
}

def _list_files(root: pathlib.Path) -> List[pathlib.Path]:
    out: List[pathlib.Path] = []
    for p in root.rglob("*"):
        if p.is_file():
            out.append(p)
    return out

def detect_python_project(project_root: str) -> Dict[str, Any]:
    root = pathlib.Path(project_root)
    files = _list_files(root)[:5000]
    names = {f.name.lower() for f in files}
    rels = [str(f.relative_to(root)).replace("\\", "/") for f in files]
    content_samples = "\n".join(
        read_text(f, "")[:3000] for f in files if f.suffix in {".py", ".txt", ".toml", ".cfg", ".ini", ".yml", ".yaml"}
    )[:50000]

    frameworks: List[str] = []
    for framework, hints in FRAMEWORK_HINTS.items():
        if any(h.lower() in content_samples.lower() or h.lower() in " ".join(rels).lower() for h in hints):
            frameworks.append(framework)

    entry_candidates = []
    for rel in rels:
        if rel.endswith(("main.py", "app.py", "server.py", "manage.py", "run.py", "wsgi.py", "asgi.py")):
            entry_candidates.append(rel)

    has_requirements = "requirements.txt" in names
    has_pyproject = "pyproject.toml" in names

    ports = sorted(set(re.findall(r'PORT["\']?\)?\s*[,)]?\s*or\s*(\d{2,5})|port\s*=\s*(\d{2,5})', content_samples, re.I)))
    flat_ports = sorted({p for tup in ports for p in tup if p})

    return {
        "root_exists": root.exists(),
        "root": str(root),
        "is_python_project": any(f.suffix == ".py" for f in files),
        "frameworks": frameworks,
        "entry_candidates": entry_candidates[:20],
        "has_requirements_txt": has_requirements,
        "has_pyproject_toml": has_pyproject,
        "detected_ports": flat_ports,
        "sample_files": rels[:50],
    }

def suggest_runtime_commands(project_root: str) -> Dict[str, Any]:
    info = detect_python_project(project_root)
    frameworks = info["frameworks"]
    entry = info["entry_candidates"][0] if info["entry_candidates"] else None
    commands = []
    if "fastapi" in frameworks:
        target = "main:app"
        if entry and entry.endswith(".py"):
            target = entry[:-3].replace("/", ".").replace("\\", ".") + ":app"
        commands.append(f"uvicorn {target} --host 0.0.0.0 --port $PORT")
    if "flask" in frameworks:
        if entry:
            commands.append(f"python {entry}")
        commands.append("flask run --host=0.0.0.0 --port=$PORT")
    if "django" in frameworks:
        commands.append("python manage.py runserver 0.0.0.0:$PORT")
    if entry:
        commands.append(f"python {entry}")
    return {"adapter": "python", "commands": commands, "info": info}
