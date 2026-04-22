from __future__ import annotations
from dataclasses import dataclass
from .cache import CacheStore
from .router import MissionRouter
from .runtime_manager import RuntimeManager
from .ollama_client import OllamaClient
from .model_resolver import ModelResolver
from .project_scanner import ProjectScanner


@dataclass
class MissionResult:
    mission: str
    intent: str
    used_cache: bool
    route: dict
    runtime: dict
    model_used: str | None
    project: dict
    answer: str


class MissionController:
    def __init__(self, routing_config: dict, models_config: dict) -> None:
        self.router = MissionRouter(routing_config)
        self.models_config = models_config
        self.cache = CacheStore()
        provider_cfg = models_config["providers"]["ollama"]
        self.ollama = OllamaClient(
            base_url=provider_cfg["base_url"],
            timeout_seconds=provider_cfg.get("timeout_seconds", 90),
        )
        self.runtime = RuntimeManager()
        self.model_resolver = ModelResolver()
        self.project_scanner = ProjectScanner()

    def run(self, mission_text: str, project_root: str | None = None) -> MissionResult:
        route = self.router.resolve(mission_text)
        runtime_info = self.runtime.inspect()
        project_info = self.project_scanner.scan(project_root)
        cache_payload = {
            "mission": mission_text,
            "route": route.model_key,
            "project_root": project_root or "",
            "models": self.model_resolver.available,
        }
        cached = self.cache.get("mission_response", cache_payload)
        if cached:
            return MissionResult(
                mission=mission_text,
                intent=route.intent,
                used_cache=True,
                route=route.__dict__,
                runtime=runtime_info,
                model_used=cached.get("model_used"),
                project=project_info,
                answer=cached["answer"],
            )

        preferred_model = self.models_config["models"][route.model_key]["name"]
        model_name = self.model_resolver.resolve(preferred_model)
        if not model_name:
            answer = "Falha controlada: nenhum modelo local do Ollama disponível."
            return MissionResult(
                mission=mission_text,
                intent=route.intent,
                used_cache=False,
                route=route.__dict__,
                runtime=runtime_info,
                model_used=None,
                project=project_info,
                answer=answer,
            )

        prompt = self._build_prompt(mission_text, route.intent, runtime_info, project_info)
        response = self.ollama.generate(model_name, prompt)

        if response.get("ok"):
            answer = response.get("response") or "Sem resposta do modelo local."
        else:
            detail = response.get("error") or "erro desconhecido no cliente Ollama"
            answer = (
                "Falha no modelo local. Verifique Ollama e modelo configurado. "
                f"Detalhe: {detail}"
            )

        self.cache.set("mission_response", cache_payload, {"answer": answer, "model_used": model_name})
        return MissionResult(
            mission=mission_text,
            intent=route.intent,
            used_cache=False,
            route=route.__dict__,
            runtime=runtime_info,
            model_used=model_name,
            project=project_info,
            answer=answer,
        )

    @staticmethod
    def _build_prompt(mission_text: str, intent: str, runtime_info: dict, project_info: dict) -> str:
        return (
            "Você é o núcleo local do Jarvis Core Hybrid V2.2. "
            "Responda de forma técnica, objetiva e orientada à execução.\n\n"
            f"Intent: {intent}\n"
            f"Runtime: {runtime_info}\n"
            f"Projeto: {project_info}\n"
            f"Missão: {mission_text}\n\n"
            "Entregue:\n"
            "1. diagnóstico curto\n"
            "2. ações imediatas\n"
            "3. próximos passos\n"
            "4. riscos e bloqueios\n"
        )
