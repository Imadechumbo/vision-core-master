# Runtime V2.2 AUTÔNOMO

## Uso
```bash
cd runtime_v22
python -m pip install -r requirements.txt
python apps/cli/jarvis.py "diagnosticar runtime" --json-only
python apps/cli/jarvis.py "corrigir vision do technetgame" --project-root "C:\\caminho\\do\\projeto"
```

## O que esta versão faz
- autodetect de modelos Ollama
- evita quebra por timeout_seconds / payload inconsistente
- inspeciona projeto local
- registra resposta em cache SQLite
- responde mesmo sem Docker
