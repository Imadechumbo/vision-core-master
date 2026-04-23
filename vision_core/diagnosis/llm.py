import os
from dataclasses import dataclass

@dataclass(slots=True)
class HermesLLMResponse:
    summary: str
    root_cause: str
    confidence: float
    strategy: str
    source: str = "llm"

class HermesLLMAdapter:
    def __init__(self) -> None:
        self.provider = os.getenv("HERMES_LLM_PROVIDER", "").strip()
        self.model = os.getenv("HERMES_LLM_MODEL", "").strip()
        self.api_key = os.getenv("HERMES_LLM_API_KEY", "").strip()

    def is_configured(self) -> bool:
        return bool(self.provider and self.model and self.api_key)

    def analyze(self, mission_text: str) -> HermesLLMResponse:
        # Placeholder determinístico para integração futura real.
        lowered = mission_text.lower()
        if "runtime" in lowered:
            return HermesLLMResponse(
                summary="LLM inferred runtime instability with adaptive remediation recommendation",
                root_cause="runtime_instability",
                confidence=0.90,
                strategy="stabilize_runtime_then_validate",
            )
        if "backend" in lowered:
            return HermesLLMResponse(
                summary="LLM inferred backend contract issue and safer incremental patch strategy",
                root_cause="backend_contract_issue",
                confidence=0.86,
                strategy="contract_fix_then_regression_test",
            )
        return HermesLLMResponse(
            summary="LLM returned a generic technical assessment",
            root_cause="unknown",
            confidence=0.60,
            strategy="inspect_then_patch",
        )
