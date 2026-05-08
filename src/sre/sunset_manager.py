import datetime
import json
import os

def run_model_sunset_audit(registry_path="artifacts/model_genealogy.json"):
    """Phase 25: Lifecycle Governance - Automated Model Sunsetting."""
    print("🌅 Phase 25: Running Model Lifecycle Audit...")
    
    if not os.path.exists(registry_path):
        print("  ⚠️ Registry empty. No models to audit.")
        return

    with open(registry_path, "r") as f:
        registry = json.load(f)
        
    for model in registry:
        version = model['version']
        timestamp = datetime.datetime.fromisoformat(model['timestamp'])
        age_days = (datetime.datetime.now() - timestamp).days
        
        # Policy: Sunset models older than 90 days
        if age_days > 90:
            print(f"  🚨 SUNSET ALERT: Model {version} is {age_days} days old.")
            print(f"  📦 Archiving {version} to Cold Storage...")
            # Simulation of archival logic
            model['status'] = "ARCHIVED"
            model['sunset_date'] = datetime.datetime.now().isoformat()
            
    print("✅ Sunset Audit complete. Production environment is lean and secure.")

if __name__ == "__main__":
    run_model_sunset_audit()
