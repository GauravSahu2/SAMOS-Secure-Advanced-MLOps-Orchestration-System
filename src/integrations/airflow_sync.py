"""
====================================================================================================
SAMOS INTEGRATIONS: airflow_sync.py
Integration: Apache Airflow → SAMOS Orchestrator
Phase: Cross-cutting (Pipeline Scheduling)

FIX APPLIED (Gap #8):
    Previously a dead stub that generated a simplistic DAG template.
    Now delegates to the real production DAG at configs/airflow_dags/samos_pipeline_dag.py
    and provides a CLI to trigger/list DAG runs via the Airflow REST API.
====================================================================================================
"""

import logging
import os
import shutil

logger = logging.getLogger("samos.airflow_sync")

REAL_DAG_PATH = os.path.join("configs", "airflow_dags", "samos_pipeline_dag.py")
AIRFLOW_API_BASE = os.environ.get("AIRFLOW_API_BASE", "http://localhost:8080/api/v1")
AIRFLOW_DAG_ID = "samos_25_phase_pipeline"


def deploy_dag(target_dir: str = "") -> str:
    """
    Copies the real SAMOS DAG to the Airflow dags_folder.

    Args:
        target_dir: Path to Airflow's dags_folder. Defaults to $AIRFLOW_HOME/dags
                    or ~/airflow/dags if AIRFLOW_HOME is not set.

    Returns:
        The path where the DAG was deployed.
    """
    if not target_dir:
        airflow_home = os.environ.get("AIRFLOW_HOME", os.path.expanduser("~/airflow"))
        target_dir = os.path.join(airflow_home, "dags")

    os.makedirs(target_dir, exist_ok=True)
    dest = os.path.join(target_dir, "samos_pipeline_dag.py")

    if not os.path.exists(REAL_DAG_PATH):
        logger.error("Real DAG not found at %s — run from project root.", REAL_DAG_PATH)
        return ""

    shutil.copy2(REAL_DAG_PATH, dest)
    logger.info("✅ SAMOS DAG deployed to %s", dest)
    return dest


def trigger_dag() -> dict:
    """
    Triggers the SAMOS pipeline DAG via the Airflow REST API.

    Requires:
        - Airflow webserver running on AIRFLOW_API_BASE
        - DAG already deployed via deploy_dag()
    """
    try:
        import requests
    except ImportError:
        logger.error("requests package not installed — cannot trigger DAG via API.")
        return {"error": "requests not installed"}

    url = f"{AIRFLOW_API_BASE}/dags/{AIRFLOW_DAG_ID}/dagRuns"
    headers = {"Content-Type": "application/json"}

    # Basic auth from env
    username = os.environ.get("AIRFLOW_USERNAME", "admin")
    auth_pass = os.environ.get("AIRFLOW_PASSWORD", "admin")  # nosec B105

    try:
        resp = requests.post(
            url,
            headers=headers,
            auth=(username, auth_pass),
            json={"conf": {}},
            timeout=10,
        )
        resp.raise_for_status()
        result = resp.json()
        logger.info("✅ DAG triggered — run_id: %s", result.get("dag_run_id"))
        return result
    except Exception as exc:
        logger.warning("DAG trigger failed: %s", exc)
        return {"error": str(exc)}


def list_dag_runs(limit: int = 5) -> list:
    """Lists recent DAG runs via the Airflow REST API."""
    try:
        import requests
    except ImportError:
        logger.error("requests package not installed.")
        return []

    url = f"{AIRFLOW_API_BASE}/dags/{AIRFLOW_DAG_ID}/dagRuns"
    username = os.environ.get("AIRFLOW_USERNAME", "admin")
    auth_pass = os.environ.get("AIRFLOW_PASSWORD", "admin")  # nosec B105

    try:
        resp = requests.get(
            url,
            auth=(username, auth_pass),
            params={"limit": limit, "order_by": "-start_date"},
            timeout=10,
        )
        resp.raise_for_status()
        runs = resp.json().get("dag_runs", [])
        for run in runs:
            logger.info(
                "  📋 Run %s — state: %s — start: %s",
                run.get("dag_run_id"), run.get("state"), run.get("start_date"),
            )
        return runs
    except Exception as exc:
        logger.warning("Failed to list DAG runs: %s", exc)
        return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "trigger":
        trigger_dag()
    elif len(sys.argv) > 1 and sys.argv[1] == "deploy":
        deploy_dag()
    elif len(sys.argv) > 1 and sys.argv[1] == "runs":
        list_dag_runs()
    else:
        print("Usage: python -m src.integrations.airflow_sync [deploy|trigger|runs]")
