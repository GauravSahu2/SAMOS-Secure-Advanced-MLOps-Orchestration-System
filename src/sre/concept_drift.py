import numpy as np

def detect_concept_drift(stable_preds, actual_outcomes, window_size=100):
    """Phase 25: Advanced Telemetry - Concept Drift Detection."""
    print("🔍 Phase 25: Monitoring Concept Stability (Relationship Shift)...")
    
    # Calculate error rate over time
    errors = np.abs(np.array(stable_preds) - np.array(actual_outcomes))
    
    # If error rate spikes in the recent window, it's Concept Drift
    recent_error = np.mean(errors[-window_size:])
    baseline_error = np.mean(errors[:-window_size]) if len(errors) > window_size else 0.1
    
    drift_score = recent_error / baseline_error if baseline_error > 0 else 1.0
    
    print(f"  🎯 Concept Drift Score: {drift_score:.2f} (Recent Error: {recent_error:.4f})")
    
    if drift_score > 1.5:
        print("🚨 CONCEPT DRIFT DETECTED: The 'Truth' has changed. Model logic is obsolete.")
        print("🔄 TRIGGERING EMERGENCY RETRAIN...")
        return True
    else:
        print("✅ Concepts are stable. Relationship between features and target is consistent.")
        return False

if __name__ == "__main__":
    # Simulating a spike in errors (0.1 baseline, 0.2 recent)
    preds = [0]*1000 + [1]*100
    actuals = [0]*1000 + [0]*100 # Model thinks they'll churn, but they didn't
    detect_concept_drift(preds, actuals)
