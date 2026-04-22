from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.mission.schema import Mission
from intelligence.intent.resolver import resolve_intent
from core.mission.normalizer import normalize_mission
from core.orchestration.runner import run_mission


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JARVIS CORE V3 EXECUTÁVEL")
    parser.add_argument("mission", help="Missão em linguagem natural")
    parser.add_argument("--project-id", default="technetgame")
    parser.add_argument("--project-root", default=None)
    parser.add_argument("--json-only", action="store_true")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    intent = resolve_intent(args.mission)
    mission: Mission = normalize_mission(
        raw_mission=args.mission,
        project_id=args.project_id,
        project_root=args.project_root,
        intent=intent,
    )
    result = run_mission(mission)
    if args.json_only:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("JARVIS CORE V3 EXECUTÁVEL")
        print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
