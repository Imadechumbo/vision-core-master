from jarvis_core.models import RCAResult


def build_rca(mission, evidence, playbook) -> RCAResult:
    intent = mission.intent
    if intent == 'fix_vision':
        return RCAResult(
            root_cause='Endpoint vision provavelmente acessa upload/arquivo sem validar presença ou provider multimodal não está configurado.',
            cause_chain=[
                'Input chega sem arquivo ou metadata esperada',
                'Código tenta ler mimetype em objeto nulo',
                'Handler lança erro interno em vez de retornar 4xx',
                'Gate GOLD falha por contrato quebrado'
            ],
            confidence='high',
            evidence=evidence,
        )
    if intent == 'fix_cors':
        return RCAResult(
            root_cause='Middleware CORS/preflight inconsistente ou incompleto.',
            cause_chain=[
                'Origin não é liberado',
                'OPTIONS falha ou não retorna cabeçalhos corretos',
                'Frontend recebe bloqueio do navegador'
            ],
            confidence='medium',
            evidence=evidence,
        )
    return RCAResult(
        root_cause='Causa raiz ainda parcial; missão exige inspeção supervisionada.',
        cause_chain=['Sintoma reportado', 'Evidência inicial consolidada', 'Patch sugerido depende de confirmação por gates'],
        confidence='medium',
        evidence=evidence,
    )
