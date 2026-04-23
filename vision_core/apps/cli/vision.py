import sys
from vision_core.runtime.pipeline import VisionPipeline


def print_usage():
    print("VISION CORE CLI")
    print("")
    print("Uso:")
    print('  python -m vision_core.apps.cli.vision mission "corrigir runtime do technetgame"')
    print("  python -m vision_core.apps.cli.vision health")


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
    print("VALIDATION:", result.data["validation"].outcome)
    print("PASS_GOLD:", result.data["validation"].pass_gold)
    print("PROMOTION_ALLOWED:", result.data["security"].promotion_allowed)
    print("APPLIED_FILES:", result.data["execution_receipt"].applied_files)
    print("SNAPSHOT_ID:", result.data["snapshot_id"])
    print("")

    for step in result.steps:
        print(f"[{step['time']}] {step['step']}: {step['info']}")

    return 0


def health():
    print("VISION CORE OK")
    return 0


def main():
    if len(sys.argv) < 2:
        print_usage()
        raise SystemExit(1)

    command = sys.argv[1].lower()

    if command == "mission":
        code = run_mission(sys.argv[2:])
        raise SystemExit(code)

    if command == "health":
        code = health()
        raise SystemExit(code)

    print(f"[ERRO] Comando inválido: {command}")
    print_usage()
    raise SystemExit(1)


if __name__ == "__main__":
    main()
