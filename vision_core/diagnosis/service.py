from vision_core.diagnosis.contracts import DiagnosisResult, EvidenceItem


class HermesService:
    def analyze(self, mission_id: str, mission_text: str) -> DiagnosisResult:
        evidence = [EvidenceItem(kind="mission_text", value=mission_text)]

        lowered = mission_text.lower()
        root_cause = "unknown"
        summary = "Hermes could not determine a precise root cause"
        confidence = 0.35

        if "runtime" in lowered:
            root_cause = "runtime_instability"
            summary = "Hermes detected probable runtime instability"
            confidence = 0.82
        elif "backend" in lowered:
            root_cause = "backend_contract_issue"
            summary = "Hermes detected probable backend contract issue"
            confidence = 0.78
        elif "policy" in lowered:
            root_cause = "policy_or_configuration_issue"
            summary = "Hermes detected probable policy/configuration issue"
            confidence = 0.74
        elif "rollback" in lowered:
            root_cause = "rollback_recovery_issue"
            summary = "Hermes detected probable rollback/recovery issue"
            confidence = 0.77

        return DiagnosisResult(
            mission_id=mission_id,
            summary=summary,
            root_cause=root_cause,
            confidence=confidence,
            evidence=evidence,
            metadata={"engine": "HermesService"},
        )
