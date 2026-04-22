from __future__ import annotations
from pathlib import Path
from jarvis_v5.utils.fs import ensure_dir, load_json, save_json

class PatchRegistry:
    def __init__(self, storage_dir: str):
        self.storage_dir = Path(storage_dir)
        self.index_path = self.storage_dir / "patches" / "index.json"
        ensure_dir(self.index_path.parent)

    def add(self, record: dict) -> None:
        data = load_json(self.index_path, default=[])
        data = [r for r in data if r.get("patch_id") != record.get("patch_id")]
        data.insert(0, record)
        save_json(self.index_path, data)

    def list(self, project: str | None = None) -> list[dict]:
        data = load_json(self.index_path, default=[])
        if project:
            return [r for r in data if r.get("project") == project]
        return data

    def get(self, patch_id: str) -> dict | None:
        for record in self.list():
            if record.get("patch_id") == patch_id:
                return record
        return None
