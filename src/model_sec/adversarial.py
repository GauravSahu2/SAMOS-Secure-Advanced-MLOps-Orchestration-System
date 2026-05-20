import numpy as np
import pickle  # nosec # noqa
import os

def check_adversarial_robustness(model_path: str, data_path: str) -> None:
    """Phase 14: Adversarial Robustness (Simplified ART logic)."""
    print("🚀 Phase 14: Running Adversarial Robustness Tests...")
    
    if not os.path.exists(model_path):
        print("❌ Model not found for robustness test.")
        return

    with open(model_path, "rb") as f:
        model = pickle.load(f)  # nosec # noqa
        
    df = pd.read_csv(data_path)
    x_matrix = df.drop(['user_id', 'churn'], axis=1).to_numpy()
    
    # 1. Base prediction
    base_preds = model.predict(x_matrix[:10])
    
    # 2. Add Adversarial Perturbation (Noise)
    rng = np.random.default_rng(42)
    noise = rng.normal(0, 0.1, x_matrix[:10].shape)
    x_adv = x_matrix[:10] + noise
    
    adv_preds = model.predict(x_adv)
    
    # 3. Calculate Robustness Score
    stability = np.mean(base_preds == adv_preds)
    print(f"✅ Robustness Score: {stability * 100:.2f}%")
    
    if stability < 0.8:
        print("⚠️ Warning: Model is sensitive to small perturbations.")
    else:
        print("✅ Model is stable against noise.")

if __name__ == "__main__":
    import pandas as pd
    check_adversarial_robustness("models/churn_model.pkl", "data/features.csv")
