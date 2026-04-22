import shutil
import subprocess
from pathlib import Path
from vision_core.utils import utc_now_iso

def _run(cmd, cwd):
    proc = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True, check=False)
    return {
        "cmd": cmd,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }

def prepare_branch_and_commit(project_root, title, branch_name=None):
    root = Path(project_root)
    if not root.exists() or not root.is_dir():
        return {"ok": False, "error": "invalid_project_root", "project_root": str(root)}

    git = shutil.which("git")
    if not git:
        return {"ok": False, "error": "git_not_found", "project_root": str(root)}

    inside = _run([git, "rev-parse", "--is-inside-work-tree"], root)
    if inside["returncode"] != 0 or inside["stdout"].lower() != "true":
        return {"ok": False, "error": "not_git_repo", "project_root": str(root), "probe": inside}

    branch = branch_name or "mission/vision-core-fix"
    steps = [
        _run([git, "checkout", "-b", branch], root),
        _run([git, "add", "."], root),
        _run([git, "commit", "-m", title], root),
    ]
    ok = steps[0]["returncode"] == 0 and steps[1]["returncode"] == 0 and steps[2]["returncode"] in (0, 1)
    return {
        "ok": ok,
        "prepared_at": utc_now_iso(),
        "project_root": str(root),
        "branch": branch,
        "steps": steps,
        "note": "Branch e commit local preparados. PR remoto por API fica para próxima versão.",
    }
