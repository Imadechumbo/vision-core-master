from vision_core.diagnosis.contracts import DiagnosisResult
from vision_core.execution.apply import ExecutionApplier
from vision_core.execution.contracts import ExecutionPlan, ExecutionReceipt
from vision_core.execution.planner import ExecutionPlanner


class ExecutionService:
    def __init__(self) -> None:
        self.planner = ExecutionPlanner()
        self.applier = ExecutionApplier()

    def prepare(self, mission_id: str, mission_text: str, diagnosis: DiagnosisResult, project_root: str | None = None) -> ExecutionPlan:
        return self.planner.build_plan(mission_id, mission_text, diagnosis, project_root)

    def execute(self, plan: ExecutionPlan, snapshot_id: str, project_root: str | None = None) -> ExecutionReceipt:
        return self.applier.apply(plan, snapshot_id, project_root)
