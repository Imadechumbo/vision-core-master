from __future__ import annotations
import pathlib
from typing import Any, Dict, List
from vision_core.utils.io import read_json, write_json, ensure_dir
from vision_core.utils.time import utc_now_iso, utc_stamp

def _path(data_dir: str) -> pathlib.Path:
    ensure_dir(data_dir)
    return pathlib.Path(data_dir) / "incidents.json"

def add_incident(data_dir: str, title: str, details: Dict[str, Any]) -> Dict[str, Any]:
    path = _path(data_dir)
    incidents = read_json(path, default=[])
    item = {
        "id": f"inc_{utc_stamp()}",
        "created_at": utc_now_iso(),
        "status": "open",
        "title": title,
        "details": details,
    }
    incidents.append(item)
    write_json(path, incidents)
    return item

def count_open_incidents(data_dir: str) -> int:
    incidents = read_json(_path(data_dir), default=[])
    return sum(1 for x in incidents if x.get("status") == "open")
