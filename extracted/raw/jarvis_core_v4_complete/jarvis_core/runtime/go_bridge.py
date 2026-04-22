import os


def ensure_runtime_binary_message(host: str = '127.0.0.1', port: int = 8090) -> str:
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    main_go = os.path.join(root, 'runtime-go', 'main.go')
    return (
        'Runtime Go disponível.\n'
        f'Arquivo: {main_go}\n'
        f'Rodar: go run runtime-go/main.go --host {host} --port {port}\n'
        'Endpoints: /health, /runtime, /execute'
    )
