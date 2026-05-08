import pandas as pd
import numpy as np

def heal_data(input_path, output_path):
    """Phase 2: Self-Healing Data Repair (Auto-Imputation)."""
    print("🩹 Phase 2: Starting Self-Healing Data Repair...")
    
    df = pd.read_csv(input_path)
    
    # 1. Detect missing values
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"🛠 Detected {missing_count} missing values. Applying Mean Imputation...")
        # Simple Mean Imputation for numeric columns
        for col in df.select_dtypes(include=[np.number]).columns:
            df[col] = df[col].fillna(df[col].mean())
            
    # 2. Fix range outliers (e.g., Age > 120)
    print("🛠 Fixing out-of-range values (e.g. Age > 120)...")
    df.loc[df['age'] > 120, 'age'] = df['age'].median()
    
    df.to_csv(output_path, index=False)
    print(f"✅ Data Healed and Saved to {output_path}")

if __name__ == "__main__":
    heal_data("data/features_chaos.csv", "data/features_healed.csv")
