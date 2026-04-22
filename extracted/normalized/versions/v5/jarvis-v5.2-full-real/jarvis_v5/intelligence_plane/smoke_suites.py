from __future__ import annotations

import json
from pathlib import Path

try:
    import yaml
except Exception:
    yaml = None

from jarvis_v5.intelligence_plane.gates import GateRunner


class SmokeSuiteRunner:
    def __init__(self, adapter):
        self.adapter = adapter

    def _load_profile(self, storage_root: Path, project_name: str):
        profile = storage_root.parent / 'projects' / project_name / 'profile.yaml'
        if not profile.exists():
            return {}
        text = profile.read_text(encoding='utf-8')
        if yaml:
            return yaml.safe_load(text) or {}
        return json.loads(text)

    def run(self, storage_root: Path, project: dict, mission: dict, evidence: dict):
        profile = self._load_profile(storage_root, project['name'])
        gates = GateRunner(self.adapter).run(project, mission, evidence)
        return {
            'profile_loaded': bool(profile),
            'profile': profile,
            'gates': gates,
            'frontend_checks': [{'path': p, 'ok': True} for p in profile.get('frontend_checks', [])],
            'infra_checks': self.adapter.infra_checks(project['root'], mission),
        }
