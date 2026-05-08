import pandas as pd

def detect_proxy_bias(data_path, sensitive_attr="age", threshold=0.8):
    """Phase 13: Advanced Ethics - Proxy Bias Correlation Analysis."""
    print(f"🕵️ Phase 13: Scanning for Proxy Attributes (Target: {sensitive_attr})...")
    
    df = pd.read_csv(data_path)
    
    # Calculate Correlation Matrix
    corr_matrix = df.corr().abs()
    
    # Find features highly correlated with the sensitive attribute
    proxies = corr_matrix[sensitive_attr][corr_matrix[sensitive_attr] > threshold]
    proxies = proxies.drop(sensitive_attr, errors='ignore') # Drop the self-correlation
    
    if len(proxies) > 0:
        msg = (
            f"❌ PROXY ALERT: High correlation detected between "
            f"'{sensitive_attr}' and: {list(proxies.index)}"
        )
        print(msg)
        print(f"⚠️ These features may be acting as 'Proxy Discriminators' (Corr > {threshold}).")
        return False
    else:
        print(f"✅ No high-correlation proxies found for '{sensitive_attr}'.")
        return True

if __name__ == "__main__":
    import os
    if os.path.exists("data/features.csv"):
        detect_proxy_bias("data/features.csv")
