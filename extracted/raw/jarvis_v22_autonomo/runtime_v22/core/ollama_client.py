from __future__ import annotations
import requests


class OllamaClient:
    def __init__(self, base_url: str, timeout_seconds: int = 90, timeout: int | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout if timeout is not None else timeout_seconds

    def generate(self, model: str, prompt: str) -> dict:
        url = f"{self.base_url}/api/generate"

        try:
            response = requests.post(
                url,
                json={"model": model, "prompt": prompt, "stream": False},
                timeout=self.timeout_seconds,
            )
        except Exception as exc:
            return {
                "ok": False,
                "provider": "ollama",
                "model": model,
                "response": "",
                "error": f"request_failed: {exc}",
                "raw": None,
            }

        if response.status_code != 200:
            return {
                "ok": False,
                "provider": "ollama",
                "model": model,
                "response": "",
                "error": f"http_{response.status_code}: {response.text}",
                "raw": None,
            }

        try:
            data = response.json()
        except Exception:
            return {
                "ok": False,
                "provider": "ollama",
                "model": model,
                "response": "",
                "error": f"invalid_json: {response.text}",
                "raw": None,
            }

        if not isinstance(data, dict):
            return {
                "ok": False,
                "provider": "ollama",
                "model": model,
                "response": "",
                "error": f"unexpected_payload_type: {type(data).__name__}",
                "raw": data,
            }

        return {
            "ok": True,
            "provider": "ollama",
            "model": model,
            "response": str(data.get("response", "")).strip(),
            "error": None,
            "raw": data,
        }
