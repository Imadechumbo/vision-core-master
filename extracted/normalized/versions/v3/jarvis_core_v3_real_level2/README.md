# JARVIS CORE V3 EXECUTÁVEL — V3 REAL NÍVEL 2

Base operacional inicial do JARVIS CORE V3 com:
- CLI funcional
- parser de missão
- registry de projetos
- adapter inicial do TechNetGame
- RCA básico por evidência
- gates SDDF base
- integração Ollama via cliente HTTP
- serviço Go de runtime com `/health`, `/runtime` e `/execute`

## Estrutura

```text
apps/cli/jarvis.py
core/mission/
intelligence/intent/
diagnostics/
validation/gates/
security/aegis/
adapters/projects/
runtime/go/
registry/projects/
docs/
```

## Execução rápida

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
pip install -r requirements.txt
python apps/cli/jarvis.py "corrigir vision do technetgame" --project-root /caminho/do/projeto --json-only
```

## Serviço Go

```bash
cd runtime/go
go run ./cmd/autonomy
```

Endpoints:
- `GET /health`
- `GET /runtime`
- `POST /execute`

## Regra central

**Sem PASS GOLD, nada é promovido.**
