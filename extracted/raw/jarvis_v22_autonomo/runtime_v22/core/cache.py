from __future__ import annotations
import hashlib
import json
import sqlite3
import time
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "cache_data" / "jarvis_cache.sqlite3"
DB_PATH.parent.mkdir(parents=True, exist_ok=True)


class CacheStore:
    def __init__(self) -> None:
        self.conn = sqlite3.connect(DB_PATH)
        self._init_db()

    def _init_db(self) -> None:
        self.conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cache_entries (
                key TEXT PRIMARY KEY,
                namespace TEXT NOT NULL,
                value TEXT NOT NULL,
                created_at REAL NOT NULL
            )
            """
        )
        self.conn.commit()

    @staticmethod
    def make_key(namespace: str, payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(f"{namespace}:{raw}".encode("utf-8")).hexdigest()

    def get(self, namespace: str, payload: dict) -> dict | None:
        key = self.make_key(namespace, payload)
        row = self.conn.execute(
            "SELECT value FROM cache_entries WHERE key = ?", (key,)
        ).fetchone()
        if not row:
            return None
        return json.loads(row[0])

    def set(self, namespace: str, payload: dict, value: dict) -> None:
        key = self.make_key(namespace, payload)
        self.conn.execute(
            "REPLACE INTO cache_entries (key, namespace, value, created_at) VALUES (?, ?, ?, ?)",
            (key, namespace, json.dumps(value, ensure_ascii=False), time.time()),
        )
        self.conn.commit()
