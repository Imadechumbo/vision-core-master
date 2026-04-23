from __future__ import annotations

from vision_core.integration.contracts import PullRequestValidationResult, ValidationGateStatus


class PRValidationService:
    def validate(self, data: dict) -> PullRequestValidationResult:
        mission_id = data["mission_id"]
        validation = data["validation"]
        security = data["security"]
        receipt = data["execution_receipt"]

        checks = [
            ValidationGateStatus(
                name="pass_gold_required",
                passed=bool(validation.pass_gold),
                detail="Sem PASS GOLD não existe merge nem promoção.",
            ),
            ValidationGateStatus(
                name="promotion_allowed",
                passed=bool(security.promotion_allowed),
                detail="Aegis precisa liberar promoção em produção.",
            ),
            ValidationGateStatus(
                name="execution_has_diffs",
                passed=bool(receipt.applied_files >= 1 and len(receipt.diffs) >= 1),
                detail="PR precisa conter alterações reais e diff visível.",
            ),
            ValidationGateStatus(
                name="validation_not_fail",
                passed=validation.outcome != "FAIL",
                detail="SDDF não pode retornar FAIL.",
            ),
        ]

        merge_allowed = all(item.passed for item in checks)
        status = "approved" if merge_allowed else "blocked"
        summary = "PR validation approved" if merge_allowed else "PR validation blocked"

        return PullRequestValidationResult(
            mission_id=mission_id,
            status=status,
            merge_allowed=merge_allowed,
            checks=checks,
            summary=summary,
            metadata={"engine": "PRValidationService"},
        )
