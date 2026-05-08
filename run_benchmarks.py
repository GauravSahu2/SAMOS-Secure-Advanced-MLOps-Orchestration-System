"""
====================================================================================================
FILE: run_benchmarks.py
ROLE: Local High-Assurance Evaluation Engine (SANITY CHECK MODE)
====================================================================================================
"""

import os
import subprocess
import sys

# Disable strict PyTorch unpickling
os.environ["TORCH_LOAD_WEIGHTS_ONLY"] = "0"

def execute_benchmarks():
    """Triggers a 10-sample sanity check to verify the pipeline."""
    
    if not os.path.exists("benchmarks"):
        os.makedirs("benchmarks")

    current_dir = os.getcwd()
    model_path = os.path.join(current_dir, "hgf")

    # [SANITY CHECK UPGRADE]
    # Added '--limit 10' to run only 10 questions per task.
    # This proves the pipeline works without waiting 90 hours for hallucinations.
    command = [
        "lm_eval",
        "--model", "hf",
        "--model_args", f"pretrained={model_path},trust_remote_code=True,ignore_mismatched_sizes=True",
        "--tasks", "mmlu,arc_challenge,gsm8k",
        "--device", "cuda:0", 
        "--batch_size", "8", 
        "--limit", "10",
        "--output_path", "benchmarks/results.json"
    ]

    print("\n🚀 [BENCHMARK] Executing Sanity-Check (Limit: 10)...")
    print(f"📡 Device: NVIDIA RTX 5070")
    print(f"📡 Mode: Pipeline Validation (ETA: ~2 Minutes)")
    print("="*50)

    try:
        # [TRIGGER] Rapid Validation
        subprocess.run(command, check=True)
        print("\n✅ [SUCCESS] Pipeline Validated! Results saved in 'benchmarks/results.json'.")
        print("💡 When you have your 8GB final weights, remove '--limit 10' for the full run.")
    except Exception as e:
        print(f"\n❌ [ERROR] Benchmark Failed: {e}")

if __name__ == "__main__":
    execute_benchmarks()
