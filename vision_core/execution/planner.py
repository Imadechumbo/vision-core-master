from pathlib import Path
from vision_core.diagnosis.contracts import DiagnosisResult
from vision_core.execution.contracts import ExecutionPlan, FileOperation

class PatchPlanner:
    def build_plan(self, mission_id: str, diagnosis: DiagnosisResult, workspace_root: str, feedback: list[dict] | None = None) -> ExecutionPlan:
        workspace = Path(workspace_root)
        workspace.mkdir(parents=True, exist_ok=True)

        mission_file = workspace / "mission_output.txt"
        incident_file = workspace / "incident_summary.txt"
        adaptive_file = workspace / "adaptive_notes.txt"

        operations = [
            FileOperation(
                target_file=str(mission_file),
                op="append_text",
                content=(
                    f"mission_id={mission_id}\n"
                    f"root_cause={diagnosis.root_cause}\n"
                    f"summary={diagnosis.summary}\n"
                    f"strategy={diagnosis.strategy}\n"
                ),
            ),
            FileOperation(
                target_file=str(incident_file),
                op="replace_text",
                content=(
                    f"incident={mission_id}\n"
                    f"confidence={diagnosis.confidence}\n"
                    f"root_cause={diagnosis.root_cause}\n"
                    f"source={diagnosis.source}\n"
                ),
            ),
        ]

        if feedback:
            avg_score = sum(item["score"] for item in feedback) / len(feedback)
            operations.append(
                FileOperation(
                    target_file=str(adaptive_file),
                    op="replace_text",
                    content=(
                        f"adaptive_context_for={diagnosis.root_cause}\n"
                        f"feedback_count={len(feedback)}\n"
                        f"avg_score={avg_score:.2f}\n"
                        f"preferred_strategy={diagnosis.strategy}\n"
                    ),
                )
            )

        return ExecutionPlan(
            mission_id=mission_id,
            operations=operations,
            metadata={"engine": "PatchPlanner", "feedback_used": bool(feedback)},
        )
