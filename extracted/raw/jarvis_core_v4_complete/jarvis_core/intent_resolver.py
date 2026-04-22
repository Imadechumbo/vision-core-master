def resolve_intent(text: str) -> str:
    t = text.lower()
    if 'vision' in t:
        return 'fix_vision'
    if 'cors' in t:
        return 'fix_cors'
    if 'deploy' in t:
        return 'deploy_recovery'
    if 'rollback' in t:
        return 'rollback'
    return 'generic_fix'
