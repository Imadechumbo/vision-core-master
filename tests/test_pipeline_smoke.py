from vision_core.runtime.pipeline import VisionPipeline


def test_pipeline_gold_smoke():
    result = VisionPipeline().run("corrigir runtime do technetgame", environment="production")
    assert result.status == "GOLD"
    assert result.data["validation"]["pass_gold"] is True
    assert result.data["security"]["promotion_allowed"] is True
