
## `AGENTS.md`

```md
# AGENTS

## Objective

Unificar todas as versões e fragmentos deste repositório em uma arquitetura única chamada **VISION CORE**.

O resultado esperado é uma base reconstruída em `/vision-core/`, com separação clara por domínio, rastreabilidade da origem e preservação do histórico.

---

## Repository map

### Fonte histórica
- `extracted/raw/` → dump bruto preservado
- `extracted/normalized/versions/` → evolução temporal do sistema
- `versions/` → zips originais preservados

### Fonte arquitetural principal
- `extracted/normalized/fragments/core/` → blocos reutilizáveis prioritários

### Fonte secundária
- `extracted/normalized/fragments/misc/` → itens residuais, não prioritários

---

## Core rules

- Nunca alterar `extracted/raw/`
- Nunca usar `fragments/misc/` como base principal
- Sempre priorizar `fragments/core/`
- Usar `versions/` como referência evolutiva
- Preservar rastreabilidade da origem dos componentes
- Evitar duplicação desnecessária
- Preferir refatoração e consolidação a simples cópia cega
- Sem PASS GOLD nada é promovido

---

## Target architecture domains

### 1. orchestration
Responsáveis:
- OpenClaw
- OpenSquad

Objetivo:
- roteamento de missão
- decomposição de tarefas
- coordenação de agentes
- scheduling de alto nível

### 2. diagnosis
Responsável:
- Hermes

Objetivo:
- coleta de evidências
- RCA
- classificação de incidentes
- recomendação de ação

### 3. security
Responsável:
- Aegis

Objetivo:
- policy enforcement
- controle de risco
- bloqueios de segurança
- governança de execução

### 4. validation
Responsável:
- SDDF

Objetivo:
- gates
- PASS / FAIL / GOLD
- validação técnica obrigatória
- bloqueio de promoção

### 5. rollback
Responsável:
- Stable Vault

Objetivo:
- snapshots
- restore
- rollback multi-arquivo
- baseline GOLD

### 6. execution
Responsáveis:
- Operator
- OpenClaude

Objetivo:
- execução de planos
- apply patch
- worker loop
- scheduler runtime

### 7. memory
Responsáveis:
- Archivist
- Obsidian

Objetivo:
- incident store
- memória persistente
- histórico de decisões
- knowledge base operacional

### 8. structure
Responsável:
- Navigator

Objetivo:
- mapeamento do projeto
- dependências
- topologia
- contratos e arquivos críticos

### 9. integration
Responsáveis:
- Codex
- GitHub

Objetivo:
- PRs
- bridge de integração
- organização de branches
- revisão e consolidação

### 10. performance
Responsável:
- Go services

Objetivo:
- workers de alta performance
- queue
- scheduler
- otimizações de runtime

---

## Reconstruction policy

Ao reconstruir `/vision-core/`:

1. criar uma arquitetura limpa e modular
2. separar responsabilidades por domínio
3. manter nomes consistentes
4. remover redundâncias
5. preferir componentes mais novos quando forem claramente superiores
6. preservar componentes mais antigos quando trouxerem capacidade única
7. registrar a origem lógica das fusões em comentários ou documentação quando útil

---

## Forbidden actions

- Não apagar histórico bruto
- Não sobrescrever arbitrariamente versões antigas
- Não promover nada sem gate explícito
- Não tratar `misc/` como fonte primária
- Não colapsar todos os módulos em um único arquivo monolítico
- Não remover rollback
- Não remover policy enforcement
- Não remover memória/incident tracking

---

## Review guidelines

Ao gerar mudanças:

- separar PRs por domínio arquitetural
- manter mudanças pequenas e rastreáveis
- descrever claramente o que foi consolidado
- destacar conflitos entre versões
- explicar decisões de priorização
- apontar riscos de regressão
- respeitar a regra de PASS GOLD

---

## Expected output

Criar ou reconstruir a árvore principal em:

```text
vision-core/