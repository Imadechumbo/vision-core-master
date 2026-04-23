import argparse
import json
import sys
from pathlib import Path

from vision_core.adapters.detect import detect_adapter
from vision_core.adapters.python_adapter import inspect_python_project
from vision_core.adapters.node_adapter import inspect_node_project
from vision_core.gates.engine import run_gates
from vision_core.patches.planner import build_patch_plan
from vision_core.patches.apply import apply_plan
from vision_core.patches.rollback import rollback_snapshot
from vision_core.policy.engine import evaluate_policy
from vision_core.codex.bridge import prepare_branch_and_commit
from vision_core.runtime.runner import run_mission
from vision_core.queue.store import enqueue_mission
from vision_core.queue.worker import worker_run_once
from vision_core.scheduler.loop import scheduler_loop


def _print(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("detect-adapter")
    p.add_argument("--project-root", required=True)
    p.add_argument("--profile", default="auto")

    p = sub.add_parser("python-adapter")
    p.add_argument("--project-root", required=True)

    p = sub.add_parser("node-adapter")
    p.add_argument("--project-root", required=True)

    p = sub.add_parser("patch-plan")
    p.add_argument("--project-root", required=True)
    p.add_argument("--failure-type", required=True)
    p.add_argument("--profile", default="auto")
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
    p.add_argument("--profile", default="auto")

    p = sub.add_parser("github-prepare-pr")
    p.add_argument("--project-root", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--branch-name", default=None)

    p = sub.add_parser("run")
    p.add_argument("--project-root", required=True)
    p.add_argument("--mission", required=True)
    p.add_argument("--profile", default="auto")

    p = sub.add_parser("queue-enqueue")
    p.add_argument("--mission", required=True)
    p.add_argument("--project-root", required=True)
    p.add_argument("--profile", default="auto")

    p = sub.add_parser("worker-run-once")

    p = sub.add_parser("scheduler-loop")
    p.add_argument("--tick-seconds", type=int, default=10)

    args = parser.parse_args()

    if args.cmd == "detect-adapter":
        _print(detect_adapter(args.project_root, args.profile))
        return

    if args.cmd == "python-adapter":
        _print(inspect_python_project(args.project_root))
        return

    if args.cmd == "node-adapter":
        _print(inspect_node_project(args.project_root))
        return

    if args.cmd == "patch-plan":
        plan = build_patch_plan(args.project_root, args.failure_type, args.profile)
        Path(args.plan_file).write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
        _print(plan)
        return

    if args.cmd == "apply-plan":
        plan = json.loads(Path(args.plan_file).read_text(encoding="utf-8"))
        _print(apply_plan(args.project_root, plan))
        return

    if args.cmd == "rollback":
        _print(rollback_snapshot(args.project_root, args.snapshot_id))
        return

    if args.cmd == "policy-check":
        gates = json.loads(args.gates_json)
        patch_plan = json.loads(args.patch_plan_json)
        _print(evaluate_policy(pass_gold=args.pass_gold, gates=gates, patch_plan=patch_plan,
                               codex_review_requested=args.codex_review_requested,
                               incidents_open=args.incidents_open))
        return

    if args.cmd == "gates":
        _print(run_gates(args.project_root, args.profile))
        return

    if args.cmd == "github-prepare-pr":
        _print(prepare_branch_and_commit(args.project_root, args.title, args.branch_name))
        return

    if args.cmd == "run":
        _print(run_mission(args.project_root, args.mission, args.profile))
        return

    if args.cmd == "queue-enqueue":
        _print(enqueue_mission(args.project_root, args.mission, args.profile))
        return

    if args.cmd == "worker-run-once":
        _print(worker_run_once())
        return

    if args.cmd == "scheduler-loop":
        _print(scheduler_loop(args.tick_seconds))
        return


if __name__ == "__main__":
    main()
