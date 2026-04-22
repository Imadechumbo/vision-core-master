import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class IncidentStore:
    def __init__(self, storage_root: Path):
        self.root = Path(storage_root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.json_file = self.root / "incidents.json"
        self.db_file = self.root / "incidents.db"
        if not self.json_file.exists():
            self.json_file.write_text("[]", encoding="utf-8")
        self._ensure_db()

    def _ensure_db(self):
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id TEXT PRIMARY KEY,
                project TEXT,
                mission_text TEXT,
                intent TEXT,
                root_cause TEXT,
                pass_gold INTEGER,
                created_at TEXT,
                payload_json TEXT
            )
            """)

    def record(self, project, mission, evidence, rca, patch, policy, execution, gates):
        entry = {
            "id": f"incident_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}",
            "project": project,
            "mission": mission,
            "evidence": evidence,
            "rca": rca,
            "patch": patch,
            "policy": policy,
            "execution": execution,
            "gates": gates,
            "pass_gold": gates["pass_gold"],
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        data = json.loads(self.json_file.read_text(encoding="utf-8"))
        data.append(entry)
        self.json_file.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

        with sqlite3.connect(self.db_file) as conn:
            conn.execute(
                "INSERT INTO incidents (id, project, mission_text, intent, root_cause, pass_gold, created_at, payload_json) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    entry["id"], project, mission["text"], mission["intent"], rca["root_cause"], int(gates["pass_gold"]),
                    entry["created_at"], json.dumps(entry, ensure_ascii=False)
                ),
            )
        return entry

    def query(self, project=None, keyword=None):
        sql = "SELECT payload_json FROM incidents WHERE 1=1"
        params = []
        if project:
            sql += " AND project = ?"
            params.append(project)
        if keyword:
            sql += " AND (mission_text LIKE ? OR intent LIKE ? OR root_cause LIKE ?)"
            like = f"%{keyword}%"
            params += [like, like, like]
        sql += " ORDER BY created_at DESC"
        with sqlite3.connect(self.db_file) as conn:
            rows = conn.execute(sql, params).fetchall()
        return [json.loads(row[0]) for row in rows]
