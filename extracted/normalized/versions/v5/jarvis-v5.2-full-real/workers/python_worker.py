from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jarvis_v5.execution_plane.worker_loop import WorkerLoop


if __name__ == "__main__":
    WorkerLoop(ROOT / "storage").run_forever()
