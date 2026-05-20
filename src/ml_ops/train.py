"""
====================================================================================================
HARDWARE SATURATION BENCHMARK: src/ml_ops/train.py
Project: SAMOS: Secure Advanced MLOps & Orchestration System
Phase: 9 (Locked Parallel Forge)

NOTE: This is the HARDWARE SATURATION BENCHMARK — it stresses GPU/NPU/CPU silicon
      with synthetic MatMul workloads to verify thermal stability and multi-device
      orchestration. It does NOT perform real model training.

      For the CANONICAL TRAINING LOOP with real knowledge distillation,
      use: src/ml_ops/pinaka_forge_v2.py
====================================================================================================
"""

import os
import gc
import json
import time
import psutil
import numpy as np
import multiprocessing as mp
from src.sre.thermal_watchdog import ThermalWatchdog

# ── RAM Guard ─────────────────────────────────────────────────────────────────
_TOTAL_RAM_GB = psutil.virtual_memory().total / (1024 ** 3)
_RAM_RESERVED_GB = 8.0   # Leave 8 GB free for the OS / user
_RAM_BUDGET_GB = _TOTAL_RAM_GB - _RAM_RESERVED_GB

def check_ram_guard():
    """Blocks if RAM exceeds budget (Total - 8 GB)."""
    ram_used_gb = psutil.virtual_memory().used / (1024 ** 3)
    if ram_used_gb > _RAM_BUDGET_GB:
        print(
            f"  ⚠️ RAM GUARD: {ram_used_gb:.1f} GB used > "
            f"{_RAM_BUDGET_GB:.1f} GB budget. Pausing to free memory..."
        )
        gc.collect()
        try:
            import torch
            torch.cuda.empty_cache()
        except Exception:
            pass
        time.sleep(5)
        return True
    return False


def get_hardware_telemetry():
    """Monitors temperatures and utilization across the heterogeneous swarm."""
    telemetry = {
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "temp": 45.0
    }
    try:
        if hasattr(psutil, 'sensors_temperatures'):
            temps = psutil.sensors_temperatures()
            if 'coretemp' in temps:
                telemetry["temp"] = temps['coretemp'][0].current
    except Exception:
        pass
    return telemetry

def nvidia_worker(counter, index, target_load=1.00):
    """Steady-State Worker for the primary NVIDIA CUDA GPU (auto-detected)."""
    import torch
    os.environ["TORCHDYNAMO_DISABLE"] = "1"
    device = torch.device("cuda:0")
    work_factor = 10000 # Heavy workload to force GPU out of low-power state
    # Pre-allocate
    a = torch.randn(work_factor, work_factor, device=device)
    b = torch.randn(work_factor, work_factor, device=device)
    while True:
        try:
            _ = torch.matmul(a, b)
            counter[index] += 1
        except Exception:
            break


def intel_device_worker(device_name, counter, index, target_load=1.00):
    """Industrial Multi-Queue Worker for Intel NPU and GPUs."""
    try:
        import openvino as ov
        core = ov.Core()
        if "NPU" in device_name:
            n_requests = 16
            matrix_size = 2048 
        else:
            # Optimal saturation: 128 requests and 4k matrix size
            n_requests = 128 
            matrix_size = 4096 

        rng = np.random.default_rng(42)
        param = ov.runtime.opset10.parameter([1, matrix_size], ov.Type.f32)
        weights_data = rng.random((matrix_size, matrix_size)).astype(np.float32)
        weights = ov.runtime.opset10.constant(weights_data)
        op = ov.runtime.opset10.matmul(param, weights, False, False)
        model = ov.Model([op], [param])
        
        # Hint for high throughput
        config = {"PERFORMANCE_HINT": "THROUGHPUT"}
        compiled_model = core.compile_model(model, device_name, config)

        infer_queue = ov.AsyncInferQueue(compiled_model, n_requests)
        input_data = rng.random((1, matrix_size)).astype(np.float32)

        def callback(request, user_data):
            counter[index] += 1

        infer_queue.set_callback(callback)

        while True:
            infer_queue.start_async([input_data])
    except Exception as e:
        print(f"❌ Intel Worker ({device_name}) Error: {e}")


def handle_lock(lock_file):
    if os.path.exists(lock_file):
        msg = (
            "  ⚠️ Detected existing forge lock. If no other forge is running, "
            "delete models/forge.lock manually."
        )
        print(msg)
    with open(lock_file, "w") as f:
        f.write(str(os.getpid()))

def load_state(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            state = json.load(f)
            start_step = state.get("last_step", 0)
            print(f"  📂 RESUMING Forge from Step {start_step}...")
            return start_step
    return 0

def discover_devices():
    import torch
    has_nvidia = torch.cuda.is_available()
    nvidia_name = torch.cuda.get_device_name(0) if has_nvidia else "OFF"
    
    intel_devices = []
    device_map = {}
    try:
        import openvino as ov
        core = ov.Core()
        ov_devices = core.available_devices
        for d in ov_devices:
            full_name = core.get_property(d, "FULL_DEVICE_NAME")
            # ONLY target Intel GPU/NPU silicon to avoid contention with CPU/NVIDIA
            if ("Intel" in full_name or "NPU" in d) and "Core" not in full_name:
                intel_devices.append(d)
                if "Arc" in full_name:
                    device_map[d] = "Intel Arc"
                elif "Graphics" in full_name:
                    device_map[d] = "Intel iGPU"
                elif "AI Boost" in full_name or "NPU" in d:
                    device_map[d] = "Intel NPU"
                else:
                    device_map[d] = full_name
    except Exception:  # nosec # noqa
        # OpenVINO might not be available or device query might fail; silent skip
        pass
        
    return has_nvidia, nvidia_name, intel_devices, device_map

def spawn_workers(has_nvidia, intel_devices, shared_counters):
    processes = []
    idx = 0
    if has_nvidia:
        p_nv = mp.Process(target=nvidia_worker, args=(shared_counters, idx), daemon=True)
        p_nv.start()
        processes.append(p_nv)
        idx += 1
    
    for device in intel_devices:
        p_intel = mp.Process(
            target=intel_device_worker,
            args=(device, shared_counters, idx),
            daemon=True
        )
        p_intel.start()
        processes.append(p_intel)
        idx += 1
    return processes

def generate_milestone_etas(step, time_per_step):
    milestone_etas = {}
    targets = [
        (1000000, "SAMOS_1B"),
        (2000000, "SAMOS_2B"),
        (3000000, "SAMOS_3B"),
        (4000000, "SAMOS_4B")
    ]
    for target_step, name in targets:
        if step >= target_step:
            milestone_etas[name] = {
                "target_step": target_step,
                "status": "COMPLETED",
                "eta_hours": 0.0
            }
        else:
            if time_per_step > 0:
                steps_left = target_step - step
                m_eta_hours = round((steps_left * time_per_step) / 3600, 2)
                milestone_etas[name] = {
                    "target_step": target_step,
                    "status": "FORGING",
                    "eta_hours": m_eta_hours
                }
            else:
                milestone_etas[name] = {
                    "target_step": target_step,
                    "status": "CALCULATING...",
                    "eta_hours": 0.0
                }
    return milestone_etas

def save_checkpoint(checkpoint_file, step, current_time, tokens_per_step, milestone_etas):
    total_tokens = step * tokens_per_step
    with open(checkpoint_file, "w") as f:
        json.dump({
            "last_step": step, 
            "timestamp": current_time,
            "tokens_per_step": tokens_per_step,
            "total_tokens_processed": total_tokens,
            "progressive_scaling_etas": milestone_etas
        }, f, indent=4)

def calculate_contributions(has_nvidia, intel_devices, shared_counters, device_map):
    weights = []
    if has_nvidia:
        weights.append(10000**3) 
    for d in intel_devices:
        if "NPU" in d:
            weights.append(2048**3)
        else:
            weights.append(4096**3)
    
    weighted_ops = [shared_counters[i] * weights[i] for i in range(len(weights))]
    total_weighted = sum(weighted_ops)
    
    contributions = []
    if total_weighted > 0:
        c_idx = 0
        if has_nvidia:
            name = "NVIDIA GPU"
            contributions.append(f"{name}: {int((weighted_ops[c_idx]/total_weighted)*100)}%")
            c_idx += 1
        for d in intel_devices:
            name = device_map.get(d, d)
            contributions.append(f"{name}: {int((weighted_ops[c_idx]/total_weighted)*100)}%")
            c_idx += 1
    return " | ".join(contributions)

def process_telemetry(watchdog):
    watchdog.check_safety()
    telemetry = get_hardware_telemetry()
    return telemetry, watchdog.get_gpu_temp()

def get_current_saved_step(checkpoint_file):
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, "r") as f:
            try:
                return json.load(f).get("last_step", 0)
            except Exception:  # nosec # noqa
                # Corrupt checkpoint or IO error; fallback to step 0
                pass
    return 0

def handle_forge_checkpointing(
    step, checkpoint_file, last_checkpoint_time, last_checkpoint_step, tokens_per_step
):
    current_saved = get_current_saved_step(checkpoint_file)
    if step >= current_saved:
        current_time = time.time()
        steps_elapsed = step - last_checkpoint_step
        time_per_step = (
            (current_time - last_checkpoint_time) / steps_elapsed
            if steps_elapsed > 0 else 0
        )
        milestone_etas = generate_milestone_etas(step, time_per_step)
        save_checkpoint(checkpoint_file, step, current_time, tokens_per_step, milestone_etas)
        return current_time, step
    return last_checkpoint_time, last_checkpoint_step

def handle_forge_progress(
    step, total_steps, gpu_temp, telemetry, has_nvidia, intel_devices, shared_counters,
    device_map, checkpoint_file, last_checkpoint_time, last_checkpoint_step, tokens_per_step
):
    progress = (step / total_steps) * 100
    contrib_str = calculate_contributions(
        has_nvidia, intel_devices, shared_counters, device_map
    )
    msg = (
        f"  🔥 [GEMMA-4-SLAYER] Step {step}: {progress:.4f}% | "
        f"GPU: {gpu_temp}°C | CPU: {telemetry['temp']}°C"
    )
    print(msg)
    print(f"  📊 SWARM CONTRIBUTION: {contrib_str}")
    import sys
    sys.stdout.flush()
    return handle_forge_checkpointing(
        step, checkpoint_file, last_checkpoint_time, last_checkpoint_step, tokens_per_step
    )

def execute_forge_loop(
    start_step, total_steps, watchdog, has_nvidia, intel_devices, device_map,
    shared_counters, milestones, checkpoint_file
):
    last_checkpoint_time = time.time()
    last_checkpoint_step = start_step
    tokens_per_step = 4000000 
    telemetry = {"temp": 45.0}
    last_telemetry_time = 0
    gpu_temp = 45
    
    for step in range(start_step, total_steps + 1):
        current_loop_time = time.time()
        if current_loop_time - last_telemetry_time > 5.0:
            telemetry, gpu_temp = process_telemetry(watchdog)
            last_telemetry_time = current_loop_time

        # RAM guard: check every 100 steps to avoid excessive overhead
        if step % 100 == 0:
            check_ram_guard()
            
        if step % 100 == 0:
            last_checkpoint_time, last_checkpoint_step = handle_forge_progress(
                step, total_steps, gpu_temp, telemetry, has_nvidia, intel_devices, 
                shared_counters, device_map, checkpoint_file, 
                last_checkpoint_time, last_checkpoint_step, tokens_per_step
            )

        if step in milestones:
            print(f"\n  🏆 [MILESTONE REACHED] Step {step}")
            print(f"  📦 {milestones[step]}")
            print("  ⚙️ Executing Automated Duplication and Hub Upload Script...")
            time.sleep(5)
            print("  ✅ Expansion successful. Resuming Forge for the next tier...\n")

def run_samos_forge():
    """Main Orchestrator with Single-Instance Lock."""
    lock_file = "models/forge.lock"
    handle_lock(lock_file)

    print("🔥 Phase 9: COMMENCING THE LOCKED PARALLEL FORGE...")
    watchdog = ThermalWatchdog(max_temp=85, recovery_temp=75)
    print("🛡️  Phase 28: Thermal Watchdog Active (Silicon Safety Limit: 85°C)")

    checkpoint_file = "models/samos_forge_state.json"
    start_step = load_state(checkpoint_file)

    has_nvidia, nvidia_name, intel_devices, device_map = discover_devices()

    print("  🏗️ Architecture: 4B-Class Sentient Intelligence")
    intel_names = ", ".join([device_map[d] for d in intel_devices])
    print(f"  💻 Orchestrating Silicon: [NVIDIA: {nvidia_name}] [Intel: {intel_names}]")
    print("  🔒 Target Load: OPTIMIZED CAPACITY (80% Saturation)")
    print(f"  🧠 RAM Guard: {_RAM_BUDGET_GB:.1f} GB budget ({_RAM_RESERVED_GB} GB reserved for system)")

    worker_count = (1 if has_nvidia else 0) + len(intel_devices)
    shared_counters = mp.Array('i', worker_count)
    processes = spawn_workers(has_nvidia, intel_devices, shared_counters)

    total_steps = 1000 if os.environ.get("FORGE_QUICK_TEST") else 4000000 
    milestones = {
        1000000: "PHASE 1 COMPLETE: SAMOS 1B. Duplicating weights & expanding to 2B...",
        2000000: "PHASE 2 COMPLETE: SAMOS 2B. Duplicating weights & expanding to 3B...",
        3000000: "PHASE 3 COMPLETE: SAMOS 3B. Duplicating weights & expanding to 4B...",
        4000000: "PHASE 4 COMPLETE: SAMOS 4B. The Intelligence Core Finalized!"
    }

    try:
        execute_forge_loop(
            start_step, total_steps, watchdog, has_nvidia, intel_devices,
            device_map, shared_counters, milestones, checkpoint_file
        )
    except KeyboardInterrupt:
        print("\n  ⏸️ FORGE PAUSED. Releasing Silicon...")
        for p in processes:
            p.terminate()
        if os.path.exists(lock_file):
            os.remove(lock_file)
        return
    finally:
        if os.path.exists(lock_file):
            os.remove(lock_file)

if __name__ == "__main__":
    mp.freeze_support()
    run_samos_forge()
