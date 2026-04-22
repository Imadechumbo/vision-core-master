from __future__ import annotations

from pathlib import Path


class InfraPatchEngine:
    def patch_runtime_config(self, project_root: str, api_base_url: str | None):
        root = Path(project_root)
        target = next(iter([p for p in root.rglob('runtime-config.js') if p.is_file()]), None)
        if not target:
            return self._missing('runtime_config_missing')
        before = target.read_text(encoding='utf-8', errors='ignore')
        api = api_base_url or 'https://api.example.local'
        if 'API_BASE_URL' in before:
            lines = []
            replaced = False
            for line in before.splitlines():
                if 'API_BASE_URL' in line:
                    lines.append(f"  API_BASE_URL: '{api}',")
                    replaced = True
                elif 'API_URL' in line:
                    lines.append(f"  API_URL: '{api}',")
                else:
                    lines.append(line)
            after = '\n'.join(lines)
            if not replaced:
                after = f"window.RUNTIME_CONFIG = Object.assign({{ API_BASE_URL: '{api}', API_URL: '{api}' }}, window.RUNTIME_CONFIG || {{}});\n" + before
        else:
            snippet = f"window.RUNTIME_CONFIG = Object.assign({{ API_BASE_URL: '{api}', API_URL: '{api}' }}, window.RUNTIME_CONFIG || {{}});\n"
            after = snippet + before
        return self._candidate('infra_runtime_config_patch', target, before, after, 'runtime-config.js alinhado com API base')

    def patch_redirects(self, project_root: str):
        root = Path(project_root)
        target = root / '_redirects'
        before = target.read_text(encoding='utf-8', errors='ignore') if target.exists() else ''
        required = ['/ /index.html 200', '/relatorios /relatorios/ 301', '/relatorios.html /relatorios/ 301']
        lines = [l.rstrip() for l in before.splitlines() if l.strip()]
        for line in required:
            if line not in lines:
                lines.append(line)
        after = '\n'.join(lines).strip() + '\n'
        return self._candidate('infra_redirects_patch', target, before, after, '_redirects reforçado para páginas críticas')

    def patch_procfile(self, project_root: str):
        root = Path(project_root)
        target = root / 'Procfile'
        before = target.read_text(encoding='utf-8', errors='ignore') if target.exists() else ''
        after = 'web: npm start\n'
        return self._candidate('infra_procfile_patch', target, before, after, 'Procfile mínimo gerado para Node')

    def patch_ebextensions(self, project_root: str):
        root = Path(project_root)
        target = root / '.ebextensions' / '00-jarvis.config'
        before = target.read_text(encoding='utf-8', errors='ignore') if target.exists() else ''
        after = """option_settings:
  aws:elasticbeanstalk:application:environment:
    PORT: '8080'
    HOST: '0.0.0.0'
"""
        return self._candidate('infra_ebextensions_patch', target, before, after, 'Config EB mínima gerada com PORT/HOST')

    def patch_dockerfile(self, project_root: str):
        root = Path(project_root)
        target = root / 'Dockerfile'
        before = target.read_text(encoding='utf-8', errors='ignore') if target.exists() else ''
        after = """FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV HOST=0.0.0.0
ENV PORT=8080
EXPOSE 8080
CMD [\"npm\", \"start\"]
"""
        return self._candidate('infra_dockerfile_patch', target, before, after, 'Dockerfile mínimo gerado para Node')

    def _missing(self, strategy_key: str):
        return {'strategy_key': strategy_key, 'target_file': None, 'before': '', 'after': '', 'operations': [], 'summary': 'Arquivo alvo não encontrado.', 'metadata': {'infra': True, 'ast': False, 'missing': True}}

    def _candidate(self, strategy_key: str, target: Path, before: str, after: str, summary: str):
        return {'strategy_key': strategy_key, 'target_file': str(target), 'before': before, 'after': after, 'operations': [{'type': 'replace_file', 'file': str(target)}], 'summary': summary, 'metadata': {'infra': True, 'ast': False}}
