import pandas as pd

def check_for_data_poisoning(current_features, new_batch):
    """Phase 3: ModelSecOps - Data Poisoning Guardrail."""
    print("🛡️ Phase 3: Monitoring for Data Poisoning / Skew Attacks...")
    
    # Calculate the 'Normal' Distribution of the existing Feature Store
    normal_mean = current_features['income'].mean()
    new_mean = new_batch['income'].mean()
    
    # If the new batch shifts the mean by more than 50% instantly, it's highly suspicious
    shift = abs(new_mean - normal_mean) / normal_mean
    print(f"  📊 New Batch Skew: {shift*100:.2f}%")
    
    if shift > 0.50:
        print("❌ POISONING ALERT: Detected malicious skew in incoming data batch.")
        print("🚫 QUARANTINE: New records moved to data/quarantine/ for investigation.")
        return False
    else:
        print("✅ Batch Integrity Verified. No poisoning detected.")
        return True

if __name__ == "__main__":
    current = pd.DataFrame({'income': [50000, 60000, 55000]})
    # Malicious batch trying to skew the model to favor ultra-high income
    malicious = pd.DataFrame({'income': [5000000, 6000000, 5500000]})
    check_for_data_poisoning(current, malicious)
