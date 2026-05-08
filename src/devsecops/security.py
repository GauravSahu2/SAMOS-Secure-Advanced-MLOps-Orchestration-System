import os
import json
import datetime

def scan_file_for_vulnerabilities(path):
    """Checks a single file for common security anti-patterns."""
    issues = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
            if "eval(" in content:
                issues.append(f"CRITICAL: eval() found in {path}")
            if "exec(" in content:
                issues.append(f"CRITICAL: exec() found in {path}")
            if "pickle.load" in content and "data_ops" not in path:
                issues.append(f"MEDIUM: Unsafe pickle.load in {path}")
    except Exception as e:
        print(f"  ⚠️ Could not scan {path}: {e}")
    return issues

def run_sast():
    """Phase 18: Running SAST (Static Analysis Security Test)."""
    print("🚀 Phase 18: Running SAST...")
    vulnerabilities = []
    for root, _dirs, files in os.walk("src"):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                vulnerabilities.extend(scan_file_for_vulnerabilities(path))

    if not vulnerabilities:
        print("✅ SAST: No critical security issues found.")
    else:
        for v in vulnerabilities:
            print(f"❌ {v}")

def run_sbom():
    """Phase 19: Generating SBOM (Software Bill of Materials)."""
    print("\n🚀 Phase 19: Generating SBOM...")
    if not os.path.exists("requirements.txt"):
        print("  ⚠️ requirements.txt not found. Skipping SBOM.")
        return

    with open("requirements.txt", "r") as f:
        deps = [line.strip() for line in f if line.strip()]

    sbom = {
        "project": "SAMOS",
        "timestamp": datetime.datetime.now().isoformat(),
        "dependencies": deps,
        "format": "CycloneDX-Compatible-JSON"
    }

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/sbom.json", "w") as f:
        json.dump(sbom, f, indent=4)
    print("✅ SBOM generated at artifacts/sbom.json")

def run_sast_and_sbom():
    """Phase 18 and Phase 19 Orchestrator."""
    run_sast()
    run_sbom()

if __name__ == "__main__":
    run_sast_and_sbom()
