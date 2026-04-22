package models

type HealthResponse struct {
    OK      bool   `json:"ok"`
    Service string `json:"service"`
    Version string `json:"version"`
}

type RuntimeResponse struct {
    DockerAvailable bool     `json:"docker_available"`
    DockerVersion   string   `json:"docker_version,omitempty"`
    OllamaAvailable bool     `json:"ollama_available"`
    OllamaModels    []string `json:"ollama_models,omitempty"`
}
