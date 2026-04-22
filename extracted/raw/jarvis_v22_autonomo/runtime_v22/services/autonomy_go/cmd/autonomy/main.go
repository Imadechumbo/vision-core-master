package main

import (
    "log"
    "net/http"
    "os"

    "jarvis/autonomy_go/internal/server"
)

func main() {
    port := os.Getenv("JARVIS_GO_PORT")
    if port == "" {
        port = "8088"
    }

    mux := server.NewMux()
    log.Printf("[autonomy-go] listening on :%s", port)
    if err := http.ListenAndServe(":"+port, mux); err != nil {
        log.Fatal(err)
    }
}
