import os
from jarvis_core.utils import safe_read_text, safe_write_text, utc_now_iso, slugify, write_json
from jarvis_core.diff_engine import generate_diff
from jarvis_core.config import PATCHES_DIR


def apply_patch(project_root: str, patch, apply: bool) -> dict:
    results = []
    patch_id = slugify(f"{utc_now_iso()}-{patch.summary}")[:80]
    patch_dir = os.path.join(PATCHES_DIR, patch_id)
    os.makedirs(patch_dir, exist_ok=True)

    for index, op in enumerate(patch.operations, start=1):
        target_path = os.path.join(project_root, op.file)
        before = ''
        if os.path.exists(target_path):
            try:
                before = safe_read_text(target_path)
            except Exception:
                before = ''

        if op.op_type == 'insert':
            after = before + ('\n' if before and not before.endswith('\n') else '') + op.content + '\n'
        elif op.op_type == 'replace' and op.target == '__FULL_FILE__':
            after = op.content + '\n'
        elif op.op_type == 'delete':
            after = ''
        else:
            after = before

        diff = generate_diff(before, after, f"a/{op.file}", f"b/{op.file}")
        diff_path = os.path.join(patch_dir, f"{index:03d}_{os.path.basename(op.file)}.diff")
        meta_path = os.path.join(patch_dir, f"{index:03d}_{os.path.basename(op.file)}.meta.json")
        safe_write_text(diff_path, diff)
        write_json(meta_path, {'file': op.file, 'reason': op.reason, 'apply': apply})

        if apply:
            if after == '':
                if os.path.exists(target_path):
                    os.remove(target_path)
            else:
                safe_write_text(target_path, after)

        results.append({'file': op.file, 'applied': apply, 'diff_path': diff_path, 'meta_path': meta_path})

    return {'patch_dir': patch_dir, 'results': results}
