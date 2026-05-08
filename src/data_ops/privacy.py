import pandas as pd
import numpy as np

def apply_differential_privacy(input_path, output_path, epsilon=0.1):
    """Phase 3: DataSecOps - Differential Privacy Layer."""
    print(f"🛡️ Applying Differential Privacy (Epsilon={epsilon})...")
    
    df = pd.read_csv(input_path)
    
    # Adding Laplace Noise to sensitive features (Income)
    # Sensitivity of income is assumed to be the range
    sensitivity = df['income'].max() - df['income'].min()
    scale = sensitivity / epsilon
    
    noise = np.random.laplace(0, scale, len(df))
    df['income'] = df['income'] + noise
    
    df.to_csv(output_path, index=False)
    print(f"✅ Privacy-Preserving Data saved to {output_path}")

if __name__ == "__main__":
    apply_differential_privacy("data/silver_data.csv", "data/private_data.csv")
