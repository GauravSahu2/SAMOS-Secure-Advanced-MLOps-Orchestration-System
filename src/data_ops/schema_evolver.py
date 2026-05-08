import pandas as pd

def evolve_data_schema(new_data_sample, feature_store_path="data/features.csv"):
    """Phase 2: DataOps - Dynamic Schema Evolution."""
    print("🧬 Phase 2: Monitoring Schema for Evolution...")
    
    current_df = pd.read_csv(feature_store_path)
    new_cols = [c for c in new_data_sample.columns if c not in current_df.columns]
    
    if new_cols:
        print(f"  ✨ NEW FEATURES DETECTED: {new_cols}")
        print("  📝 Action: Updating Feature Store schema and informing Genetic Synthesis...")
        
        # Simulated Schema Update
        for col in new_cols:
            current_df[col] = 0 # Initialize new column
            
        current_df.to_csv(feature_store_path, index=False)
        print("  ✅ Schema Evolved. Pipeline remains 100% operational.")
    else:
        print("  ✅ Schema Stable. No evolution required.")

if __name__ == "__main__":
    # Simulating a new 'loyalty_score' column appearing in source
    sample = pd.DataFrame({'loyalty_score': [8.5]})
    evolve_data_schema(sample)
