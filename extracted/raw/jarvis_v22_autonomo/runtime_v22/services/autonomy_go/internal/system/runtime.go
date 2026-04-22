package system

import (
    "bytes"
    "os/exec"
    "strings"
)

func DetectDocker() (bool, string) {
    cmd := exec.Command("docker", "--version")
    var out bytes.Buffer
    cmd.Stdout = &out
    cmd.Stderr = &out
    if err := cmd.Run(); err != nil {
        return false, ""
    }
    return true, strings.TrimSpace(out.String())
}

func DetectOllamaModels() (bool, []string) {
    cmd := exec.Command("ollama", "list")
    var out bytes.Buffer
    cmd.Stdout = &out
    cmd.Stderr = &out
    if err := cmd.Run(); err != nil {
        return false, nil
    }
    lines := strings.Split(out.String(), "\n")
    models := make([]string, 0)
    for i, line := range lines {
        if i == 0 {
            continue
        }
        fields := strings.Fields(line)
        if len(fields) > 0 {
            models = append(models, fields[0])
        }
    }
    return true, models
}
