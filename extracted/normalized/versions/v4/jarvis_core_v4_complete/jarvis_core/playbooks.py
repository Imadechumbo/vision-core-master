PLAYBOOKS = {
    'fix_vision': {
        'goal': 'Corrigir endpoint multimodal/vision sem quebrar contrato.',
        'checks': [
            'Validar presença de arquivo antes de ler mimetype',
            'Garantir resposta 4xx para input inválido',
            'Validar provider multimodal e variáveis de ambiente',
            'Executar gates HTTP em /api/v1/chat/vision'
        ],
    },
    'fix_cors': {
        'goal': 'Corrigir política CORS e preflight.',
        'checks': [
            'Verificar origins permitidos',
            'Garantir OPTIONS global',
            'Aplicar headers também em error handler'
        ],
    },
    'generic_fix': {
        'goal': 'Aplicar diagnóstico seguro e validação final.',
        'checks': [
            'Consolidar evidências',
            'Gerar plano supervisionado',
            'Executar gates'
        ],
    },
}


def get_playbook(intent: str):
    return PLAYBOOKS.get(intent, PLAYBOOKS['generic_fix'])
