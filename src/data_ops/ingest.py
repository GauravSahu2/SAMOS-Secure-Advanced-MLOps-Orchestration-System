"""
====================================================================================================
INGESTION ENGINE: src/data_ops/ingest.py
Project: The Autonomous Intelligence Factory
Phase: 1 (Multi-Source Ingestion)
====================================================================================================

PURPOSE:
    The entry point for all information. It connects to raw data streams (SQL, S3, API) 
    and converts them into the factory's internal processing format.

ALGORITHM:
    1. DISCOVERY: Scans registered data sources for new updates.
    2. STREAMING: Pulls data in chunks to prevent memory overflow.
    3. STANDARDIZATION: Normalizes timestamps and schemas for Domain 1 processing.
    4. HANDOFF: Saves raw artifacts to the 'data/' lake for Phase 2 validation.

CONNECTION ORDER:
    - START: Triggered as the first operational step in 'main.py'.
    - OUTPUT: Feeds 'src/data_ops/validate.py' and 'src/data_ops/lake_health.py'.
====================================================================================================
"""

import pandas as pd
import numpy as np
import os
from datetime import datetime

def generate_data(num_records=1000):
    """Simulates raw data sourcing from APIs/Logs."""
    np.random.seed(42)
    data = {
        'timestamp': [datetime.now().isoformat() for _ in range(num_records)],
        'user_id': np.random.randint(1000, 9999, size=num_records),
        'age': np.random.randint(18, 80, size=num_records),
        'income': np.random.randint(20000, 150000, size=num_records),
        'email': [f"user_{i}@example.com" for i in range(num_records)],
        'credit_score': np.random.randint(300, 850, size=num_records),
        'churn': np.random.choice([0, 1], size=num_records, p=[0.8, 0.2])
    }
    df = pd.DataFrame(data)
    
    # Introduce some noise/errors for Phase 2 (Validation)
    df.loc[0:10, 'income'] = -100  # Invalid income
    df.loc[10:20, 'age'] = 200     # Invalid age
    
    return df

def main():
    print("🚀 Phase 1: Sourcing Data...")
    df = generate_data()
    
    output_path = "data/bronze_data.csv"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Data saved to {output_path}")

if __name__ == "__main__":
    main()
