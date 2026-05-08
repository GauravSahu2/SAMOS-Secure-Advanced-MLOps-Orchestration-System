import pandas as pd
import pickle
from sklearn.metrics import accuracy_score

def run_intersectional_audit(model_path, data_path):
    """Phase 13: Advanced Ethics - Intersectional Bias Analysis."""
    print("🧬 Phase 13: Starting Intersectional Bias Audit...")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)  # noqa: S301
        
    df = pd.read_csv(data_path)
    
    # Define Intersectional Cohorts
    intersections = {
        "Senior + Low Income": df[(df['age'] >= 60) & (df['income'] < 40000)],
        "Senior + High Income": df[(df['age'] >= 60) & (df['income'] > 100000)],
        "Young + Low Income": df[(df['age'] <= 35) & (df['income'] < 40000)],
        "Young + High Income": df[(df['age'] <= 35) & (df['income'] > 100000)]
    }
    
    print("  📊 Intersectional Performance Breakdown:")
    for name, cohort_df in intersections.items():
        if len(cohort_df) < 5:
            continue  # Skip statistically insignificant groups
        X = cohort_df.drop(['user_id', 'churn'], axis=1)
        y = cohort_df['churn']
        acc = accuracy_score(y, model.predict(X))
        print(f"    - {name:<22}: {acc*100:.2f}% (N={len(cohort_df)})")

    print("\n✅ Intersectional Audit Complete. Results logged for Ethics Board review.")

if __name__ == "__main__":
    import os
    if os.path.exists("models/churn_model.pkl"):
        run_intersectional_audit("models/churn_model.pkl", "data/features.csv")
