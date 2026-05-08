import pandas as pd
import numpy as np
import pickle

def generate_counterfactual(model_path, user_data):
    """Phase 13: Actionable XAI - Counterfactual Explanations."""
    print("🔍 Phase 13: Generating Counterfactual Explanation...")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    original_pred = model.predict(user_data)[0]
    print(f"  Current Prediction: {'CHURN' if original_pred == 1 else 'STAY'}")
    
    if original_pred == 0:
        print("  ✅ User is stable. No counterfactual needed.")
        return

    # Simple search for a counterfactual (incrementing credit score)
    # In a real scenario, use DiCE or similar libraries
    cf_data = user_data.copy()
    for i in range(1, 100):
        cf_data['credit_score'] += 10
        if model.predict(cf_data)[0] == 0:
            print(f"  💡 COUNTERFACTUAL FOUND: If Credit Score increases by {i*10}, user will STAY.")
            return

    print("  ❌ No simple counterfactual found within reasonable bounds.")

if __name__ == "__main__":
    import os
    # Example user who is likely to churn
    user = pd.DataFrame({'age': [45], 'income': [30000], 'credit_score': [400], 'income_per_age': [666.6], 'high_credit': [0]})
    if os.path.exists("models/churn_model.pkl"):
        generate_counterfactual("models/churn_model.pkl", user)
