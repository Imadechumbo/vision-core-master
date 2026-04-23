# VISION CORE V8.1

V8.1 blinda a integração GitHub/Codex do V8.

## Melhorias

- Reuso de branch se ela já existir localmente
- Abort seguro quando não há alterações staged para commit
- Reuso de PR aberto no GitHub em vez de tentar criar duplicado
- Persistência do último estado da integração em `integration/last_integration.json`
- Novo endpoint: `GET /api/integration/last`
- Dashboard com refresh do último estado e checks detalhados

## Regras preservadas

- sem PASS GOLD não existe merge
- sem PASS GOLD não existe promotion
- auto merge só ocorre se `VISION_AUTO_MERGE=true` e todos os checks passarem
