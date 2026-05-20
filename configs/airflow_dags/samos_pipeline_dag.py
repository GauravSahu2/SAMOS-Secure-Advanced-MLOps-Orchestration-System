"""
configs/airflow_dags/samos_pipeline_dag.py
============================================
Apache Airflow DAG for the full 25-phase SAMOS pipeline.

Architecture:
  - NiFi handles the INGESTION layer (real-time bytes: Kafka/S3/IoT → Bronze Lake).
  - THIS DAG handles the ORCHESTRATION layer (schedules Phases 1-25 as Airflow Tasks).

The DAG wraps each SAMOS phase as a PythonOperator that calls the same
`run_phase()` function used by main.py, giving you:
  - Retry policies per phase
  - Full task history & logs in the Airflow UI
  - Trigger buttons for any individual phase
  - Cross-phase dependency enforcement (XCom + upstream/downstream)
  - Email/Slack alerts on failure (configure via Airflow connections)

Usage:
  docker-compose --profile airflow up airflow
  Then visit: http://localhost:8080 (admin / changeme)
"""

from __future__ import annotations

import os
import sys
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

# ── Ensure SAMOS project root is on path ──────────────────────────────────────
_SAMOS_ROOT = os.environ.get("PYTHONPATH", "/opt/airflow/samos").split(":")[0]
if _SAMOS_ROOT not in sys.path:
    sys.path.insert(0, _SAMOS_ROOT)

from main import run_phase  # noqa: E402


# ── DAG defaults ──────────────────────────────────────────────────────────────
_DEFAULT_ARGS = {
    "owner": "samos",
    "depends_on_past": False,
    "email_on_failure": False,   # Set to True + configure SMTP in Airflow UI
    "email_on_retry": False,
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
}

# ── Phase registry (mirrors samos.py PHASE_SCRIPTS) ──────────────────────────
# Format: (script_path, description, group)
PHASE_REGISTRY: list[tuple[str, str, str]] = [
    # ── DataOps ──────────────────────────────────────────────────────────────
    ("src/data_ops/ingest.py",          "Phase 1: Data Sourcing",             "dataops"),
    ("src/data_ops/lake_health.py",     "Phase 1: Data Lake Health Audit",    "dataops"),
    ("src/data_ops/data_summarizer.py", "Phase 1: Dataset Summary Card",      "dataops"),
    ("src/data_ops/multi_modal.py",     "Phase 1: Multi-Modal Fusion",        "dataops"),
    ("src/data_ops/digital_twin.py",    "Phase 1: Digital Twin Simulation",   "dataops"),
    ("src/data_ops/validate.py",        "Phase 2: Data Validation",           "dataops"),
    ("src/data_ops/anomaly_inversion.py","Phase 2: Anomaly Inversion",        "dataops"),
    ("src/data_ops/schema_evolver.py",  "Phase 2: Schema Evolution",          "dataops"),
    ("src/data_ops/self_healing.py",    "Phase 2: Self-Healing Repair",       "dataops"),
    ("src/data_ops/mask_pii.py",        "Phase 3: PII Masking",               "dataops"),
    ("src/data_ops/privacy.py",         "Phase 3: Differential Privacy",      "dataops"),
    ("src/data_ops/sovereignty.py",     "Phase 3: Data Sovereignty",          "dataops"),
    ("src/data_ops/data_purge.py",      "Phase 3: GDPR Right-to-Forget",      "dataops"),
    ("src/data_ops/multi_tenant.py",    "Phase 3: Multi-Tenant Isolation",    "dataops"),
    ("src/data_ops/zk_data_proof.py",   "Phase 3: ZK Data Proof",             "dataops"),
    ("src/data_ops/process.py",         "Phase 4-5: Feature Store",           "dataops"),
    ("src/data_ops/genetic_features.py","Phase 4: Genetic Feature Evolution", "dataops"),
    ("src/ml_ops/rfe_optimizer.py",     "Phase 4: RFE Feature Selection",     "dataops"),
    ("src/ml_ops/ant_colony.py",        "Phase 4: Bio-Inspired Selection",    "dataops"),
    # ── MLOps ────────────────────────────────────────────────────────────────
    ("src/ml_ops/automl.py",            "Phase 10: Auto-ML Tournament",       "mlops"),
    ("src/ml_ops/nas.py",               "Phase 10: Neural Architecture Search","mlops"),
    ("src/ml_ops/debate.py",            "Phase 9: Model Debate",              "mlops"),
    ("src/ml_ops/ensemble.py",          "Phase 9: Ensemble Voting",           "mlops"),
    ("src/ml_ops/curriculum.py",        "Phase 9: Curriculum Training",       "mlops"),
    ("src/ml_ops/train.py",             "Phase 9: Training Champion",         "mlops"),
    ("src/ml_ops/distill.py",           "Phase 21: KD Distillation",          "mlops"),
    ("src/ml_ops/multi_teacher.py",     "Phase 21: Multi-Teacher Distillation","mlops"),
    # ── ModelSecOps ──────────────────────────────────────────────────────────
    ("src/model_sec/evaluate.py",       "Phase 12: Model Evaluation",         "modelsecops"),
    ("src/model_sec/bias_audit.py",     "Phase 13: Bias Audit",               "modelsecops"),
    ("src/model_sec/adversarial.py",    "Phase 14: Adversarial Robustness",   "modelsecops"),
    ("src/model_sec/compliance_filing.py","Phase 16: Regulatory Filing",      "modelsecops"),
    ("src/model_sec/omni_governance.py","Phase 25: Omni-Governance Gate",     "modelsecops"),
    # ── DevSecOps ────────────────────────────────────────────────────────────
    ("src/devsecops/self_healing_code.py","Phase 18: Self-Healing Code",      "devsecops"),
    ("src/devsecops/dependency_patcher.py","Phase 18: Supply-Chain Hardening","devsecops"),
    ("src/devsecops/red_team.py",       "Phase 20: Red-Team Attack",          "devsecops"),
    ("src/devsecops/zero_trust.py",     "Phase 19: Zero-Trust Sync",          "devsecops"),
    # ── SRE ──────────────────────────────────────────────────────────────────
    ("src/sre/mab_gateway.py",          "Phase 23: MAB Traffic Routing",      "sre"),
    ("src/sre/concept_drift.py",        "Phase 25: Concept Drift Detection",  "sre"),
    ("src/sre/incident_response.py",    "Phase 25: Autonomous Incident Response","sre"),
    ("src/sre/power_optimizer.py",      "Phase 24: Green-AI Optimization",    "sre"),
    ("src/sre/meta_critic.py",          "Phase 25: Meta-Critic Audit",        "sre"),
]

GROUP_ORDER = ["dataops", "mlops", "modelsecops", "devsecops", "sre"]


def _make_task_id(script_path: str) -> str:
    """Converts a script path to a safe Airflow task ID."""
    return script_path.replace("/", "__").replace(".py", "")


# ── DAG definition ─────────────────────────────────────────────────────────────
with DAG(
    dag_id="samos_full_pipeline",
    description="SAMOS 25-Phase AI Factory — Scheduled & Monitored via Airflow",
    schedule="@daily",                        # Change to @weekly or a cron expression
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args=_DEFAULT_ARGS,
    tags=["samos", "mlops", "devsecops"],
    doc_md=__doc__,
) as dag:

    # Build task groups per domain pillar
    group_last_tasks: dict[str, list[PythonOperator]] = {g: [] for g in GROUP_ORDER}
    all_tasks: dict[str, PythonOperator] = {}

    for group_name in GROUP_ORDER:
        group_phases = [(sp, desc) for sp, desc, g in PHASE_REGISTRY if g == group_name]
        with TaskGroup(group_id=group_name) as tg:
            prev_task = None
            for script_path, description in group_phases:
                task_id = _make_task_id(script_path)
                task = PythonOperator(
                    task_id=task_id,
                    python_callable=run_phase,
                    op_args=[script_path, description],
                    retries=_DEFAULT_ARGS["retries"],
                    retry_delay=_DEFAULT_ARGS["retry_delay"],
                )
                if prev_task is not None:
                    prev_task >> task  # Sequential within each group
                prev_task = task
                all_tasks[task_id] = task
            if prev_task:
                group_last_tasks[group_name].append(prev_task)

    # Cross-group dependency chain: dataops → mlops → modelsecops → devsecops → sre
    for i in range(len(GROUP_ORDER) - 1):
        current_group = GROUP_ORDER[i]
        next_group = GROUP_ORDER[i + 1]
        next_phases = [(sp, desc) for sp, desc, g in PHASE_REGISTRY if g == next_group]
        if next_phases:
            first_next_task_id = _make_task_id(next_phases[0][0])
            first_next_task = all_tasks.get(first_next_task_id)
            if first_next_task and group_last_tasks[current_group]:
                group_last_tasks[current_group][-1] >> first_next_task
