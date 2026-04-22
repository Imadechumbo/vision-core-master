from __future__ import annotations


def classify_root_cause(evidence: dict) -> dict:
    signals = evidence.get("signals", [])
    if "vision_requested" in signals and not evidence.get("project_root_exists"):
        return {
            "root_cause_class": "missing_project_root_or_invalid_path",
            "confidence": 0.82,
            "recommended_action": "provide_valid_project_root",
        }
    if "vision_requested" in signals:
        return {
            "root_cause_class": "vision_pipeline_needs_validation",
            "confidence": 0.67,
            "recommended_action": "run_vision_contract_and_provider_checks",
        }
    if "zip_requested" in signals and "image_requested" in signals:
        return {
            "root_cause_class": "multimodal_ingest_not_fully_validated",
            "confidence": 0.74,
            "recommended_action": "run_multimodal_gates",
        }
    return {
        "root_cause_class": "general_mission_pending_domain_specific_checks",
        "confidence": 0.41,
        "recommended_action": "inspect_adapter_and_execute_gates",
    }
