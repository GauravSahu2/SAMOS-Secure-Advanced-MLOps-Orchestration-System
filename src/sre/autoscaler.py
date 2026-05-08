import time
import random

def run_autoscaler_loop():
    """Phase 24: Elastic Infrastructure - KEDA Auto-scaler Simulation."""
    print("📈 Phase 24: Initializing Infrastructure Auto-scaler...")
    
    current_pods = 2
    
    # Simulating a traffic wave
    for i in range(1, 6):
        request_volume = random.randint(10, 500)  # nosec # noqa
        print(f"  🕒 Step {i}: Request Volume = {request_volume} req/sec")
        
        # Scaling Logic
        desired_pods = (request_volume // 100) + 1
        
        if desired_pods > current_pods:
            print(f"  🔺 SCALE UP: Current Pods={current_pods} -> Desired Pods={desired_pods}")
            current_pods = desired_pods
        elif desired_pods < current_pods:
            print(f"  🔻 SCALE DOWN: Current Pods={current_pods} -> Desired Pods={desired_pods}")
            current_pods = desired_pods
        else:
            print(f"  ✅ STABLE: Traffic handled by {current_pods} pods.")
            
        time.sleep(0.5)

if __name__ == "__main__":
    run_autoscaler_loop()
