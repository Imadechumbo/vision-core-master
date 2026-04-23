from vision_core.validation.contracts import ValidationResult
from vision_core.security.contracts import SecurityDecision


class AegisService:
    def enforce(self, mission_id: str, validation: ValidationResult, environment: str = "production") -> SecurityDecision:
        requires_gold = environment == "production"
        reasons: list[str] = []

        allowed = validation.outcome != "FAIL"
        if not allowed:
            reasons.append("Validation outcome is FAIL")

        if requires_gold:
            promotion_allowed = validation.pass_gold
            if not validation.pass_gold:
                reasons.append("Sem PASS GOLD nada é promovido")
        else:
            promotion_allowed = validation.outcome in {"PASS", "GOLD"}

        return SecurityDecision(
            mission_id=mission_id,
            allowed=allowed,
            requires_gold=requires_gold,
            promotion_allowed=promotion_allowed,
            reasons=reasons,
            metadata={"engine": "AegisService", "environment": environment},
        )
