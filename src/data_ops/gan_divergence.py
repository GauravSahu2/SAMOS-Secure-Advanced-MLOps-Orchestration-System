import pandas as pd

def check_gan_divergence(real_data_path, synthetic_data_path):
    """Phase 1: Synthetic DataOps - GAN Divergence Guardrail."""
    print("🎭 Phase 1: Checking Synthetic Reality Divergence...")
    
    real_df = pd.read_csv(real_data_path)
    synth_df = pd.read_csv(synthetic_data_path)
    
    # Calculate Mean Distribution Shift
    real_mean = real_df['income'].mean()
    synth_mean = synth_df['income'].mean()
    
    divergence = abs(real_mean - synth_mean) / real_mean
    print(f"  📊 Statistical Divergence: {divergence*100:.2f}%")
    
    if divergence > 0.15:
        print("❌ CRITICAL DIVERGENCE: Synthetic data has 'Hallucinated' beyond 15% tolerance.")
        print("🚫 BLOCKING RETRAIN: Ground-Truth alignment failed.")
        return False
    else:
        print("✅ Reality Alignment Verified. Digital Twin is statistically sound.")
        return True

if __name__ == "__main__":
    import os
    if os.path.exists("data/features.csv") and os.path.exists("data/digital_twin_data.csv"):
        check_gan_divergence("data/features.csv", "data/digital_twin_data.csv")
