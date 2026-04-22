import os

COMMON_ENV_FILES = ['.env', '.env.example', '.env.production', '.env.local']
ROUTE_HINTS = ['routes', 'api', 'src/routes', 'server', 'app']


def scan_project(project_root: str) -> dict:
    files = []
    max_files = 4000
    route_candidates = []
    env_files = []
    package_json = None
    requirements = None

    for current_root, dirs, names in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in ('.git', '.venv', 'node_modules', '__pycache__', '.next')]
        for n in names:
            rel = os.path.relpath(os.path.join(current_root, n), project_root)
            files.append(rel)
            if n in COMMON_ENV_FILES:
                env_files.append(rel)
            if n == 'package.json':
                package_json = rel
            if n == 'requirements.txt':
                requirements = rel
            lower_rel = rel.replace('\\', '/').lower()
            if any(hint in lower_rel for hint in ROUTE_HINTS):
                route_candidates.append(rel)
            if len(files) >= max_files:
                break
        if len(files) >= max_files:
            break

    stack = []
    if package_json:
        stack.append('node')
    if requirements:
        stack.append('python')
    if os.path.exists(os.path.join(project_root, 'go.mod')):
        stack.append('go')

    return {
        'project_root': project_root,
        'total_files_scanned': len(files),
        'sample_files': files[:200],
        'route_candidates': route_candidates[:100],
        'env_files': env_files,
        'stack': stack or ['unknown'],
    }
