import json
from pathlib import Path

class LocalQueue:
    def __init__(self, root: Path):
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def enqueue(self, payload: dict):
        path = self.root / f"{payload['id']}.json"
        path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        return str(path)

    def dequeue(self):
        items = sorted(self.root.glob("mission_*.json"))
        if not items:
            return None
        path = items[0]
        data = json.loads(path.read_text(encoding="utf-8"))
        path.unlink(missing_ok=True)
        return data
