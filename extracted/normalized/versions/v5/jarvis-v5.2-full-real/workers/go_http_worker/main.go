package main

import (
	"encoding/json"
	"log"
	"net/http"
)

type Health struct {
	Ok      bool   `json:"ok"`
	Service string `json:"service"`
}

func healthHandler(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	resp := Health{Ok: true, Service: "jarvis-v5-go-http-worker"}
	json.NewEncoder(w).Encode(resp)
}

func main() {
	http.HandleFunc("/health", healthHandler)
	log.Println("go_http_worker listening on :8099")
	log.Fatal(http.ListenAndServe(":8099", nil))
}
