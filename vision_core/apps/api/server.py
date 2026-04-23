from flask import Flask, jsonify, request
from vision_core.runtime.pipeline import VisionPipeline

app = Flask(__name__)


@app.get("/api/health")
def health():
    return {"ok": True, "service": "vision_core_api"}


@app.post("/api/mission")
def mission():
    payload = request.get_json(force=True, silent=True) or {}
    mission_text = payload.get("mission", "default mission")
    environment = payload.get("environment", "production")

    pipeline = VisionPipeline()
    result = pipeline.run(mission_text, environment=environment)

    return jsonify(
        {
            "status": result.status,
            "mission_id": result.data["mission_id"],
            "root_cause": result.data["diagnosis"].root_cause,
            "validation": result.data["validation"].outcome,
            "pass_gold": result.data["validation"].pass_gold,
            "promotion_allowed": result.data["security"].promotion_allowed,
            "steps": result.steps,
        }
    )


if __name__ == "__main__":
    app.run(port=8080)
