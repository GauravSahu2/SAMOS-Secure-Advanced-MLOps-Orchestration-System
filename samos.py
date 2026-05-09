#!/usr/bin/env python3
"""
====================================================================================================
SAMOS COMMAND CENTER: samos.py
Project: Secure Advanced MLOps & Orchestration System
Description: Granular phase and group orchestration CLI.
====================================================================================================
"""

import sys
import argparse
import os
from main import run_phase

# Mapping of all phases to their respective scripts (Phase 0 is for Enterprise Integrations)
PHASE_SCRIPTS = {
    0: [
        ("src/data_ops/nifi_bridge.py", "Apache NiFi Data Bridge"),
        ("src/integrations/airflow_sync.py", "Airflow Workflow Sync"),
        ("src/integrations/prometheus_metrics.py", "Prometheus Telemetry Export"),
        ("src/integrations/tool_integrator.py", "Full 75-Tool Enterprise Synchronization"),
    ],
    1: [
        ("src/data_ops/ingest.py", "Data Sourcing"),
        ("src/data_ops/lake_health.py", "Data Lake Health Audit"),
        ("src/data_ops/data_summarizer.py", "Dataset Summary Card"),
        ("src/data_ops/multi_modal.py", "Multi-Modal Signal Fusion"),
        ("src/data_ops/digital_twin.py", "Digital Twin Data Simulation"),
        ("src/data_ops/gan_divergence.py", "Synthetic Reality Guardrail"),
        ("src/data_ops/kafka_backbone.py", "Apache Kafka Backbone"),
        ("src/data_ops/spark_compute.py", "Apache Spark Compute"),
        ("src/data_ops/clickhouse_olap.py", "ClickHouse OLAP Sync"),
    ],
    2: [
        ("src/data_ops/validate.py", "Data Validation"),
        ("src/data_ops/anomaly_inversion.py", "Data Anomaly Inversion"),
        ("src/data_ops/semantic_guard.py", "Semantic Integrity Check"),
        ("src/data_ops/schema_evolver.py", "Dynamic Schema Evolution"),
        ("src/data_ops/self_healing.py", "Self-Healing Data Repair"),
    ],
    3: [
        ("src/data_ops/data_purge.py", "Right to be Forgotten Purge"),
        ("src/data_ops/sovereignty.py", "Data Sovereignty Check"),
        ("src/data_ops/multi_tenant.py", "Multi-Tenant Data Isolation"),
        ("src/data_ops/zk_data_proof.py", "ZK Data Integrity Proof"),
        ("src/data_ops/mask_pii.py", "DataSecOps (PII Masking)"),
        ("src/data_ops/privacy.py", "Differential Privacy"),
        ("src/model_sec/enclave.py", "Confidential Computing Enclave"),
    ],
    4: [
        ("src/data_ops/process.py", "Processing & Feature Store"),
        ("src/data_ops/genetic_features.py", "Genetic Feature Evolution"),
        ("src/ml_ops/rfe_optimizer.py", "Recursive Feature Elimination"),
        ("src/ml_ops/ant_colony.py", "Bio-Inspired Feature Selection"),
    ],
    5: [
        ("src/data_ops/process.py", "Feature Store Finalization"),
    ],
    6: [
        ("src/ml_ops/genealogy.py", "Data Genealogy & Lineage"),
    ],
    7: [
        ("src/ml_ops/active_learning.py", "Active Learning Loop"),
    ],
    8: [
        ("src/ml_ops/rlhf.py", "Reinforcement Learning from Human Feedback"),
    ],
    9: [
        ("src/ml_ops/debate.py", "Model Debate Protocol"),
        ("src/ml_ops/ensemble.py", "Multi-Model Ensemble Voting"),
        ("src/ml_ops/expert_router.py", "Neural Expert Routing"),
        ("src/ml_ops/curriculum.py", "Curriculum-Based Training"),
        ("src/ml_ops/train.py", "Training Champion Architecture"),
        ("src/ml_ops/transfer_logic.py", "Cross-Domain Knowledge Transfer"),
        ("src/ml_ops/swa_merger.py", "Stochastic Weight Averaging"),
        ("src/ml_ops/fisher_merging.py", "Fisher-Information Merging"),
        ("src/ml_ops/federated.py", "Federated Weight Aggregation"),
        ("src/ml_ops/ray_scaler.py", "Ray Distributed Scaler"),
    ],
    10: [
        ("src/ml_ops/automl.py", "Auto-ML Model Tournament"),
        ("src/ml_ops/llm_tuner.py", "LLM-Guided Parameter Tuning"),
        ("src/ml_ops/nas.py", "Neural Architecture Search"),
        ("src/ml_ops/quantum_ml.py", "Quantum-ML Weighting"),
    ],
    11: [
        ("src/ml_ops/knowledge_graph.py", "Knowledge Graph Integration"),
    ],
    12: [
        ("src/model_sec/evaluate.py", "Evaluation & Governance"),
        ("src/ml_ops/uncertainty.py", "Uncertainty Calibration"),
        ("src/model_sec/counterfactuals.py", "Counterfactual Explanations"),
    ],
    13: [
        ("src/model_sec/bias_audit.py", "Ethical Bias Audit"),
        ("src/model_sec/live_bias_fix.py", "Inference-Time Bias Mitigation"),
        ("src/model_sec/regret_minimizer.py", "Ethical Regret Minimization"),
        ("src/model_sec/intersectional_bias.py", "Intersectional Bias Check"),
        ("src/model_sec/proxy_bias.py", "Proxy Variable Bias Audit"),
        ("src/model_sec/fairlearn_audit.py", "Fairlearn Ethical Audit"),
    ],
    14: [
        ("src/model_sec/adversarial.py", "Adversarial Robustness Testing"),
        ("src/sre/chaos_monkey_v2.py", "Extreme Chaos Monkey V2"),
        ("src/model_sec/chaos_test.py", "Model Structure Chaos Test"),
        ("src/model_sec/poisoning_guard.py", "Data Poisoning Guard"),
        ("src/model_sec/garak_scan.py", "Garak LLM Vulnerability Scan"),
    ],
    15: [
        ("src/ml_ops/watermark.py", "Model IP Watermarking"),
    ],
    16: [
        ("src/model_sec/compliance_filing.py", "Automated Regulatory Filing"),
        ("src/devsecops/social_trust.py", "Zero-Knowledge Social Proof"),
        ("src/ml_ops/ledger.py", "Immutable Governance Ledger"),
        ("src/sre/multi_lang_cards.py", "Multi-Language Regulatory Transparency"),
        ("src/model_sec/model_card.py", "Model Card Generation"),
        ("src/model_sec/zkp_guard.py", "ZKP Privacy Guard"),
    ],
    17: [
        ("src/sre/serve.py", "Serving Layer Deployment"),
        ("src/devsecops/advanced_security.py", "Advanced Inference Security"),
    ],
    18: [
        ("src/devsecops/self_healing_code.py", "Self-Healing Code Patching"),
        ("src/devsecops/style_repair.py", "Infinite Style Auto-Repair"),
        ("src/devsecops/dependency_patcher.py", "Supply-Chain Hardening"),
        ("src/devsecops/trivy_scan.py", "Trivy Vulnerability Scan"),
        ("src/devsecops/vault_manager.py", "HashiCorp Vault Sync"),
    ],
    19: [
        ("src/devsecops/agent_audit.py", "Autonomous Agent Audit"),
        ("src/devsecops/zero_trust.py", "Zero-Trust Architecture Sync"),
    ],
    20: [
        ("src/devsecops/red_team.py", "Automated Red-Team Attack"),
        ("src/devsecops/pqc_sim.py", "Post-Quantum Cryptography"),
        ("src/devsecops/prompt_sec.py", "Prompt Injection Guard"),
    ],
    21: [
        ("src/ml_ops/distill.py", "Teacher-Student Knowledge Distillation"),
        ("src/ml_ops/one_shot_distill.py", "One-Shot Model Compression"),
        ("src/ml_ops/multi_teacher.py", "Multi-Teacher Committee Distillation"),
        ("src/devsecops/pruning.py", "Extreme Model Pruning"),
        ("src/devsecops/optimize.py", "Model Optimization & Quantization"),
        ("src/ml_ops/bentoml_server.py", "BentoML Serving Build"),
        ("src/ml_ops/triton_adapter.py", "NVIDIA Triton Configuration"),
    ],
    22: [
        ("src/sre/autoscaler.py", "Intelligent Resource Autoscaler"),
        ("src/sre/failover.py", "High-Availability Failover Logic"),
    ],
    23: [
        ("src/sre/mab_gateway.py", "MAB Dynamic Traffic Routing"),
    ],
    24: [
        ("src/sre/llm_explainer.py", "LLM Prediction Narrative"),
        ("src/sre/power_optimizer.py", "Green-AI Power Optimization"),
        ("src/sre/cascading.py", "Model Cascading Router"),
        ("src/sre/threshold_tuner.py", "Strategic Threshold Tuning"),
        ("src/sre/resource_auction.py", "Economic Resource Allocation"),
    ],
    25: [
        ("src/sre/proactive_drift.py", "Proactive Drift Forecasting"),
        ("src/sre/concept_drift.py", "Concept Drift Detection"),
        ("src/sre/incident_response.py", "Autonomous Incident Response"),
        ("src/sre/planetary_latency.py", "Inter-Planet Latency Sync"),
        ("src/ml_ops/pipeline_optimizer.py", "Genetic Pipeline Architect"),
        ("src/model_sec/omni_governance.py", "Absolute Omni-Governance"),
        ("src/sre/diagram_generator.py", "Visual Architecture Mapping"),
        ("src/sre/meta_critic.py", "Meta-Critic Execution Audit"),
        ("src/sre/sunset_manager.py", "Model Lifecycle Sunsetting"),
        ("src/sre/live_docs.py", "Autonomous Self-Documentation"),
        ("src/sre/wiki_gen.py", "Model Wiki Generator"),
        ("src/sre/walkthrough_gen.py", "Automated Video Scripting"),
        ("src/sre/visualizer.py", "Terminal Command Center Visualizer"),
        ("src/sre/stress_test_v2.py", "Inference Stress-Test"),
        ("src/sre/rollback.py", "Automated Model Rollback"),
        ("src/sre/notif.py", "Real-Time Webhook Notifications"),
        ("src/sre/nlp_orchestrator.py", "Natural Language Pipeline Orchestration"),
        ("src/sre/nlp_deploy.py", "Human-Aligned Deployment"),
        ("src/sre/meta_optimizer.py", "Pipeline Efficiency Audit"),
        ("src/sre/ct_loop.py", "Continuous Training Loop"),
        ("src/sre/alert_formatter.py", "Telemetry Alert Formatting"),
        ("src/sre/chaos_mesh.py", "Chaos Mesh Resilience Trigger"),
        ("src/sre/opentelemetry_trace.py", "OpenTelemetry Global Trace"),
        ("src/sre/jaeger_tracer.py", "Jaeger Distributed Tracing"),
    ],
}

# Mapping of groups to phase ranges
GROUP_MAPPING = {
    "integrations": [0],
    "dataops": list(range(0, 7)), # Now includes Phase 0
    "mlops": list(range(7, 12)),
    "modelsecops": list(range(12, 17)),
    "devsecops": list(range(17, 22)),
    "sre": list(range(22, 26)),
}

def execute_phases(phase_list):
    """Executes a list of phases in order."""
    for phase in sorted(list(set(phase_list))):
        if phase in PHASE_SCRIPTS:
            for script_path, description in PHASE_SCRIPTS[phase]:
                run_phase(script_path, f"Phase {phase}: {description}")
        else:
            print(f"⚠️ Warning: Phase {phase} has no registered scripts.")

def main():
    parser = argparse.ArgumentParser(description="SAMOS Command Center: Trigger specific phases or groups of the pipeline.")
    
    # Phase selection
    parser.add_argument("--phase", type=int, help="Trigger a single phase (1-25)")
    parser.add_argument("--phases", type=str, help="Comma-separated list of phases (e.g., 1,2,4 or 3-6,15)")
    
    # Group selection
    parser.add_argument("--group", type=str, choices=GROUP_MAPPING.keys(), help="Trigger a specific domain group")
    parser.add_argument("--groups", type=str, help="Comma-separated list of groups (e.g., dataops,mlops)")
    
    # Modes and All
    parser.add_argument("--all", action="store_true", help="Trigger the entire 25-phase pipeline")
    parser.add_argument("--mode", type=str, choices=["structured", "llm"], default="structured", help="Execution mode (default: structured)")
    
    args = parser.parse_args()

    # Determine which phases to run
    phases_to_run = []

    if args.all:
        phases_to_run = list(range(1, 26))
    
    if args.group:
        phases_to_run.extend(GROUP_MAPPING[args.group])
    
    if args.groups:
        for g in args.groups.split(','):
            g = g.strip().lower()
            if g in GROUP_MAPPING:
                phases_to_run.extend(GROUP_MAPPING[g])
            else:
                print(f"❌ Error: Group '{g}' not found.")
                sys.exit(1)
    
    if args.phase is not None:
        phases_to_run.append(args.phase)
    
    if args.phases:
        # Handle ranges like 1-5 and individual numbers
        for part in args.phases.split(','):
            if '-' in part:
                start, end = map(int, part.split('-'))
                phases_to_run.extend(list(range(start, end + 1)))
            else:
                phases_to_run.append(int(part))

    if not phases_to_run:
        parser.print_help()
        sys.exit(0)

    # Dedup and sort
    phases_to_run = sorted(list(set(phases_to_run)))

    print(f"🎯 SAMOS Command Center: Triggering {len(phases_to_run)} phases...")
    execute_phases(phases_to_run)
    
    print("\n🏆 OPERATION COMPLETE.")

if __name__ == "__main__":
    main()
