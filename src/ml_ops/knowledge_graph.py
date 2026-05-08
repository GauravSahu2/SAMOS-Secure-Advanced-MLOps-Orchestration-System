import json

def generate_knowledge_graph():
    """Phase 11: Meta-Lineage - Knowledge Graph Generator."""
    print("🌳 Phase 11: Building the Universal Knowledge Graph...")
    
    graph = {
        "nodes": [
            {"id": "data_v1", "type": "Dataset", "label": "Churn Data V1"},
            {"id": "proc_v1", "type": "Process", "label": "Feature Engineering"},
            {"id": "train_v1", "type": "Training", "label": "Auto-ML Tournament"},
            {"id": "model_v1", "type": "Model", "label": "Champion RF Model"},
            {"id": "audit_v1", "type": "Security", "label": "Red-Team Audit"},
            {"id": "serve_v1", "type": "Deployment", "label": "FastAPI Production"}
        ],
        "links": [
            {"source": "data_v1", "target": "proc_v1"},
            {"source": "proc_v1", "target": "train_v1"},
            {"source": "train_v1", "target": "model_v1"},
            {"source": "model_v1", "target": "audit_v1"},
            {"source": "audit_v1", "target": "serve_v1"}
        ]
    }
    
    with open("artifacts/knowledge_graph.json", "w") as f:
        json.dump(graph, f, indent=4)
        
    print("✅ Knowledge Graph saved: artifacts/knowledge_graph.json")
    print("💡 This JSON can be rendered in D3.js for visual lineage exploration.")

if __name__ == "__main__":
    generate_knowledge_graph()
