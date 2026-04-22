import os
import sqlite3
from jarvis_core.config import INCIDENT_DB_PATH, INCIDENT_JSON_DIR
from jarvis_core.utils import utc_now_iso, slugify, write_json

CREATE_SQL = """
CREATE TABLE IF NOT EXISTS incidents (
    id TEXT PRIMARY KEY,
    created_at TEXT NOT NULL,
    project TEXT NOT NULL,
    mission TEXT NOT NULL,
    intent TEXT NOT NULL,
    pass_gold INTEGER NOT NULL,
    root_cause TEXT NOT NULL,
    summary TEXT NOT NULL,
    patch_dir TEXT,
    stable_snapshot TEXT
)
"""


def _db():
    conn = sqlite3.connect(INCIDENT_DB_PATH)
    conn.execute(CREATE_SQL)
    return conn


def save_incident(payload: dict) -> dict:
    incident_id = slugify(f"{payload['project']}-{payload['intent']}-{utc_now_iso()}")
    created_at = utc_now_iso()
    payload = {**payload, 'id': incident_id, 'created_at': created_at}

    json_path = os.path.join(INCIDENT_JSON_DIR, f"{incident_id}.json")
    write_json(json_path, payload)

    conn = _db()
    conn.execute(
        'INSERT INTO incidents (id, created_at, project, mission, intent, pass_gold, root_cause, summary, patch_dir, stable_snapshot) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (
            payload['id'], payload['created_at'], payload['project'], payload['mission'], payload['intent'],
            1 if payload['pass_gold'] else 0, payload['root_cause'], payload['summary'], payload.get('patch_dir', ''), payload.get('stable_snapshot', '')
        )
    )
    conn.commit()
    conn.close()
    return {'incident_id': incident_id, 'json_path': json_path}


def query_incidents(filter_text: str = '', limit: int = 20):
    conn = _db()
    if filter_text:
        q = f"%{filter_text}%"
        rows = conn.execute(
            '''
            SELECT id, created_at, project, mission, intent, pass_gold, root_cause, summary
            FROM incidents
            WHERE mission LIKE ? OR intent LIKE ? OR root_cause LIKE ? OR summary LIKE ?
            ORDER BY created_at DESC
            LIMIT ?
            ''',
            (q, q, q, q, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            '''
            SELECT id, created_at, project, mission, intent, pass_gold, root_cause, summary
            FROM incidents
            ORDER BY created_at DESC
            LIMIT ?
            ''',
            (limit,),
        ).fetchall()
    conn.close()
    return rows
