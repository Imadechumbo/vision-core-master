from vision_core.execution.contracts import ExecutionPlan
from vision_core.rollback.contracts import RestoreResult, SnapshotRecord
from vision_core.rollback.restore import RestoreManager
from vision_core.rollback.snapshot import SnapshotManager


class VaultService:
    def __init__(self) -> None:
        self.snapshot_manager = SnapshotManager()
        self.restore_manager = RestoreManager()

    def snapshot(self, mission_id: str, plan: ExecutionPlan, project_root: str | None = None) -> SnapshotRecord:
        return self.snapshot_manager.create(mission_id, plan, project_root)

    def rollback(self, snapshot: SnapshotRecord, project_root: str | None = None) -> RestoreResult:
        return self.restore_manager.restore(snapshot, project_root)
