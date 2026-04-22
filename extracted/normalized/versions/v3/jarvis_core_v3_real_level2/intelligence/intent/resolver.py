from __future__ import annotations


def resolve_intent(raw: str) -> str:
    text = raw.lower()
    if "vision" in text:
        return "fix_vision"
    if "zip" in text and "print" in text:
        return "enable_multimodal_ingest"
    if "runtime" in text:
        return "diagnose_runtime"
    if "deploy" in text:
        return "safe_deploy"
    return "general_technical_mission"
