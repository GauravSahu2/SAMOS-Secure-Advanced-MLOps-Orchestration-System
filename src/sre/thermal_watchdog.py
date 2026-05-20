"""
====================================================================================================
GUARDIAN ENGINE: src/sre/thermal_watchdog.py
Project: The Autonomous Intelligence Factory (SAMOS Edition)
Phase: 28 (Thermal Watchdog & Silicon Safety)
====================================================================================================

PURPOSE:
    Protects GPU hardware during multi-day "Deep Forge" 
    sessions. Monitors real-time thermal telemetry and enforces hardware throttling 
    to prevent silicon degradation.

LOGIC:
    1. Telemetry: Queries nvidia-smi for precise GPU junction/core temperatures.
    2. Threshold: 85°C (Safety Limit).
    3. Action: If temp > 85°C, it triggers a 'Cooling Pause' (time.sleep) until 
       temps stabilize below 75°C.
    4. Integration: Called by Phase 9 (Training) to ensure safety-aware compute.
====================================================================================================
"""

import subprocess  # nosec # noqa
import time
import logging

# Configure logging for Phase 28
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [PHASE-28-WATCHDOG] %(message)s',
    handlers=[
        logging.FileHandler("artifacts/thermal_logs.log"),
        logging.StreamHandler()
    ]
)

class ThermalWatchdog:
    def __init__(self, max_temp=85, recovery_temp=75):
        self.max_temp = max_temp
        self.recovery_temp = recovery_temp
        self.is_throttled = False

    def get_gpu_temp(self):
        """Queries NVIDIA-SMI for the current GPU temperature."""
        try:
            cmd = ["nvidia-smi", "--query-gpu=temperature.gpu", "--format=csv,noheader,nounits"]
            output = subprocess.check_output(cmd).decode('utf-8').strip()  # nosec # noqa
            return int(output)
        except Exception:
            logging.exception("Failed to query GPU temperature")
            return 0

    def check_safety(self):
        """
        Executes a safety check. If temperature exceeds threshold, 
        blocks execution until hardware cools down.
        """
        temp = self.get_gpu_temp()
        
        if temp >= self.max_temp:
            msg = f"⚠️ CRITICAL THERMAL ALERT: GPU at {temp}°C! Limit is {self.max_temp}°C."
            logging.warning(msg)
            # Dynamic cooldown: Sleep in 10s increments until recovery temp is reached
            while temp > self.recovery_temp:
                logging.info(f"  🌡️ Cooling in progress... Current: {temp}°C | Target: {self.recovery_temp}°C")
                time.sleep(10)
                temp = self.get_gpu_temp()
            
            msg = (
                f"✅ Cooldown complete. Hardware cooled to {temp}°C. "
                "Resuming Forge..."
            )
            logging.info(msg)
            self.is_throttled = False
            return True # Indicates we had to cool down

            
        return False # No cooldown needed

if __name__ == "__main__":
    # Standalone test mode
    watchdog = ThermalWatchdog()
    print(f"Current GPU Temp: {watchdog.get_gpu_temp()}°C")
    watchdog.check_safety()
