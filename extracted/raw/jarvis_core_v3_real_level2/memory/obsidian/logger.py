from __future__ import annotations

from pathlib import Path
from datetime import datetime


def write_obsidian_note(vault_path: str, title: str, body: str) -> str:
    vault = Path(vault_path)
    vault.mkdir(parents=True, exist_ok=True)
    safe_title = title.replace("/", "-")
    note_path = vault / f"{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}_{safe_title}.md"
    note_path.write_text(body, encoding="utf-8")
    return str(note_path)
