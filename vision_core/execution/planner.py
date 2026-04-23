from pathlib import Path
from vision_core.diagnosis.contracts import DiagnosisResult
from vision_core.execution.contracts import ExecutionPlan, FileOperation


class PatchPlanner:
    def build_plan(self, mission_id: str, diagnosis: DiagnosisResult, workspace_root: str) -> ExecutionPlan:
        workspace = Path(workspace_root)
        workspace.mkdir(parents=True, exist_ok=True)

        mission_file = workspace / "mission_output.txt"
        incident_file = workspace / "incident_summary.txt"

        operations = [
            FileOperation(
                target_file=str(mission_file),
                op="append_text",
                content=(
                    f"mission_id={mission_id}\n"
                    f"root_cause={diagnosis.root_cause}\n"
                    f"summary={diagnosis.summary}\n"
                ),
            ),
            FileOperation(
                target_file=str(incident_file),
                op="replace_text",
                content=(
                    f"incident={mission_id}\n"
                    f"confidence={diagnosis.confidence}\n"
                    f"root_cause={diagnosis.root_cause}\n"
                ),
            ),
        ]

        return ExecutionPlan(
            mission_id=mission_id,
            operations=operations,
            metadata={"engine": "PatchPlanner"},
        )
