import re
from jarvis_core.models import Mission
from jarvis_core.intent_resolver import resolve_intent


def normalize_mission(text: str) -> str:
    text = (text or '').strip()
    text = re.sub(r'\s+', ' ', text)
    return text


def parse_mission(raw: str) -> Mission:
    normalized = normalize_mission(raw)
    intent = resolve_intent(normalized)
    return Mission(raw=raw, normalized=normalized, intent=intent)
