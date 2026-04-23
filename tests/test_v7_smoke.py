from vision_core.runtime.pipeline import VisionPipeline

def test_v7_feedback_and_adaptive_planning():
    pipeline = VisionPipeline(project_root=".vision_core_test_runtime_v7")
    result = pipeline.run("corrigir runtime do technetgame", environment="production")
    assert result.status == "GOLD"
    assert result.data["diagnosis"].strategy != ""
    assert result.data["feedback_record"]["score"] == 1.0
