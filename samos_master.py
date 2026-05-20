"""
====================================================================================================
MASTER ORCHESTRATOR: samos_master.py
Project: SAMOS: Secure Advanced MLOps & Orchestration System
Role: Unified Logging & Execution Control
====================================================================================================
"""

import subprocess
import sys
import os
import time

LOG_FILE = "samos_master.log"

def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] {message}"
    print(formatted_msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted_msg + "\n")

def run_command(command, description):
    log(f"🚀 STARTING PHASE: {description}")
    log(f"💻 Running: {command}")
    
    # We use unbuffered output to ensure the log file updates in real-time
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env={**os.environ, "PYTHONPATH": ".", "PYTHONUNBUFFERED": "1"}
    )
    
    if process.stdout is not None:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            for line in process.stdout:
                sys.stdout.write(line)
                f.write(line)
                f.flush()
            
    process.wait()
    if process.returncode == 0:
        log(f"✅ PHASE COMPLETE: {description}")
    else:
        log(f"❌ PHASE FAILED: {description} (Exit Code: {process.returncode})")
        sys.exit(process.returncode)

def main():
    # Clear existing log
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write("=== SAMOS MASTER FORGE LOG ===\n")
        
    log("🌟 SAMOS MASTER FORGE INITIATED 🌟")
    
    # Phase 1: Download Teachers
    run_command("python -u download_swarm.py", "Teacher Model Acquisition")
    
    # Phase 2: Start Training
    run_command("python -u src/ml_ops/pinaka_forge_v2.py", "Pinaka 1B Real Distillation Forge")

    log("🏆 ALL FORGE PHASES COMPLETE. SINGULARITY ACHIEVED.")

if __name__ == "__main__":
    main()
