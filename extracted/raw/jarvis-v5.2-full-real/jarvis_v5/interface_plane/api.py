from pathlib import Path
import sys

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from jarvis_v5.control_plane.registry import ProjectRegistry
from jarvis_v5.control_plane.scheduler import SchedulerService
from jarvis_v5.memory_plane.incident_store import IncidentStore
from jarvis_v5.memory_plane.strategy_store import StrategyStore
from jarvis_v5.memory_plane.stable_vault import StableVault
from jarvis_v5.memory_plane.patch_history import PatchHistoryStore
from jarvis_v5.execution_plane.distributed_queue import DistributedQueue

app = FastAPI(title='JARVIS V5.2 FULL REAL Dashboard')
registry = ProjectRegistry(ROOT / 'storage' / 'projects')
incidents = IncidentStore(ROOT / 'storage')
strategies = StrategyStore(ROOT / 'storage')
stable = StableVault(ROOT / 'storage')
patches = PatchHistoryStore(ROOT / 'storage')
queue = DistributedQueue(ROOT / 'storage' / 'queue')
scheduler = SchedulerService(ROOT / 'storage', registry, queue)

@app.get('/api/projects')
def api_projects(): return registry.list_projects()

@app.get('/api/incidents')
def api_incidents(project: str | None = None): return incidents.query(project=project)

@app.get('/api/strategies')
def api_strategies(project: str | None = None): return strategies.list_ranked(project=project)

@app.get('/api/stable')
def api_stable(project: str | None = None): return stable.list_entries(project=project)

@app.get('/api/queue')
def api_queue(): return queue.info()

@app.get('/api/patches')
def api_patches(project: str | None = None): return patches.list(project=project)

@app.get('/api/scheduler')
def api_scheduler(project: str | None = None): return scheduler.list_jobs(project=project)

@app.get('/', response_class=HTMLResponse)
def home():
    projects = registry.list_projects()
    incidents_data = incidents.query()[:8]
    strategies_data = strategies.list_ranked()[:8]
    patch_data = patches.list()[:8]
    queue_info = queue.info()
    sched = scheduler.list_jobs()[:8]
    html = f"""
    <!doctype html><html><head><meta charset='utf-8'><title>JARVIS V5.2 Dashboard</title>
    <style>body{{font-family:Arial,sans-serif;margin:24px;background:#111;color:#eee}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.card{{background:#1b1b1b;border:1px solid #333;border-radius:12px;padding:16px}}h1,h2{{margin-top:0}}pre{{white-space:pre-wrap;word-break:break-word}}</style>
    </head><body><h1>JARVIS CORE V5.2 FULL REAL</h1><div class='grid'>
    <div class='card'><h2>Projetos</h2><pre>{projects}</pre></div>
    <div class='card'><h2>Fila</h2><pre>{queue_info}</pre></div>
    <div class='card'><h2>Scheduler</h2><pre>{sched}</pre></div>
    <div class='card'><h2>Incidentes recentes</h2><pre>{incidents_data}</pre></div>
    <div class='card'><h2>Estratégias</h2><pre>{strategies_data}</pre></div>
    <div class='card'><h2>Patches</h2><pre>{patch_data}</pre></div>
    </div></body></html>"""
    return html
