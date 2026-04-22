import os
from jarvis_core.utils import safe_read_text


def collect_evidence(project_root: str, scan_result: dict, mission_text: str):
    evidence = []
    for rel in scan_result.get('route_candidates', [])[:20]:
        full = os.path.join(project_root, rel)
        try:
            text = safe_read_text(full)
        except Exception:
            continue
        lower = text.lower()
        if 'vision' in mission_text.lower() and 'vision' in lower:
            evidence.append({'type': 'route_candidate', 'file': rel, 'snippet': text[:800]})
        elif 'cors' in mission_text.lower() and 'cors' in lower:
            evidence.append({'type': 'route_candidate', 'file': rel, 'snippet': text[:800]})
    return evidence[:10]
