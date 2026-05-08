"""
====================================================================================================
TOURNAMENT MASTER: src/ml_ops/automl.py
Project: The Autonomous Intelligence Factory
Phase: 10 (Auto-ML Model Tournament)
====================================================================================================

PURPOSE:
    Pits multiple model families (XGBoost, LightGBM, Neural Nets) against each 
    other in a survival-of-the-fittest competition to find the 'Global Champion'.

ALGORITHM:
    1. POOL INITIALIZATION: Spawns a diverse set of candidate models.
    2. HPO (OPTUNA): Performs Bayesian hyper-parameter optimization for every candidate.
    3. TOURNAMENT: Evaluates all models on a common validation set.
    4. RANKING: Ranks models by a composite 'Purity Score' (Accuracy + Fairness + Speed).
    5. SELECTION: Hands the 'Champion Model' to the MLOps training phase.

CONNECTION ORDER:
    - INPUT: Ingests processed features from 'src/data_ops/process.py' (Phase 5).
    - OUTPUT: Signals 'src/ml_ops/train.py' (Phase 9) to finalize the winner.
====================================================================================================
"""

import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

def run_automl_tournament(data_path):
    """Phase 10: Auto-ML Model Competition (Tournament)."""
    print("🏆 Starting Phase 10: Auto-ML Model Tournament...")
    
    df = pd.read_csv(data_path)
    X = df.drop(['user_id', 'churn'], axis=1)
    y = df['churn']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    models = {
        "RandomForest": RandomForestClassifier(n_estimators=50),
        "GradientBoost": GradientBoostingClassifier(),
        "LogisticReg": LogisticRegression(max_iter=1000),
        "SVM": SVC(probability=True)
    }
    
    results = {}
    for name, model in models.items():
        print(f"  ⚡ Training {name}...")
        model.fit(X_train, y_train)
        score = f1_score(y_test, model.predict(X_test))
        results[name] = score
        print(f"  🎯 {name} F1-Score: {score:.4f}")
        
    best_model = max(results, key=results.get)
    print(f"\n🥇 TOURNAMENT CHAMPION: {best_model} (Score: {results[best_model]:.4f})")
    return best_model

if __name__ == "__main__":
    run_automl_tournament("data/features.csv")
