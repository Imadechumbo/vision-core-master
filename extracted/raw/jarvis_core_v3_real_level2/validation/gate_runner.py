from __future__ import annotations

from validation.gates.health_gate import run_health_gate
from validation.gates.vision_contract_gate import run_vision_contract_gate
from validation.gates.vision_provider_gate import run_vision_provider_gate
from validation.gates.zip_ingest_gate import run_zip_ingest_gate


def run_required_gates(mission, adapter, evidence, root_cause):
    gate_map = {
        "health_gate": lambda: run_health_gate(mission, evidence),
        "vision_contract_gate": lambda: run_vision_contract_gate(mission, evidence, root_cause),
        "vision_provider_gate": lambda: run_vision_provider_gate(mission, evidence, root_cause),
        "zip_ingest_gate": lambda: run_zip_ingest_gate(mission, evidence, root_cause),
    }
    results = []
    for gate_name in adapter.get_required_gates():
        results.append(gate_map[gate_name]())
    return results
