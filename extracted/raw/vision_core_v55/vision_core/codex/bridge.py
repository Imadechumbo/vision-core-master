from __future__ import annotations
import pathlib, subprocess, shlex
from typing import Any, Dict, List
from vision_core.utils.time import utc_stamp, utc_now_iso

def _run(cmd: List[str], cwd: str) -> Dict[str, Any]:
    try:
        proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
        return {
            "cmd": cmd,
            "returncode": proc.returncode,
            "stdout": proc.stdout.strip(),
            "stderr": proc.stderr.strip(),
        }
    except FileNotFoundError:
        return {"cmd": cmd, "returncode": 127, "stdout": "", "stderr": "command_not_found"}

def prepare_branch_and_commit(project_root: str, title: str, branch_name: str | None = None) -> Dict[str, Any]:
    root = pathlib.Path(project_root)
    branch = branch_name or f"vision/{utc_stamp()}"
    steps = []
    steps.append(_run(["git", "rev-parse", "--is-inside-work-tree"], str(root)))
    steps.append(_run(["git", "checkout", "-b", branch], str(root)))
    steps.append(_run(["git", "add", "-A"], str(root)))
    steps.append(_run(["git", "commit", "-m", title], str(root)))

    ok = all(step["returncode"] == 0 for step in steps[:1]) and steps[-1]["returncode"] in (0, 1)
    return {
        "ok": ok,
        "prepared_at": utc_now_iso(),
        "branch": branch,
        "title": title,
        "steps": steps,
        "pr_payload": {
            "title": title,
            "head": branch,
            "base": "main",
            "body": "PR preparado pelo VISION CORE. Revisao Codex/GitHub pendente."
        }
    }
