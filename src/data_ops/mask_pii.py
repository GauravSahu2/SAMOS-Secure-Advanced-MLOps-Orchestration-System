import pandas as pd
import os

def mask_pii(input_path: str, secured_path: str) -> None:
    """Simulates Phase 3: DataSecOps & PII Masking."""
    print("🚀 Phase 3: Masking PII...")
    df = pd.read_csv(input_path)
    
    # Simple masking (emulating Presidio)
    if 'email' in df.columns:
        df['email'] = df['email'].apply(lambda x: x.split('@')[0][0] + "***@" + x.split('@')[1] if isinstance(x, str) and '@' in x else x)
    
    os.makedirs(os.path.dirname(secured_path), exist_ok=True)
    df.to_csv(secured_path, index=False)
    
    print(f"✅ PII Masked. Data saved to {secured_path}")

if __name__ == "__main__":
    mask_pii("data/silver_data.csv", "data/secured_data.csv")
