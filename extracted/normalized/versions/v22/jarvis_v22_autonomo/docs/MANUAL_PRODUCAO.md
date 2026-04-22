# Manual de Produção — JARVIS CORE V2.2 AUTÔNOMO

## Requisitos mínimos
- Python 3.10+
- Ollama ativo em `http://127.0.0.1:11434`
- ao menos 1 modelo local instalado

## Requisitos opcionais
- Docker Desktop
- Go 1.22+

## Procedimento de uso
1. Entrar em `runtime_v22`
2. Instalar requirements
3. Confirmar `ollama list`
4. Rodar missão

## Continuidade entre chats
Sempre registrar no novo chat:
- versão atual: V2.2 AUTÔNOMO
- modelos locais disponíveis
- docker presente ou ausente
- caminhos reais de projeto usados
- falha atual observada
- últimos ajustes em `models.yaml`, `ollama_client.py`, `mission_controller.py`
