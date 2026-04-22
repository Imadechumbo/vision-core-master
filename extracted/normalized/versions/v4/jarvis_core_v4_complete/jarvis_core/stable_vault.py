import os
import shutil
from jarvis_core.config import STABLE_VAULT_DIR
from jarvis_core.utils import utc_now_iso, slugify, copytree_filtered, write_json


def _project_dir(project: str) -> str:
    path = os.path.join(STABLE_VAULT_DIR, project)
    os.makedirs(path, exist_ok=True)
    os.makedirs(os.path.join(path, 'history'), exist_ok=True)
    return path


def promote_to_gold(project: str, source_dir: str) -> dict:
    pdir = _project_dir(project)
    history_id = slugify(f"{utc_now_iso()}-gold")
    snapshot_dir = os.path.join(pdir, 'history', history_id)
    copytree_filtered(source_dir, snapshot_dir)

    gold_dir = os.path.join(pdir, 'GOLD')
    if os.path.exists(gold_dir):
        shutil.rmtree(gold_dir)
    shutil.copytree(snapshot_dir, gold_dir)

    manifest = {'project': project, 'created_at': utc_now_iso(), 'source_dir': source_dir, 'snapshot_id': history_id}
    write_json(os.path.join(gold_dir, 'manifest.json'), manifest)
    return {'gold_dir': gold_dir, 'snapshot_id': history_id, 'manifest': manifest}


def rollback_gold(project: str, target_dir: str) -> dict:
    pdir = _project_dir(project)
    gold_dir = os.path.join(pdir, 'GOLD')
    if not os.path.exists(gold_dir):
        raise FileNotFoundError('GOLD inexistente para este projeto')
    copytree_filtered(gold_dir, target_dir)
    return {'rolled_back_from': gold_dir, 'target_dir': target_dir}


def list_snapshots(project: str) -> dict:
    pdir = _project_dir(project)
    history = os.path.join(pdir, 'history')
    items = sorted(os.listdir(history), reverse=True) if os.path.exists(history) else []
    return {'project': project, 'gold_exists': os.path.exists(os.path.join(pdir, 'GOLD')), 'snapshots': items}
