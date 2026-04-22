from jarvis_core.mission_parser import parse_mission
from jarvis_core.scanner import scan_project
from jarvis_core.evidence import collect_evidence
from jarvis_core.playbooks import get_playbook
from jarvis_core.rca import build_rca
from jarvis_core.patch_planner import plan_patch
from jarvis_core.policy import evaluate_policy
from jarvis_core.patch_applier import apply_patch
from jarvis_core.gates import run_http_gates
from jarvis_core.incident_store import save_incident
from jarvis_core.obsidian_logger import log_obsidian
from jarvis_core.stable_vault import promote_to_gold, rollback_gold
from jarvis_core.adapters.factory import get_adapter


def run_mission(mission: str, project_root: str, project: str, base_url: str, apply: bool, dry_run: bool, auto_rollback: bool):
    mission_obj = parse_mission(mission)
    scan_result = scan_project(project_root)
    evidence = collect_evidence(project_root, scan_result, mission)
    playbook = get_playbook(mission_obj.intent)
    rca = build_rca(mission_obj, evidence, playbook)
    patch = plan_patch(mission_obj, scan_result, rca)
    policy = evaluate_policy(mission_obj, patch)

    patch_result = {'patch_dir': '', 'results': []}
    if policy['allowed']:
        patch_result = apply_patch(project_root, patch, apply=apply and not dry_run)

    adapter = get_adapter(project)
    gates = run_http_gates(base_url=base_url, adapter=adapter)

    stable = None
    rollback = None
    if gates['pass_gold']:
        stable = promote_to_gold(project=project, source_dir=project_root)
    elif auto_rollback:
        try:
            rollback = rollback_gold(project=project, target_dir=project_root)
        except Exception as e:
            rollback = {'error': str(e)}

    summary = f"{gates['summary']} | intent={mission_obj.intent} | risk={policy['risk_level']}"
    incident = save_incident({
        'project': project,
        'mission': mission_obj.normalized,
        'intent': mission_obj.intent,
        'pass_gold': gates['pass_gold'],
        'root_cause': rca.root_cause,
        'summary': summary,
        'patch_dir': patch_result.get('patch_dir', ''),
        'stable_snapshot': (stable or {}).get('snapshot_id', ''),
    })

    obsidian_path = log_obsidian(
        project=project,
        mission=mission_obj.normalized,
        summary=summary,
        content=(
            f"Root cause: {rca.root_cause}\n\n"
            f"Cause chain: {rca.cause_chain}\n\n"
            f"Policy: {policy}\n\n"
            f"Gates: {gates}\n"
        ),
    )

    return {
        'ok': True,
        'mission': mission_obj.__dict__,
        'scan': scan_result,
        'playbook': playbook,
        'rca': rca.to_dict(),
        'patch_plan': patch.to_dict(),
        'policy': policy,
        'patch_result': patch_result,
        'gates': gates,
        'stable': stable,
        'rollback': rollback,
        'incident': incident,
        'obsidian_path': obsidian_path,
    }
