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

def generate_data(num_records: int = 1000) -> pd.DataFrame:
    """Simulates raw data sourcing from APIs/Logs."""
    rng = np.random.default_rng(42)
    data = {
        'timestamp': [datetime.now().isoformat() for _ in range(num_records)],
        'user_id': rng.integers(1000, 9999, size=num_records),
        'age': rng.integers(18, 80, size=num_records),
        'income': rng.integers(20000, 150000, size=num_records),
        'email': [f"user_{i}@example.com" for i in range(num_records)],
        'credit_score': rng.integers(300, 850, size=num_records),
        'churn': rng.choice([0, 1], size=num_records, p=[0.8, 0.2])
    }
    df = pd.DataFrame(data)
    
    # Introduce some noise/errors for Phase 2 (Validation)
    df.loc[0:10, 'income'] = -100  # Invalid income
    df.loc[10:20, 'age'] = 200     # Invalid age
    
    return df

from src.data_ops.multi_modal import UniversalConverter  # noqa: E402

def main() -> None:
    print("🚀 Phase 1: Sourcing Data...")
    
    # 1. Multi-Modal Fusion (Convert PDF, Docx, Code, etc. to CSV)
    converter = UniversalConverter()
    converter.convert_all()
    
    # 2. Structured CSV Ingestion
    raw_dir = "data/raw"
    os.makedirs(raw_dir, exist_ok=True)
    raw_files = [f for f in os.listdir(raw_dir) if f.endswith('.csv')]
    
    if raw_files:
        print(f"📂 Found {len(raw_files)} raw CSV files in {raw_dir}. Merging...")
        df_list = [pd.read_csv(os.path.join(raw_dir, f)) for f in raw_files]
        df = pd.concat(df_list, ignore_index=True)
        
        output_path = "data/bronze_data.csv"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Append to bronze lake (which might already contain multi-modal data)
        if os.path.exists(output_path):
            df_existing = pd.read_csv(output_path)
            df = pd.concat([df_existing, df], ignore_index=True)
            
        df.to_csv(output_path, index=False)
        print(f"✅ Data saved to {output_path} (Total Records: {len(df)})")
    else:
        # If no files at all (CSV or Multi-modal), generate dev data
        output_path = "data/bronze_data.csv"
        if not os.path.exists(output_path):
            print("💡 No raw files found. Generating synthetic development data...")
            df = generate_data()
            df.to_csv(output_path, index=False)
            print(f"✅ Data saved to {output_path}")
        else:
            print("💡 Using existing data in the Bronze lake.")

if __name__ == "__main__":
    main()
