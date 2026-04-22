import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

class StrategyStore:
    def __init__(self, storage_root: Path):
        self.root = Path(storage_root)
        self.db_file = self.root / "strategies.db"
        self._ensure_db()

    def _ensure_db(self):
        self.root.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.db_file) as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS strategies (
                project TEXT,
                strategy_key TEXT,
                score REAL,
                successes INTEGER,
                failures INTEGER,
                updated_at TEXT,
                metadata_json TEXT,
                PRIMARY KEY (project, strategy_key)
            )
            """)

    def update_score(self, project: str, strategy_key: str, success: bool, metadata: dict):
        with sqlite3.connect(self.db_file) as conn:
            row = conn.execute(
                "SELECT score, successes, failures FROM strategies WHERE project = ? AND strategy_key = ?",
                (project, strategy_key),
            ).fetchone()
            if row:
                score, successes, failures = row
            else:
                score, successes, failures = 0.0, 0, 0
            if success:
                score += 10.0
                successes += 1
            else:
                score -= 3.0
                failures += 1
            conn.execute(
                "REPLACE INTO strategies (project, strategy_key, score, successes, failures, updated_at, metadata_json) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (
                    project, strategy_key, score, successes, failures,
                    datetime.now(timezone.utc).isoformat(), json.dumps(metadata, ensure_ascii=False),
                ),
            )

    def list_ranked(self, project=None):
        sql = "SELECT project, strategy_key, score, successes, failures, updated_at, metadata_json FROM strategies"
        params = []
        if project:
            sql += " WHERE project = ?"
            params.append(project)
        sql += " ORDER BY score DESC, successes DESC, failures ASC"
        with sqlite3.connect(self.db_file) as conn:
            rows = conn.execute(sql, params).fetchall()
        result = []
        for row in rows:
            result.append({
                "project": row[0],
                "strategy_key": row[1],
                "score": row[2],
                "successes": row[3],
                "failures": row[4],
                "updated_at": row[5],
                "metadata": json.loads(row[6]) if row[6] else {},
            })
        return result
