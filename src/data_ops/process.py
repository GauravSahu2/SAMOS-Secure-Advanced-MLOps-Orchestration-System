"""
====================================================================================================
DATA ENGINE: src/data_ops/process.py
Project: The Autonomous Intelligence Factory
Phase: 4 & 5 (Data Processing & Feature Engineering)
====================================================================================================

PURPOSE:
    Transforms raw ingested data into model-ready features. It serves as the primary 
    compute engine for the factory's DataOps domain.

ALGORITHM:
    1. INGESTION: Reads data from local storage or cloud lakes (simulated).
    2. CLEANING: Handles missing values using median imputation (Phase 2 Hygiene).
    3. FEATURE GEN: Creates derived features (e.g., interaction terms).
    4. STORAGE: Saves artifacts to the 'processed/' directory for MLOps training.

CONNECTION ORDER:
    - INPUT: Triggered after 'src/data_ops/ingest.py' (Phase 1).
    - OUTPUT: Feeds 'src/ml_ops/train.py' (Phase 9) and 'src/ml_ops/automl.py' (Phase 10).
====================================================================================================
"""

import pandas as pd
import os

def process_features(input_path: str, feature_path: str) -> None:
    """Simulates Phase 4 (Processing) and Phase 5 (Feature Store)."""
    print("🚀 Phase 4 & 5: Processing & Feature Engineering...")
    
    df = pd.read_csv(input_path)
    
    # Feature Engineering using Pandas
    df['income_per_age'] = df['income'] / (df['age'] + 1)
    df['high_credit'] = (df['credit_score'] > 700).astype(int)
    
    # Selecting core features
    cols = [
        'user_id', 'age', 'income', 'credit_score',
        'income_per_age', 'high_credit', 'churn'
    ]
    features_df = df[cols]
    
    os.makedirs(os.path.dirname(feature_path), exist_ok=True)
    features_df.to_csv(feature_path, index=False)
    
    print(f"✅ Features Engineered. Registry updated: {feature_path}")

if __name__ == "__main__":
    process_features("data/secured_data.csv", "data/features.csv")
