from __future__ import annotations

from adapters.projects.technetgame import TechNetGameAdapter


def load_project_adapter(project_id: str):
    if project_id == "technetgame":
        return TechNetGameAdapter()
    raise ValueError(f"No adapter registered for project_id={project_id}")
