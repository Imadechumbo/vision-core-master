# JARVIS CORE V5.2.1 PATCH

Patch cirúrgico para V5.2 FULL REAL.

## Corrige
1. Scanner Node/Express mais confiável
2. HTTP gates reais (`/api/health`, `/api/news/latest`, `/api/v1/chat`, `/api/v1/chat/vision`)
3. Registry/index de patches para rollback por `patch_id`
4. Fallback de runtime com `python -m uvicorn`

## Aplicação
Extraia este ZIP na raiz do projeto `jarvis-v5.2-full-real`, sobrescrevendo os arquivos.

## Comandos
```bash
python apps/cli/jarvis.py scan --project-root "CAMINHO"
python apps/cli/jarvis.py http-gates --base-url "https://api.technetgame.com.br"
python apps/cli/jarvis.py patches --project technetgame
python apps/cli/jarvis.py rollback-patch --project technetgame --patch-id PATCH_ID
python -m uvicorn jarvis_v5.interface_plane.api:app --host 127.0.0.1 --port 8088
python -m uvicorn runtime.server:app --host 127.0.0.1 --port 8090
```
