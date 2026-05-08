import pandas as pd
import os

def purge_user_data(user_id_to_purge, data_path="data/features.csv"):
    """Phase 3: Data Ethics - Automated Right to be Forgotten."""
    print(f"🧹 Phase 3: Executing Data Purge for User {user_id_to_purge}...")
    
    if not os.path.exists(data_path):
        print("  ⚠️ Data file not found. Nothing to purge.")
        return

    df = pd.read_csv(data_path)
    
    # 1. Surgical Removal
    initial_count = len(df)
    df_clean = df[df['user_id'] != user_id_to_purge]
    
    if len(df_clean) < initial_count:
        df_clean.to_csv(data_path, index=False)
        print(f"  ✅ PURGED: {initial_count - len(df_clean)} records removed.")
        
        # 2. Trigger Retraining Flag
        print("  🔄 RE-TRAIN TRIGGERED: Marking model for urgent update due to data removal.")
        with open("artifacts/RETRAIN_NEEDED.txt", "w") as f:
            f.write(f"Purge Event: User {user_id_to_purge} at {os.times().elapsed}")
    else:
        print("  ℹ️ User ID not found in dataset. No action required.")

if __name__ == "__main__":
    # Test purge
    purge_user_data(1001)
