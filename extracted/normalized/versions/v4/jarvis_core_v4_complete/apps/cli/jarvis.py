#!/usr/bin/env python3
import argparse
import json
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from jarvis_core.commands.run_mission import run_mission
from jarvis_core.commands.incidents import query_incidents_command
from jarvis_core.commands.stable import stable_command
from jarvis_core.runtime.go_bridge import ensure_runtime_binary_message


def build_main_parser():
    parser = argparse.ArgumentParser(description='JARVIS CORE V4 REAL')
    parser.add_argument('mission', help='Missão principal')
    parser.add_argument('--project-root', default=os.getcwd())
    parser.add_argument('--project', default='technetgame')
    parser.add_argument('--base-url', default='')
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--dry-run', action='store_true')
    parser.add_argument('--auto-rollback', action='store_true')
    return parser


def build_incidents_parser():
    parser = argparse.ArgumentParser(description='Consultar incidentes')
    parser.add_argument('--filter', default='')
    parser.add_argument('--limit', type=int, default=20)
    return parser


def build_stable_parser():
    parser = argparse.ArgumentParser(description='Operações do stable vault')
    sub = parser.add_subparsers(dest='stable_action', required=True)
    p1 = sub.add_parser('list')
    p1.add_argument('--project', required=True)
    p2 = sub.add_parser('promote')
    p2.add_argument('--project', required=True)
    p2.add_argument('--source', required=True)
    p3 = sub.add_parser('rollback')
    p3.add_argument('--project', required=True)
    p3.add_argument('--target', default='')
    return parser


def build_runtime_parser():
    parser = argparse.ArgumentParser(description='Runtime Go')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=8090)
    return parser


def main():
    argv = sys.argv[1:]
    if argv and argv[0] == 'incidents':
        args = build_incidents_parser().parse_args(argv[1:])
        print(query_incidents_command(filter_text=args.filter, limit=args.limit))
        return
    if argv and argv[0] == 'stable':
        args = build_stable_parser().parse_args(argv[1:])
        print(stable_command(args))
        return
    if argv and argv[0] == 'runtime':
        args = build_runtime_parser().parse_args(argv[1:])
        print(ensure_runtime_binary_message(host=args.host, port=args.port))
        return

    args = build_main_parser().parse_args(argv)
    if not args.apply and not args.dry_run:
        args.dry_run = True

    result = run_mission(
        mission=args.mission,
        project_root=args.project_root,
        project=args.project,
        base_url=args.base_url,
        apply=args.apply,
        dry_run=args.dry_run,
        auto_rollback=args.auto_rollback,
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
