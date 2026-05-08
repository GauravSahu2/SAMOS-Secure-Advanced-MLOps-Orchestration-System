def run_model_debate(user_id, model_a_pred, model_b_pred):
    """Phase 9: Collaborative Intelligence - Model Debate Protocol."""
    print(f"🤝 Phase 9: Starting Model Debate for User {user_id}...")
    
    print(f"  🤖 Model A (RF) Prediction: {model_a_pred}")
    print(f"  🤖 Model B (LLM) Prediction: {model_b_pred}")
    
    if model_a_pred == model_b_pred:
        print("  ✅ Consensus Reached. Proceeding with prediction.")
        return model_a_pred
    else:
        print("  🚨 DISAGREEMENT DETECTED! Calling Arbiter Model...")
        # Simple Arbiter Logic: Choose the more conservative prediction
        final_pred = 1 # Safety first (predict churn)
        print(f"  ⚖️ Arbiter Decision: {final_pred} (Conservative Bias)")
        return final_pred

if __name__ == "__main__":
    run_model_debate("USER-101", 0, 1)
