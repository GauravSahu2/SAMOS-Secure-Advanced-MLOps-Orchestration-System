import pandas as pd
import os

def validate_data(input_path: str, silver_path: str, dlq_path: str) -> None:
    """Simulates Phase 2: Data Quality & Validation."""
    print("🚀 Phase 2: Validating Data...")
    df = pd.read_csv(input_path)
    
    # Simple validation rules (emulating Great Expectations)
    valid_age = (df['age'] >= 0) & (df['age'] <= 120)
    valid_income = (df['income'] >= 0)
    
    clean_df = df[valid_age & valid_income]
    dirty_df = df[~(valid_age & valid_income)]
    
    os.makedirs(os.path.dirname(silver_path), exist_ok=True)
    os.makedirs(os.path.dirname(dlq_path), exist_ok=True)
    
    clean_df.to_csv(silver_path, index=False)
    dirty_df.to_csv(dlq_path, index=False)
    
    print(f"✅ Validation Complete. Clean: {len(clean_df)}, Dirty: {len(dirty_df)}")
    print(f"📂 Silver Data: {silver_path}")
    print(f"📂 Dead Letter Queue: {dlq_path}")

if __name__ == "__main__":
    validate_data("data/bronze_data.csv", "data/silver_data.csv", "data/dlq_data.csv")
