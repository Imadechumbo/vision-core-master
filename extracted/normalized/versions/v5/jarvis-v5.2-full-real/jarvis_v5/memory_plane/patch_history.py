from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class PatchHistoryStore:
    def __init__(self, storage_root: Path):
        self.root = Path(storage_root)
        self.file = self.root / 'patch_history.json'
        if not self.file.exists():
            self.file.write_text('[]', encoding='utf-8')

    def record(self, project: str, patch: dict, execution: dict):
        data = json.loads(self.file.read_text(encoding='utf-8') or '[]')
        entry = {
            'patch_id': f"patch_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            'project': project,
            'target_file': patch.get('target_file'),
            'strategy_key': patch.get('strategy_key'),
            'backup_file': execution.get('backup_file'),
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        data.append(entry)
        self.file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')
        return entry

    def list(self, project: str | None = None):
        data = json.loads(self.file.read_text(encoding='utf-8') or '[]')
        if project:
            data = [d for d in data if d['project'] == project]
        return list(reversed(data))

    def get(self, patch_id: str):
        for entry in json.loads(self.file.read_text(encoding='utf-8') or '[]'):
            if entry['patch_id'] == patch_id:
                return entry
        return None
