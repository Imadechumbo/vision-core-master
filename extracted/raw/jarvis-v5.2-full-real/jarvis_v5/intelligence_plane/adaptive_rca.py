class AdaptiveRCA:
    def __init__(self, incident_store, strategy_store):
        self.incident_store = incident_store
        self.strategy_store = strategy_store

    def analyze(self, mission: dict, evidence: dict):
        prior = self.incident_store.query(project=mission['project']['name'], keyword=mission['intent'])
        ranked = self.strategy_store.list_ranked(project=mission['project']['name'])
        intent = mission['intent']
        if intent == 'fix_vision':
            root_cause = 'vision_contract_or_upload_validation'
            chain = ['endpoint multimodal falhou', 'ausência de validação robusta para arquivo/imagem', 'contrato vision inconsistente']
        elif intent == 'fix_runtime_config':
            root_cause = 'frontend_api_base_misalignment'
            chain = ['runtime-config.js desalinhado', 'frontend aponta para API errada']
        elif intent == 'fix_redirects':
            root_cause = 'redirect_rules_inconsistent'
            chain = ['_redirects ausente ou incompleto', 'rotas HTML/SPA quebrando navegação']
        elif intent == 'fix_procfile':
            root_cause = 'procfile_missing_or_invalid'
            chain = ['ambiente EB sem Procfile estável']
        elif intent == 'fix_docker':
            root_cause = 'container_entrypoint_or_port_misconfiguration'
            chain = ['Dockerfile/compose inconsistente']
        elif mission['project'].get('stack') == 'cloudflare_pages':
            root_cause = 'edge_runtime_or_pages_configuration'
            chain = ['configuração Cloudflare/Pages possivelmente inconsistente']
        elif mission['project'].get('stack') == 'aws_elastic_beanstalk':
            root_cause = 'elastic_beanstalk_runtime_or_env'
            chain = ['Procfile, porta, Node engine ou env podem estar inconsistentes']
        elif mission['project'].get('stack') == 'docker_runtime':
            root_cause = 'container_runtime_or_image_misconfiguration'
            chain = ['Dockerfile/compose/runtime podem estar inconsistentes']
        elif not evidence['scan_signals']['root_exists']:
            root_cause = 'invalid_project_root'
            chain = ['caminho do projeto não existe']
        else:
            root_cause = 'stack_or_runtime_misconfiguration'
            chain = ['diagnóstico geral por sinais do projeto']
        anomalies = []
        if not evidence['critical_files']:
            anomalies.append('nenhum arquivo crítico foi identificado pelo adapter')
        if not prior:
            anomalies.append('sem incidentes prévios semelhantes')
        return {'root_cause': root_cause, 'cause_chain': chain, 'anomalies': anomalies, 'prior_incident_count': len(prior), 'top_strategies': ranked[:3]}
