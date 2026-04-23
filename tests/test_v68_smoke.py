from vision_core.runtime.pipeline import VisionPipeline

def test_v68_pipeline_and_memory():
    pipeline = VisionPipeline(project_root=".vision_core_test_runtime_v68")
    result = pipeline.run("corrigir runtime do technetgame", environment="production")
    assert result.status == "GOLD"
    assert result.data["execution_receipt"].applied_files >= 2
    assert pipeline.get_memory(result.data["mission_id"]) is not None
