from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

from vision_core.runtime.pipeline import VisionPipeline

DASHBOARD_DIR = Path(__file__).resolve().parents[1] / "dashboard"
app = Flask(__name__, static_folder=str(DASHBOARD_DIR), static_url_path="/static")


def _pipeline() -> VisionPipeline:
    return VisionPipeline()


def _build_mission_response(result) -> dict:
    integration = result.data.get("integration")
    return {
        "status": result.status,
        "mission_id": result.data["mission_id"],
        "root_cause": result.data["diagnosis"].root_cause,
        "validation": result.data["validation"].outcome,
        "pass_gold": result.data["validation"].pass_gold,
        "promotion_allowed": result.data["security"].promotion_allowed,
        "applied_files": result.data["execution_receipt"].applied_files,
        "snapshot_id": result.data["snapshot_id"],
        "diffs": result.data.get("diffs", []),
        "integration": integration.to_dict() if integration else None,
        "steps": result.steps,
    }


@app.get("/")
def dashboard():
    return send_from_directory(DASHBOARD_DIR, "index.html")


@app.get("/api/health")
def health():
    return {"ok": True, "service": "vision_core_api"}


@app.post("/api/mission")
def mission():
    payload = request.get_json(force=True, silent=True) or {}
    mission_text = payload.get("mission", "default mission")
    environment = payload.get("environment", "production")
    integration_context = payload.get("integration_context")

    pipeline = _pipeline()
    result = pipeline.run(
        mission_text,
        environment=environment,
        integration_context=integration_context,
    )

    return jsonify(_build_mission_response(result))


@app.get("/api/integration/last")
def integration_last():
    pipeline = _pipeline()
    return jsonify(pipeline.get_last_integration())


@app.get("/api/integration/history")
def integration_history():
    pipeline = _pipeline()
    page = request.args.get("page", default=1, type=int)
    page_size = request.args.get("page_size", default=10, type=int)
    return jsonify(pipeline.get_integration_history_page(page=page, page_size=page_size))


@app.get("/api/memory")
def memory_list():
    pipeline = _pipeline()
    return jsonify(pipeline.list_memory())


@app.get("/api/memory/<mission_id>")
def memory_get(mission_id: str):
    pipeline = _pipeline()
    item = pipeline.get_memory(mission_id)
    if item is None:
        return jsonify({"error": "mission_id not found"}), 404
    return jsonify(item)


@app.post("/api/rollback")
def rollback_snapshot():
    payload = request.get_json(force=True, silent=True) or {}
    snapshot_id = payload.get("snapshot_id")
    if not snapshot_id:
        return jsonify({"error": "snapshot_id is required"}), 400

    pipeline = _pipeline()
    result = pipeline.restore_manager.restore_snapshot(snapshot_id)
    return jsonify(result)


@app.post("/api/rollback-file")
def rollback_file():
    payload = request.get_json(force=True, silent=True) or {}
    snapshot_id = payload.get("snapshot_id")
    target_file = payload.get("target_file")
    if not snapshot_id or not target_file:
        return jsonify({"error": "snapshot_id and target_file are required"}), 400

    pipeline = _pipeline()
    result = pipeline.rollback_file(snapshot_id, target_file)
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8080)