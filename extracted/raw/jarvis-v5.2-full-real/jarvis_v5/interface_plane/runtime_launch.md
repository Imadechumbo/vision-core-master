# Runtime launch

Use fallback seguro quando `uvicorn` não estiver no PATH:

```bash
python -m uvicorn jarvis_v5.interface_plane.api:app --host 127.0.0.1 --port 8088
python -m uvicorn runtime.server:app --host 127.0.0.1 --port 8090
```
