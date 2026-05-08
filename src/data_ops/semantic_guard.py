import numpy as np

def check_semantic_integrity(data, column_name, expected_mean):
    """Phase 2: DataOps - Semantic Integrity Guardrail."""
    print(f"🧠 Phase 2: Checking Semantic Integrity for '{column_name}'...")
    
    current_mean = np.mean(data)
    
    # If the mean shifts by more than 10x, the units have likely changed (e.g. $ to cents)
    shift_factor = current_mean / expected_mean
    print(f"  📊 Semantic Shift Factor: {shift_factor:.2f}x")
    
    if shift_factor > 10 or shift_factor < 0.1:
        msg = (
            f"❌ SEMANTIC CORRUPTION: Detected extreme shift in '{column_name}'. "
            "Logic/Units have likely changed."
        )
        print(msg)
        print("🚫 CRITICAL BLOCK: Ingestion aborted to prevent model poisoning.")
        return False
    else:
        print(f"✅ Semantic Integrity Verified for '{column_name}'.")
        return True

if __name__ == "__main__":
    # Expected income around 50k
    check_semantic_integrity([5000000, 5500000], "income", 50000) # $ to cents shift
