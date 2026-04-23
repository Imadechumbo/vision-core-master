# VISION CORE V8.1

V8.1 adiciona blindagem operacional ao V8:

- Codex export bundle por missão
- PR validation real antes de merge
- GitHub bridge com branch automática, reuso de branch existente, commit, push e PR
- reuso de PR aberto no GitHub quando já existir
- abort seguro quando não há mudanças staged para commit
- auto merge opcional apenas com PASS GOLD
- diff visual real no dashboard
- endpoint dedicado `GET /api/integration/last`

## Regra central

Sem PASS GOLD nada é promovido, mergeado, liberado ou marcado como stable.

## Variáveis opcionais

- `HERMES_LLM_PROVIDER`
- `HERMES_LLM_MODEL`
- `HERMES_LLM_API_KEY`
- `GITHUB_TOKEN`
- `GITHUB_REPO`
- `GITHUB_BASE_BRANCH`
- `VISION_REPO_ROOT`
- `VISION_AUTO_MERGE`

Sem variáveis GitHub, o V8.1 continua exportando o bundle para Codex e validando o PR localmente, mas não publica no GitHub.


## V8.2 blindado real
- histórico de integração em `integration/history.json`
- endpoint `GET /api/integration/history`
- retry controlado para GitHub API
- classificação de falhas por `error_class`


## V8.3
- histórico paginado de integração via `/api/integration/history?page=1&page_size=5`
- dashboard com navegação de páginas do histórico
