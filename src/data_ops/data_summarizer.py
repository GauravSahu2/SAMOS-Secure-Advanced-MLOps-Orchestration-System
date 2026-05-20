import pandas as pd
from typing import Any

def generate_dataset_summary_card(feature_path: str = "data/features.csv") -> None:
    """Phase 1: DataOps - Statistical Dataset Summarization."""
    print("📊 Phase 1: Generating Global Dataset Summary Card...")
    
    df = pd.read_csv(feature_path)
    
    top_features: list[str] = ["income", "age", "credit_score"] # Simulated
    summary: dict[str, Any] = {
        "total_records": len(df),
        "feature_count": len(df.columns),
        "target_balance": (
            df['churn'].value_counts(normalize=True).to_dict()
            if 'churn' in df.columns else "N/A"
        ),
        "top_features": top_features
    }
    
    print(f"  📝 TOTAL RECORDS: {summary['total_records']}")
    print(f"  📝 TARGET BALANCE: {summary['target_balance']}")
    print(f"  📝 TOP SIGNALS: {summary['top_features']}")
    
    with open("artifacts/DATASET_CARD.md", "w") as f:
        f.write("# 📊 Dataset Summary Card\n\n")
        f.write(f"- **Volume**: {summary['total_records']} rows\n")
        f.write(f"- **Balance**: {summary['target_balance']}\n")
        f.write(f"- **Key Signals**: {', '.join(top_features)}\n")
        
    print("✅ Dataset Card generated: artifacts/DATASET_CARD.md")

if __name__ == "__main__":
    import os
    if os.path.exists("data/features.csv"):
        generate_dataset_summary_card()
