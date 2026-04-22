# VISION CORE V5.5 inicial executável

Pacote Python executável com:

- patch planner multi-arquivo real
- adapter Python funcional
- policy engine integrado
- bridge GitHub preparado
- worker e scheduler básicos
- snapshots/rollback transacional por plano

## Requisitos

- Python 3.10+
- Git opcional para fluxo GitHub
- Windows/Linux/macOS

## Instalação

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Uso rápido

### 1) Detectar projeto Python

```bash
python apps/cli/jarvis.py python-adapter --project-root "C:\SEU_PROJETO"
```

### 2) Gerar plano de patch multi-arquivo

```bash
python apps/cli/jarvis.py patch-plan \
  --project-root "C:\SEU_PROJETO" \
  --failure-type health_endpoint_failed \
  --plan-file plan.json
```

### 3) Aplicar plano com backup real

```bash
python apps/cli/jarvis.py apply-plan \
  --project-root "C:\SEU_PROJETO" \
  --plan-file plan.json
```

### 4) Reverter snapshot

```bash
python apps/cli/jarvis.py rollback \
  --project-root "C:\SEU_PROJETO" \
  --snapshot-id SNAPSHOT_ID
```

### 5) Verificar política de promoção

```bash
python apps/cli/jarvis.py policy-check \
  --pass-gold \
  --gates-json "{}" \
  --patch-plan-json "{}"
```

### 6) Preparar branch GitHub

```bash
python apps/cli/jarvis.py github-prepare-pr \
  --project-root "C:\SEU_PROJETO" \
  --title "fix(runtime): corrigir runtime"
```

### 7) Pipeline automático

```bash
python apps/cli/jarvis.py run \
  --project-root "C:\SEU_PROJETO" \
  --mission "corrigir runtime" \
  --profile python-service
```

## Estrutura

```text
vision_core_v55/
├── apps/cli/jarvis.py
├── vision_core/
│   ├── adapters/python.py
│   ├── patches/planner.py
│   ├── patches/apply.py
│   ├── patches/store.py
│   ├── policy/engine.py
│   ├── codex/bridge.py
│   ├── runtime/mission.py
│   ├── runtime/pipeline.py
│   ├── gates/basic.py
│   ├── scheduler/loop.py
│   ├── queue/worker.py
│   ├── snapshots/manager.py
│   └── incidents/store.py
└── data/
```

## Observações

- Não faz promoção sem `PASS GOLD`.
- O bridge GitHub está preparado com fluxo local por Git e saída padronizada para futura integração por API/PR real.
- O patch planner gera correções seguras com foco em healthcheck, porta, host, requirements e bootstrap.
- O rollback usa backup dos arquivos afetados por snapshot.

## Próximo salto

- status checks GitHub API
- PR real remoto
- impact map por dependência
- execução multiambiente
