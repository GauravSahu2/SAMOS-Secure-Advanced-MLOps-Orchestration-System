import pandas as pd

def check_data_sovereignty(data_path, current_region="US"):
    """Phase 3: DataSecOps - Sovereignty & Residency Guardrail."""
    print(f"🗺️ Phase 3: Checking Data Sovereignty (Current Region: {current_region})...")
    
    df = pd.read_csv(data_path)
    
    # Simulate a region column if not present
    if 'region' not in df.columns:
        df['region'] = 'EU' # Simulating sensitive data
        
    violations = df[df['region'] != current_region]
    
    if len(violations) > 0:
        print(f"❌ SOVEREIGNTY BREACH: Found {len(violations)} records from restricted region: {violations['region'].unique()}")
        print("🚫 ABORTING OPERATION: Data Residency Policy (V1.2) violated.")
        return False
    else:
        print("✅ Sovereignty verified. All data belongs to local region.")
        return True

if __name__ == "__main__":
    import os
    if os.path.exists("data/features.csv"):
        check_data_sovereignty("data/features.csv", current_region="US")
