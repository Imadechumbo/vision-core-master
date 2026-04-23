from __future__ import annotations

import sqlite3
from pathlib import Path


class SQLiteMemoryStore:
    def __init__(self, root: str):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)
        self.db_path = self.root / "memory.db"
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS mission_memory (
                    mission_id TEXT PRIMARY KEY,
                    mission TEXT NOT NULL,
                    root_cause TEXT NOT NULL,
                    validation_outcome TEXT NOT NULL,
                    pass_gold INTEGER NOT NULL,
                    promotion_allowed INTEGER NOT NULL,
                    snapshot_id TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    recorded_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def record(self, item: dict) -> dict:
        payload = {
            "mission_id": item["mission_id"],
            "mission": item["mission"],
            "root_cause": item["root_cause"],
            "validation_outcome": item["validation_outcome"],
            "pass_gold": 1 if item["pass_gold"] else 0,
            "promotion_allowed": 1 if item["promotion_allowed"] else 0,
            "snapshot_id": item["snapshot_id"],
            "decision": item["decision"],
        }
        with self._connect() as conn:
            conn.execute(
                """
                INSERT OR REPLACE INTO mission_memory (
                    mission_id, mission, root_cause, validation_outcome,
                    pass_gold, promotion_allowed, snapshot_id, decision
                ) VALUES (
                    :mission_id, :mission, :root_cause, :validation_outcome,
                    :pass_gold, :promotion_allowed, :snapshot_id, :decision
                )
                """,
                payload,
            )
        return self.get_by_mission_id(payload["mission_id"])

    def list_all(self) -> list[dict]:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """
                SELECT mission_id, mission, root_cause, validation_outcome,
                       pass_gold, promotion_allowed, snapshot_id, decision, recorded_at
                FROM mission_memory
                ORDER BY recorded_at DESC, mission_id DESC
                """
            ).fetchall()
        return [self._row_to_dict(row) for row in rows]

    def get_by_mission_id(self, mission_id: str) -> dict | None:
        with self._connect() as conn:
            conn.row_factory = sqlite3.Row
            row = conn.execute(
                """
                SELECT mission_id, mission, root_cause, validation_outcome,
                       pass_gold, promotion_allowed, snapshot_id, decision, recorded_at
                FROM mission_memory
                WHERE mission_id = ?
                """,
                (mission_id,),
            ).fetchone()
        return self._row_to_dict(row) if row else None

    @staticmethod
    def _row_to_dict(row: sqlite3.Row) -> dict:
        return {
            "mission_id": row["mission_id"],
            "mission": row["mission"],
            "root_cause": row["root_cause"],
            "validation_outcome": row["validation_outcome"],
            "pass_gold": bool(row["pass_gold"]),
            "promotion_allowed": bool(row["promotion_allowed"]),
            "snapshot_id": row["snapshot_id"],
            "decision": row["decision"],
            "recorded_at": row["recorded_at"],
        }
