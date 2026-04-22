import time
from pathlib import Path

from jarvis_v5.execution_plane.distributed_queue import DistributedQueue
from jarvis_v5.execution_plane.executor import MissionExecutor
from jarvis_v5.control_plane.registry import ProjectRegistry
from jarvis_v5.memory_plane.incident_store import IncidentStore
from jarvis_v5.memory_plane.strategy_store import StrategyStore
from jarvis_v5.memory_plane.stable_vault import StableVault


class WorkerLoop:
    def __init__(self, storage_root: Path):
        storage_root = Path(storage_root)
        self.queue = DistributedQueue(storage_root / "queue")
        self.executor = MissionExecutor(
            storage_root=storage_root,
            registry=ProjectRegistry(storage_root / "projects"),
            incident_store=IncidentStore(storage_root),
            strategy_store=StrategyStore(storage_root),
            stable_vault=StableVault(storage_root),
        )

    def run_forever(self, interval: float = 1.0):
        while True:
            job = self.queue.dequeue()
            if job:
                self.executor.execute(job)
            else:
                time.sleep(interval)
