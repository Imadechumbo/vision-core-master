from pathlib import Path

from jarvis_v5.intelligence_plane.infra_patch_engine import InfraPatchEngine

try:
    import docker
except Exception:
    docker = None


class DockerAdapter:
    def __init__(self):
        self.infra = InfraPatchEngine()

    def find_critical_files(self, files):
        return [f for f in files if any(k in f.lower() for k in ['dockerfile','docker-compose','compose.yml','compose.yaml','container'])][:20]

    def critical_endpoints(self):
        return []

    def infer_notes(self, mission):
        return ['adapter Docker ativo', 'autopatch de Dockerfile disponível']

    def inspect(self):
        if docker is None:
            return {'docker_python_available': False, 'engine_access': False}
        try:
            client = docker.from_env(); client.ping(); return {'docker_python_available': True, 'engine_access': True}
        except Exception as exc:
            return {'docker_python_available': True, 'engine_access': False, 'error': str(exc)}

    def build_patch_candidate(self, mission, evidence, project_root):
        if mission['intent'] in {'fix_docker','stabilize_deploy'}:
            return self.infra.patch_dockerfile(project_root)
        return {"strategy_key": 'docker_config_review', "target_file": None, "before": '', "after": '', "operations": [], "summary": 'Adapter Docker faz inspeção de runtime e autopatch seletivo.', "metadata": {"infra": True}}

    def estimate_risk(self, candidate):
        return 'low' if candidate.get('metadata', {}).get('infra') and candidate.get('target_file') else 'high'

    def apply_patch(self, patch, project_root):
        if not patch.get('target_file'):
            return {"applied": False, "mode": 'require_approval', "notes": ['Patch Docker não gerou alvo.']}
        path = Path(patch['target_file'])
        path.parent.mkdir(parents=True, exist_ok=True)
        backup = path.with_suffix(path.suffix + '.jarvis.bak') if path.suffix else Path(str(path) + '.jarvis.bak')
        backup.write_text(patch.get('before',''), encoding='utf-8')
        path.write_text(patch.get('after',''), encoding='utf-8')
        return {"applied": True, "mode": 'auto_apply', "notes": [f'Patch infra aplicado em {path.name}'], "backup_file": str(backup), "target_file": str(path)}

    def infra_checks(self, project_root: str, mission: dict):
        root = Path(project_root)
        return [{'check': 'dockerfile', 'ok': (root / 'Dockerfile').exists()}]
