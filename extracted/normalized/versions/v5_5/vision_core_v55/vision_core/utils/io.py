from __future__ import annotations
import json, os, pathlib, hashlib, shutil
from typing import Any

def ensure_dir(path: str | pathlib.Path) -> pathlib.Path:
    p = pathlib.Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def read_text(path: str | pathlib.Path, default: str = "") -> str:
    p = pathlib.Path(path)
    if not p.exists():
        return default
    return p.read_text(encoding="utf-8", errors="ignore")

def write_text(path: str | pathlib.Path, content: str) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")

def read_json(path: str | pathlib.Path, default: Any = None) -> Any:
    p = pathlib.Path(path)
    if not p.exists():
        return default
    return json.loads(p.read_text(encoding="utf-8"))

def write_json(path: str | pathlib.Path, data: Any) -> None:
    p = pathlib.Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

def sha256_text(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def copy_file(src: str | pathlib.Path, dst: str | pathlib.Path) -> None:
    pathlib.Path(dst).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
