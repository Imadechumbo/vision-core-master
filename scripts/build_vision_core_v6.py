import os
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

EXTRACTED = ROOT / "extracted" / "normalized"
FRAGMENTS = EXTRACTED / "fragments" / "core"
VERSIONS = EXTRACTED / "versions"

TARGET = ROOT / "vision-core"

DOMAINS = {
    "orchestration": ["openclaw", "opensquad"],
    "diagnosis": ["hermes"],
    "security": ["aegis"],
    "validation": ["sddf"],
    "rollback": ["vault", "rollback", "snapshot"],
    "execution": ["operator", "execution"],
    "memory": ["memory", "archivist"],
    "structure": ["navigator", "structure"],
    "integration": ["integration", "codex", "github"],
    "performance": ["go", "worker", "scheduler"]
}


def ensure_dirs():
    for domain in DOMAINS:
        (TARGET / "core" / domain).mkdir(parents=True, exist_ok=True)

    (TARGET / "apps" / "cli").mkdir(parents=True, exist_ok=True)
    (TARGET / "apps" / "api").mkdir(parents=True, exist_ok=True)
    (TARGET / "apps" / "dashboard").mkdir(parents=True, exist_ok=True)


def classify_folder(name):
    name = name.lower()

    for domain, keywords in DOMAINS.items():
        for k in keywords:
            if k in name:
                return domain

    return None


def copy_fragments():
    report = []

    if not FRAGMENTS.exists():
        print("Fragments não encontrados")
        return report

    for item in FRAGMENTS.iterdir():
        if not item.is_dir():
            continue

        domain = classify_folder(item.name)

        if domain:
            dest = TARGET / "core" / domain / item.name
        else:
            dest = TARGET / "core" / "structure" / item.name

        shutil.copytree(item, dest, dirs_exist_ok=True)

        report.append((item.name, domain if domain else "structure"))

    return report


def generate_cli():
    cli_file = TARGET / "apps" / "cli" / "vision.py"

    cli_file.write_text(
        """import sys

def main():
    print("VISION CORE CLI")
    print("Comando:", sys.argv)

if __name__ == "__main__":
    main()
"""
    )


def generate_api():
    api_file = TARGET / "apps" / "api" / "server.py"

    api_file.write_text(
        """from flask import Flask, request, jsonify

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
"""
    )


def generate_dashboard():
    dash = TARGET / "apps" / "dashboard" / "index.html"

    dash.write_text(
        """<!DOCTYPE html>
<html>
<head>
<title>VISION CORE</title>
<style>
body { background: #02060d; color: #00ffff; font-family: monospace; }
button { margin: 10px; padding: 10px; }
</style>
</head>
<body>
<h1>VISION CORE V6</h1>

<button onclick="runMission()">Executar Missão</button>

<pre id="log"></pre>

<script>
function runMission() {
    fetch("/api/mission", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ mission: "test" })
    })
    .then(r => r.json())
    .then(d => {
        document.getElementById("log").innerText =
            JSON.stringify(d, null, 2);
    });
}
</script>

</body>
</html>
"""
    )


def generate_report(report):
    report_file = ROOT / "inventory" / "v6_build_report.md"
    report_file.parent.mkdir(parents=True, exist_ok=True)

    lines = ["# V6 BUILD REPORT", ""]

    for name, domain in report:
        lines.append(f"- {name} -> {domain}")

    report_file.write_text("\n".join(lines), encoding="utf-8")
def main():
    print("=== BUILD VISION CORE V6 ===")

    ensure_dirs()

    report = copy_fragments()

    generate_cli()
    generate_api()
    generate_dashboard()

    generate_report(report)

    print("✔ Estrutura criada em vision-core/")
    print("✔ CLI gerado")
    print("✔ API gerada")
    print("✔ Dashboard gerado")
    print("✔ Relatório gerado")


if __name__ == "__main__":
    main()