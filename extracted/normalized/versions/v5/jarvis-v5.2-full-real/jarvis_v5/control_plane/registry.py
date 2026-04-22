import json
from pathlib import Path
from typing import Optional

class ProjectRegistry:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.file = self.root / "registry.json"
        if not self.file.exists():
            self.file.write_text("{}", encoding="utf-8")

    def _load(self):
        return json.loads(self.file.read_text(encoding="utf-8") or "{}")

    def _save(self, data):
        self.file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def add_project(self, name: str, root: str, stack: str):
        data = self._load()
        project_root = Path(root)
        entry = {
            "name": name,
            "root": str(project_root),
            "stack": stack,
            "context_dir": str(self.root / name),
        }
        data[name] = entry
        self._save(data)
        (self.root / name / "history").mkdir(parents=True, exist_ok=True)
        (self.root / name / "stable").mkdir(parents=True, exist_ok=True)
        return entry

    def get_project(self, name: str) -> Optional[dict]:
        return self._load().get(name)

    def list_projects(self):
        return list(self._load().values())
