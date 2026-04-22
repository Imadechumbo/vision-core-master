from __future__ import annotations
from pathlib import Path


class ProjectScanner:
    def scan(self, project_root: str | None) -> dict:
        if not project_root:
            return {"project_root": None, "exists": False, "summary": "no_project_root"}

        root = Path(project_root)
        if not root.exists():
            return {"project_root": str(root), "exists": False, "summary": "project_root_not_found"}

        interesting = [
            "package.json",
            "go.mod",
            "docker-compose.yml",
            "Dockerfile",
            "src/app.js",
            "src/routes/aiRoutes.js",
            "backend/src/app.js",
            "backend/src/routes/aiRoutes.js",
        ]
        found = [item for item in interesting if (root / item).exists()]

        total_files = sum(1 for _ in root.rglob("*") if _.is_file())
        return {
            "project_root": str(root),
            "exists": True,
            "summary": "project_scanned",
            "total_files": total_files,
            "detected_files": found,
        }
