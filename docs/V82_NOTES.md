# V8.2 Blindado Real

## O que entrou
- histórico persistente de integrações em `integration/history.json`
- endpoint `GET /api/integration/history`
- classificação explícita de falhas GitHub (`error_class`)
- retry controlado para chamadas GitHub API
- idempotência melhor para cenário sem mudanças staged
- dashboard com histórico, attempts e error class

## Regra central
Sem PASS GOLD não existe merge, promotion, release nem stable.

## Novos estados úteis
- `blocked_validation`
- `github_not_configured`
- `noop_no_changes`
- `retryable_network_error`
- `github_auth_error`
- `push_rejected`
- `merge_conflict`
- `merge_blocked_remote_state`

## API nova
- `GET /api/integration/history`
