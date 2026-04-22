package server

import (
    "encoding/json"
    "net/http"

    "jarvis/autonomy_go/internal/models"
    "jarvis/autonomy_go/internal/system"
)

func NewMux() *http.ServeMux {
    mux := http.NewServeMux()

    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        writeJSON(w, models.HealthResponse{OK: true, Service: "autonomy-go", Version: "v2.2"})
    })

    mux.HandleFunc("/runtime", func(w http.ResponseWriter, r *http.Request) {
        dockerOK, dockerVersion := system.DetectDocker()
        ollamaOK, ollamaModels := system.DetectOllamaModels()
        writeJSON(w, models.RuntimeResponse{
            DockerAvailable: dockerOK,
            DockerVersion:   dockerVersion,
            OllamaAvailable: ollamaOK,
            OllamaModels:    ollamaModels,
        })
    })

    return mux
}

func writeJSON(w http.ResponseWriter, payload any) {
    w.Header().Set("Content-Type", "application/json")
    _ = json.NewEncoder(w).Encode(payload)
}
