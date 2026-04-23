from vision_core.runtime.pipeline import VisionPipeline


def test_pipeline_gold_smoke():
    result = VisionPipeline().run(
        "corrigir runtime do technetgame",
        environment="production",
        integration_context={"provider": "github", "repository": "acme/vision-core"},
    )
    assert result.status == "GOLD"
    assert result.data["validation"].pass_gold is True
    assert result.data["security"].promotion_allowed is True
    assert result.data["integration"]["pass_gold_required"] is True
    assert result.data["integration"]["execution_has_diffs"] is True
    assert result.data["integration"]["validation_not_fail"] is True
    assert result.data["integration"]["merge_allowed"] is True
