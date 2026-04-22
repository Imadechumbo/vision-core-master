# VISION CORE V5.5.1 NODE REAL

Pacote executável focado em projetos Node/Express e Python, com:
- auto-detecção de adapter
- adapter Node real
- planner de patch para o caso `req.file.mimetype`
- apply com snapshot multi-arquivo
- rollback por snapshot
- gates JS (`node --check`) e Python (`py_compile`)
- policy bloqueando promoção com plano vazio
- bridge GitHub preparado e validado

## Comandos rápidos

```bash
python apps/cli/jarvis.py detect-adapter --project-root "C:\SEU_PROJETO" --profile node-service
python apps/cli/jarvis.py node-adapter --project-root "C:\SEU_PROJETO"
python apps/cli/jarvis.py patch-plan --project-root "C:\SEU_PROJETO" --failure-type "corrigir erro vision mimetype null" --profile node-service --plan-file plan.json
python apps/cli/jarvis.py apply-plan --project-root "C:\SEU_PROJETO" --plan-file plan.json
python apps/cli/jarvis.py rollback --project-root "C:\SEU_PROJETO" --snapshot-id SNAPSHOT_ID
python apps/cli/jarvis.py run --project-root "C:\SEU_PROJETO" --mission "corrigir erro vision mimetype null" --profile node-service
```
