import pandas as pd
import numpy as np
import pickle  # nosec # noqa

def identify_uncertain_samples(model_path, data_path, threshold=0.1):
    """Phase 11: Active Learning - Uncertainty Sampling."""
    print("🔍 Phase 11: Starting Active Learning Uncertainty Check...")
    
    with open(model_path, "rb") as f:
        model = pickle.load(f)  # nosec # noqa
        
    df = pd.read_csv(data_path)
    X = df.drop(['user_id', 'churn'], axis=1)
    
    # Get probability scores
    probs = model.predict_proba(X)
    
    # Uncertainty = closeness to 0.5 (for binary classification)
    uncertainty = np.abs(probs[:, 1] - 0.5)
    
    # Identify samples where the model is "confused" (near 0.5)
    uncertain_indices = np.nonzero(uncertainty < threshold)[0]
    
    print(f"✅ Found {len(uncertain_indices)} samples with high uncertainty.")
    
    if len(uncertain_indices) > 0:
        uncertain_data = df.iloc[uncertain_indices]
        os.makedirs("artifacts/active_learning", exist_ok=True)
        out_path = "artifacts/active_learning/labeling_queue.csv"
        uncertain_data.to_csv(out_path, index=False)
        msg = f"🚀 Flagged uncertain samples for review at: {out_path}"
        print(msg)
    
if __name__ == "__main__":
    import os
    identify_uncertain_samples("models/churn_model.pkl", "data/features.csv")
