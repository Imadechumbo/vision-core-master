from __future__ import annotations
import time
from typing import Any, Dict
from vision_core.queue.worker import run_once

def scheduler_loop(data_dir: str, tick_seconds: int = 10) -> None:
    while True:
        run_once(data_dir)
        time.sleep(tick_seconds)
