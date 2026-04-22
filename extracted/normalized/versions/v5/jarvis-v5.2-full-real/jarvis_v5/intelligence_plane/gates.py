import requests


class GateRunner:
    def __init__(self, adapter):
        self.adapter = adapter

    def _probe(self, method, url, json_body=None):
        try:
            r = requests.request(method, url, timeout=5, json=json_body)
            body = r.text[:300]
            return {'ok': r.status_code < 500, 'status': r.status_code, 'body': body}
        except Exception as exc:
            return {'ok': False, 'status': 0, 'body': str(exc)}

    def run(self, project: dict, mission: dict, evidence: dict):
        base_url = mission.get('base_url')
        checks = []
        if base_url:
            for endpoint in evidence.get('expected_endpoints', []):
                path = endpoint['path']
                full = base_url.rstrip('/') + path
                checks.append({'name': endpoint['name'], 'url': full, **self._probe(endpoint['method'], full, endpoint.get('json'))})
        infra_checks = self.adapter.infra_checks(project['root'], mission)
        all_http = all(c['ok'] for c in checks) if checks else True
        all_infra = all(c['ok'] for c in infra_checks) if infra_checks else True
        return {'checks': checks, 'infra_checks': infra_checks, 'pass_gold': all_http and all_infra}
