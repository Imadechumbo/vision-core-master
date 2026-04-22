import requests


class GateResult:
    def __init__(self, name: str, ok: bool, status=None, detail=''):
        self.name = name
        self.ok = ok
        self.status = status
        self.detail = detail

    def to_dict(self):
        return {'name': self.name, 'ok': self.ok, 'status': self.status, 'detail': self.detail}


def _request(method, url, **kwargs):
    try:
        response = requests.request(method, url, timeout=8, **kwargs)
        return True, response.status_code, response.text[:500]
    except Exception as e:
        return False, None, str(e)


def run_http_gates(base_url: str, adapter) -> dict:
    if not base_url:
        return {
            'pass_gold': False,
            'summary': 'base_url ausente; gates HTTP não executados.',
            'gates': [GateResult('base_url', False, detail='Informe --base-url').to_dict()],
        }

    gates = []
    for check in adapter.http_checks():
        ok, status, detail = _request(check['method'], base_url.rstrip('/') + check['path'], json=check.get('json'))
        accepted = ok and ((status in check.get('allow_status', [])) if check.get('allow_status') else (status is not None and status < 500))
        gates.append(GateResult(check['name'], accepted, status=status, detail=detail).to_dict())

    pass_gold = all(g['ok'] for g in gates)
    return {'pass_gold': pass_gold, 'summary': 'PASS GOLD' if pass_gold else 'FAIL GOLD', 'gates': gates}
