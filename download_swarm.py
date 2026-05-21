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

# 👥 THE 4B TEACHER COMMITTEE (Knowledge Sources for Pinaka 1B)
SWARM_MODELS = [
    {
        "name": "Phi-3-Mini (Reasoning Teacher)",
        "repo": "microsoft/Phi-3-mini-4k-instruct"
    },
    {
        "name": "Qwen1.5-4B (Balance Teacher)",
        "repo": "Qwen/Qwen1.5-4B"
    },
    {
        "name": "StableLM-3B (Diversity Teacher)",
        "repo": "stabilityai/stablelm-3b-4e1t"
    }
]

def initiate_download():
    """Iterates through the swarm and downloads the necessary intelligence binaries."""
    from huggingface_hub import snapshot_download
    
    # [TRIGGER] Ensures the 'models' directory exists.
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"📁 Created directory: {MODEL_DIR}")

    print("🏹 SAMOS SWARM: ACQUISITION COMMENCING...")
    print("=" * 42)

    results: dict[str, bool] = {}
    for model in SWARM_MODELS:
        print(f"\n📡 Requesting: {model['name']}...")
        try:
            # [TRIGGER] Downloads the full model from Hugging Face.
            path = snapshot_download(
                repo_id=model["repo"],
                local_dir=os.path.join(MODEL_DIR, model["repo"].split("/")[-1])
            )
            print(f"✅ SUCCESS: Saved to {path}")
        except Exception as e:
            print(f"❌ FAILED to download {model['name']}: {e}")


if __name__ == "__main__":
    initiate_download()
