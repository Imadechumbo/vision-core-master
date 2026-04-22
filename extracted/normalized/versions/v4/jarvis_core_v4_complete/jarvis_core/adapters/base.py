class BaseAdapter:
    name = 'base'

    def http_checks(self):
        return [
            {'name': 'health', 'method': 'GET', 'path': '/health', 'allow_status': [200]}
        ]
