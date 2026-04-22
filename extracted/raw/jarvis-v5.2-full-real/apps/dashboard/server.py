from pathlib import Path
import sys

import uvicorn

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


if __name__ == '__main__':
    uvicorn.run('jarvis_v5.interface_plane.api:app', host='127.0.0.1', port=8088, reload=False)
