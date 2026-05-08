# 🚀 SAMOS: Comprehensive Setup & Deployment Guide

This guide provides step-by-step instructions for running the **Secure Advanced MLOps & Orchestration System (SAMOS)** on any local machine, deploying it as a production pipeline, and configuring the GitHub Actions Gauntlet.

---

## 💻 1. Local System Setup

SAMOS is designed to be hardware-agnostic. It will automatically detect and utilize NVIDIA GPUs or Intel NPUs if present, otherwise falling back to optimized CPU execution.

### Prerequisites

- **Python**: 3.12+
- **Git**: For version control.
- **Docker**: (Optional) For containerized deployment.

### Step 1: Clone and Initialize

```bash
# Clone the repository
git clone https://github.com/GauravSahu2/SAMOS-Secure-Advanced-MLOps-Orchestration-System.git
cd SAMOS

# Create a virtual environment
python -m venv venv

# Activate the environment
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

### Step 2: Install Dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 3: Run the Factory (Validation)

To ensure everything is working correctly on your hardware, run the **Quick Test** mode. This executes all 25+ phases with a reduced workload.

```powershell
# Windows (PowerShell)
$env:FORGE_QUICK_TEST="1"; python main.py

# Linux/macOS
FORGE_QUICK_TEST=1 python main.py
```

### Step 4: Start the Production Server

Once the factory finishes (reaches "SINGULARITY"), you can serve the model:

```bash
uvicorn src.sre.serve:app --reload
```

The API will be available at <http://127.0.0.1:8000/docs>.

---

## 🏗️ 2. Deploying as a Pipeline

SAMOS is a modular factory. You can deploy specific domains or the full orchestrator.

### Docker Deployment

Build the high-assurance production image:

```bash
docker build -t samos-factory:latest .

# Run the container
docker run -p 8000:8000 samos-factory:latest
```

### CI/CD Orchestration

The project is designed for **GitOps** workflows.

1. **ArgoCD**: Point your ArgoCD application to the `kubernetes/` folder (if available) or use the Docker image in a Deployment manifest.
2. **MLflow Registry**: The pipeline uses a local SQLite backend by default (`mlflow.db`). For production, update `main.py` to point to a centralized MLflow server:

    ```python
    os.environ['MLFLOW_TRACKING_URI'] = "https://your-mlflow-server.com"
    ```

---

## 🛡️ 3. GitHub Actions Setup

The **SAMOS Gauntlet** is currently preserved in the repository but disabled by default to prevent accidental runs during setup.

### Step 1: Re-enable Workflows

1. Navigate to `.github/workflows/`.
2. Rename `gauntlet.yml.disabled` to `gauntlet.yml`.
3. Rename `pipeline.yml.disabled` to `pipeline.yml`.
4. Open the files and uncomment the `on:` trigger section:

    ```yaml
    on:
      push:
        branches: [ main, master ]
      pull_request:
        branches: [ main, master ]
    ```

### Step 2: Configure Repository Secrets

To enable the full 32-tier validation (SonarQube, Gitleaks), add the following secrets in your GitHub Repository Settings (`Settings > Secrets and variables > Actions`):

| Secret Name | Description |
| :--- | :--- |
| `SONAR_TOKEN` | Your SonarQube project token. |
| `SONAR_HOST_URL` | Your SonarQube server URL (e.g., <https://sonarcloud.io>). |
| `DOCKER_PASSWORD` | (Optional) For pushing images to Docker Hub. |

### Step 3: Trigger the Gauntlet

Simply push a change to the `main` branch:

```bash
git add .
git commit -m "Enable SAMOS Gauntlet"
git push origin main
```

View the results in the **Actions** tab of your GitHub repository.

---

## 🛠️ Hardware Fallbacks & Performance

| Hardware | Status | Behavior |
| :--- | :--- | :--- |
| **NVIDIA GPU** | Supported | Uses CUDA (Torch) for Phase 9 Training. |
| **Intel NPU/Arc** | Supported | Uses OpenVINO for Phase 9 Training. |
| **CPU Only** | Supported | Graceful fallback; system runs simulation-heavy logic. |
| **Low RAM** | Supported | Uses streaming ingestion (Phase 1) to manage memory. |

---

> [!IMPORTANT]
> **Silicon Safety**: On high-end NVIDIA hardware, Phase 28 (Thermal Watchdog) is active. If temperatures exceed 85°C, the forge will pause for 10 minutes to prevent silicon degradation.
