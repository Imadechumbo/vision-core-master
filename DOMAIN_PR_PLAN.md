# DOMAIN PR PLAN

## Validação explícita da arquitetura VISION CORE

Status da validação da fundação arquitetural (com base nas regras e domínios definidos para reconstrução):

- [x] **Bloqueio de promoção sem PASS GOLD**: promoção condicionada aos gates de validação (PASS / FAIL / GOLD), com bloqueio explícito sem GOLD.
- [x] **Domínio de rollback real**: snapshots, restore, rollback multi-arquivo e baseline GOLD mantidos como domínio dedicado.
- [x] **Domínio de orchestration separado**: roteamento de missão, decomposição de tarefas e coordenação em domínio próprio.
- [x] **Domínio de diagnosis separado**: coleta de evidências, RCA e classificação em domínio próprio.
- [x] **Memória persistente**: incident store, histórico de decisões e base de conhecimento operacional preservados.
- [x] **Policy enforcement**: enforcement de políticas, controle de risco e governança definidos como responsabilidade explícita de segurança.

## Sequência de PRs por domínio (continuação)

A continuação será fatiada em PRs pequenos e rastreáveis, na ordem solicitada:

1. **orchestration**
   - Estruturação do domínio de orquestração e contratos de missão/scheduling.
2. **diagnosis-memory**
   - Consolidação de diagnóstico (evidence + RCA) e memória persistente (incident/history/store).
3. **security-validation**
   - Policy enforcement (Aegis) + gates SDDF com bloqueio de promoção sem PASS GOLD.
4. **rollback-execution**
   - Stable Vault, snapshots/restore/rollback e acoplamento seguro com runtime de execução.
5. **integration-performance**
   - Bridge de integração (Codex/GitHub) e trilha de performance (workers/queue/scheduler otimizado).

## Critérios transversais para todos os PRs

- Rastreabilidade da origem dos componentes preservada.
- `extracted/raw/` permanece imutável.
- `fragments/core/` priorizado como base principal.
- `fragments/misc/` apenas complementar, nunca fonte primária.
- Nenhuma promoção sem gate explícito e PASS GOLD.
