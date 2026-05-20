# Contributing to SAMOS

Thank you for your interest in contributing to SAMOS (Secure Advanced MLOps & Orchestration System).

## Getting Started

### Prerequisites

- Python 3.12+
- Git
- (Optional) Docker & Docker Compose for infrastructure services

### Setup

```bash
# Clone the repository
git clone https://github.com/YOUR_ORG/SAMOS.git
cd SAMOS

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\Activate.ps1  # Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp env.example .env
# Edit .env with your actual values
```

### Running Tests

```bash
# Run the full test suite
python -m pytest tests/ -v

# Run a specific pillar
python -m pytest tests/test_data_ops.py -v
python -m pytest tests/test_ml_ops.py -v
python -m pytest tests/test_model_sec.py -v
python -m pytest tests/test_sre_devsecops.py -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### Running the Application

```bash
# Start the FastAPI server (local dev)
python src/sre/serve.py

# Start with Docker
docker-compose up samos-api

# Start with full infrastructure (NiFi + Airflow)
docker-compose --profile nifi --profile airflow up
```

---

## Code Standards

### Style

- **Formatter**: `ruff format` (line length 100)
- **Linter**: `ruff check` with `E`, `F`, `B`, `S` rules enabled
- **Type checker**: `mypy --strict` (missing imports ignored)

### Testing

- Write tests for all new functionality
- Place tests in the appropriate pillar file (`test_data_ops.py`, `test_ml_ops.py`, etc.)
- Use `conftest.py` fixtures — don't add `sys.path` hacks in test files
- Target: 80%+ line coverage

### Logging

- Import the centralized logger: `from src.logging_config import get_logger`
- Never use `print()` for operational output
- Use `logger.exception()` (not `logger.error()`) when catching exceptions

### Imports

- Use `from src.MODULE.FILE import FUNCTION` — no relative imports
- Guard optional heavy dependencies with `try/except ImportError`

---

## Pull Request Process

1. **Branch naming**: `feat/short-description`, `fix/short-description`, `docs/short-description`
2. **Commit messages**: Use [Conventional Commits](https://www.conventionalcommits.org/)
   - `feat: add MAB state persistence to Redis`
   - `fix: correct k8s containerPort from 8000 to 7860`
   - `docs: add CONTRIBUTING.md`
3. **Before submitting**:
   - Run `ruff check .` — zero warnings
   - Run `python -m pytest tests/` — all tests passing
   - Update `CHANGELOG.md` under `[Unreleased]`
4. **Review**: At least 1 approving review required before merge

---

## Architecture Overview

SAMOS is organized into 6 pillars:

| Pillar       | Directory            | Phases       |
| ------------ | -------------------- | ------------ |
| DataOps      | `src/data_ops/`      | 1–5          |
| MLOps        | `src/ml_ops/`        | 6–11         |
| ModelSecOps  | `src/model_sec/`     | 12–16        |
| DevSecOps    | `src/devsecops/`     | 17–20        |
| SRE          | `src/sre/`           | 21–25        |
| Integrations | `src/integrations/`  | Cross-cutting|

See [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for detailed module descriptions.

---

## Reporting Issues

- Use GitHub Issues with the appropriate label (`bug`, `enhancement`, `security`)
- For security vulnerabilities, **do not** open a public issue — email the maintainers directly
