from vision_core.integration.github.bridge import GitHubBridge
from vision_core.runtime.pipeline import VisionPipeline


def test_v82_persists_integration_history():
    runtime_root = ".vision_core_test_runtime_v82_history"
    pipeline = VisionPipeline(project_root=runtime_root)
    pipeline.run("corrigir backend runtime", environment="production")
    pipeline.run("corrigir backend runtime novamente", environment="production")

    history = pipeline.get_integration_history()
    assert isinstance(history, list)
    assert len(history) >= 2
    assert history[0]["mission_id"].startswith("mission-")
    assert "recorded_at" in history[0]


def test_v82_retryable_error_classification():
    bridge = GitHubBridge(repository_root=".")
    assert bridge._classify_error("HTTP 503 temporary upstream timeout") == "retryable_network_error"
    assert bridge._classify_error("remote: error: GH006 push rejected") == "push_rejected"


def test_v82_api_retry_succeeds_on_transient_error():
    bridge = GitHubBridge(repository_root=".")
    bridge.max_api_attempts = 3
    state = {"calls": 0}

    def flaky_operation():
        state["calls"] += 1
        if state["calls"] < 3:
            raise RuntimeError("temporary")
        return {"ok": True}

    # wrap RuntimeError as GitHubApiError at call site to mirror client behavior
    from vision_core.integration.github.client import GitHubApiError

    def adapter():
        try:
            return flaky_operation()
        except RuntimeError as exc:
            raise GitHubApiError(str(exc)) from exc

    result = bridge._api_call(adapter)
    assert result == {"ok": True}
    assert bridge._last_attempts == 3
