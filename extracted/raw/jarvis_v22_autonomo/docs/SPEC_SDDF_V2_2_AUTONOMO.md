# SPEC SDDF V2.2 — JARVIS CORE OMEGA HYBRID AUTÔNOMO

## Objetivo

Manter um núcleo operacional híbrido, offline-first, capaz de:
- interpretar missão em linguagem natural
- registrar contexto e arquitetura
- executar diagnóstico local com LLM offline
- inspecionar projeto local
- detectar runtime disponível (Ollama, Docker, perfis)
- produzir resposta estruturada
- sobreviver a mudanças de chat sem perder arquitetura

## Regras absolutas
- Sem PASS GOLD, nada é promovido.
- Offline first.
- Free API second.
- Paid API last resort.
- Toda arquitetura e ferramenta nova precisa ser registrada em manual SDDF.

## Componentes V2.2
- Python CLI Orchestrator
- Ollama client robusto
- Model resolver com autodetect
- Project scanner local
- Cache SQLite
- Runtime manager
- Serviço Go de autonomia
- Perfis YAML de runtime
- Configuração de modelos e roteamento
- Manual de produto, projeto e produção

## Limites desta versão
- Ainda não faz deploy real
- Ainda não aplica patch automático em múltiplos arquivos
- Ainda não possui gates SDDF reais de produção
- Ainda não integra Portainer/Docker automaticamente quando Docker está ausente

## Próximo salto
- V2.3: gates reais, leitura de projeto mais profunda, fallback local→free API, Aegis enforcement básico.
