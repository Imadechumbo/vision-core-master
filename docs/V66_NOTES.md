# V6.6 Notes

## Entregas
- snapshot real multi-arquivo
- restore seletivo por arquivo
- planner multi-file
- apply engine com diff unificado real
- memory persistente em SQLite
- pipeline integrado com promotion gate

## Fluxo
mission -> orchestration -> diagnosis -> planning -> snapshot -> execution -> validation -> security -> decision -> memory -> rollback(if needed)
