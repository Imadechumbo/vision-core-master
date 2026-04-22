from pathlib import Path

from jarvis_v5.intelligence_plane.ast_patchers import JavaScriptASTPatcher
from jarvis_v5.intelligence_plane.infra_patch_engine import InfraPatchEngine


class NodeExpressAdapter:
    def __init__(self):
        self.js_patcher = JavaScriptASTPatcher()
        self.infra = InfraPatchEngine()

    def find_critical_files(self, files):
        scored = []
        for file in files:
            lowered = file.lower().replace('\\', '/')
            score = 0
            if lowered.endswith('airoutes.js'):
                score += 20
            if '/routes/' in lowered:
                score += 10
            if 'vision' in lowered:
                score += 8
            if 'chat' in lowered:
                score += 5
            if lowered.endswith(('server.js', 'app.js', 'index.js')):
                score += 3
            if any(k in lowered for k in ['runtime-config', '_redirects', 'procfile', 'dockerfile']):
                score += 6
            if score:
                scored.append((score, file))
        return [item[1] for item in sorted(scored, reverse=True)[:25]]

    def critical_endpoints(self):
        return [
            {'name': 'health', 'method': 'GET', 'path': '/api/health'},
            {'name': 'chat', 'method': 'POST', 'path': '/api/v1/chat', 'json': {'message': 'ping'}},
            {'name': 'vision', 'method': 'POST', 'path': '/api/v1/chat/vision', 'json': {'message': 'ping'}},
        ]

    def infer_notes(self, mission):
        notes = ['adapter Node/Express ativo']
        if mission['intent'] == 'fix_vision':
            notes.append('patch AST JavaScript habilitado para vision/upload')
        if mission['intent'] in {'stabilize_deploy', 'fix_runtime_config', 'fix_redirects', 'fix_procfile', 'fix_docker'}:
            notes.append('infra autopatch habilitado')
        return notes

    def _pick_target(self, project_root):
        root = Path(project_root)
        candidates = []
        for p in root.rglob('*.js'):
            rel = str(p.relative_to(root)).replace('\\', '/')
            score = 0
            lowered = rel.lower()
            if lowered.endswith('airoutes.js'):
                score += 30
            if '/routes/' in lowered:
                score += 20
            if 'vision' in lowered:
                score += 10
            if 'chat' in lowered:
                score += 7
            if lowered.endswith(('server.js', 'app.js', 'index.js')):
                score += 4
            if score:
                candidates.append((score, rel, p))
        candidates.sort(reverse=True)
        return candidates[0][2] if candidates else None

    def build_patch_candidate(self, mission, evidence, project_root):
        intent = mission['intent']
        if intent == 'fix_runtime_config':
            return self.infra.patch_runtime_config(project_root, mission.get('base_url'))
        if intent == 'fix_redirects':
            return self.infra.patch_redirects(project_root)
        if intent == 'fix_procfile':
            return self.infra.patch_procfile(project_root)
        if intent == 'fix_docker':
            return self.infra.patch_dockerfile(project_root)

        target = self._pick_target(project_root)
        before = target.read_text(encoding='utf-8', errors='ignore') if target and target.exists() else ''
        if intent == 'fix_vision' and before:
            patch = self.js_patcher.patch_express_vision(before)
            return {
                'strategy_key': patch.strategy_key,
                'target_file': str(target),
                'before': before,
                'after': patch.after,
                'operations': [{'type': 'ast_insert_guard', 'file': str(target)}],
                'summary': patch.summary,
                'metadata': patch.metadata,
            }
        return {
            'strategy_key': 'node_express_noop',
            'target_file': str(target) if target else None,
            'before': before,
            'after': before,
            'operations': [],
            'summary': 'Nenhum patch automático definido para esta missão.',
            'metadata': {'ast': False},
        }

    def estimate_risk(self, candidate):
        if not candidate.get('target_file'):
            return 'high'
        if candidate.get('metadata', {}).get('ast'):
            return 'low'
        if candidate.get('metadata', {}).get('infra'):
            return 'low'
        return 'medium'

    def apply_patch(self, patch, project_root):
        target_file = patch.get('target_file')
        if not target_file:
            return {'applied': False, 'mode': 'require_approval', 'notes': ['Arquivo alvo não identificado.']}
        path = Path(target_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        backup = Path(str(path) + '.jarvis.bak')
        backup.write_text(patch.get('before', ''), encoding='utf-8')
        path.write_text(patch.get('after', ''), encoding='utf-8')
        return {'applied': True, 'mode': 'auto_apply', 'notes': [f'Patch aplicado em {path.name}'], 'backup_file': str(backup), 'target_file': str(path)}

    def infra_checks(self, project_root: str, mission: dict):
        root = Path(project_root)
        runtime_files = list(root.rglob('runtime-config.js'))
        results = []
        if runtime_files:
            txt = runtime_files[0].read_text(encoding='utf-8', errors='ignore')
            results.append({'check': 'runtime_config', 'ok': 'API_BASE_URL' in txt})
        redirects = root / '_redirects'
        results.append({'check': 'redirects', 'ok': redirects.exists()})
        procfile = root / 'Procfile'
        results.append({'check': 'procfile', 'ok': procfile.exists() or (root / 'package.json').exists()})
        return results
