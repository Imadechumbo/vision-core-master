import os
from jarvis_core.config import OBSIDIAN_DIR
from jarvis_core.utils import utc_now_iso, slugify, safe_write_text


def log_obsidian(project: str, mission: str, summary: str, content: str) -> str:
    note_id = slugify(f"{project}-{utc_now_iso()}-{mission}")[:90]
    path = os.path.join(OBSIDIAN_DIR, f"{note_id}.md")
    body = f"""# {summary}

- project: {project}
- mission: {mission}
- created_at: {utc_now_iso()}

## Registro

{content}
"""
    safe_write_text(path, body)
    return path
