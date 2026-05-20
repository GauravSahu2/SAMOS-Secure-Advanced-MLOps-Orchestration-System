"""
====================================================================================================
SAMOS DEVSECOPS: vault_manager.py
Integration: HashiCorp Vault
Phase: 18 (Zero-Trust Secret Management)

FIX APPLIED (Gap #14):
    Previously a dead stub. Now provides real HVAC integration:
      - fetch_secret(path, key) — reads from Vault's KV v2 engine
      - sync_secrets() — bulk-syncs configured paths into the process environment
      - Graceful fallback to os.environ if Vault is unreachable
====================================================================================================
"""

import logging
import os

logger = logging.getLogger("samos.vault_manager")

# ── Optional HVAC import ───────────────────────────────────────────────────────
try:
    import hvac  # type: ignore[import-not-found]
    HVAC_AVAILABLE = True
except ImportError:
    HVAC_AVAILABLE = False

# ── Vault configuration ───────────────────────────────────────────────────────
VAULT_ADDR = os.environ.get("VAULT_ADDR", "http://127.0.0.1:8200")
VAULT_TOKEN = os.environ.get("VAULT_TOKEN", "")
VAULT_MOUNT = os.environ.get("VAULT_MOUNT_POINT", "secret")

# Paths to sync from Vault → environment
SYNC_PATHS = [
    ("samos/database", ["DB_HOST", "DB_PORT", "DB_USER", "DB_PASS"]),
    ("samos/mlflow", ["MLFLOW_TRACKING_URI", "MLFLOW_S3_ENDPOINT_URL"]),
    ("samos/airflow", ["AIRFLOW_SECRET_KEY", "AIRFLOW__CORE__FERNET_KEY"]),
    ("samos/huggingface", ["HF_TOKEN"]),
]


def _get_client() -> "hvac.Client | None":
    """Creates and authenticates an HVAC client."""
    if not HVAC_AVAILABLE:
        logger.warning("hvac package not installed — Vault integration disabled.")
        return None

    if not VAULT_TOKEN:
        logger.warning("VAULT_TOKEN not set — Vault integration disabled.")
        return None

    try:
        client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
        if client.is_authenticated():
            logger.info("🔐 Connected to Vault at %s", VAULT_ADDR)
            return client
        logger.warning("Vault authentication failed — token may be expired.")
        return None
    except Exception as exc:
        logger.warning("Vault connection failed: %s", exc)
        return None


def fetch_secret(path: str, key: str, default: str = "") -> str:
    """
    Fetches a single secret from Vault's KV v2 engine.

    Args:
        path: Secret path (e.g., "samos/database")
        key:  Key within the secret (e.g., "DB_PASS")
        default: Fallback value if Vault is unreachable

    Returns:
        The secret value, or `default` if Vault is unavailable.
    """
    client = _get_client()
    if client is None:
        env_value = os.environ.get(key, default)
        if env_value != default:
            logger.debug("Vault unavailable — using env var %s", key)
        return env_value

    try:
        response = client.secrets.kv.v2.read_secret_version(
            path=path, mount_point=VAULT_MOUNT
        )
        data = response.get("data", {}).get("data", {})
        value = data.get(key, default)
        logger.debug("🔑 Fetched %s/%s from Vault", path, key)
        return str(value)
    except Exception as exc:
        logger.warning("Vault read failed for %s/%s: %s — falling back to env", path, key, exc)
        return os.environ.get(key, default)


def sync_secrets():
    """
    Bulk-syncs secrets from Vault into the current process environment.
    Skips keys that already have a non-empty env var to avoid overwriting
    explicit operator configuration.
    """
    logger.info("🔐 Phase 18: Synchronizing secrets from Vault...")

    client = _get_client()
    if client is None:
        logger.info("  ⚠️ Vault unavailable — all secrets sourced from environment variables.")
        return

    synced = 0
    for path, keys in SYNC_PATHS:
        try:
            response = client.secrets.kv.v2.read_secret_version(
                path=path, mount_point=VAULT_MOUNT
            )
            data = response.get("data", {}).get("data", {})
            for key in keys:
                if key in data and not os.environ.get(key):
                    os.environ[key] = str(data[key])
                    synced += 1
                    logger.debug("  ✅ Synced %s/%s → $%s", path, key, key)
        except Exception as exc:
            logger.warning("  ⚠️ Vault read failed for path '%s': %s", path, exc)

    logger.info("  ✅ Vault sync complete — %d secrets injected into environment.", synced)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    sync_secrets()
