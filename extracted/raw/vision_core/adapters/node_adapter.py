import json
import re
from pathlib import Path

ROUTE_RE = re.compile(r"""(?:router|app)\.(get|post|put|patch|delete|options|use)\(\s*['"`]([^'"`]+)['"`]""", re.I)
REQ_FILE_RE = re.compile(r"\breq\.file\b")
MIMETYPE_RE = re.compile(r"\breq\.file\.mimetype\b")

def inspect_node_project(project_root):
    root = Path(project_root)
    exists = root.exists() and root.is_dir()
    info = {
        "root_exists": exists,
        "root": str(root),
        "is_node_project": False,
        "frameworks": [],
        "entry_candidates": [],
        "has_package_json": False,
        "detected_ports": [],
        "sample_files": [],
        "routes": [],
        "vision_candidates": [],
        "req_file_usages": [],
        "mimetype_usages": [],
    }
    if not exists:
        return info

    pkg = root / "package.json"
    info["has_package_json"] = pkg.exists()
    if pkg.exists():
        info["is_node_project"] = True
        try:
            data = json.loads(pkg.read_text(encoding="utf-8"))
            deps = {**data.get("dependencies", {}), **data.get("devDependencies", {})}
            if "express" in deps:
                info["frameworks"].append("Express")
            if "fastify" in deps:
                info["frameworks"].append("Fastify")
            if "koa" in deps:
                info["frameworks"].append("Koa")
        except Exception:
            pass

    file_list = []
    for pattern in ("*.js", "*.mjs", "*.cjs", "*.ts"):
        file_list.extend(root.rglob(pattern))
    for p in sorted(file_list)[:120]:
        rel = p.relative_to(root).as_posix()
        info["sample_files"].append(rel)
        if p.name in {"app.js", "server.js", "index.js", "main.js"}:
            info["entry_candidates"].append(rel)
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue

        if "express(" in text and "Express" not in info["frameworks"]:
            info["frameworks"].append("Express")
        for m in re.findall(r"(?:PORT|port)\s*[:=]\s*['\"]?(\d{2,5})", text):
            if m not in info["detected_ports"]:
                info["detected_ports"].append(m)
        for mm in ROUTE_RE.finditer(text):
            method, route = mm.groups()
            info["routes"].append({"file": rel, "method": method.lower(), "route": route})
        if REQ_FILE_RE.search(text):
            info["req_file_usages"].append(rel)
        if MIMETYPE_RE.search(text):
            info["mimetype_usages"].append(rel)
        lowered = rel.lower()
        if "vision" in lowered or "ai" in lowered or "/vision" in text or "mimetype" in text:
            info["vision_candidates"].append(rel)

    info["routes"] = info["routes"][:80]
    info["vision_candidates"] = list(dict.fromkeys(info["vision_candidates"]))[:20]
    return info
