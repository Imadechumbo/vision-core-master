import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(ROOT_DIR, 'data')
INCIDENT_JSON_DIR = os.path.join(DATA_DIR, 'incidents', 'json')
INCIDENT_DB_PATH = os.path.join(DATA_DIR, 'incidents', 'incidents.sqlite')
OBSIDIAN_DIR = os.path.join(ROOT_DIR, 'obsidian')
PATCHES_DIR = os.path.join(ROOT_DIR, 'patches')
STABLE_VAULT_DIR = os.path.join(ROOT_DIR, 'stable_vault')

for path in [DATA_DIR, INCIDENT_JSON_DIR, OBSIDIAN_DIR, PATCHES_DIR, STABLE_VAULT_DIR, os.path.dirname(INCIDENT_DB_PATH)]:
    os.makedirs(path, exist_ok=True)
