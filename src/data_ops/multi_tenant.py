import pandas as pd

def enforce_tenant_isolation(data, request_tenant_id):
    """Phase 3: DataSecOps - Multi-Tenant Privacy Isolation."""
    print(f"🧱 Phase 3: Enforcing Isolation for Tenant: {request_tenant_id}...")
    
    # Simulating data with tenant tags
    df = pd.DataFrame(data)
    if 'tenant_id' not in df.columns:
        df['tenant_id'] = 'TENANT-001' # Default for simulation
        
    cross_tenant_data = df[df['tenant_id'] != request_tenant_id]
    
    if len(cross_tenant_data) > 0:
        msg = (
            "❌ SECURITY BREACH: Cross-Tenant leakage detected! "
            f"(Found data for: {cross_tenant_data['tenant_id'].unique()})"
        )
        print(msg)
        print("🚫 CRITICAL SHUTDOWN: Purging memory and aborting request.")
        return False
    else:
        print(f"✅ Isolation Verified. Request is safe for {request_tenant_id}.")
        return True

if __name__ == "__main__":
    test_data = [
        {'user_id': 1, 'tenant_id': 'TENANT-001'},
        {'user_id': 2, 'tenant_id': 'TENANT-002'}
    ]
    enforce_tenant_isolation(test_data, "TENANT-001")
