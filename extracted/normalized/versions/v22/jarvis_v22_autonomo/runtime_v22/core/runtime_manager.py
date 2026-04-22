from __future__ import annotations
import shutil
import subprocess
from pathlib import Path


class RuntimeManager:
    def __init__(self) -> None:
        self.docker_available = shutil.which("docker") is not None
        self.ollama_available = shutil.which("ollama") is not None

    def inspect(self) -> dict:
        return {
            "docker_available": self.docker_available,
            "docker_status": self._docker_status(),
            "ollama_available": self.ollama_available,
            "profiles": self.available_profiles(),
        }

    def _docker_status(self) -> str:
        if not self.docker_available:
            return "docker_not_found"
        try:
            result = subprocess.run(
                ["docker", "info", "--format", "{{json .ServerVersion}}"],
                capture_output=True,
                text=True,
                timeout=15,
            )
            return "ok" if result.returncode == 0 else "docker_error"
        except Exception:
            return "docker_exception"

    def available_profiles(self) -> list[str]:
        profile_dir = Path(__file__).resolve().parents[1] / "runtime" / "profiles"
        return sorted([p.stem for p in profile_dir.glob("*.yaml")])
