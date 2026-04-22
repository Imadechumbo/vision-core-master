from pathlib import Path
import os

from jarvis_v5.intelligence_plane.infra_patch_engine import InfraPatchEngine


class CloudflareAdapter:
    def __init__(self):
        self.infra = InfraPatchEngine()

    def find_critical_files(self, files):
        return [f for f in files if any(k in f.lower() for k in ['wrangler','_redirects','runtime-config','cloudflare','pages'])][:20]

    def critical_endpoints(self):
        return []

    def infer_notes(self, mission):
        return ['adapter Cloudflare ativo', 'autopatch de _redirects e runtime-config disponível']

    def inspect(self, project_root: str):
        return {'has_token': bool(os.getenv('CLOUDFLARE_API_TOKEN')), 'has_zone': bool(os.getenv('CLOUDFLARE_ZONE_ID')), 'has_account': bool(os.getenv('CLOUDFLARE_ACCOUNT_ID'))}

    def build_patch_candidate(self, mission, evidence, project_root):
        if mission['intent'] == 'fix_redirects':
            return self.infra.patch_redirects(project_root)
        if mission['intent'] == 'fix_runtime_config':
            return self.infra.patch_runtime_config(project_root, mission.get('base_url'))
        return {"strategy_key": 'cloudflare_config_review', "target_file": None, "before": '', "after": '', "operations": [], "summary": 'Adapter Cloudflare faz inspeção e autopatch seletivo.', "metadata": {"infra": True}}

    def estimate_risk(self, candidate):
        return 'low' if candidate.get('metadata', {}).get('infra') and candidate.get('target_file') else 'high'

    def apply_patch(self, patch, project_root):
        if not patch.get('target_file'):
            return {"applied": False, "mode": 'require_approval', "notes": ['Patch Cloudflare não gerou alvo.']}
        path = Path(patch['target_file'])
        path.parent.mkdir(parents=True, exist_ok=True)
        backup = path.with_suffix(path.suffix + '.jarvis.bak') if path.suffix else Path(str(path) + '.jarvis.bak')
        backup.write_text(patch.get('before',''), encoding='utf-8')
        path.write_text(patch.get('after',''), encoding='utf-8')
        return {"applied": True, "mode": 'auto_apply', "notes": [f'Patch infra aplicado em {path.name}'], "backup_file": str(backup), "target_file": str(path)}

    def infra_checks(self, project_root: str, mission: dict):
        root = Path(project_root)
        return [{'check': 'redirects', 'ok': (root / '_redirects').exists()}, {'check': 'runtime_config', 'ok': any(root.rglob('runtime-config.js'))}]
