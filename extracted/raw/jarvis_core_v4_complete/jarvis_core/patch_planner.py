from jarvis_core.models import StructuredPatch, PatchOperation

VISION_GUARD_SNIPPET = """# JARVIS_PATCH_V4_VISION_GUARD_START
uploaded_file = payload.get('file') or payload.get('image') or payload.get('upload')
if uploaded_file is None:
    return {'ok': False, 'error': 'missing_file', 'message': 'Arquivo de imagem obrigatório para vision.'}, 400
mimetype = getattr(uploaded_file, 'mimetype', None) or getattr(uploaded_file, 'content_type', None)
if not mimetype:
    return {'ok': False, 'error': 'missing_mimetype', 'message': 'Arquivo sem mimetype válido.'}, 400
# JARVIS_PATCH_V4_VISION_GUARD_END
"""

CORS_SNIPPET = """# JARVIS_PATCH_V4_CORS_START
allowed_origins = set((os.getenv('ALLOWED_ORIGINS') or '').split(','))
origin = request.headers.get('Origin', '')
if origin and origin in allowed_origins:
    response.headers['Access-Control-Allow-Origin'] = origin
    response.headers['Vary'] = 'Origin'
response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,PATCH,DELETE,OPTIONS'
response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Refresh-Token, Accept'
response.headers['Access-Control-Max-Age'] = '86400'
# JARVIS_PATCH_V4_CORS_END
"""


def plan_patch(mission, scan_result, rca_result):
    patch = StructuredPatch(risk_level='medium', summary='Plano supervisionado baseado em intent.')
    if mission.intent == 'fix_vision':
        target_file = scan_result.get('route_candidates', [None])[0] or 'server.js'
        patch.operations.append(PatchOperation(
            file=target_file,
            op_type='insert',
            target='VISION_HANDLER_GUARD',
            content=VISION_GUARD_SNIPPET,
            reason='Adicionar guarda para arquivo/mimetype no fluxo vision',
        ))
    elif mission.intent == 'fix_cors':
        target_file = scan_result.get('route_candidates', [None])[0] or 'server.js'
        patch.operations.append(PatchOperation(
            file=target_file,
            op_type='insert',
            target='CORS_HANDLER',
            content=CORS_SNIPPET,
            reason='Aplicar cabeçalhos CORS consistentes',
        ))
    else:
        patch.operations.append(PatchOperation(
            file='JARVIS_PATCH_NOTE.txt',
            op_type='replace',
            target='__FULL_FILE__',
            content='Patch genérico supervisionado: revisar manualmente antes de promover.',
            reason='Missão genérica',
        ))
    return patch
