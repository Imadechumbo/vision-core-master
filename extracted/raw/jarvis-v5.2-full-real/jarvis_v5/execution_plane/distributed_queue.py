import json
import os
from pathlib import Path

try:
    import redis
except Exception:
    redis = None

from jarvis_v5.execution_plane.local_queue import LocalQueue


class DistributedQueue:
    def __init__(self, root: Path, queue_name: str = "jarvis:v5:missions", redis_url: str | None = None):
        self.root = Path(root)
        self.queue_name = queue_name
        self.redis_url = redis_url or os.getenv("REDIS_URL")
        self.local = LocalQueue(self.root / "local_fallback")
        self._client = None
        if self.redis_url and redis is not None:
            try:
                self._client = redis.Redis.from_url(self.redis_url, decode_responses=True)
                self._client.ping()
            except Exception:
                self._client = None

    @property
    def mode(self) -> str:
        return "redis" if self._client else "local"

    def info(self) -> dict:
        size = 0
        if self._client:
            try:
                size = int(self._client.llen(self.queue_name))
            except Exception:
                size = 0
        else:
            size = len(list((self.local.root).glob("mission_*.json")))
        return {"mode": self.mode, "queue": self.queue_name, "size": size}

    def enqueue(self, payload: dict):
        if self._client:
            self._client.rpush(self.queue_name, json.dumps(payload, ensure_ascii=False))
            return {"mode": "redis", "queue": self.queue_name, "id": payload["id"]}
        path = self.local.enqueue(payload)
        return {"mode": "local", "path": path, "id": payload["id"]}

    def dequeue(self):
        if self._client:
            item = self._client.lpop(self.queue_name)
            return json.loads(item) if item else None
        return self.local.dequeue()
