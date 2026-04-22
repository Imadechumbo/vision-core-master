from __future__ import annotations
import json
from urllib import request, error
from typing import Any

def _call(url: str, method: str = "GET", payload: dict | None = None, timeout: int = 8) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = request.Request(url, data=data, headers=headers, method=method.upper())
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            return {"ok": 200 <= resp.status < 400, "status": resp.status, "body": body[:500]}
    except error.HTTPError as e:
        try:
            body = e.read().decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return {"ok": False, "status": e.code, "body": body[:500]}
    except Exception as e:
        return {"ok": False, "status": 0, "error": str(e)}

def run_http_checks(base_url: str | None, endpoints: list[dict[str, Any]]) -> list[dict]:
    if not base_url:
        return []
    base_url = base_url.rstrip("/")
    results = []
    for ep in endpoints:
        url = f"{base_url}{ep['path']}"
        result = _call(url, ep.get("method", "GET"), ep.get("json"))
        results.append({
            "name": ep.get("name", ep["path"]),
            "method": ep.get("method", "GET"),
            "path": ep["path"],
            **result
        })
    return results
