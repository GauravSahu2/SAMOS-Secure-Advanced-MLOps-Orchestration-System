import pandas as pd

def heal_data(input_path: str, output_path: str) -> pd.DataFrame:
    """Phase 2: Self-Healing Data Repair (Auto-Imputation)."""
    print("🩹 Phase 2: Starting Self-Healing Data Repair...")
    df = pd.read_csv(input_path)
    missing_count = df.isnull().sum().sum()
    if missing_count > 0:
        print(f"🛠 Detected {missing_count} missing values. Applying Mean Imputation...")
        for col in df.select_dtypes(include='number').columns:
            df[col] = df[col].fillna(df[col].mean())
    if 'age' in df.columns:
        print("🛠 Fixing out-of-range values (e.g. Age > 120)...")
        df.loc[df['age'] > 120, 'age'] = df['age'].median()
    df.to_csv(output_path, index=False)
    print(f"✅ Data Healed and Saved to {output_path}")
    return df


def run_self_healing(path: str) -> None:
    """In-place variant: reads `path`, heals, and writes back to same path."""
    heal_data(path, path)


if __name__ == "__main__":
    heal_data("data/bronze_data.csv", "data/features_healed.csv")
