.PHONY: lint test build serve compose-up clean help

help:
	@echo "SAMOS Enterprise Makefile"
	@echo "---------------------------------------"
	@echo "lint        - Run ruff (linter) and bandit (security scanner)"
	@echo "test        - Run pytest with coverage"
	@echo "build       - Build the SAMOS Docker image"
	@echo "serve       - Run the FastAPI server locally"
	@echo "compose-up  - Start the core infrastructure (API, MLflow, Redis, Prometheus, Grafana)"
	@echo "clean       - Remove __pycache__ and coverage artifacts"

lint:
	ruff check src/ && bandit -r src/ -ll

test:
	python -m pytest tests/ -v --cov=src

build:
	docker build -t samos:dev .

serve:
	python src/sre/serve.py

compose-up:
	docker-compose up -d samos-api mlflow-server redis-cache prometheus grafana

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -f .coverage coverage.xml
	rm -rf .pytest_cache .ruff_cache .hypothesis
