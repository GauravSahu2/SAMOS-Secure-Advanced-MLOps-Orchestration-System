import pandas as pd
import numpy as np

def run_chaos_experiment(data_path):
    """Phase 14: Chaos Engineering for ML (Stress Testing)."""
    print("🧪 Starting ML Chaos Experiment...")
    
    df = pd.read_csv(data_path)
    
    # 1. Feature Corruption (NaN Injection)
    print("⚠️ Injecting NaNs into 'income' feature...")
    df.loc[df.sample(frac=0.1).index, 'income'] = np.nan
    
    # 2. Distribution Shift (Outlier Injection)
    print("⚠️ Injecting Extreme Outliers into 'age'...")
    df.loc[df.sample(n=5).index, 'age'] = 999
    
    # 3. Target Flip (Label Poisoning)
    print("⚠️ Simulating Label Poisoning (1% flip)...")
    df.loc[df.sample(frac=0.01).index, 'churn'] = 1 - df['churn']
    
    # Save for Validation Test
    chaos_path = data_path.replace(".csv", "_chaos.csv")
    df.to_csv(chaos_path, index=False)
    
    print(f"✅ Chaos Data Generated: {chaos_path}")
    print("🚀 Triggering Phase 2 (Validation) to see if it detects the corruption...")

if __name__ == "__main__":
    run_chaos_experiment("data/features.csv")
