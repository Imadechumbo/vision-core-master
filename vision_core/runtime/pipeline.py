from __future__ import annotations
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from vision_core.diagnosis.service import HermesService
from vision_core.execution.apply import OperatorEngine
from vision_core.execution.planner import PatchPlanner
from vision_core.memory.store import SQLiteMemoryStore
from vision_core.integration.diff_service import DiffService
from vision_core.integration.service import IntegrationOrchestrator
from vision_core.rollback.restore import RestoreManager
from vision_core.rollback.snapshot import SnapshotManager
from vision_core.security.service import AegisService
from vision_core.validation.service import SDDFService

class PipelineResult:
    def __init__(self):
        self.steps = []
        self.status = "UNKNOWN"
        self.data = {}

    def log(self, step, info):
        self.steps.append({"step": step, "info": info, "time": datetime.now(timezone.utc).isoformat()})

class VisionPipeline:
    def __init__(self, project_root: str | None = None):
        self.result = PipelineResult()
        self.project_root = Path(project_root or ".vision_core_runtime")
        self.workspace_root = self.project_root / "workspace"
        self.vault_root = self.project_root / "vault" / "snapshots"
        self.memory_root = self.project_root / "memory"

        self.workspace_root.mkdir(parents=True, exist_ok=True)
        self.vault_root.mkdir(parents=True, exist_ok=True)
        self.memory_root.mkdir(parents=True, exist_ok=True)

        self.hermes = HermesService()
        self.sddf = SDDFService()
        self.aegis = AegisService()
        self.planner = PatchPlanner()
        self.operator = OperatorEngine()
        self.snapshot_manager = SnapshotManager(str(self.vault_root))
        self.restore_manager = RestoreManager(str(self.vault_root))
        self.memory = SQLiteMemoryStore(str(self.memory_root))
        self.diff_service = DiffService()
        self.integration = IntegrationOrchestrator(runtime_root=self.project_root, repository_root=self.project_root)

    def run(self, mission: str, environment: str = "production"):
        mission_id = f"mission-{uuid4().hex[:12]}"
        self.result.data["mission_id"] = mission_id
        self.result.data["mission_text"] = mission

        self.result.log("mission", mission)
        data = self.orchestration(mission_id, mission)
        diagnosis = self.diagnosis(data)
        data["diagnosis"] = diagnosis

        feedback = self.memory.get_feedback_for_root_cause(diagnosis.root_cause)
        data["feedback"] = feedback
        self.result.log("feedback", f"loaded {len(feedback)} feedback records")

        plan = self.planning(data)
        data["plan"] = plan

        snapshot_id = self.snapshot(data)
        data["snapshot_id"] = snapshot_id

        receipt = self.execution(data)
        data["execution_receipt"] = receipt

        validation = self.validation(data)
        data["validation"] = validation

        security = self.security(data, environment=environment)
        data["security"] = security

        data["diffs"] = self.diff_service.build_payload(receipt.diffs)

        decision = self.decision(data)
        data["decision"] = decision

        if decision == "FAIL":
            rollback_info = self.rollback(data)
            data["rollback"] = rollback_info
            self.result.status = "ROLLED_BACK"
        elif decision == "GOLD":
            self.result.status = "GOLD"
        else:
            self.result.status = "PASS"

        integration_result = self.integration.run(data)
        data["integration"] = integration_result

        memory_record = self.persist_memory(data)
        data["memory_record"] = memory_record

        # feedback loop
        score = 1.0 if decision == "GOLD" else (0.5 if decision == "PASS" else 0.0)
        feedback_record = self.memory.record_feedback(
            mission_id=mission_id,
            root_cause=diagnosis.root_cause,
            strategy=diagnosis.strategy,
            score=score,
            notes=f"source={diagnosis.source}; decision={decision}",
        )
        data["feedback_record"] = feedback_record

        self.result.data.update({
            "diagnosis": diagnosis,
            "plan": plan,
            "snapshot_id": snapshot_id,
            "execution_receipt": receipt,
            "validation": validation,
            "security": security,
            "decision": decision,
            "diffs": data["diffs"],
            "integration": integration_result,
            "memory_record": memory_record,
            "feedback_record": feedback_record,
        })
        return self.result

    def orchestration(self, mission_id, mission):
        self.result.log("orchestration", "dispatch mission")
        return {"mission_id": mission_id, "mission": mission}

    def diagnosis(self, data):
        self.result.log("diagnosis", "Hermes analyzing")
        return self.hermes.analyze(mission_id=data["mission_id"], mission_text=data["mission"])

    def planning(self, data):
        self.result.log("planning", "creating adaptive execution plan")
        return self.planner.build_plan(
            mission_id=data["mission_id"],
            diagnosis=data["diagnosis"],
            workspace_root=str(self.workspace_root),
            feedback=data.get("feedback", []),
        )

    def snapshot(self, data):
        self.result.log("snapshot", "creating pre-execution snapshot")
        return self.snapshot_manager.create_snapshot(mission_id=data["mission_id"], plan=data["plan"])

    def execution(self, data):
        self.result.log("execution", "Operator applying plan")
        return self.operator.apply(data["plan"])

    def validation(self, data):
        self.result.log("validation", "SDDF running gates")
        return self.sddf.validate(mission_id=data["mission_id"], diagnosis=data["diagnosis"], execution_data=data)

    def security(self, data, environment="production"):
        self.result.log("security", "Aegis policy check")
        return self.aegis.enforce(mission_id=data["mission_id"], validation=data["validation"], environment=environment)

    def decision(self, data):
        self.result.log("decision", "evaluating")
        validation = data["validation"]
        security = data["security"]
        if validation.outcome == "FAIL":
            return "FAIL"
        if validation.outcome == "GOLD" and security.promotion_allowed:
            return "GOLD"
        return "PASS"

    def rollback(self, data):
        self.result.log("rollback", "restoring snapshot")
        return self.restore_manager.restore_snapshot(data["snapshot_id"])

    def rollback_file(self, snapshot_id: str, target_file: str):
        return self.restore_manager.restore_file(snapshot_id, target_file)

    def list_memory(self):
        return self.memory.list_all()

    def get_memory(self, mission_id: str):
        return self.memory.get_by_mission_id(mission_id)

    def get_last_integration(self):
        return self.integration.read_last()

    def get_integration_history(self):
        return self.integration.read_history()

    def get_integration_history_page(self, page: int = 1, page_size: int = 10):
        return self.integration.read_history_page(page=page, page_size=page_size)

    def persist_memory(self, data):
        record = {
            "mission_id": data["mission_id"],
            "mission": data["mission"],
            "root_cause": data["diagnosis"].root_cause,
            "validation_outcome": data["validation"].outcome,
            "pass_gold": data["validation"].pass_gold,
            "promotion_allowed": data["security"].promotion_allowed,
            "snapshot_id": data["snapshot_id"],
            "decision": data["decision"],
            "strategy": data["diagnosis"].strategy,
            "source": data["diagnosis"].source,
        }
        return self.memory.record(record)
