"""
====================================================================================================
SAMOS DATAOPS: nifi_bridge.py
Integration: Apache NiFi -> SAMOS Ingestion
Description: Automated bridge to pull orchestrated data from NiFi flowfiles.
====================================================================================================
"""

import os
try:
    import nipyapi
except ImportError:
    nipyapi = None

def check_nifi_status():
    """Checks the health of the NiFi cluster."""
    print("🔍 Checking Apache NiFi status...")
    if not nipyapi:
        print("⚠️ NiPyApi not installed. Run 'pip install nipyapi' for full integration.")
        return False
    
    nifi_url = os.getenv("NIFI_URL", "http://localhost:8080/nifi-api")
    nipyapi.config.nifi_config.host = nifi_url
    
    try:
        status = nipyapi.system.get_nifi_status()
        print(f"✅ NiFi is ONLINE. Cluster state: {status.process_group_status.aggregate_snapshot.active_thread_count} active threads.")
        return True
    except Exception as e:
        print(f"❌ Could not connect to NiFi: {e}")
        return False

def pull_data_from_nifi(output_port_name="SAMOS_OUT"):
    """
    Simulates pulling data from a NiFi Output Port.
    In a real production environment, this would use Site-to-Site (S2S) 
    or a dedicated NiFi REST API endpoint.
    """
    print(f"📥 Attempting to pull data from NiFi Output Port: {output_port_name}")
    # Production Logic: Use nipyapi.canvas.get_port() and then fetch flowfiles
    print("✨ NiFi Bridge: Data stream synchronized. (Simulated)")
    return True

if __name__ == "__main__":
    if check_nifi_status():
        pull_data_from_nifi()
    else:
        print("🚀 Proceeding with Local DataOps (NiFi fallback active).")
