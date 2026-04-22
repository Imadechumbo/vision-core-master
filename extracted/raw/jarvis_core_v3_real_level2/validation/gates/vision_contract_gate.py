from __future__ import annotations


def run_vision_contract_gate(mission, evidence, root_cause):
    wants_vision = "vision_requested" in evidence.get("signals", [])
    has_local = evidence.get("project_root_exists", False)
    status = "PASS" if (not wants_vision or has_local) else "FAIL"
    return {
        "gate": "vision_contract_gate",
        "status": status,
        "severity": "high",
        "details": "Valida se há base mínima para analisar contrato vision.",
    }
