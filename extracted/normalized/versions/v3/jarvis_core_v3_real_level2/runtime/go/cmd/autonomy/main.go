package main

import (
    "encoding/json"
    "log"
    "net/http"
)

type ExecuteRequest struct {
    Mission string `json:"mission"`
}

type ExecuteResponse struct {
    Ok      bool   `json:"ok"`
    Status  string `json:"status"`
    Message string `json:"message"`
}

func main() {
    mux := http.NewServeMux()
    mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
        respondJSON(w, map[string]any{"ok": true, "service": "autonomy-go", "status": "healthy"})
    })
    mux.HandleFunc("/runtime", func(w http.ResponseWriter, r *http.Request) {
        respondJSON(w, map[string]any{"ok": true, "runtime": "go", "mode": "level2"})
    })
    mux.HandleFunc("/execute", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != http.MethodPost {
            w.WriteHeader(http.StatusMethodNotAllowed)
            respondJSON(w, ExecuteResponse{Ok: false, Status: "error", Message: "POST required"})
            return
        }
        var req ExecuteRequest
        _ = json.NewDecoder(r.Body).Decode(&req)
        respondJSON(w, ExecuteResponse{Ok: true, Status: "accepted", Message: "mission accepted: " + req.Mission})
    })

    log.Println("autonomy-go listening on :8085")
    log.Fatal(http.ListenAndServe(":8085", mux))
}

func respondJSON(w http.ResponseWriter, payload any) {
    w.Header().Set("Content-Type", "application/json")
    _ = json.NewEncoder(w).Encode(payload)
}
