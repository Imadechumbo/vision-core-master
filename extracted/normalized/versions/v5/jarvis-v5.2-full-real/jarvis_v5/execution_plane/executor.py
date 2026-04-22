from pathlib import Path
from jarvis_v5.integration_plane.adapter_router import AdapterRouter
from jarvis_v5.intelligence_plane.project_scanner import ProjectScanner
from jarvis_v5.intelligence_plane.evidence_collector import EvidenceCollector
from jarvis_v5.intelligence_plane.adaptive_rca import AdaptiveRCA
from jarvis_v5.intelligence_plane.patch_engine import SmartPatchEngine
from jarvis_v5.intelligence_plane.policy_engine import AegisPolicy
from jarvis_v5.intelligence_plane.smoke_suites import SmokeSuiteRunner
from jarvis_v5.memory_plane.patch_history import PatchHistoryStore


class MissionExecutor:
    def __init__(self, storage_root: Path, registry, incident_store, strategy_store, stable_vault):
        self.storage_root = Path(storage_root)
        self.registry = registry
        self.incident_store = incident_store
        self.strategy_store = strategy_store
        self.stable_vault = stable_vault
        self.patch_history = PatchHistoryStore(storage_root)

    def execute(self, mission: dict):
        project = mission['project']
        adapter = AdapterRouter().for_project(project)
        scan = ProjectScanner().scan(project['root'])
        evidence = EvidenceCollector(adapter).collect(scan=scan, mission=mission)
        rca = AdaptiveRCA(self.incident_store, self.strategy_store).analyze(mission, evidence)
        patch = SmartPatchEngine(adapter, self.strategy_store).generate(mission, evidence, rca, project['root'])
        policy = AegisPolicy().evaluate(patch, mission)
        execution = {'applied': False, 'mode': 'blocked', 'notes': []}
        patch_record = None
        if policy['decision'] == 'auto_apply' and not mission.get('dry_run'):
            execution = adapter.apply_patch(patch, project['root'])
            if execution.get('applied'):
                patch_record = self.patch_history.record(project['name'], patch, execution)
        else:
            execution = {'applied': False, 'mode': 'dry_run' if mission.get('dry_run') else policy['decision'], 'notes': ['Patch não aplicado automaticamente.']}
        smoke = SmokeSuiteRunner(adapter).run(self.storage_root, project, mission, evidence)
        gates = smoke['gates']
        pass_gold = gates['pass_gold']
        incident = self.incident_store.record(project=project['name'], mission=mission, evidence=evidence, rca=rca, patch=patch, policy=policy, execution=execution, gates=gates)
        self.strategy_store.update_score(project=project['name'], strategy_key=patch['strategy_key'], success=pass_gold, metadata={'intent': mission['intent'], 'risk': patch['risk_level']})
        if pass_gold:
            stable_result = self.stable_vault.promote(project['name'], project['root'])
        elif mission.get('auto_rollback') and execution.get('backup_file'):
            stable_result = self.stable_vault.rollback_patch(execution['target_file'], execution['backup_file'])
        elif mission.get('auto_rollback'):
            stable_result = self.stable_vault.rollback(project['name'], project['root'])
        else:
            stable_result = {'status': 'not_promoted'}
        return {'mission': mission, 'scan': scan, 'evidence': evidence, 'rca': rca, 'patch': patch, 'policy': policy, 'execution': execution, 'patch_record': patch_record, 'smoke': smoke, 'gates': gates, 'pass_gold': pass_gold, 'incident': incident, 'stable': stable_result}
