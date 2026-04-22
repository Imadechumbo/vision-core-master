package main

import (
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"net/http"
	"time"
)

func main() {
	host := flag.String("host", "127.0.0.1", "host")
	port := flag.Int("port", 8090, "port")
	flag.Parse()

	mux := http.NewServeMux()
	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"ok": true, "name": "jarvis-runtime-go", "time": time.Now().UTC().Format(time.RFC3339)})
	})
	mux.HandleFunc("/runtime", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"ok": true, "component": "runtime-go", "endpoints": []string{"/health", "/runtime", "/execute"}})
	})
	mux.HandleFunc("/execute", func(w http.ResponseWriter, r *http.Request) {
		writeJSON(w, map[string]any{"ok": true, "message": "execução delegada ao orquestrador principal"})
	})

	addr := fmt.Sprintf("%s:%d", *host, *port)
	log.Printf("runtime-go ouvindo em http://%s", addr)
	log.Fatal(http.ListenAndServe(addr, mux))
}

func writeJSON(w http.ResponseWriter, payload map[string]any) {
	w.Header().Set("Content-Type", "application/json")
	_ = json.NewEncoder(w).Encode(payload)
}
