# MANUAL MESTRE DO PROJETO V4

## 1. Objetivo
Transformar missões técnicas em ciclo controlado:
`scan -> evidence -> RCA -> patch -> gates -> stable -> rollback -> incidentes -> logs`

## 2. Componentes
- **Mission Parser**: normaliza missão
- **Intent Resolver**: classifica intenção
- **Project Scanner**: inventaria árvore, rotas, env e stack
- **Evidence Collector**: consolida evidências
- **RCA Engine**: causa raiz e cause chain
- **Playbooks**: conhecimento por intent
- **Patch Planner**: plano estruturado
- **Patch Applier**: aplica patch supervisionado
- **Diff Engine**: gera diff unificado
- **Aegis Policy**: gates de risco
- **HTTP Gates**: validação real
- **Stable Vault**: baseline GOLD
- **Rollback**: restauração rápida
- **Incident Store**: JSON + SQLite
- **Obsidian Logger**: histórico markdown
- **Runtime Go**: runtime local

## 3. Fluxo V4
1. Recebe missão
2. Resolve intent
3. Faz scan
4. Carrega playbook
5. Consolida evidências
6. Gera RCA
7. Planeja patch
8. Aegis aprova ou bloqueia
9. Aplica patch (dry-run ou apply)
10. Gera diff
11. Executa gates HTTP reais
12. Se PASS GOLD promove para Stable Vault
13. Se FAIL pode executar rollback
14. Registra incidente
15. Escreve nota no Obsidian

## 4. Regra operacional
**SEM PASS GOLD -> NADA E PROMOVIDO**

## 5. TechNetGame
Adapter padrão valida:
- `/api/health`
- `/api/news/latest`
- `/api/v1/chat`
- `/api/v1/chat/vision`
