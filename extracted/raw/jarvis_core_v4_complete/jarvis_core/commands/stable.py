import json
from jarvis_core.stable_vault import list_snapshots, promote_to_gold, rollback_gold


def stable_command(args) -> str:
    if args.stable_action == 'list':
        return json.dumps(list_snapshots(args.project), ensure_ascii=False, indent=2)
    if args.stable_action == 'promote':
        return json.dumps(promote_to_gold(args.project, args.source), ensure_ascii=False, indent=2)
    if args.stable_action == 'rollback':
        target = args.target or '.'
        return json.dumps(rollback_gold(args.project, target), ensure_ascii=False, indent=2)
    raise ValueError('Ação stable inválida')
