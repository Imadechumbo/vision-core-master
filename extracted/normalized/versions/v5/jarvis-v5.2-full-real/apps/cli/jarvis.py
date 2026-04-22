from __future__ import annotations
import argparse
import json
from pathlib import Path

from jarvis_v5.intelligence_plane.project_scanner import scan_project
from jarvis_v5.execution_plane.http_gates import run_http_checks
from jarvis_v5.execution_plane.rollback_executor import rollback_patch
from jarvis_v5.memory_plane.patch_registry import PatchRegistry

DEFAULT_STORAGE = Path("storage")

TECHNETGAME_ENDPOINTS = [
    {"name": "health", "method": "GET", "path": "/api/health"},
    {"name": "news_latest", "method": "GET", "path": "/api/news/latest"},
    {"name": "chat", "method": "POST", "path": "/api/v1/chat", "json": {"message": "ping"}},
    {"name": "vision", "method": "POST", "path": "/api/v1/chat/vision", "json": {"message": "ping"}},
]

def cmd_scan(args):
    print(json.dumps(scan_project(args.project_root), ensure_ascii=False, indent=2))

def cmd_http_gates(args):
    print(json.dumps(run_http_checks(args.base_url, TECHNETGAME_ENDPOINTS), ensure_ascii=False, indent=2))

def cmd_patches(args):
    reg = PatchRegistry(args.storage)
    print(json.dumps(reg.list(project=args.project), ensure_ascii=False, indent=2))

def cmd_rollback(args):
    result = rollback_patch(args.storage, args.project, args.patch_id, args.target_root)
    print(json.dumps(result, ensure_ascii=False, indent=2))

def build_parser():
    p = argparse.ArgumentParser(description="JARVIS V5.2.1 patch CLI")
    sub = p.add_subparsers(dest="command")

    scan = sub.add_parser("scan")
    scan.add_argument("--project-root", required=True)
    scan.set_defaults(func=cmd_scan)

    gates = sub.add_parser("http-gates")
    gates.add_argument("--base-url", required=True)
    gates.set_defaults(func=cmd_http_gates)

    patches = sub.add_parser("patches")
    patches.add_argument("--project", required=False)
    patches.add_argument("--storage", default=str(DEFAULT_STORAGE))
    patches.set_defaults(func=cmd_patches)

    rollback = sub.add_parser("rollback-patch")
    rollback.add_argument("--project", required=True)
    rollback.add_argument("--patch-id", required=True)
    rollback.add_argument("--target-root", required=False)
    rollback.add_argument("--storage", default=str(DEFAULT_STORAGE))
    rollback.set_defaults(func=cmd_rollback)
    return p

def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)

if __name__ == "__main__":
    main()
