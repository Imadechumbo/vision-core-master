from jarvis_core.adapters.base import BaseAdapter


class TechNetGameAdapter(BaseAdapter):
    name = 'technetgame'
    REQUIRED_ENVS = ['OPENAI_API_KEY', 'GROQ_API_KEY']
    CRITICAL_ENDPOINTS = ['/api/health', '/api/news/latest', '/api/v1/chat', '/api/v1/chat/vision']

    def http_checks(self):
        return [
            {'name': 'api_health', 'method': 'GET', 'path': '/api/health', 'allow_status': [200]},
            {'name': 'news_latest', 'method': 'GET', 'path': '/api/news/latest', 'allow_status': [200]},
            {'name': 'chat_basic', 'method': 'POST', 'path': '/api/v1/chat', 'allow_status': [200, 400, 401], 'json': {'message': 'ping'}},
            {'name': 'chat_vision_contract', 'method': 'POST', 'path': '/api/v1/chat/vision', 'allow_status': [200, 400, 401], 'json': {'message': 'vision probe'}},
        ]
