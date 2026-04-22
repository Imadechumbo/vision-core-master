from __future__ import annotations
from pathlib import Path

NODE_SIGNAL_FILES = [
    "package.json", "server.js", "app.js", "index.js", "main.js", "tsconfig.json",
]
NODE_SIGNAL_DIRS = ["routes", "src", "api", "controllers", "middlewares"]
PY_SIGNAL_FILES = ["requirements.txt", "pyproject.toml", "main.py", "app.py"]

def _exists_any(root: Path, items: list[str]) -> bool:
    return any((root / item).exists() for item in items)

def _collect_sample_files(root: Path, limit: int = 20) -> list[str]:
    out = []
    for p in root.rglob("*"):
        if len(out) >= limit:
            break
        if p.is_file():
            try:
                out.append(str(p.relative_to(root)).replace("/", "\\"))
            except Exception:
                out.append(p.name)
    return out

def scan_project(root_path: str) -> dict:
    root = Path(root_path)
    root_exists = root.exists() and root.is_dir()
    sample_files = _collect_sample_files(root) if root_exists else []
    env_files = []
    if root_exists:
        env_files = [
            str(p.relative_to(root)).replace("/", "\\")
            for p in root.rglob("*")
            if p.is_file() and (p.name.startswith(".env") or p.name.endswith(".env"))
        ][:20]

    node_project = root_exists and _exists_any(root, NODE_SIGNAL_FILES + NODE_SIGNAL_DIRS)
    python_project = root_exists and _exists_any(root, PY_SIGNAL_FILES)
    has_routes = root_exists and any((root / d).exists() for d in ["routes", "src/routes", "api", "src/api"])
    has_api = root_exists and (has_routes or any("api" in s.lower() or "route" in s.lower() for s in sample_files))

    return {
        "root_exists": root_exists,
        "root": str(root),
        "sample_files": sample_files,
        "env_files": env_files,
        "signals": {
            "node_project": bool(node_project),
            "python_project": bool(python_project),
            "has_routes": bool(has_routes),
            "has_api": bool(has_api),
        }
    }
