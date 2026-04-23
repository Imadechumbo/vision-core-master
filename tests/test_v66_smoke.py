from pathlib import Path
from vision_core.runtime.pipeline import VisionPipeline


def test_pipeline_runs_gold_for_runtime_mission():
    pipeline = VisionPipeline(project_root=".vision_core_test_runtime")
    result = pipeline.run("corrigir runtime do technetgame", environment="production")

    assert result.status == "GOLD"
    assert result.data["validation"].pass_gold is True
    assert result.data["security"].promotion_allowed is True
    assert result.data["snapshot_id"].startswith("snap-")
    assert result.data["execution_receipt"].applied_files >= 2
    assert Path(".vision_core_test_runtime/memory/memory.db").exists()
