from __future__ import annotations
import difflib
from pathlib import Path
from vision_core.execution.contracts import ExecutionPlan, ExecutionReceipt, FileDiff

class OperatorEngine:
    def apply(self, plan: ExecutionPlan) -> ExecutionReceipt:
        details = []
        diffs = []
        applied_files = 0

        for operation in plan.operations:
            target = Path(operation.target_file)
            target.parent.mkdir(parents=True, exist_ok=True)

            old_content = ""
            if target.exists():
                old_content = target.read_text(encoding="utf-8")

            if operation.op == "append_text":
                new_content = old_content + operation.content
                details.append(f"append_text applied to {target}")
            elif operation.op == "replace_text":
                new_content = operation.content
                details.append(f"replace_text applied to {target}")
            else:
                details.append(f"unknown operation skipped: {operation.op}")
                continue

            diff_text = "".join(
                difflib.unified_diff(
                    old_content.splitlines(keepends=True),
                    new_content.splitlines(keepends=True),
                    fromfile=f"{target}.before",
                    tofile=f"{target}.after",
                )
            )

            target.write_text(new_content, encoding="utf-8")
            diffs.append(FileDiff(target_file=str(target), diff_text=diff_text))
            applied_files += 1

        return ExecutionReceipt(
            mission_id=plan.mission_id,
            status="applied",
            applied_files=applied_files,
            details=details,
            diffs=diffs,
            metadata={"engine": "OperatorEngine"},
        )
