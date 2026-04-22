import json
import shutil
from datetime import datetime, timezone
from pathlib import Path


class StableVault:
    def __init__(self, storage_root: Path):
        self.root = Path(storage_root) / 'stable_vault'
        self.root.mkdir(parents=True, exist_ok=True)

    def _project_dir(self, project: str):
        d = self.root / project
        d.mkdir(parents=True, exist_ok=True)
        return d

    def promote(self, project: str, source_root: str | None = None):
        d = self._project_dir(project)
        stamp = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')
        entry = {
            'project': project,
            'snapshot': stamp,
            'status': 'gold',
            'created_at': datetime.now(timezone.utc).isoformat(),
        }
        if source_root:
            snap_dir = d / stamp
            snap_dir.mkdir(parents=True, exist_ok=True)
            marker = snap_dir / 'SNAPSHOT.txt'
            marker.write_text(f'source_root={source_root}\n', encoding='utf-8')
            entry['snapshot_dir'] = str(snap_dir)
        (d / f'{stamp}.json').write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding='utf-8')
        (d / 'LATEST_GOLD.json').write_text(json.dumps(entry, indent=2, ensure_ascii=False), encoding='utf-8')
        return entry

    def list_entries(self, project=None):
        projects = [project] if project else [p.name for p in self.root.glob('*') if p.is_dir()]
        out = []
        for name in projects:
            for f in sorted((self.root / name).glob('*.json'), reverse=True):
                if f.name == 'LATEST_GOLD.json':
                    continue
                out.append(json.loads(f.read_text(encoding='utf-8')))
        return out

    def rollback(self, project: str, target: str):
        d = self._project_dir(project)
        latest = d / 'LATEST_GOLD.json'
        if not latest.exists():
            return {'status': 'no_gold_snapshot'}
        payload = json.loads(latest.read_text(encoding='utf-8'))
        target_path = Path(target)
        target_path.mkdir(parents=True, exist_ok=True)
        marker = target_path / 'ROLLBACK_FROM_GOLD.txt'
        marker.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding='utf-8')
        return {'status': 'rolled_back', 'target': str(target_path), 'snapshot': payload}

    def rollback_patch(self, target_file: str, backup_file: str):
        t = Path(target_file)
        b = Path(backup_file)
        if not b.exists():
            return {'status': 'backup_missing', 'backup': str(b)}
        t.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(b, t)
        return {'status': 'rolled_back_patch', 'target_file': str(t), 'backup_file': str(b)}
