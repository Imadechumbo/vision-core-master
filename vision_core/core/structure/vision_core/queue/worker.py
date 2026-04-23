from vision_core.queue.store import QUEUE_FILE
from vision_core.runtime.runner import run_mission
from vision_core.utils import read_json, write_json, utc_now_iso

def worker_run_once():
    data = read_json(QUEUE_FILE, default={"items": []})
    queued = next((x for x in data["items"] if x["status"] == "queued"), None)
    if not queued:
        return {"ok": True, "status": "idle", "message": "queue_empty"}
    queued["status"] = "running"
    queued["started_at"] = utc_now_iso()
    result = run_mission(queued["project_root"], queued["mission"], queued["profile"])
    queued["finished_at"] = utc_now_iso()
    queued["status"] = "done" if result.get("ok") else "failed"
    queued["result"] = result
    write_json(QUEUE_FILE, data)
    return {"ok": True, "status": queued["status"], "job": queued}
