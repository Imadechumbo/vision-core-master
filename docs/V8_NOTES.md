# VISION CORE V8

## O que entrou

1. Codex bundle automático por missão em `.vision_core_runtime/codex_exports/`
2. PR validation real via `PRValidationService`
3. GitHub bridge real com git local + GitHub API
4. auto merge opcional somente com PASS GOLD e checks aprovados
5. diff visual no dashboard e resposta da API

## Regras de merge

- `validation.pass_gold == True`
- `security.promotion_allowed == True`
- `execution_receipt.applied_files >= 1`
- diffs presentes

Se qualquer gate falhar, a integração fica bloqueada.

## Script-base para Codex organizar

Cada missão GOLD/PASS gera um JSON bundle contendo:

- missão
- root cause
- strategy
- resultado do SDDF
- decisão do Aegis
- snapshot id
- diffs reais

Esse bundle é a base para o Codex reestruturar commits, PRs ou futuros fluxos de automação.
