from __future__ import annotations
import pathlib, time
from typing import Any, Dict, List
from vision_core.utils.io import read_json, write_json, ensure_dir
from vision_core.runtime.pipeline import run_pipeline
from vision_core.utils.time import utc_now_iso, utc_stamp

def _queue_path(data_dir: str) -> pathlib.Path:
    ensure_dir(data_dir)
    return pathlib.Path(data_dir) / "queue.json"

def enqueue(data_dir: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    path = _queue_path(data_dir)
    queue = read_json(path, default=[])
    item = {
        "id": f"job_{utc_stamp()}",
        "created_at": utc_now_iso(),
        "status": "queued",
        "retries": 0,
        **payload,
    }
    queue.append(item)
    write_json(path, queue)
    return item

def run_once(data_dir: str) -> Dict[str, Any]:
    path = _queue_path(data_dir)
    queue = read_json(path, default=[])
    for item in queue:
        if item.get("status") == "queued":
            try:
                result = run_pipeline(item["project_root"], item["mission"], data_dir, item.get("profile", "python-service"))
                item["status"] = "done"
                item["result"] = result
                item["finished_at"] = utc_now_iso()
                write_json(path, queue)
                return {"ok": True, "job_id": item["id"], "status": "done"}
            except Exception as exc:
                item["retries"] = item.get("retries", 0) + 1
                item["status"] = "queued" if item["retries"] < 3 else "failed"
                item["last_error"] = str(exc)
                write_json(path, queue)
                return {"ok": False, "job_id": item["id"], "status": item["status"], "error": str(exc)}
    return {"ok": True, "status": "idle"}
