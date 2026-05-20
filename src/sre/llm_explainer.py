
from typing import Any

def explain_prediction_with_llm(prediction: int, shap_values: dict[str, float], user_profile: dict[str, Any]) -> str:
    """Phase 24: Conversational AI - LLM Prediction Explainer."""
    print("💬 Phase 24: Generating LLM Narrative Explanation...")
    
    # In a real scenario, this would be a prompt to Qwen/Llama
    # Here we simulate the LLM's natural language output
    
    explanation = (
        f"The model predicts that this user is "
        f"{'LIKELY' if prediction == 1 else 'UNLIKELY'} to churn.\n\n"
        "Reasoning:\n"
        f"- The primary driver is 'Income' (SHAP: {shap_values.get('income', 0.8)}), "
        "which is below the cohort average.\n"
        f"- 'Age' ({user_profile['age']}) provides some stability, but not enough "
        "to offset the financial risk.\n\n"
        "Strategic Recommendation:\n"
        "- Offer a 'Loyalty Retention' package with a 15% discount to mitigate "
        "the income-related churn risk.\n"
    )
    
    print(f"🤖 LLM Narrative:\n{explanation}")
    return explanation

if __name__ == "__main__":
    shap = {"income": 0.85, "age": -0.2}
    profile = {"age": 45, "income": 35000}
    explain_prediction_with_llm(1, shap, profile)
