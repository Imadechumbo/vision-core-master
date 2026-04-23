# VISION CORE V6.7

Pacote V6.7 com:

- Hermes (diagnosis)
- SDDF (validation)
- Aegis (security)
- Operator (execution)
- Stable Vault (rollback)
- Memory store persistente em SQLite
- Diff real por arquivo
- Patch multi-arquivo
- Rollback seletivo
- CLI avançado
- API real com endpoints de missão, memória e rollback

## Comandos

```bash
python -m vision_core.apps.cli.vision health
python -m vision_core.apps.cli.vision mission "corrigir runtime do technetgame"
python -m vision_core.apps.cli.vision memory list
python -m vision_core.apps.cli.vision memory get <mission_id>
python -m vision_core.apps.cli.vision rollback <snapshot_id>
python -m vision_core.apps.cli.vision rollback-file <snapshot_id> <target_file>
python -m vision_core.apps.cli.run_pipeline
```

## Regra central

Sem PASS GOLD nada é promovido.
