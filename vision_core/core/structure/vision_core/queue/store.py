from pathlib import Path
from vision_core.utils import utc_now_iso, utc_stamp, ensure_dir, read_json, write_json

QUEUE_FILE = Path(".vision_core_runtime") / "queue.json"

def enqueue_mission(project_root, mission, profile="auto"):
    ensure_dir(QUEUE_FILE.parent)
    data = read_json(QUEUE_FILE, default={"items": []})
    item = {
        "id": f"job_{utc_stamp()}",
        "project_root": project_root,
        "mission": mission,
        "profile": profile,
        "created_at": utc_now_iso(),
        "status": "queued",
    }
    data["items"].append(item)
    write_json(QUEUE_FILE, data)
    return {"ok": True, "enqueued": item, "queue_file": str(QUEUE_FILE)}
