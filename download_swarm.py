"""
download_swarm.py — Swarm Acquisition Engine
FIX APPLIED (Gap #6):
    Added robust per-model error handling and retry logic.
    A single failed download no longer crashes the whole script.
    An exit-code summary is printed at the end so samos_master.py can
    make an informed decision about whether to proceed with the forge.
"""

import os
import sys
import time
from typing import TypedDict

# [TRIGGER] Checks if the huggingface_hub library is installed.
try:
    from huggingface_hub import snapshot_download
except ImportError:
    print("❌ ERROR: 'huggingface_hub' not found. Run 'pip install huggingface_hub' first.")
    sys.exit(1)

# 📂 TARGET DIRECTORY
MODEL_DIR = "models"


class ModelSpec(TypedDict):
    """Schema for each teacher model entry in SWARM_MODELS."""
    name: str
    repo: str
    required: bool


# 👥 THE 4B TEACHER COMMITTEE (Knowledge Sources for Pinaka 1B)
SWARM_MODELS: list[ModelSpec] = [
    {
        "name": "Phi-3-Mini (Reasoning Teacher)",
        "repo": "microsoft/Phi-3-mini-4k-instruct",
        "required": True,   # Forge will abort if a *required* model fails
    },
    {
        "name": "Qwen1.5-4B (Balance Teacher)",
        "repo": "Qwen/Qwen1.5-4B",
        "required": False,  # Optional — forge degrades gracefully
    },
    {
        "name": "StableLM-3B (Diversity Teacher)",
        "repo": "stabilityai/stablelm-3b-4e1t",
        "required": False,
    },
]

MAX_RETRIES = 3
RETRY_DELAY_SECONDS = 5


def download_model(model: ModelSpec, model_dir: str) -> bool:
    """
    Downloads a single model with retry logic.

    Returns:
        True  if the download succeeded.
        False if all retries were exhausted.
    """
    local_dir = os.path.join(model_dir, model["repo"].split("/")[-1])

    # Skip if already present
    local_files = os.listdir(local_dir) if os.path.isdir(local_dir) else []
    has_weights = any(
        f.endswith((".bin", ".safetensors", ".gguf")) for f in local_files
    )
    if os.path.isdir(local_dir) and has_weights:
        print(f"  ✅ CACHE HIT: {model['name']} already downloaded at {local_dir}")
        return True

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  📡 Attempt {attempt}/{MAX_RETRIES}: Downloading {model['name']}...")
            path = snapshot_download(
                repo_id=model["repo"],
                local_dir=local_dir,
            )
            print(f"  ✅ SUCCESS: {model['name']} saved to {path}")
            return True
        except Exception as exc:
            print(f"  ⚠️ Attempt {attempt} FAILED for {model['name']}: {exc}")
            if attempt < MAX_RETRIES:
                print(f"  ⏳ Retrying in {RETRY_DELAY_SECONDS}s...")
                time.sleep(RETRY_DELAY_SECONDS)

    print(f"  ❌ FATAL: Could not download {model['name']} after {MAX_RETRIES} attempts.")
    return False


def initiate_download() -> bool:
    """
    Iterates through the swarm and downloads all teacher models.

    Returns:
        True  if all *required* models downloaded successfully.
        False if any required model failed.
    """
    os.makedirs(MODEL_DIR, exist_ok=True)

    print("🏹 SAMOS SWARM: ACQUISITION COMMENCING...")
    print("=" * 42)

    results: dict[str, bool] = {}
    for model in SWARM_MODELS:
        model_name: str = model["name"]
        print(f"\n📡 Requesting: {model_name}...")
        results[model_name] = download_model(model, MODEL_DIR)

    # ── Summary ────────────────────────────────────────────────────────────
    print("\n" + "=" * 42)
    print("📊 DOWNLOAD SUMMARY")
    print("=" * 42)
    all_required_ok = True
    for model in SWARM_MODELS:
        model_name = model["name"]
        passed = results[model_name]
        if passed:
            status = "✅"
        elif model["required"]:
            status = "❌ REQUIRED"
        else:
            status = "⚠️ optional"
        print(f"  {status}  {model_name}")
        if not passed and model["required"]:
            all_required_ok = False

    if all_required_ok:
        print("\n🏆 SWARM BUNDLE READY. Proceeding to forge.")
        print("👉 Next Step: Run 'python samos_master.py' to start the forge.")
    else:
        print("\n❌ One or more REQUIRED teachers failed to download.")
        print("   The forge cannot guarantee full distillation quality.")
        print("   Fix network/auth issues and re-run: python download_swarm.py")

    return all_required_ok


if __name__ == "__main__":
    success = initiate_download()
    sys.exit(0 if success else 1)
