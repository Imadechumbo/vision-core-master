from pathlib import Path
from jarvis_v5.execution_plane.distributed_queue import DistributedQueue
from jarvis_v5.execution_plane.executor import MissionExecutor


class ExecutionController:
    def __init__(self, storage_root: Path, registry, incident_store, strategy_store, stable_vault):
        self.queue = DistributedQueue(storage_root / "queue")
        self.executor = MissionExecutor(storage_root, registry, incident_store, strategy_store, stable_vault)

    def run_mission(self, mission: dict):
        enqueue_info = self.queue.enqueue(mission)
        job = self.queue.dequeue()
        result = self.executor.execute(job)
        result["queue"] = {**enqueue_info, **self.queue.info()}
        return result
