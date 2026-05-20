# 🚀 SAMOS: Where to Deploy & CI/CD Setup Guide

---

## The Core Problem Diagnosed

Both existing workflows were **commented out at the `on:` trigger block** AND renamed to `.disabled`. GitHub Actions **ignores any file that doesn't end in `.yml` or `.yaml`**. That's why nothing ever ran.

**3 new live workflow files have been created:**

| File | Trigger | Purpose |
|---|---|---|
| `.github/workflows/ci.yml` | Every push + PR to `main` | Lint → SAST → Tests → Docker build → SBOM |
| `.github/workflows/cd_huggingface.yml` | `git tag v1.0.0` push | Deploy serving layer to Hugging Face Spaces |
| `.github/workflows/cd_render.yml` | Push to `main` (serve.py changes) | Build Docker image + deploy to Render.com |

---

## What to Deploy Where

SAMOS has **3 separate deployable components.** They should go to different platforms:

```
SAMOS
├── 🧠 API / Inference Server  (src/sre/serve.py)  → Render.com  OR  HF Spaces
├── 📊 Infra Stack             (MLflow, Redis, NiFi) → Railway.app OR  Docker locally
└── 🔥 Training Forge          (pinaka_forge_v2.py)  → Your local machine (ONLY)
```

> [!IMPORTANT]
> **The forge should NEVER be deployed to the cloud.** 4M training steps on a cloud GPU would cost thousands of dollars. The forge runs on your local NVIDIA+Intel machine. Only the **API server** gets deployed.

---

## Platform Decision Matrix

| Platform | Best For | Cost | GPU | Ease |
|---|---|---|---|---|
| **Hugging Face Spaces** | Public demo, portfolio visibility | Free | No | ⭐⭐⭐⭐⭐ |
| **Render.com** | Always-on API, auto-deploy from Docker Hub | Free tier (spins down) | No | ⭐⭐⭐⭐ |
| **Railway.app** | Full infra stack (MLflow+Redis+NiFi) | ~$5/mo | No | ⭐⭐⭐⭐ |
| **Google Cloud Run** | Serverless, scales to zero, production-grade | Pay per request | No | ⭐⭐⭐ |
| **AWS EC2 / Lambda** | Enterprise, maximum control | Pay as you go | Yes (p3/g4) | ⭐⭐ |

### 🎯 Recommended Setup (Free & Zero Cost)

```
GitHub Repo
    ↓ push to main
GitHub Actions CI (ci.yml) — always runs
    ↓ on tag push (v1.0.0)
GitHub Actions CD → Hugging Face Spaces (FREE demo)
    ↓ simultaneously
GitHub Actions CD → Render.com (FREE API endpoint)
```

---

## Step 1: Fix the Disabled Workflows

The old files must be deleted (or renamed back). The 3 new `.yml` files are already created.

Optionally, delete the dead stubs:
```bash
git rm .github/workflows/gauntlet.yml.disabled
git rm .github/workflows/pipeline.yml.disabled
git commit -m "ci: replace disabled stubs with live CI/CD workflows"
git push
```

---

## Step 2: Add GitHub Secrets

Go to: **GitHub Repo → Settings → Secrets and variables → Actions → New repository secret**

### For `ci.yml` (Required)
| Secret Name | Where to Get It |
|---|---|
| `CODECOV_TOKEN` | Sign up at [codecov.io](https://codecov.io), connect repo, copy token |
| `SONAR_TOKEN` | [SonarCloud.io](https://sonarcloud.io) → Your account → Security → Generate token |
| `SONAR_HOST_URL` | Use `https://sonarcloud.io` (free for public repos) |

> [!TIP]
> SonarQube in `ci.yml` is set to `continue-on-error: true` so it won't block your CI even before you set up Sonar.

### For `cd_huggingface.yml` (Required for HF deploy)
| Secret Name | Where to Get It |
|---|---|
| `HF_TOKEN` | [HuggingFace](https://huggingface.co/settings/tokens) → New token (Write access) |
| `HF_SPACE_ID` | The Space identifier e.g. `GauravSahu/SAMOS` |

**Setup HF Space first:**
1. Go to https://huggingface.co/new-space
2. Select **Docker** as the SDK
3. Name it `SAMOS`
4. That creates `GauravSahu/SAMOS` — use that as `HF_SPACE_ID`

### For `cd_render.yml` (Required for Render deploy)
| Secret Name | Where to Get It |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub → Account Settings → Security → New Access Token |
| `RENDER_DEPLOY_HOOK_URL` | Render dashboard → Your service → Settings → Deploy Hooks → Create |

---

## Step 3: Deploy to Hugging Face Spaces (Manual First Run)

Before the CD workflow can push, the Space must exist. Do this once:

```bash
# Install HF CLI
pip install huggingface_hub

# Login
huggingface-cli login  # paste your HF_TOKEN

# Push initial version manually
cd SAMOS
huggingface-cli upload GauravSahu/SAMOS samos_dashboard.html /samos_dashboard.html
huggingface-cli upload GauravSahu/SAMOS src/ /src/
huggingface-cli upload GauravSahu/SAMOS requirements.txt /requirements.txt
```

After that, every `git tag v1.x.x && git push --tags` auto-deploys.

---

## Step 4: Deploy to Render.com

1. Go to [render.com](https://render.com) → **New Web Service**
2. Connect your GitHub repo
3. Settings:
   - **Environment:** Docker
   - **Dockerfile Path:** `./Dockerfile`
   - **Port:** `7860`
   - **Plan:** Free
4. Add environment variables:
   ```
   PORT=7860
   PYTHONPATH=.
   ```
5. Copy the **Deploy Hook URL** → add to GitHub Secrets as `RENDER_DEPLOY_HOOK_URL`

---

## Step 5: Deploy Infrastructure Stack (MLflow + Redis) to Railway

This is for `mlflow.db` and `Redis` — the shared state that all phases use.

```bash
# Install Railway CLI
npm install -g @railway/cli
railway login

# Inside the SAMOS directory
railway init
railway up --service mlflow-server --docker docker-compose.yml
```

Or use the Railway dashboard to deploy from `docker-compose.yml` directly.

---

## CI/CD Flow Diagram

```
Developer pushes code
        │
        ▼
┌─────────────────────────────────────────┐
│  ci.yml (ALWAYS runs on push + PR)      │
│  1. Ruff lint                           │
│  2. Bandit SAST                         │
│  3. MyPy type check                     │
│  4. Gitleaks secret scan                │
│  5. Pytest + coverage                   │
│  6. SonarQube                           │
│  7. Docker build validation             │
│  8. Trivy container scan                │
│  9. SBOM (on main only)                 │
└─────────────────────────────────────────┘
        │
        │  If pushing to main + serve.py changed
        ▼
┌─────────────────────────────────────────┐
│  cd_render.yml                          │
│  1. Build Docker image                  │
│  2. Push to Docker Hub                  │
│  3. Trigger Render redeploy             │
└─────────────────────────────────────────┘
        │
        │  If pushing a version tag (v1.x.x)
        ▼
┌─────────────────────────────────────────┐
│  cd_huggingface.yml                     │
│  1. Sync src/sre + dashboard to HF      │
│  2. Push to HF Space repo               │
│  3. HF auto-deploys Docker container    │
└─────────────────────────────────────────┘
```

---

## What Each Workflow Does NOT Do (By Design)

| Excluded | Reason |
|---|---|
| `pip install -r requirements.txt` in full | `requirements.txt` has 120+ packages including `apache-airflow`, `pyspark`, `vllm` — this would take 30+ minutes. CI uses only the packages needed for analysis and tests. |
| Run `python main.py` (full pipeline) | The full 25-phase pipeline needs real data, models, and hardware. CI only validates code correctness. |
| Run `pinaka_forge_v2.py` | Training runs on local NVIDIA hardware. Cloud CI runners have no GPU. |
| Auto-deploy on every push | CD only triggers on specific tags or serve.py changes to avoid noisy deploys. |

---

## Quick Start Commands

```bash
# Step 1: Activate the CI (just push to main)
git add .github/workflows/ci.yml
git commit -m "ci: activate SAMOS validation gauntlet"
git push origin main  # CI triggers automatically

# Step 2: First production deploy
git tag v1.0.0
git push --tags  # Triggers HF Spaces CD

# Step 3: Test your deployed API
curl https://your-samos-space.hf.space/predict \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello SAMOS"}'
```
