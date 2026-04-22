from __future__ import annotations


def run_zip_ingest_gate(mission, evidence, root_cause):
    wants_zip = "zip_requested" in evidence.get("signals", [])
    ok = not wants_zip or evidence.get("project_root_exists", False)
    return {
        "gate": "zip_ingest_gate",
        "status": "PASS" if ok else "FAIL",
        "severity": "high",
        "details": "ZIP ingest requer base local válida neste nível.",
    }
