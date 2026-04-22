# JARVIS CORE V4 REAL

Orquestrador offline-first para diagnóstico, patch supervisionado, gates reais, stable vault e rollback.

## Destaques V4
- CLI unificada
- Mission parser e intent resolver
- Scanner de projeto
- Evidence collector
- RCA + cause chain
- Playbooks por intent
- Patch planner estruturado
- Patch applier supervisionado
- Diff engine
- Gates HTTP reais
- Stable Vault + rollback
- Incident store JSON + SQLite
- Incident query via CLI
- Obsidian logger
- Adapter TechNetGame completo (base)
- Runtime Go (`/health`, `/runtime`, `/execute`)

## Regra central
**SEM PASS GOLD -> NADA E PROMOVIDO**

## Estrutura
Ver `MANUAL_MESTRE_V4.md`.

## Setup rapido
```bash
python -m venv .venv
source .venv/bin/activate
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Exemplo
```bash
python apps/cli/jarvis.py "corrigir vision do technetgame" --project-root "/caminho/projeto" --base-url "https://api.technetgame.com.br"
```

## Comandos uteis
```bash
python apps/cli/jarvis.py "corrigir vision do technetgame" --project-root "/projeto" --dry-run
python apps/cli/jarvis.py incidents --filter vision
python apps/cli/jarvis.py stable list --project technetgame
python apps/cli/jarvis.py stable rollback --project technetgame
python apps/cli/jarvis.py runtime --host 127.0.0.1 --port 8090
```
