from pathlib import Path
from vision_core.execution.contracts import ExecutionPlan, ExecutionReceipt


class OperatorEngine:
    def apply(self, plan: ExecutionPlan) -> ExecutionReceipt:
        target = Path(plan.target_file)
        target.parent.mkdir(parents=True, exist_ok=True)

        details: list[str] = []
        applied = 0
        changed = False

        content = ""
        if target.exists():
            content = target.read_text(encoding="utf-8")

        for operation in plan.operations:
            op = operation.get("op")
            if op == "append_text":
                text = operation.get("text", "")
                content += text
                applied += 1
                changed = True
                details.append("append_text applied")
            else:
                details.append(f"unknown operation skipped: {op}")

        target.write_text(content, encoding="utf-8")

        return ExecutionReceipt(
            mission_id=plan.mission_id,
            target_file=str(target),
            status="applied",
            changed=changed,
            applied_operations=applied,
            details=details,
            metadata={"engine": "OperatorEngine"},
        )
