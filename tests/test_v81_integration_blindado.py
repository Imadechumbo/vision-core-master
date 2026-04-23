from pathlib import Path

from vision_core.integration.github.bridge import GitHubBridge
from vision_core.runtime.pipeline import VisionPipeline


def test_v81_persists_last_integration_state():
    runtime_root = ".vision_core_test_runtime_v81_state"
    pipeline = VisionPipeline(project_root=runtime_root)
    result = pipeline.run("corrigir runtime do technetgame", environment="production")

    state = pipeline.get_last_integration()
    assert state["mission_id"] == result.data["mission_id"]
    assert Path(runtime_root, "integration", "last_integration.json").exists()
    assert isinstance(state.get("diffs"), list)


def test_v81_github_bridge_debug_state_without_git_config():
    bridge = GitHubBridge(repository_root=".")
    state = bridge.get_debug_state()
    assert "repository_root" in state
    assert "base_branch" in state
