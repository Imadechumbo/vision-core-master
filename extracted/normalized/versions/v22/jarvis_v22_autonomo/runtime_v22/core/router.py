from __future__ import annotations
from dataclasses import dataclass


@dataclass
class MissionRoute:
    intent: str
    model_key: str
    mode: str
    fallback: str


class MissionRouter:
    def __init__(self, routing_config: dict) -> None:
        self.routing = routing_config.get("routes", {})

    def detect_intent(self, mission_text: str) -> str:
        text = mission_text.lower()
        if "print e zip" in text or "vision e zip" in text or "leitura de print e zip" in text:
            return "vision_and_zip_working"
        if "runtime" in text or "docker" in text or "ollama" in text:
            return "diagnose_runtime"
        if "vision" in text:
            return "fix_vision"
        if any(term in text for term in ["explica", "explain", "erro", "diagnostic", "diagnosticar"]):
            return "explain"
        return "default"

    def resolve(self, mission_text: str) -> MissionRoute:
        intent = self.detect_intent(mission_text)
        config = self.routing.get(intent, self.routing.get("default", {}))
        return MissionRoute(
            intent=intent,
            model_key=config.get("model", "small-router"),
            mode=config.get("mode", "local"),
            fallback=config.get("fallback", "none"),
        )
