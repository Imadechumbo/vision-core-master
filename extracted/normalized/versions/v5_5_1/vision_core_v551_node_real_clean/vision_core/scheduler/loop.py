from vision_core.utils import utc_now_iso

def scheduler_loop(tick_seconds=10):
    return {
        "ok": True,
        "started_at": utc_now_iso(),
        "mode": "single_response_stub",
        "tick_seconds": tick_seconds,
        "note": "Loop contínuo não é mantido neste ambiente; use worker-run-once em conjunto com queue-enqueue.",
    }
