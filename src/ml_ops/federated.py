import numpy as np

def simulate_federated_learning():
    """Phase 9: Federated Learning (FedAvg Simulation)."""
    print("🌐 Initializing Federated Learning Aggregator...")
    
    # Simulating 3 Decentralized Clients (e.g., 3 different hospitals)
    # Each client has its own local model weights
    client_1_weights = np.random.normal(0, 1, (5, 5))
    client_2_weights = np.random.normal(0, 1, (5, 5))
    client_3_weights = np.random.normal(0.1, 1, (5, 5))
    
    print("📡 Receiving weight updates from 3 local nodes...")
    
    # Federated Averaging (FedAvg)
    global_model_weights = (client_1_weights + client_2_weights + client_3_weights) / 3
    
    print("✅ Global Model Updated. Weights aggregated successfully.")
    print(f"📊 Global Model Variance: {np.var(global_model_weights):.4f}")

if __name__ == "__main__":
    simulate_federated_learning()
