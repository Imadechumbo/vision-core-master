# Manual do Projeto — JARVIS CORE V2.2 AUTÔNOMO

## Propósito
Evitar perda de contexto técnico durante ciclos longos de teste, debug, troca de repositório e troca de chat.

## Estrutura
- `docs/` documentação SDDF e continuidade
- `runtime_v22/` runtime local funcional
- `v1_1_spec/` referência arquitetural de base

## Stack atual
- Python: orquestração local e CLI
- Go: serviço de autonomia para escalagem futura
- Ollama: LLM local
- SQLite: cache local
- YAML: roteamento, modelos, políticas, perfis

## Princípios
- arquitetura registrada antes de grandes mudanças
- evitar dependência total de API paga
- usar Go para componentes que exigem eficiência e escalabilidade futura
