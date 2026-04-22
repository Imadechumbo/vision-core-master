from pathlib import Path
import os
import sys

from fastapi import FastAPI
from pydantic import BaseModel

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jarvis_v5.execution_plane.distributed_queue import DistributedQueue
from jarvis_v5.control_plane.registry import ProjectRegistry
from jarvis_v5.control_plane.scheduler import SchedulerService

app = FastAPI(title='JARVIS V5.2 Runtime')
queue = DistributedQueue(ROOT / 'storage' / 'queue')
registry = ProjectRegistry(ROOT / 'storage' / 'projects')
scheduler = SchedulerService(ROOT / 'storage', registry, queue)

class ExecutePayload(BaseModel):
    task: str
    args: dict = {}

@app.get('/health')
def health(): return {'ok': True, 'service': 'jarvis-v5.2-runtime'}

@app.get('/runtime')
def runtime_info():
    return {'workers': ['distributed_queue','executor','python_worker','go_http_worker'], 'mode': queue.mode, 'redis_url_configured': bool(os.getenv('REDIS_URL')), 'queue': queue.info(), 'scheduler_jobs': scheduler.list_jobs()}

@app.post('/execute')
def execute(payload: ExecutePayload):
    mission = {'id': f"mission_runtime_{payload.task}", 'text': payload.task, 'intent': payload.args.get('intent', 'general_diagnosis'), 'project': payload.args.get('project', {'name': 'runtime', 'root': str(ROOT), 'stack': 'generic'}), 'base_url': payload.args.get('base_url'), 'dry_run': payload.args.get('dry_run', True), 'auto_apply': payload.args.get('auto_apply', False), 'auto_rollback': payload.args.get('auto_rollback', False)}
    enqueue = queue.enqueue(mission)
    return {'ok': True, 'received': payload.model_dump(), 'enqueue': enqueue, 'queue': queue.info()}

@app.post('/scheduler/run')
def scheduler_run(force: bool = False):
    return scheduler.run_due_jobs(force=force)
