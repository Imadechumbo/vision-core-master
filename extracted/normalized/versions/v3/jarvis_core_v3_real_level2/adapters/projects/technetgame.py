from __future__ import annotations

from adapters.projects.base import BaseProjectAdapter


class TechNetGameAdapter(BaseProjectAdapter):
    def __init__(self) -> None:
        super().__init__(project_id="technetgame")

    def detect_stack(self) -> dict:
        return {
            "backend": "node-express",
            "frontend": "static-html-js",
            "infra": ["cloudflare-pages", "aws-eb", "railway"],
        }

    def get_required_gates(self) -> list[str]:
        return [
            "health_gate",
            "vision_contract_gate",
            "vision_provider_gate",
            "zip_ingest_gate",
        ]
