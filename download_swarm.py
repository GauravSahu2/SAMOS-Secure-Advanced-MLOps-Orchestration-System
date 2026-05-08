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

# 👥 THE CS COMMITTEE SPECIALISTS (GGUF Quantized for speed)
SWARM_MODELS = [
    {
        "name": "Qwen-Coder (Syntax Master)",
        "repo": "Qwen/Qwen2.5-Coder-1.5B-Instruct-GGUF",
        "file": "qwen2.5-coder-1.5b-instruct-q4_k_m.gguf"
    },
    {
        "name": "DeepSeek-Coder (Logic Engine)",
        "repo": "deepseek-ai/deepseek-coder-1.3b-instruct",
        "file": "pytorch_model.bin" # Using small-footprint torch weights.
    }
]

def initiate_download():
    """Iterates through the swarm and downloads the necessary intelligence binaries."""
    
    # [TRIGGER] Ensures the 'models' directory exists.
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)
        print(f"📁 Created directory: {MODEL_DIR}")

    print("🏹 SAMOS SWARM: ACQUISITION COMMENCING...")
    print("==========================================")

    for model in SWARM_MODELS:
        print(f"\n📡 Requesting: {model['name']}...")
        try:
            # [TRIGGER] Downloads the specific file from Hugging Face.
            # Rationale: We download specific quantized files to ensure 
            # they fit in your laptop's RAM alongside SAMOS 4B.
            path = hf_hub_download(
                repo_id=model["repo"],
                filename=model["file"],
                local_dir=MODEL_DIR,
                local_dir_use_symlinks=False
            )
            print(f"✅ SUCCESS: Saved to {path}")
        except Exception as e:
            print(f"❌ FAILED to download {model['name']}: {e}")

    print("\n" + "="*40)
    print("🏆 SWARM BUNDLE READY.")
    print("👉 Next Step: Restart 'serve.py' to activate the CS Committee.")
    print("="*40)

if __name__ == "__main__":
    # [TRIGGER] The user has requested to only generate this file.
    # To run the download, the user will execute: python download_swarm.py
    print("🛡️ SCRIPT GENERATED: Run 'python download_swarm.py' when you are ready to download.")
