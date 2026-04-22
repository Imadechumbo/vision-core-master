from datetime import datetime, timezone


class MissionRouter:
    def route(self, text: str, project: dict, base_url: str | None, dry_run: bool, auto_apply: bool, auto_rollback: bool):
        lowered = text.lower()
        if 'vision' in lowered:
            intent = 'fix_vision'
        elif 'runtime-config' in lowered or 'api base' in lowered:
            intent = 'fix_runtime_config'
        elif 'redirect' in lowered:
            intent = 'fix_redirects'
        elif 'procfile' in lowered:
            intent = 'fix_procfile'
        elif 'docker' in lowered:
            intent = 'fix_docker'
        elif 'deploy' in lowered or 'build' in lowered:
            intent = 'stabilize_deploy'
        elif 'smoke' in lowered:
            intent = 'scheduled_smoke'
        else:
            intent = 'general_diagnosis'

        return {
            'id': f"mission_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            'text': text,
            'intent': intent,
            'project': project,
            'base_url': base_url,
            'dry_run': dry_run,
            'auto_apply': auto_apply,
            'auto_rollback': auto_rollback,
        }
