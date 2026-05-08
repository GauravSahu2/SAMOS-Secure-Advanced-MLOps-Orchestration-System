"""
====================================================================================================
CENTRAL NERVOUS SYSTEM: main.py
Project: SAMOS: Secure Advanced MLOps & Orchestration System
Phase: 0-25 Orchestration (Absolute Terminus)
====================================================================================================

OVERVIEW:
    This is the master orchestrator of the world's most advanced AI factory. It manages 
    over 190 specialized modules, ensuring they execute in a rigorous, dependency-aware 
    sequence. From raw data ingestion to inter-planetary latency simulation, every 
    phase is controlled here.

ARCHITECTURE DOMAINS:
    1. DataOps: Ingests, fuses, and evolved features. (The Source)
    2. MLOps: Trains, distills, and optimizes neural architectures. (The Soul)
    3. ModelSecOps: Audits, attacks, and hardens the model. (The Judge)
    4. DevSecOps: Self-heals code and secures the supply chain. (The Purity)
    5. SRE: Serves, scales, and optimizes for planetary operations. (The Guardian)

CONNECTION LOGIC:
    - Input: Environment variables, requirements.txt, and raw dataset pointers.
    - Output: A production-ready, ethically-aligned, and hardware-optimized model.
    - Flow: Sequential domain execution with failure isolation and self-healing.
====================================================================================================
"""

import subprocess
import os
import sys

def run_phase(script_path, description):
    """
    Standardizes the execution of a factory module.
    
    Logic:
        1. Encapsulates each phase in a subprocess for memory/env isolation.
        2. Captures stdout/stderr for the 'Meta-Critic' and 'Live-Docs' agents.
        3. Fails-fast on critical errors to prevent cascading corruption.
    """
    print(f"\n{'='*20}")
    print(f"🚀 RUNNING PHASE: {description}")
    print(f"{'='*20}")
    try:
        # Pass current environment to subprocess to maintain session context
        # Ensure the project root is in PYTHONPATH for cross-module imports
        env = os.environ.copy()
        env["PYTHONPATH"] = os.getcwd() + os.pathsep + env.get("PYTHONPATH", "")
        
        command_args = [sys.executable] + script_path.split()
        result = subprocess.run(command_args, check=True, capture_output=True, text=True, env=env)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        print(e.stderr)
        sys.exit(1)

def main():
    """
    Main execution loop. Routes between LLM (Unstructured) and Tabular (Structured) modes.
    """
    # Set up environment variables for MLflow tracking (The Immutable Ledger)
    os.environ['MLFLOW_TRACKING_URI'] = "sqlite:///mlflow.db"
    
    mode = sys.argv[1] if len(sys.argv) > 1 else "structured"
    
    if mode == "llm":
        # ------------------------------------------------------------------------------------------
        # LLM PIPELINE: Optimized for Large Language Model Fine-Tuning (PEFT/LoRA)
        # ------------------------------------------------------------------------------------------
        print("🌟 STARTING LLM PIPELINE (Qwen/Llama Style) 🌟")
        run_phase("src/data_ops/ingest.py", "Phase 1: LLM Data Sourcing")
        run_phase("src/ml_ops/train.py llm", "Phase 9: LLM Fine-Tuning (PEFT/LoRA)")
        run_phase("src/devsecops/optimize.py ./final_llm_model turboquant", "Phase 21: TurboQuant & Optimization")
        
    else:
        # ------------------------------------------------------------------------------------------
        # STRUCTURED PIPELINE: The Full 25-Phase Intelligence Factory
        # ------------------------------------------------------------------------------------------
        print("📊 STARTING STRUCTURED DATA PIPELINE 📊")
        
        # --- DOMAIN 1: DATA OPS (THE SOURCE) ---
        # Connection: Prepares data for the AutoML tournament and training.
        run_phase("src/data_ops/ingest.py", "Phase 1: Data Sourcing")
        run_phase("src/data_ops/lake_health.py", "Phase 1: Data Lake Health Audit")
        run_phase("src/data_ops/data_summarizer.py", "Phase 1: Dataset Summary Card")
        run_phase("src/data_ops/multi_modal.py", "Phase 1: Multi-Modal Signal Fusion")
        run_phase("src/data_ops/digital_twin.py", "Phase 1: Digital Twin Data Simulation")
        run_phase("src/data_ops/gan_divergence.py", "Phase 1: Synthetic Reality Guardrail")
        run_phase("src/data_ops/data_purge.py", "Phase 3: Right to be Forgotten Purge")
        run_phase("src/data_ops/sovereignty.py", "Phase 3: Data Sovereignty Check")
        run_phase("src/data_ops/validate.py", "Phase 2: Data Validation")
        run_phase("src/data_ops/anomaly_inversion.py", "Phase 2: Data Anomaly Inversion")
        run_phase("src/data_ops/semantic_guard.py", "Phase 2: Semantic Integrity Check")
        run_phase("src/data_ops/schema_evolver.py", "Phase 2: Dynamic Schema Evolution")
        run_phase("src/data_ops/self_healing.py", "Phase 2: Self-Healing Data Repair")
        run_phase("src/data_ops/multi_tenant.py", "Phase 3: Multi-Tenant Data Isolation")
        run_phase("src/data_ops/zk_data_proof.py", "Phase 3: ZK Data Integrity Proof")
        run_phase("src/data_ops/mask_pii.py", "Phase 3: DataSecOps (PII Masking)")
        run_phase("src/data_ops/privacy.py", "Phase 3: Differential Privacy")
        run_phase("src/data_ops/process.py", "Phase 4 & 5: Processing & Feature Store")
        run_phase("src/data_ops/genetic_features.py", "Phase 4: Genetic Feature Evolution")
        run_phase("src/ml_ops/rfe_optimizer.py", "Phase 4: Recursive Feature Elimination")
        run_phase("src/ml_ops/ant_colony.py", "Phase 4: Bio-Inspired Feature Selection")
        
        # --- DOMAIN 2: ML OPS (THE SOUL) ---
        # Connection: Uses features from DataOps to generate high-performance models.
        run_phase("src/ml_ops/automl.py", "Phase 10: Auto-ML Model Tournament")
        run_phase("src/ml_ops/llm_tuner.py", "Phase 10: LLM-Guided Parameter Tuning")
        run_phase("src/ml_ops/nas.py", "Phase 10: Neural Architecture Search")
        run_phase("src/ml_ops/quantum_ml.py", "Phase 10: Quantum-ML Weighting")
        run_phase("src/ml_ops/debate.py", "Phase 9: Model Debate Protocol")
        run_phase("src/ml_ops/ensemble.py", "Phase 9: Multi-Model Ensemble Voting")
        run_phase("src/ml_ops/expert_router.py", "Phase 9: Neural Expert Routing")
        run_phase("src/ml_ops/curriculum.py", "Phase 9: Curriculum-Based Training")
        run_phase("src/ml_ops/train.py", "Phase 9: Training Champion Architecture")
        run_phase("src/ml_ops/transfer_logic.py", "Phase 9: Cross-Domain Knowledge Transfer")
        run_phase("src/ml_ops/swa_merger.py", "Phase 9: Stochastic Weight Averaging")
        run_phase("src/ml_ops/fisher_merging.py", "Phase 9: Fisher-Information Merging")
        run_phase("src/ml_ops/federated.py", "Phase 9: Federated Weight Aggregation")
        run_phase("src/ml_ops/distill.py", "Phase 21: Teacher-Student Knowledge Distillation")
        run_phase("src/ml_ops/one_shot_distill.py", "Phase 21: One-Shot Model Compression")
        run_phase("src/ml_ops/multi_teacher.py", "Phase 21: Multi-Teacher Committee Distillation")
        
        # --- DOMAIN 3: MODEL SEC OPS (THE JUDGE) ---
        # Connection: Audits MLOps outputs before final deployment.
        run_phase("src/model_sec/evaluate.py", "Phase 12-16: Evaluation & Governance")
        run_phase("src/ml_ops/uncertainty.py", "Phase 12: Uncertainty Calibration")
        run_phase("src/model_sec/compliance_filing.py", "Phase 16: Automated Regulatory Filing")
        run_phase("src/devsecops/social_trust.py", "Phase 16: Zero-Knowledge Social Proof")
        run_phase("src/ml_ops/ledger.py", "Phase 16: Immutable Governance Ledger")
        run_phase("src/model_sec/bias_audit.py", "Phase 13: Ethical Bias Audit")
        run_phase("src/model_sec/live_bias_fix.py", "Phase 13: Inference-Time Bias Mitigation")
        run_phase("src/model_sec/regret_minimizer.py", "Phase 13: Ethical Regret Minimization")
        run_phase("src/model_sec/enclave.py", "Phase 3: Confidential Computing Enclave")
        run_phase("src/model_sec/adversarial.py", "Phase 14: Adversarial Robustness Testing")
        run_phase("src/sre/chaos_monkey_v2.py", "Phase 14: Extreme Chaos Monkey V2")
        
        # --- DOMAIN 4: DEV SEC OPS (THE PURITY) ---
        # Connection: Ensures the codebase and supply chain are untainted.
        run_phase("src/devsecops/self_healing_code.py", "Phase 18: Self-Healing Code Patching")
        run_phase("src/devsecops/style_repair.py", "Phase 18: Infinite Style Auto-Repair")
        run_phase("src/devsecops/red_team.py", "Phase 20: Automated Red-Team Attack")
        run_phase("src/devsecops/pqc_sim.py", "Phase 20: Post-Quantum Cryptography")
        run_phase("src/devsecops/dependency_patcher.py", "Phase 18: Supply-Chain Hardening")
        run_phase("src/devsecops/pruning.py", "Phase 21: Extreme Model Pruning")
        
        # --- DOMAIN 5: SRE (THE GUARDIAN) ---
        # Connection: Final interface between model and world.
        run_phase("src/sre/mab_gateway.py", "Phase 23: MAB Dynamic Traffic Routing")
        run_phase("src/sre/proactive_drift.py", "Phase 25: Proactive Drift Forecasting")
        run_phase("src/sre/concept_drift.py", "Phase 25: Concept Drift Detection")
        run_phase("src/sre/incident_response.py", "Phase 25: Autonomous Incident Response")
        run_phase("src/sre/planetary_latency.py", "Phase 25: Inter-Planet Latency Sync")
        run_phase("src/sre/llm_explainer.py", "Phase 24: LLM Prediction Narrative")
        run_phase("src/ml_ops/pipeline_optimizer.py", "Phase 25: Genetic Pipeline Architect")
        run_phase("src/sre/power_optimizer.py", "Phase 24: Green-AI Power Optimization")
        run_phase("src/model_sec/omni_governance.py", "Phase 25: Absolute Omni-Governance")
        run_phase("src/sre/live_docs.py", "Meta-Phase: Autonomous Self-Documentation")
        run_phase("src/sre/cascading.py", "Phase 24: Model Cascading Router")
        run_phase("src/sre/diagram_generator.py", "Phase 25: Visual Architecture Mapping")
        run_phase("src/sre/meta_critic.py", "Phase 25: Meta-Critic Execution Audit")
        run_phase("src/sre/sunset_manager.py", "Phase 25: Model Lifecycle Sunsetting")

    print("\n" + "🏆"*40)
    print("THE FACTORY HAS ACHIEVED SINGULARITY. OPERATION COMPLETE.")
    print("🏆"*40)
    print("To start the production server, run: uvicorn src.sre.serve:app --reload")

if __name__ == "__main__":
    main()
