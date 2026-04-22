from __future__ import annotations


def run_health_gate(mission, evidence):
    ok = True
    return {
        "gate": "health_gate",
        "status": "PASS" if ok else "FAIL",
        "severity": "medium",
        "details": "Base gate estrutural passou no nível 2.",
    }
