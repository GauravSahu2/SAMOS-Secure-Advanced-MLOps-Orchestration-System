"""
====================================================================================================
SAMOS INTEGRATIONS: prometheus_metrics.py
Integration: Prometheus Exporter
Description: Exports factory telemetry (throughput, latency, drift) to Prometheus.
====================================================================================================
"""

import time
import random
try:
    from prometheus_client import start_http_server, Gauge, Counter
except ImportError:
    start_http_server = None

# Define custom metrics for SAMOS
PHASE_LATENCY = Gauge('samos_phase_latency_seconds', 'Latency of the last executed phase', ['phase'])
FACTORY_THROUGHPUT = Counter('samos_processed_tokens_total', 'Total tokens processed by the factory')
MODEL_DRIFT_SCORE = Gauge('samos_model_drift_score', 'Current estimated model drift (0.0 - 1.0)')

def start_metrics_server(port=9091):
    """Starts the Prometheus metrics server."""
    if not start_http_server:
        print("⚠️ prometheus_client not installed. Metrics export disabled.")
        return
    
    print(f"📊 Starting Prometheus Metrics Server on port {port}...")
    start_http_server(port)
    
    # Simulate some initial metrics
    MODEL_DRIFT_SCORE.set(random.uniform(0.01, 0.05))
    print("✅ Metrics server is live. Scrape target: http://localhost:9091/metrics")

if __name__ == "__main__":
    start_metrics_server()
    # Keep alive for demonstration
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Stopping metrics server.")
