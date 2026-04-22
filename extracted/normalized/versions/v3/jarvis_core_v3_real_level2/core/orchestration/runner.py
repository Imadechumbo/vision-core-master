from __future__ import annotations

from core.mission.schema import Mission
from adapters.projects.loader import load_project_adapter
from diagnostics.evidence.collector import collect_evidence
from diagnostics.classifier.root_cause_classifier import classify_root_cause
from diagnostics.cause_chain.engine import build_cause_chain
from security.aegis.policy import evaluate_policy
from validation.gate_runner import run_required_gates


def run_mission(mission: Mission) -> dict:
    adapter = load_project_adapter(mission.project_id)
    evidence = collect_evidence(mission, adapter)
    root_cause = classify_root_cause(evidence)
    cause_chain = build_cause_chain(root_cause, evidence)
    policy = evaluate_policy(mission, root_cause)
    gates = run_required_gates(mission, adapter, evidence, root_cause)
    gold_pass = all(g["status"] == "PASS" for g in gates)
    return {
        "system": "jarvis-core-v3-real-level2",
        "mission": mission.to_dict(),
        "adapter": adapter.describe(),
        "evidence": evidence,
        "root_cause": root_cause,
        "cause_chain": cause_chain,
        "policy": policy,
        "gates": gates,
        "gold": "PASS" if gold_pass else "BLOCK",
        "summary": _summarize(mission.intent, root_cause, gold_pass),
    }


def _summarize(intent: str, root_cause: dict, gold_pass: bool) -> str:
    status = "PASS GOLD" if gold_pass else "PASS GOLD bloqueado"
    return f"Intent={intent}; causa principal={root_cause.get('root_cause_class', 'unknown')}; {status}."
