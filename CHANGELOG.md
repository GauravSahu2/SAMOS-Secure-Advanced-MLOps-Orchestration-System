# Changelog

All notable changes to the SAMOS project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-05-19

### Added

- **Airflow DAG** (`configs/airflow_dags/samos_pipeline_dag.py`) — full 25-phase pipeline orchestration
- **NiFi + Airflow** dual-orchestration in `docker-compose.yml` (profile-gated)
- **`/health` endpoint** on `serve.py` — liveness & readiness probe for K8s
- **MAB Thompson-Sampling routing** wired into `/predict`
- **Security middleware** — OWASP headers + sliding-window rate limiter
- **Real KD distillation loss** in `pinaka_forge_v2.py` (KL-divergence + temperature scaling)
- **Dual-path model evaluation** in `evaluate.py` (LLM perplexity + sklearn K-fold)
- **Real metric sources** in `incident_response.py` (Prometheus → MLflow → forge state)
- **LSB steganographic watermarking** in `watermark.py`
- **Hash-chained JSONL ledger** in `ledger.py`
- **Centralized logging** via `src/logging_config.py`
- **Comprehensive test suite** — 57 tests across 4 pillars
- **`conftest.py`** with shared fixtures and `sys.path` setup
- **Prometheus metrics** exported from `serve.py` (request count, latency, MAB routing)
- **MAB state persistence** to Redis (load on startup, save on update)
- **Startup env-var validation** — warns on insecure defaults
- **`TOOLS.md`** — CLI tool installation guide (trivy, gitleaks, cosign, etc.)
- **`CONTRIBUTING.md`** — contributor guidelines
- **Property-based fuzz tests** using `hypothesis`
- **Integration (e2e) tests** — full pipeline and API roundtrip
- **`gauntlet.yml`** and **`pipeline.yml`** workflows enabled
- **`__version__`** variable in `src/__init__.py`

### Changed

- **`requirements.txt`** — removed uninstallable CLI tools (trivy, gitleaks, cosign, keda, etc.)
- **`Dockerfile`** — no longer bakes model weights into the image; uses volume mounts
- **`k8s-deployment.yaml`** — fixed port 8000→7860, added readinessProbe on `/health`
- **`pyproject.toml`** — restored `--cov` flags, added `pytest-asyncio` mode
- **`download_swarm.py`** — retry logic, cache detection, `ModelSpec` TypedDict
- **`airflow_sync.py`** — now delegates to the real DAG, not a dead stub
- **`vault_manager.py`** — real HVAC integration with environment-based fallback

### Fixed

- All static analysis warnings resolved (0 IDE errors)
- `evaluate.py` no longer hardcoded to `churn_model.pkl`
- `incident_response.py` no longer uses hardcoded `accuracy = 0.40`
- Cognitive complexity reduced in `evaluate.py` and `incident_response.py`
- `test_pipeline.py` rewritten to use `conftest.py` fixtures

### Removed

- `docker-compose.enterprise.yml` — superseded by `--profile enterprise` on main compose
- `test.yml` at project root — leftover stub
- `package.json` at project root — unused JavaScript scaffolding
- `.disabled` workflow extensions — replaced with active `.yml` files
- Committed log files (`pinaka_forge.log`, `pinaka_forge_live.log`, `samos_master.log`)

## [1.0.0] - 2026-05-01

### Initial Release

- Initial 25-phase SAMOS pipeline across 6 pillars
- DataOps: ingest, validate, mask_pii, anomaly_inversion, genetic_features
- MLOps: NAS, personalization, automl, distillation, federated learning
- ModelSecOps: bias audit, adversarial testing, counterfactuals, model cards, ZKP guard
- DevSecOps: zero-trust, advanced security, dependency patching, self-healing code
- SRE: serve, chaos monkey, concept drift, power optimizer, incident response
- CI/CD: GitHub Actions workflows for CI, HuggingFace CD, Render CD
- Infrastructure: Docker, docker-compose, Kubernetes manifests
