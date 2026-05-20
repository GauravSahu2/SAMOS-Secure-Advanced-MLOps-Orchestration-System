# 🛠️ SAMOS: CLI Tool Installation Guide

These tools are **not pip-installable** — they are standalone binaries used in CI/CD pipelines
and local security workflows. Install them separately.

> **Note**: Most of these are pre-installed in CI runners (GitHub Actions) via dedicated action
> steps. You only need to install locally if running security scans on your own machine.

---

## Container & Image Security

### Trivy — Vulnerability Scanner

```bash
# macOS
brew install aquasecurity/trivy/trivy

# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# Windows (scoop)
scoop install trivy
```

### Cosign — Container Image Signing

```bash
# macOS
brew install cosign

# Linux
go install github.com/sigstore/cosign/v2/cmd/cosign@latest

# Windows
scoop install cosign
```

---

## Secret Detection

### Gitleaks — Git Secret Scanner

```bash
# macOS
brew install gitleaks

# Linux
curl -sSfL https://github.com/gitleaks/gitleaks/releases/latest/download/gitleaks-linux-amd64 -o /usr/local/bin/gitleaks && chmod +x /usr/local/bin/gitleaks

# Windows
scoop install gitleaks
```

---

## Kubernetes Security

### Kubescape — K8s Security Posture

```bash
# macOS / Linux
curl -s https://raw.githubusercontent.com/kubescape/kubescape/master/install.sh | /bin/bash

# Windows
iwr -useb https://raw.githubusercontent.com/kubescape/kubescape/master/install.ps1 | iex
```

### KEDA — Kubernetes Event-Driven Autoscaling

```bash
# Install via Helm (cluster-level, not local)
helm repo add kedacore https://kedacore.github.io/charts
helm install keda kedacore/keda --namespace keda --create-namespace
```

---

## Orchestration CLIs

### Argo Workflows — Workflow Engine

```bash
# macOS
brew install argo

# Linux
curl -sLO https://github.com/argoproj/argo-workflows/releases/latest/download/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz && chmod +x argo-linux-amd64 && mv argo-linux-amd64 /usr/local/bin/argo
```

### Chaos Mesh — Chaos Engineering

```bash
# Install via Helm (cluster-level)
helm repo add chaos-mesh https://charts.chaos-mesh.org
helm install chaos-mesh chaos-mesh/chaos-mesh --namespace chaos-mesh --create-namespace
```

---

## Security Platforms

### DefectDojo — Vulnerability Management

```bash
# Docker-based deployment (not a CLI tool)
docker-compose -f docker-compose.defectdojo.yml up -d
# Python client: pip install defectdojo-api  (if available on PyPI)
```

### Falco — Runtime Security

```bash
# Linux only (kernel module)
curl -fsSL https://falco.org/repo/falcosecurity-packages.asc | sudo gpg --dearmor -o /usr/share/keyrings/falco-archive-keyring.gpg
echo "deb [signed-by=/usr/share/keyrings/falco-archive-keyring.gpg] https://download.falco.org/packages/deb stable main" | sudo tee /etc/apt/sources.list.d/falcosecurity.list
sudo apt update && sudo apt install falco
```

---

## Usage in CI/CD

All these tools are installed automatically in GitHub Actions via dedicated steps.
See `.github/workflows/gauntlet.yml` for the full security pipeline.

```yaml
# Example: Trivy in GitHub Actions
- name: Run Trivy vulnerability scanner
  uses: aquasecurity/trivy-action@master
  with:
    image-ref: 'samos:latest'
    format: 'sarif'
    output: 'trivy-results.sarif'
```
