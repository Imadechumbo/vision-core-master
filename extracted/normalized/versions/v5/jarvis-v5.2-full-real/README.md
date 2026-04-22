# JARVIS CORE V5.2 FULL REAL

Base executável de plataforma autônoma universal com:
- multi-projeto
- AST patching Python/JavaScript
- autopatch operacional de infra
- fila local/Redis
- scheduler por projeto
- smoke suites
- stable vault e rollback contextual
- dashboard e runtime API

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

## Comandos

```bash
python apps/cli/jarvis.py project add technetgame --root "CAMINHO" --stack node_express
python apps/cli/jarvis.py mission "corrigir vision do technetgame" --project technetgame --base-url "https://api.technetgame.com.br" --dry-run
python apps/cli/jarvis.py mission "corrigir runtime-config do technetgame" --project technetgame --base-url "https://api.technetgame.com.br" --auto-apply
python apps/cli/jarvis.py scheduler list
python apps/cli/jarvis.py scheduler run --force
python apps/cli/jarvis.py patches --project technetgame
python apps/cli/jarvis.py stable rollback --project technetgame --patch-id PATCH_ID
uvicorn jarvis_v5.interface_plane.api:app --host 127.0.0.1 --port 8088
uvicorn runtime.server:app --host 127.0.0.1 --port 8090
python workers/python_worker.py
```

## Missões que já têm autopatch
- corrigir vision
- corrigir runtime-config
- corrigir redirects
- corrigir Procfile
- corrigir Dockerfile / deploy

## Observação
O pacote é executável e validado em fluxo local/dry-run. Os adapters de Cloudflare, AWS EB e Docker fazem remediação operacional seletiva em arquivos locais do projeto; eles não fazem alteração remota em provedores.
