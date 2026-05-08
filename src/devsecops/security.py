import os
import json
import datetime

def run_sast_and_sbom():
    """Phase 18 (SAST) and Phase 19 (SBOM)."""
    print("🚀 Phase 18: Running SAST (Static Analysis Security Test)...")
    
    vulnerabilities = []
    # Simple logic to find common security issues if Bandit isn't installed
    for root, dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()
                    if "eval(" in content:
                        vulnerabilities.append(f"CRITICAL: eval() found in {path}")
                    if "exec(" in content:
                        vulnerabilities.append(f"CRITICAL: exec() found in {path}")
                    if "pickle.load" in content and "data_ops" not in path:
                        vulnerabilities.append(f"MEDIUM: Unsafe pickle.load in {path}")

    if not vulnerabilities:
        print("✅ SAST: No critical security issues found.")
    else:
        for v in vulnerabilities:
            print(f"❌ {v}")

    print("\n🚀 Phase 19: Generating SBOM (Software Bill of Materials)...")
    with open("requirements.txt", "r") as f:
        deps = [line.strip() for line in f if line.strip()]
    
    sbom = {
        "project": "25-Phase-MLOps",
        "timestamp": datetime.datetime.now().isoformat(),
        "dependencies": deps,
        "format": "CycloneDX-Compatible-JSON"
    }
    
    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/sbom.json", "w") as f:
        json.dump(sbom, f, indent=4)
    print("✅ SBOM generated at artifacts/sbom.json")

if __name__ == "__main__":
    run_sast_and_sbom()
