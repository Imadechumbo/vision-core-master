class GenericAdapter:
    def find_critical_files(self, files):
        return files[:20]
    def critical_endpoints(self):
        return []
    def infer_notes(self, mission):
        return ['adapter genérico ativo']
    def build_patch_candidate(self, mission, evidence, project_root):
        return {"strategy_key": 'generic_review', "target_file": None, "before": '', "after": '', "operations": [], "summary": 'Somente diagnóstico.', "metadata": {}}
    def estimate_risk(self, candidate):
        return 'high'
    def apply_patch(self, patch, project_root):
        return {"applied": False, "mode": 'require_approval', "notes": ['Adapter genérico não aplica patch.']}
    def infra_checks(self, project_root: str, mission: dict):
        return []
