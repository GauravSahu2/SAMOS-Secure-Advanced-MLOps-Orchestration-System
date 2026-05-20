"""
conftest.py — Shared pytest fixtures for the SAMOS test suite.

Fixes:
  - Gap #17: conftest.py was missing entirely.
  - Gap #18: sys.path is patched here centrally so individual test files
             no longer need their own `sys.path.append('src')` hacks.
"""

import os
import sys
import json
import tempfile
import shutil
import pytest
import pandas as pd
import numpy as np
from typing import Any, Generator, Dict, Tuple

# ── Ensure project root + src are on sys.path ─────────────────────────────────
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _PROJECT_ROOT not in sys.path:
    sys.path.insert(0, _PROJECT_ROOT)
if os.path.join(_PROJECT_ROOT, "src") not in sys.path:
    sys.path.insert(0, os.path.join(_PROJECT_ROOT, "src"))


# ── Shared temporary workspace ─────────────────────────────────────────────────
@pytest.fixture(scope="session")  # type: ignore
def tmp_workspace(tmp_path_factory: Any) -> Any:
    """Session-scoped temp directory; mirrors the expected SAMOS folder layout."""
    workspace = tmp_path_factory.mktemp("samos_test_workspace")
    (workspace / "data" / "raw").mkdir(parents=True)
    (workspace / "models").mkdir(parents=True)
    (workspace / "artifacts").mkdir(parents=True)
    yield workspace
    shutil.rmtree(workspace, ignore_errors=True)


# ── Small synthetic tabular dataset ───────────────────────────────────────────
@pytest.fixture  # type: ignore
def sample_dataframe() -> Any:
    """Returns a minimal DataFrame that exercises the DataOps pipeline."""
    rng = np.random.default_rng(42)
    return pd.DataFrame({
        "age":          rng.integers(18, 80, 50).tolist(),
        "income":       rng.integers(20_000, 150_000, 50).tolist(),
        "credit_score": rng.integers(300, 850, 50).tolist(),
        "email":        [f"user{i}@example.com" for i in range(50)],
        "target":       rng.integers(0, 2, 50).tolist(),
    })


@pytest.fixture  # type: ignore
def sample_csv(tmp_path: Any, sample_dataframe: Any) -> Any:
    """Writes sample_dataframe to a temp CSV and returns the path."""
    path = tmp_path / "sample.csv"
    sample_dataframe.to_csv(path, index=False)
    return str(path)


# ── Minimal anomaly record ─────────────────────────────────────────────────────
@pytest.fixture  # type: ignore
def anomaly_pair() -> Any:
    """Returns (anomaly_record, neighbor_mean_record) for inversion tests."""
    return (
        {"income": -500, "age": 35, "credit_score": 700},
        {"income": 55_000, "age": 34, "credit_score": 680},
    )


# ── Small forge-state JSON ─────────────────────────────────────────────────────
@pytest.fixture  # type: ignore
def forge_state_file(tmp_path: Any) -> Any:
    """Writes a minimal forge state JSON and returns the path."""
    state = {
        "last_step": 1000,
        "timestamp": 1_700_000_000.0,
        "tokens_per_step": 512,
        "total_tokens_processed": 512_000,
        "last_ce_loss": 2.34,
        "last_kd_loss": 0.87,
        "distill_alpha": 0.7,
        "distill_temperature": 4.0,
        "progressive_scaling_etas": {},
    }
    p = tmp_path / "samos_forge_state.json"
    p.write_text(json.dumps(state, indent=2))
    return str(p)
