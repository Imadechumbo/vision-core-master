class AegisPolicy:
    SAFE_STRATEGIES = {
        'infra_runtime_config_patch', 'infra_redirects_patch', 'infra_procfile_patch', 'infra_dockerfile_patch',
        'infra_ebextensions_patch', 'node_ast_express_vision_guard', 'python_ast_fastapi_vision_guard'
    }

    def evaluate(self, patch: dict, mission: dict):
        risk = patch['risk_level']
        strategy_key = patch.get('strategy_key')
        if mission.get('dry_run'):
            return {'decision': 'dry_run', 'reason': 'dry-run solicitado'}
        if strategy_key in self.SAFE_STRATEGIES:
            return {'decision': 'auto_apply', 'reason': f'estratégia segura: {strategy_key}'}
        if risk == 'low':
            return {'decision': 'auto_apply', 'reason': 'baixo risco'}
        if risk == 'medium' and mission.get('auto_apply'):
            return {'decision': 'auto_apply', 'reason': 'médio risco com auto-apply explícito'}
        return {'decision': 'require_approval', 'reason': f'risco {risk}'}
