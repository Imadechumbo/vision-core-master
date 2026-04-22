from __future__ import annotations


def build_cause_chain(root_cause: dict, evidence: dict) -> list[dict]:
    primary = root_cause.get("root_cause_class", "unknown")
    chain = [{"type": primary, "status": "active"}]
    if not evidence.get("project_root_exists") and evidence.get("project_root"):
        chain.append({"type": "local_scan_blocked", "status": "derived"})
    return chain
