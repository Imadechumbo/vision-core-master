def evaluate_policy(mission, patch) -> dict:
    risky_keywords = ['auth', 'billing', 'payment']
    high_risk = False
    touched = []
    for op in patch.operations:
        touched.append(op.file)
        if any(k in op.file.lower() for k in risky_keywords):
            high_risk = True

    allowed = not high_risk
    return {
        'allowed': allowed,
        'reason': 'Patch permitido' if allowed else 'Patch bloqueado por área crítica',
        'risk_level': 'high' if high_risk else patch.risk_level,
        'touched_files': touched,
    }
