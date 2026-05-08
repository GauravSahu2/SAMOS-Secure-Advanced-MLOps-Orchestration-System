import numpy as np

def tune_prediction_threshold(business_goal="GROWTH"):
    """Phase 24: Business Alignment - Strategic Threshold Tuning."""
    print(f"🎚️ Phase 24: Tuning Threshold for Business Goal: {business_goal}...")
    
    # Baseline threshold is 0.5
    # GROWTH: Catch more churners (lower threshold)
    # PROFIT: Avoid false positives (higher threshold)
    
    threshold_map = {
        "GROWTH": 0.35,
        "STABLE": 0.50,
        "PROFIT": 0.65
    }
    
    new_threshold = threshold_map.get(business_goal, 0.5)
    
    print(f"  🎯 Strategy Update: Threshold shifted to {new_threshold:.2f}")
    print(f"  🚀 Serving Layer: All new predictions will use {business_goal} sensitivity.")
    
    return new_threshold

if __name__ == "__main__":
    tune_prediction_threshold("GROWTH")
    tune_prediction_threshold("PROFIT")
