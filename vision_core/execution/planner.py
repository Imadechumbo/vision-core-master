from pathlib import Path
from vision_core.diagnosis.contracts import DiagnosisResult
from vision_core.execution.contracts import ExecutionPlan


class PatchPlanner:
    def build_plan(self, mission_id: str, diagnosis: DiagnosisResult, workspace_root: str) -> ExecutionPlan:
        workspace = Path(workspace_root)
        workspace.mkdir(parents=True, exist_ok=True)
        target = workspace / "mission_output.txt"

        operations = [
            {
                "op": "append_text",
                "text": (
                    f"mission_id={mission_id}\n"
                    f"root_cause={diagnosis.root_cause}\n"
                    f"summary={diagnosis.summary}\n"
                ),
            }
        ]

        return ExecutionPlan(
            mission_id=mission_id,
            target_file=str(target),
            operations=operations,
            metadata={"engine": "PatchPlanner"},
        )
