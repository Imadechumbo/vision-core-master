from difflib import unified_diff


class SmartPatchEngine:
    def __init__(self, adapter, strategy_store):
        self.adapter = adapter
        self.strategy_store = strategy_store

    def generate(self, mission: dict, evidence: dict, rca: dict, project_root: str):
        candidate = self.adapter.build_patch_candidate(mission, evidence, project_root)
        before = candidate.get('before', '')
        after = candidate.get('after', '')
        diff = "\n".join(
            unified_diff(before.splitlines(), after.splitlines(), fromfile='before', tofile='after', lineterm='')
        )
        risk = self.adapter.estimate_risk(candidate)
        strategy_key = candidate['strategy_key']
        ranked = self.strategy_store.list_ranked(project=mission['project']['name'])
        past_score = next((s['score'] for s in ranked if s['strategy_key'] == strategy_key), 0)
        candidate.update({'diff': diff, 'risk_level': risk, 'historical_score': past_score, 'ast_enabled': bool(candidate.get('metadata', {}).get('ast'))})
        return candidate
