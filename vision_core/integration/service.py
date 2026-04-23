from __future__ import annotations

from typing import Any

from vision_core.execution.contracts import ExecutionReceipt
from vision_core.security.contracts import SecurityDecision
from vision_core.validation.contracts import ValidationResult


class IntegrationService:
    def evaluate_pr(
        self,
        validation: ValidationResult,
        security: SecurityDecision,
        execution_receipt: ExecutionReceipt,
        integration_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        context = integration_context or {}

        execution_has_diffs = (
            execution_receipt.applied_files >= 1
            and len(execution_receipt.diffs) > 0
        )

        validation_not_fail = validation.outcome != "FAIL"
        promotion_allowed = bool(security.promotion_allowed)
        pass_gold_required = True

        merge_allowed = (
            pass_gold_required
            and validation.pass_gold
            and promotion_allowed
            and execution_has_diffs
            and validation_not_fail
        )

        return {
            "provider": context.get("provider", "github"),
            "repository": context.get("repository"),
            "branch": context.get("branch"),
            "pr_number": context.get("pr_number"),
            "pass_gold_required": pass_gold_required,
            "promotion_allowed": promotion_allowed,
            "execution_has_diffs": execution_has_diffs,
            "validation_not_fail": validation_not_fail,
            "merge_allowed": merge_allowed,
            "status": "merge_ready" if merge_allowed else "blocked",
        }
