import numpy as np

def run_ensemble_vote(predictions):
    """Phase 9: Collective Intelligence - Multi-Model Voting Ensemble."""
    print("🗳️ Phase 9: Starting Multi-Model Voting Ensemble...")
    
    # predictions is a list of results from different models [0, 1, 1, 0, 1]
    votes = np.array(predictions)
    
    # Simple Majority Vote
    final_decision = 1 if np.mean(votes) > 0.5 else 0
    
    confidence = np.mean(votes) if final_decision == 1 else 1 - np.mean(votes)
    
    print(f"  🏁 Ensemble Results: {votes}")
    res_label = 'CHURN' if final_decision == 1 else 'STAY'
    msg = f"  ✅ Final Decision: {res_label} (Confidence: {confidence*100:.1f}%)"
    print(msg)
    
    return final_decision

if __name__ == "__main__":
    # Simulating 5 models in the ensemble
    run_ensemble_vote([1, 0, 1, 1, 0])
