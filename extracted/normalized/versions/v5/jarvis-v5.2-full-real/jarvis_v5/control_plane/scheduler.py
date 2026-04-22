from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


class SchedulerService:
    def __init__(self, storage_root: Path, registry, queue):
        self.storage_root = Path(storage_root)
        self.registry = registry
        self.queue = queue
        self.state_file = self.storage_root / 'scheduler_state.json'
        if not self.state_file.exists():
            self.state_file.write_text('{}', encoding='utf-8')

    def _load_state(self):
        return json.loads(self.state_file.read_text(encoding='utf-8') or '{}')

    def _save_state(self, data):
        self.state_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding='utf-8')

    def list_jobs(self, project: str | None = None):
        out = []
        projects = [self.registry.get_project(project)] if project else self.registry.list_projects()
        for p in filter(None, projects):
            sched_dir = Path(p['context_dir']).parent.parent / '..'
            sched_dir = Path(p['root']) / 'schedules' if (Path(p['root']) / 'schedules').exists() else None
            project_sched = self.storage_root.parent / 'projects' / p['name'] / 'schedules'
            for file in sorted(project_sched.glob('*.json')) if project_sched.exists() else []:
                payload = json.loads(file.read_text(encoding='utf-8'))
                payload['project'] = p['name']
                payload['schedule_file'] = str(file)
                out.append(payload)
        return out

    def run_due_jobs(self, force: bool = False):
        now = int(datetime.now(timezone.utc).timestamp())
        state = self._load_state()
        enqueued = []
        for job in self.list_jobs():
            key = f"{job['project']}::{Path(job['schedule_file']).name}"
            interval = int(job.get('interval_sec', 300))
            due = force or now >= int(state.get(key, 0)) + interval
            if due:
                mission = {
                    'id': f"mission_sched_{job['project']}_{job['kind']}_{now}",
                    'text': f"scheduled {job['kind']} for {job['project']}",
                    'intent': 'scheduled_smoke' if job['kind'] == 'smoke_suite' else 'general_diagnosis',
                    'project': self.registry.get_project(job['project']),
                    'base_url': None,
                    'dry_run': True,
                    'auto_apply': False,
                    'auto_rollback': False,
                    'scheduled': True,
                }
                self.queue.enqueue(mission)
                state[key] = now
                enqueued.append({'job': key, 'mission_id': mission['id']})
        self._save_state(state)
        return {'ok': True, 'enqueued': enqueued, 'count': len(enqueued)}
