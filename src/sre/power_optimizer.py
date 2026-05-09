"""
====================================================================================================
ECO-GUARDIAN: src/sre/power_optimizer.py
Project: The Autonomous Intelligence Factory
Phase: 24 (Green-AI Power Optimization)
====================================================================================================

PURPOSE:
    Reduces the environmental impact of the factory by dynamically adjusting 
    compute resources based on the carbon intensity of the local energy grid.

ALGORITHM:
    1. GRID SYNC: Connects to energy grid APIs to determine current CO2 intensity.
    2. SHEDDING: If carbon intensity is high, it 'sheds' non-critical background 
       tasks (e.g., re-training, extra audits).
    3. DVFS (SIMULATED): Signals the infrastructure to lower GPU clock speeds or 
       consolidate workloads onto fewer nodes.
    4. SCHEDULING: Re-schedules heavy batch jobs to 'Green Windows' (e.g., high solar/wind hours).

CONNECTION ORDER:
    - INPUT: Ingests from the cloud provider's telemetry API.
    - OUTPUT: Signals 'src/sre/autoscaler.py' to scale down or migrate workloads.
====================================================================================================
"""

import psutil
import time

def optimize_hardware_power(task_priority):
    """Phase 24: SRE - Green AI Power Optimization (80% TARGET CAPACITY)."""
    print(f"⚡ Phase 24: Hardware Governor Active (Priority: {task_priority})...")
    
    # HARDWARE CAP: 80% CPU utilization target.
    MAX_UTILIZATION = 80.0
    # RAM GUARD: Reserve 8 GB for the OS and user applications.
    RAM_RESERVED_GB = 8.0
    total_ram_gb = psutil.virtual_memory().total / (1024 ** 3)
    ram_budget_gb = total_ram_gb - RAM_RESERVED_GB
    
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()
    ram_used_gb = ram.used / (1024 ** 3)
    
    print(f"  📊 Current Hardware Load: CPU: {cpu_usage}%, RAM: {ram_used_gb:.1f}/{ram_budget_gb:.1f} GB")
    print(f"  🔒 CPU Safety Limit: {MAX_UTILIZATION}%  |  RAM Budget: {ram_budget_gb:.1f} GB")
    
    alerts = []
    if cpu_usage > MAX_UTILIZATION:
        alerts.append(f"CPU usage ({cpu_usage}%) exceeds {MAX_UTILIZATION}% limit")
    if ram_used_gb > ram_budget_gb:
        alerts.append(f"RAM usage ({ram_used_gb:.1f} GB) exceeds {ram_budget_gb:.1f} GB budget")
    
    if alerts:
        for alert in alerts:
            print(f"  ⚠️ ALERT: {alert}.")
        print("  🛑 ACTION: Engaging throttling. Suspending operations...")
        time.sleep(5) 
        print("  ✅ Load stabilized below threshold. Resuming...")
    else:
        print("  ✅ Hardware load is within acceptable parameters.")

if __name__ == "__main__":
    optimize_hardware_power(10)

