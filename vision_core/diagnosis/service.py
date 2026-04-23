from vision_core.diagnosis.contracts import DiagnosisResult, EvidenceItem
from vision_core.diagnosis.llm import HermesLLMAdapter

class HermesService:
    def __init__(self) -> None:
        self.llm = HermesLLMAdapter()

    def analyze(self, mission_id: str, mission_text: str) -> DiagnosisResult:
        evidence = [EvidenceItem(kind="mission_text", value=mission_text)]

        if self.llm.is_configured():
            llm_result = self.llm.analyze(mission_text)
            return DiagnosisResult(
                mission_id=mission_id,
                summary=llm_result.summary,
                root_cause=llm_result.root_cause,
                confidence=llm_result.confidence,
                strategy=llm_result.strategy,
                source=llm_result.source,
                evidence=evidence,
                metadata={"engine": "HermesService", "mode": "llm"},
            )

        lowered = mission_text.lower()
        root_cause = "unknown"
        summary = "Hermes heuristic mode could not determine a precise root cause"
        confidence = 0.35
        strategy = "inspect_then_patch"

        if "runtime" in lowered:
            root_cause = "runtime_instability"
            summary = "Hermes heuristic mode detected probable runtime instability"
            confidence = 0.82
            strategy = "stabilize_runtime_then_validate"
        elif "backend" in lowered:
            root_cause = "backend_contract_issue"
            summary = "Hermes heuristic mode detected probable backend contract issue"
            confidence = 0.78
            strategy = "contract_fix_then_regression_test"
        elif "policy" in lowered:
            root_cause = "policy_or_configuration_issue"
            summary = "Hermes heuristic mode detected probable policy/configuration issue"
            confidence = 0.74
            strategy = "policy_adjustment_then_validate"
        elif "rollback" in lowered:
            root_cause = "rollback_recovery_issue"
            summary = "Hermes heuristic mode detected probable rollback/recovery issue"
            confidence = 0.77
            strategy = "restore_then_verify"

        return DiagnosisResult(
            mission_id=mission_id,
            summary=summary,
            root_cause=root_cause,
            confidence=confidence,
            strategy=strategy,
            source="heuristic",
            evidence=evidence,
            metadata={"engine": "HermesService", "mode": "heuristic"},
        )
