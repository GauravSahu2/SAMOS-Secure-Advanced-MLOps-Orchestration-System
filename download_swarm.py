"""
====================================================================================================
FILE: download_swarm.py
ROLE: The Swarm Acquisition Engine
TRIGGER: Triggered manually by the user to download the specialist coding models.
====================================================================================================
"""

import os            # Imports OS for directory management.
import sys           # Imports Sys for platform checking.

# [TRIGGER] Checks if the huggingface_hub library is installed.
try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("❌ ERROR: 'huggingface_hub' not found. Run 'pip install huggingface_hub' first.")
    sys.exit(1)

# 📂 TARGET DIRECTORY
MODEL_DIR = "models" # [TRIGGER] Files will be saved here.

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
    print("==========================================")

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

    print("\n" + "="*40)
    print("🏆 SWARM BUNDLE READY.")
    print("👉 Next Step: Restart 'serve.py' to activate the CS Committee.")
    print("="*40)

if __name__ == "__main__":
    initiate_download()
