from flask import Flask, request, jsonify

app = Flask(__name__)

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/mission")
def mission():
    data = request.json
    return {"status": "queued", "data": data}

if __name__ == "__main__":
    app.run(port=8080)
