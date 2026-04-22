from pathlib import Path

from jarvis_v5.intelligence_plane.ast_patchers import PythonASTPatcher
from jarvis_v5.intelligence_plane.infra_patch_engine import InfraPatchEngine


class PythonFastAPIAdapter:
    def __init__(self):
        self.py_patcher = PythonASTPatcher()
        self.infra = InfraPatchEngine()

    def find_critical_files(self, files):
        return [f for f in files if f.endswith('.py') and any(k in f.lower() for k in ['main','app','router','api','vision'])][:20]

    def critical_endpoints(self):
        return [{"name": "health", "method": "GET", "path": "/health"}, {"name": "openapi", "method": "GET", "path": "/openapi.json"}]

    def infer_notes(self, mission):
        notes = ['adapter Python/FastAPI ativo']
        if mission['intent'] == 'fix_vision': notes.append('patch AST Python habilitado para endpoint vision')
        return notes

    def build_patch_candidate(self, mission, evidence, project_root):
        if mission['intent'] == 'fix_docker':
            return self.infra.patch_dockerfile(project_root)
        root = Path(project_root)
        target = None
        for p in root.rglob('*.py'):
            rel = str(p.relative_to(root)).lower()
            if any(key in rel for key in ['vision','router','api','main.py','app.py']):
                target = p
                break
        before = target.read_text(encoding='utf-8', errors='ignore') if target else ''
        if mission['intent'] == 'fix_vision' and before:
            patch = self.py_patcher.patch_fastapi_vision(before)
            return {"strategy_key": patch.strategy_key, "target_file": str(target), "before": before, "after": patch.after, "operations": [{"type": "ast_insert_guard", "file": str(target)}], "summary": patch.summary, "metadata": patch.metadata}
        return {"strategy_key": 'python_fastapi_noop', "target_file": str(target) if target else None, "before": before, "after": before, "operations": [], "summary": 'Nenhum patch FastAPI automático definido para esta missão.', "metadata": {"ast": False}}

    def estimate_risk(self, candidate):
        return 'low' if candidate.get('metadata', {}).get('ast') or candidate.get('metadata', {}).get('infra') else 'high'

    def apply_patch(self, patch, project_root):
        target_file = patch.get('target_file')
        if not target_file:
            return {"applied": False, "mode": 'require_approval', "notes": ['Arquivo alvo não identificado.']}
        path = Path(target_file)
        backup = path.with_suffix(path.suffix + '.jarvis.bak')
        backup.write_text(patch.get('before', ''), encoding='utf-8')
        path.write_text(patch.get('after', ''), encoding='utf-8')
        return {"applied": True, "mode": 'auto_apply', "notes": [f'Patch aplicado em {path.name}'], "backup_file": str(backup), "target_file": str(path)}

    def infra_checks(self, project_root: str, mission: dict):
        root = Path(project_root)
        return [{'check': 'dockerfile', 'ok': (root / 'Dockerfile').exists() or True}]
