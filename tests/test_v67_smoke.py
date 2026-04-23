from vision_core.runtime.pipeline import VisionPipeline

def test_v67_memory_queries_and_pipeline():
    pipeline = VisionPipeline(project_root=".vision_core_test_runtime_v67")
    result = pipeline.run("corrigir runtime do technetgame", environment="production")

    assert result.status == "GOLD"
    assert result.data["execution_receipt"].applied_files >= 2

    items = pipeline.list_memory()
    assert len(items) >= 1

    item = pipeline.get_memory(result.data["mission_id"])
    assert item is not None
    assert item["mission_id"] == result.data["mission_id"]
