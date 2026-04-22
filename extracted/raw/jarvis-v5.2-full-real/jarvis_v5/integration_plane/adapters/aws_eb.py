from pathlib import Path
import os

from jarvis_v5.intelligence_plane.infra_patch_engine import InfraPatchEngine

try:
    import boto3
except Exception:
    boto3 = None


class AwsElasticBeanstalkAdapter:
    def __init__(self):
        self.infra = InfraPatchEngine()

    def find_critical_files(self, files):
        return [f for f in files if any(k in f.lower() for k in ['procfile','.ebextensions','elasticbeanstalk','package.json','00-environment'])][:20]

    def critical_endpoints(self):
        return []

    def infer_notes(self, mission):
        return ['adapter AWS Elastic Beanstalk ativo', 'autopatch de Procfile e .ebextensions disponível']

    def inspect(self):
        return {'boto3_available': boto3 is not None, 'aws_region': os.getenv('AWS_REGION') or os.getenv('AWS_DEFAULT_REGION'), 'has_access_key': bool(os.getenv('AWS_ACCESS_KEY_ID'))}

    def build_patch_candidate(self, mission, evidence, project_root):
        if mission['intent'] == 'fix_procfile':
            return self.infra.patch_procfile(project_root)
        if mission['intent'] == 'stabilize_deploy':
            return self.infra.patch_ebextensions(project_root)
        return {"strategy_key": 'aws_eb_config_review', "target_file": None, "before": '', "after": '', "operations": [], "summary": 'Adapter AWS EB faz inspeção e autopatch seletivo.', "metadata": {"infra": True}}

    def estimate_risk(self, candidate):
        return 'low' if candidate.get('metadata', {}).get('infra') and candidate.get('target_file') else 'high'

    def apply_patch(self, patch, project_root):
        if not patch.get('target_file'):
            return {"applied": False, "mode": 'require_approval', "notes": ['Patch AWS EB não gerou alvo.']}
        path = Path(patch['target_file'])
        path.parent.mkdir(parents=True, exist_ok=True)
        backup = path.with_suffix(path.suffix + '.jarvis.bak') if path.suffix else Path(str(path) + '.jarvis.bak')
        backup.write_text(patch.get('before',''), encoding='utf-8')
        path.write_text(patch.get('after',''), encoding='utf-8')
        return {"applied": True, "mode": 'auto_apply', "notes": [f'Patch infra aplicado em {path.name}'], "backup_file": str(backup), "target_file": str(path)}

    def infra_checks(self, project_root: str, mission: dict):
        root = Path(project_root)
        return [{'check': 'procfile', 'ok': (root / 'Procfile').exists()}, {'check': 'ebextensions', 'ok': (root / '.ebextensions').exists()}]
