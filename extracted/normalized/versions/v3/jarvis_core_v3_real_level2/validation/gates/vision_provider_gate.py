from __future__ import annotations

import os


def run_vision_provider_gate(mission, evidence, root_cause):
    provider = os.getenv("VISION_PROVIDER") or os.getenv("OPENAI_BASE_URL") or "unset"
    ok = mission.intent != "fix_vision" or provider != "unset"
    return {
        "gate": "vision_provider_gate",
        "status": "PASS" if ok else "FAIL",
        "severity": "high",
        "details": f"Provider detectado: {provider}",
    }
