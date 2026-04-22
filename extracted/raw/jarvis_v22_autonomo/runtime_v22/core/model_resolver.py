from __future__ import annotations
import subprocess


class ModelResolver:
    def __init__(self) -> None:
        self.available = self._detect_models()

    def _detect_models(self) -> list[str]:
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                timeout=20,
            )
            if result.returncode != 0:
                return []
            lines = result.stdout.splitlines()[1:]
            return [line.split()[0] for line in lines if line.strip()]
        except Exception:
            return []

    def resolve(self, preferred: str) -> str | None:
        if preferred in self.available:
            return preferred
        if self.available:
            return self.available[0]
        return None
