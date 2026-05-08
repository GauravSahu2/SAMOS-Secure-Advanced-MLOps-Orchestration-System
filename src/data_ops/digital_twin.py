import pandas as pd
import numpy as np

def generate_digital_twin_samples(n=10000):
    """Phase 1: Digital Twin - Infinite Data Generation."""
    print(f"👯 Generating Digital Twin Samples (N={n})...")
    
    # Simulating the 'Statistical DNA' of our churn dataset
    data = {
        'user_id': range(10001, 10001 + n),
        'age': np.random.normal(38, 12, n),
        'income': np.random.normal(65000, 25000, n),
        'credit_score': np.random.normal(650, 100, n),
        'churn': np.random.choice([0, 1], n, p=[0.8, 0.2])
    }
    
    # Injecting a 'Black Swan' Event (Extreme Surge)
    print("⚠️ Injecting 'Black Swan' Event: Mass Churn Simulation...")
    data['churn'][0:100] = 1 # Force a 100% churn segment for stress testing
    
    df = pd.DataFrame(data)
    df.to_csv("data/digital_twin_data.csv", index=False)
    print("✅ Digital Twin Data generated: data/digital_twin_data.csv")

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    generate_digital_twin_samples()
