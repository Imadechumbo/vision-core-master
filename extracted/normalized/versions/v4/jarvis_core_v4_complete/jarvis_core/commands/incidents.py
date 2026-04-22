import json
from jarvis_core.incident_store import query_incidents


def query_incidents_command(filter_text: str, limit: int = 20) -> str:
    rows = query_incidents(filter_text=filter_text, limit=limit)
    data = [
        {
            'id': r[0],
            'created_at': r[1],
            'project': r[2],
            'mission': r[3],
            'intent': r[4],
            'pass_gold': bool(r[5]),
            'root_cause': r[6],
            'summary': r[7],
        }
        for r in rows
    ]
    return json.dumps(data, ensure_ascii=False, indent=2)
