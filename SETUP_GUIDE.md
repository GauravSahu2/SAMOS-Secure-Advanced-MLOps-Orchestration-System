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

To ensure everything is working correctly on your hardware, you can run the full factory or trigger specific phases.

#### Option A: Full 25-Phase Factory

```powershell
# Windows
samos --all

# Linux/macOS
./samos --all
```

#### Option B: Granular Phase Control

Trigger only the phases you need (e.g., DataOps domain followed by specific MLOps phases):

```bash
# Trigger the entire DataOps group
samos --group dataops

# Trigger multiple phases (e.g., 1, 2, 4 and 9)
samos --phases 1,2,4,9

# Trigger a range of phases (e.g., 3 to 10)
samos --phases 3-10

# Combine groups (e.g., DataOps and DevSecOps)
samos --groups dataops,devsecops
```

### Step 4: Start the Production Server

Once the factory finishes (reaches "SINGULARITY"), you can serve the model:

```bash
uvicorn src.sre.serve:app --reload
```

The API will be available at <http://127.0.0.1:8000/docs>.

---

## 🚀 3. SAMOS 1B Distillation Forge (Heterogeneous Swarm)

The SAMOS 1B Forge is a specialized high-performance training pipeline designed to saturate local silicon (NVIDIA + Intel) while maintaining system stability.

### Key Features

- **Heterogeneous Orchestration**: Automatically leverages NVIDIA CUDA, Intel iGPU, and Intel NPU simultaneously.
- **80% Compute Saturation**: Targets 80% utilization across all devices to maximize throughput without overheating.
- **8GB RAM Guard**: Hard-coded safety reservation that pauses the forge if system RAM exceeds `Total - 8GB`.
- **VRAM Optimization**: Uses Gradient Checkpointing and Gradient Accumulation to fit 1B+ parameter models on 8GB VRAM cards.

### Launching the Forge

```bash
# Launch the automated master forge
python samos_master.py
```

### Hardware Monitoring

The forge provides real-time telemetry:

- **GPU0**: Primary student training (NVIDIA).
- **Intel Ops**: Synthetic teacher inference throughput (NPU/iGPU).
- **RAM**: Total system usage vs. safety budget.
- **ETA**: Real-time time-to-completion forecasting based on step throughput.

---

## 🏗️ 4. Deploying as a Pipeline

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
| **NVIDIA GPU** | Supported | Uses CUDA (Torch) for training. Supports Gradient Checkpointing. |
| **Intel NPU/Arc** | Supported | Uses OpenVINO for Teacher Inference offloading. |
| **CPU Only** | Supported | Graceful fallback; system runs simulation-heavy logic. |
| **Low RAM** | Protected | **8GB RAM Guard** ensures system stability by pausing the forge. |

---

> [!IMPORTANT]
> **Silicon Safety**: On NVIDIA hardware, Phase 28 (Thermal Watchdog) is active. If temperatures exceed 85°C, the forge will enter a dynamic polling loop until temperatures return to 75°C, ensuring minimal downtime while protecting hardware.
