import json
import sys
from vision_core.runtime.pipeline import VisionPipeline

def print_usage():
    print("VISION CORE CLI")
    print("")
    print("Uso:")
    print('  python -m vision_core.apps.cli.vision mission "corrigir runtime do technetgame"')
    print("  python -m vision_core.apps.cli.vision health")
    print("  python -m vision_core.apps.cli.vision memory list")
    print("  python -m vision_core.apps.cli.vision memory get <mission_id>")
    print("  python -m vision_core.apps.cli.vision rollback <snapshot_id>")
    print("  python -m vision_core.apps.cli.vision rollback-file <snapshot_id> <target_file>")

def run_mission(args):
    if not args:
        print("[ERRO] Missão não informada.")
        print_usage()
        return 1

    mission = " ".join(args)
    pipeline = VisionPipeline()
    result = pipeline.run(mission, environment="production")

    print("STATUS:", result.status)
    print("MISSION:", mission)
    print("MISSION_ID:", result.data["mission_id"])
    print("ROOT_CAUSE:", result.data["diagnosis"].root_cause)
    print("STRATEGY:", result.data["diagnosis"].strategy)
    print("SOURCE:", result.data["diagnosis"].source)
    print("VALIDATION:", result.data["validation"].outcome)
    print("PASS_GOLD:", result.data["validation"].pass_gold)
    print("PROMOTION_ALLOWED:", result.data["security"].promotion_allowed)
    print("APPLIED_FILES:", result.data["execution_receipt"].applied_files)
    print("SNAPSHOT_ID:", result.data["snapshot_id"])
    integration = result.data.get("integration")
    if integration is not None:
        print("INTEGRATION_STATUS:", integration.status)
        print("CODEX_BUNDLE:", integration.codex.bundle_path)
        print("PR_VALIDATION:", integration.pr_validation.status)
        print("MERGE_ALLOWED:", integration.pr_validation.merge_allowed)
        print("GITHUB_STATUS:", integration.github.status)
        if integration.github.branch:
            print("GITHUB_BRANCH:", integration.github.branch)
        if integration.github.pr_url:
            print("GITHUB_PR_URL:", integration.github.pr_url)
    print("")

    for step in result.steps:
        print(f"[{step['time']}] {step['step']}: {step['info']}")
    return 0

def health():
    print("VISION CORE OK")
    return 0

def memory_list():
    pipeline = VisionPipeline()
    print(json.dumps(pipeline.list_memory(), indent=2, ensure_ascii=False))
    return 0

def memory_get(mission_id: str):
    pipeline = VisionPipeline()
    item = pipeline.get_memory(mission_id)
    if item is None:
        print(json.dumps({"error": "mission_id not found"}, indent=2))
        return 1
    print(json.dumps(item, indent=2, ensure_ascii=False))
    return 0

def rollback_snapshot(snapshot_id: str):
    pipeline = VisionPipeline()
    print(json.dumps(pipeline.restore_manager.restore_snapshot(snapshot_id), indent=2, ensure_ascii=False))
    return 0

def rollback_file(snapshot_id: str, target_file: str):
    pipeline = VisionPipeline()
    print(json.dumps(pipeline.rollback_file(snapshot_id, target_file), indent=2, ensure_ascii=False))
    return 0

def main():
    if len(sys.argv) < 2:
        print_usage()
        raise SystemExit(1)

    command = sys.argv[1].lower()
    if command == "mission":
        raise SystemExit(run_mission(sys.argv[2:]))
    if command == "health":
        raise SystemExit(health())
    if command == "memory":
        if len(sys.argv) < 3:
            print_usage()
            raise SystemExit(1)
        sub = sys.argv[2].lower()
        if sub == "list":
            raise SystemExit(memory_list())
        if sub == "get" and len(sys.argv) >= 4:
            raise SystemExit(memory_get(sys.argv[3]))
        print_usage()
        raise SystemExit(1)
    if command == "rollback" and len(sys.argv) >= 3:
        raise SystemExit(rollback_snapshot(sys.argv[2]))
    if command == "rollback-file" and len(sys.argv) >= 4:
        raise SystemExit(rollback_file(sys.argv[2], sys.argv[3]))

    print(f"[ERRO] Comando inválido: {command}")
    print_usage()
    raise SystemExit(1)

if __name__ == "__main__":
    main()
