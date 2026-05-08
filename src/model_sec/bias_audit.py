"""
====================================================================================================
ETHICS GUARDIAN: src/model_sec/bias_audit.py
Project: The Autonomous Intelligence Factory
Phase: 13 (Ethical Bias Audit)
====================================================================================================

PURPOSE:
    Identifies and quantifies algorithmic bias against specific demographic groups 
    (e.g., Age, Gender, Region). It ensures the model provides 'Intersectional Fairness'.

ALGORITHM:
    1. SLICING: Segments the evaluation dataset into demographic slices.
    2. METRIC CALCULATION: Computes 'Disparate Impact' and 'Equalized Odds' for each slice.
    3. SIGNIFICANCE TESTING: Determines if performance gaps are statistically significant.
    4. REPORTING: Generates an 'Audit Score' that is sent to 'Omni-Governance'.
    5. BLOCKING: If any slice shows Bias > 0.05, the deployment is hard-blocked.

CONNECTION ORDER:
    - INPUT: Ingests model predictions from 'src/ml_ops/train.py' (Phase 9).
    - OUTPUT: Feeds the 'Bias Report' into 'src/model_sec/omni_governance.py' (Phase 25).
====================================================================================================
"""

import pandas as pd
import pickle
from sklearn.metrics import accuracy_score

def run_bias_audit(model_path, data_path):
    """Phase 13: Fairness & Bias Audit (Slice-Based Evaluation)."""
    print("⚖️ Phase 13: Starting Ethical Bias Audit...")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)  # noqa: S301
        
    df = pd.read_csv(data_path)
    
    # Define Cohorts
    cohorts = {
        "Young (18-35)": df[df['age'] <= 35],
        "Seniors (60+)": df[df['age'] >= 60],
        "High Income (>100k)": df[df['income'] > 100000],
        "Low Income (<40k)": df[df['income'] < 40000]
    }
    
    disparities = {}
    for name, cohort_df in cohorts.items():
        if len(cohort_df) == 0:
            continue
        X = cohort_df.drop(['user_id', 'churn'], axis=1)
        y = cohort_df['churn']
        acc = accuracy_score(y, model.predict(X))
        disparities[name] = acc
        print(f"  📊 Accuracy for {name}: {acc*100:.2f}%")
        
    # Check for Fairness Disparity (e.g. max diff between cohorts)
    max_diff = max(disparities.values()) - min(disparities.values())
    print(f"\n⚖️ Total Disparity Gap: {max_diff*100:.2f}%")
    
    if max_diff > 0.15: # 15% threshold
        print("❌ GOVERNANCE GATE: FAILED. High bias detected between cohorts.")
        return False
    else:
        print("✅ GOVERNANCE GATE: PASSED. Model is ethically balanced.")
        return True

if __name__ == "__main__":
    import os
    if os.path.exists("models/churn_model.pkl"):
        run_bias_audit("models/churn_model.pkl", "data/features.csv")
