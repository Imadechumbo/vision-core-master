from vision_core.runtime.pipeline import VisionPipeline


def test_v83_history_pagination_payload():
    runtime_root = ".vision_core_test_runtime_v83_history"
    pipeline = VisionPipeline(project_root=runtime_root)
    for idx in range(7):
        pipeline.run(f"corrigir runtime {idx}", environment="production")

    page1 = pipeline.get_integration_history_page(page=1, page_size=3)
    page2 = pipeline.get_integration_history_page(page=2, page_size=3)

    assert page1["pagination"]["page"] == 1
    assert page1["pagination"]["page_size"] == 3
    assert page1["pagination"]["total_items"] >= 7
    assert page1["pagination"]["has_next"] is True
    assert len(page1["items"]) == 3
    assert page2["pagination"]["page"] == 2
    assert len(page2["items"]) == 3


def test_v83_history_pagination_clamps_values():
    runtime_root = ".vision_core_test_runtime_v83_clamp"
    pipeline = VisionPipeline(project_root=runtime_root)
    pipeline.run("corrigir backend runtime", environment="production")

    payload = pipeline.get_integration_history_page(page=999, page_size=999)

    assert payload["pagination"]["page"] == 1
    assert payload["pagination"]["page_size"] == 100
    assert payload["pagination"]["total_pages"] == 1
