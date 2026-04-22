from __future__ import annotations
import argparse, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from vision_core.adapters.python import detect_python_project, suggest_runtime_commands
from vision_core.patches.planner import generate_patch_plan
from vision_core.patches.store import load_plan
from vision_core.patches.apply import apply_patch_plan
from vision_core.snapshots.manager import rollback_snapshot
from vision_core.policy.engine import evaluate_promotion
from vision_core.gates.basic import run_default_gates
from vision_core.codex.bridge import prepare_branch_and_commit
from vision_core.runtime.pipeline import run_pipeline
from vision_core.queue.worker import enqueue, run_once
from vision_core.scheduler.loop import scheduler_loop

DATA_DIR = str(ROOT / "data")

def _print(data):
    print(json.dumps(data, ensure_ascii=False, indent=2))

def main():
    parser = argparse.ArgumentParser(prog="jarvis.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("python-adapter")
    p.add_argument("--project-root", required=True)

    p = sub.add_parser("patch-plan")
    p.add_argument("--project-root", required=True)
    p.add_argument("--failure-type", default="")
    p.add_argument("--profile", default="python-service")
    p.add_argument("--plan-file", default="plan.json")

    p = sub.add_parser("apply-plan")
    p.add_argument("--project-root", required=True)
    p.add_argument("--plan-file", required=True)

    p = sub.add_parser("rollback")
    p.add_argument("--project-root", required=True)
    p.add_argument("--snapshot-id", required=True)

    p = sub.add_parser("policy-check")
    p.add_argument("--pass-gold", action="store_true")
    p.add_argument("--gates-json", default="{}")
    p.add_argument("--patch-plan-json", default="{}")
    p.add_argument("--codex-review-requested", action="store_true")
    p.add_argument("--incidents-open", type=int, default=0)

    p = sub.add_parser("gates")
    p.add_argument("--project-root", required=True)

    p = sub.add_parser("github-prepare-pr")
    p.add_argument("--project-root", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--branch-name")

    p = sub.add_parser("run")
    p.add_argument("--project-root", required=True)
    p.add_argument("--mission", required=True)
    p.add_argument("--profile", default="python-service")

    p = sub.add_parser("queue-enqueue")
    p.add_argument("--project-root", required=True)
    p.add_argument("--mission", required=True)
    p.add_argument("--profile", default="python-service")

    p = sub.add_parser("worker-run-once")

    p = sub.add_parser("scheduler-loop")
    p.add_argument("--tick-seconds", type=int, default=10)

    args = parser.parse_args()

    if args.cmd == "python-adapter":
        _print({"detection": detect_python_project(args.project_root), "commands": suggest_runtime_commands(args.project_root)})
        return

    if args.cmd == "patch-plan":
        plan = generate_patch_plan(args.project_root, failure_type=args.failure_type, profile=args.profile)
        pathlib.Path(args.plan_file).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        _print(plan)
        return

    if args.cmd == "apply-plan":
        plan = load_plan(args.plan_file)
        _print(apply_patch_plan(args.project_root, plan, DATA_DIR))
        return

    if args.cmd == "rollback":
        _print(rollback_snapshot(args.project_root, DATA_DIR, args.snapshot_id))
        return

    if args.cmd == "policy-check":
        gates = json.loads(args.gates_json)
        patch_plan = json.loads(args.patch_plan_json)
        _print(evaluate_promotion(
            pass_gold=args.pass_gold,
            gates=gates,
            patch_plan=patch_plan,
            codex_review_requested=args.codex_review_requested,
            incidents_open=args.incidents_open,
        ))
        return

    if args.cmd == "gates":
        _print(run_default_gates(args.project_root))
        return

    if args.cmd == "github-prepare-pr":
        _print(prepare_branch_and_commit(args.project_root, args.title, args.branch_name))
        return

    if args.cmd == "run":
        _print(run_pipeline(args.project_root, args.mission, DATA_DIR, args.profile))
        return

    if args.cmd == "queue-enqueue":
        _print(enqueue(DATA_DIR, {"project_root": args.project_root, "mission": args.mission, "profile": args.profile}))
        return

    if args.cmd == "worker-run-once":
        _print(run_once(DATA_DIR))
        return

    if args.cmd == "scheduler-loop":
        scheduler_loop(DATA_DIR, args.tick_seconds)
        return

if __name__ == "__main__":
    main()
