from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.config_loader import load_yaml
from core.mission_controller import MissionController


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="JARVIS CORE OMEGA HYBRID V2.2 AUTÔNOMO")
    parser.add_argument("mission", help="Missão em linguagem natural")
    parser.add_argument("--project-root", help="Caminho do projeto alvo", default=None)
    parser.add_argument("--json-only", action="store_true", help="Saída JSON")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    routing = load_yaml("routing.yaml")
    models = load_yaml("models.yaml")
    controller = MissionController(routing, models)
    result = controller.run(args.mission, project_root=args.project_root)

    payload = {
        "mission": result.mission,
        "intent": result.intent,
        "used_cache": result.used_cache,
        "route": result.route,
        "runtime": result.runtime,
        "project": result.project,
        "model_used": result.model_used,
        "answer": result.answer,
        "version": "v2.2-autonomo",
    }

    if args.json_only:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"[JARVIS] Missão: {result.intent}")
    print(f"[JARVIS] Cache: {'hit' if result.used_cache else 'miss'}")
    print(f"[JARVIS] Runtime Docker: {result.runtime.get('docker_status')}")
    print(f"[JARVIS] Modelo usado: {result.model_used}")
    if args.project_root:
        print(f"[JARVIS] Projeto: {args.project_root}")
    print("\n[RESPOSTA]\n")
    print(result.answer)
    print("\n[JSON resumido]\n")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
