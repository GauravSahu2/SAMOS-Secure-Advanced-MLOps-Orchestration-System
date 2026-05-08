import pandas as pd
import pickle

def check_monotonicity(model_path, feature_name="credit_score", direction="negative"):
    """Phase 13: Business Logic Guardrail - Monotonicity Test."""
    print(f"📉 Phase 13: Checking Monotonicity for '{feature_name}' ({direction})...")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    # Create a synthetic sample
    sample = pd.DataFrame({'age': [35], 'income': [50000], 'credit_score': [600], 'income_per_age': [1428], 'high_credit': [0]})
    
    # Test 1: Original
    p1 = model.predict_proba(sample)[0, 1]
    
    # Test 2: Improved Feature
    sample_improved = sample.copy()
    sample_improved[feature_name] += 200
    p2 = model.predict_proba(sample_improved)[0, 1]
    
    print(f"  📊 Baseline Prob: {p1:.4f} | Improved Prob: {p2:.4f}")
    
    if direction == "negative" and p2 > p1:
        print(f"❌ LOGIC BREACH: Higher {feature_name} increased risk! Blocking model.")
        return False
    elif direction == "positive" and p2 < p1:
        print(f"❌ LOGIC BREACH: Higher {feature_name} decreased reward! Blocking model.")
        return False
        
    print(f"✅ Monotonicity Verified: Model follows '{feature_name}' business logic.")
    return True

if __name__ == "__main__":
    import os
    if os.path.exists("models/churn_model.pkl"):
        check_monotonicity("models/churn_model.pkl")
