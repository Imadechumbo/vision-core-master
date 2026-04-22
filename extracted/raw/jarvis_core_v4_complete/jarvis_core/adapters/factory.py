from jarvis_core.adapters.technetgame import TechNetGameAdapter
from jarvis_core.adapters.base import BaseAdapter


def get_adapter(project: str):
    if (project or '').lower() == 'technetgame':
        return TechNetGameAdapter()
    return BaseAdapter()
