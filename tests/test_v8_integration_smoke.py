from pathlib import Path

from vision_core.runtime.pipeline import VisionPipeline


def test_v8_generates_codex_bundle_and_diff_payload():
    runtime_root = ".vision_core_test_runtime_v8"
    pipeline = VisionPipeline(project_root=runtime_root)
    result = pipeline.run("corrigir runtime do technetgame", environment="production")

    assert result.status == "GOLD"
    assert result.data["integration"].pr_validation.merge_allowed is True
    assert result.data["integration"].codex.status == "exported"
    bundle_path = Path(result.data["integration"].codex.bundle_path)
    assert bundle_path.exists()
    assert len(result.data["diffs"]) >= 1


def test_v8_blocks_github_when_not_gold():
    runtime_root = ".vision_core_test_runtime_v8_blocked"
    pipeline = VisionPipeline(project_root=runtime_root)
    result = pipeline.run("ajustar policy sensível", environment="production")

    assert result.status in {"PASS", "ROLLED_BACK", "GOLD"}
    if result.data["validation"].pass_gold is False:
        assert result.data["integration"].pr_validation.merge_allowed is False
        assert result.data["integration"].github.status == "blocked"
