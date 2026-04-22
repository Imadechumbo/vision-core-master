from __future__ import annotations

import requests


class OllamaClient:
    def __init__(self, base_url: str = "http://127.0.0.1:11434", timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def health(self) -> dict:
        try:
            r = requests.get(f"{self.base_url}/api/tags", timeout=self.timeout)
            return {"ok": r.ok, "status_code": r.status_code}
        except Exception as exc:
            return {"ok": False, "error": str(exc)}
