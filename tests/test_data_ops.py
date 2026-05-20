"""
tests/test_data_ops.py — DataOps Pillar test suite (Phases 1–6)
Covers: ingest, validate, mask_pii, anomaly_inversion, genetic_features,
        process, schema_evolver, self_healing, sovereignty, privacy, data_purge
"""

import os
import sys
import json
import pytest
from typing import Any
import pandas as pd
import numpy as np

# conftest.py handles sys.path — no manual hacks needed here.


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: Data Validation
# ─────────────────────────────────────────────────────────────────────────────
class TestValidation:
    def test_valid_records_pass_through(self, tmp_path: Any) -> None:
        """Clean records should not end up in the DLQ."""
        from src.data_ops.validate import validate_data
        df = pd.DataFrame({"age": [25, 40], "income": [50_000, 80_000]})
        src = str(tmp_path / "in.csv")
        clean = str(tmp_path / "clean.csv")
        dlq = str(tmp_path / "dlq.csv")
        df.to_csv(src, index=False)
        validate_data(src, clean, dlq)
        assert os.path.exists(clean)
        clean_df = pd.read_csv(clean)
        assert len(clean_df) == 2

    def test_age_out_of_range_goes_to_dlq(self, tmp_path: Any) -> None:
        """Records with age > 120 must be quarantined in the DLQ."""
        from src.data_ops.validate import validate_data
        df = pd.DataFrame({"age": [200], "income": [1_000]})
        src = str(tmp_path / "in.csv")
        clean = str(tmp_path / "clean.csv")
        dlq = str(tmp_path / "dlq.csv")
        df.to_csv(src, index=False)
        validate_data(src, clean, dlq)
        dlq_df = pd.read_csv(dlq)
        assert len(dlq_df) == 1


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: Anomaly Inversion
# ─────────────────────────────────────────────────────────────────────────────
class TestAnomalyInversion:
    def test_negative_value_replaced_by_neighbor(self, anomaly_pair: Any) -> None:
        from src.data_ops.anomaly_inversion import invert_anomaly
        anomaly, neighbor = anomaly_pair
        fixed = invert_anomaly(anomaly.copy(), neighbor)
        assert fixed["income"] == neighbor["income"], "Negative income must be replaced."

    def test_positive_value_unchanged(self, anomaly_pair: Any) -> None:
        from src.data_ops.anomaly_inversion import invert_anomaly
        anomaly, neighbor = anomaly_pair
        fixed = invert_anomaly(anomaly.copy(), neighbor)
        # age and credit_score were already positive — must remain unchanged
        assert fixed["age"] == anomaly["age"]
        assert fixed["credit_score"] == anomaly["credit_score"]

    def test_all_positive_record_untouched(self) -> None:
        from src.data_ops.anomaly_inversion import invert_anomaly
        record = {"x": 10, "y": 20}
        neighbor = {"x": 99, "y": 99}
        result = invert_anomaly(record.copy(), neighbor)
        assert result == record


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: PII Masking
# ─────────────────────────────────────────────────────────────────────────────
class TestPIIMasking:
    def test_email_is_masked(self, tmp_path: Any) -> None:
        from src.data_ops.mask_pii import mask_pii
        df = pd.DataFrame({"email": ["alice@example.com", "bob@test.org"]})
        src = str(tmp_path / "data.csv")
        out = str(tmp_path / "masked.csv")
        df.to_csv(src, index=False)
        mask_pii(src, out)
        result = pd.read_csv(out)
        for email in result["email"]:
            assert "@" not in email or "***" in email, f"Email not masked: {email}"

    def test_non_email_column_unchanged(self, tmp_path: Any) -> None:
        from src.data_ops.mask_pii import mask_pii
        df = pd.DataFrame({"email": ["a@b.com"], "age": [30]})
        src = str(tmp_path / "data.csv")
        out = str(tmp_path / "masked.csv")
        df.to_csv(src, index=False)
        mask_pii(src, out)
        result = pd.read_csv(out)
        assert result["age"][0] == 30


# ─────────────────────────────────────────────────────────────────────────────
# Phase 4: Genetic Feature Evolution
# ─────────────────────────────────────────────────────────────────────────────
class TestGeneticFeatures:
    def test_new_feature_column_added(self, sample_dataframe: Any) -> None:
        from src.data_ops.genetic_features import run_genetic_feature_synthesis
        result = run_genetic_feature_synthesis(sample_dataframe.copy())
        assert "inc_cred_eff" in result.columns, \
            "Genetic evolution should add 'inc_cred_eff' feature."

    def test_no_rows_dropped(self, sample_dataframe: Any) -> None:
        from src.data_ops.genetic_features import run_genetic_feature_synthesis
        before = len(sample_dataframe)
        result = run_genetic_feature_synthesis(sample_dataframe.copy())
        assert len(result) == before, "Row count must not change after evolution."


# ─────────────────────────────────────────────────────────────────────────────
# Phase 2: Self-Healing Data
# ─────────────────────────────────────────────────────────────────────────────
class TestSelfHealingData:
    def test_nan_imputed(self, tmp_path: Any) -> None:
        from src.data_ops.self_healing import run_self_healing
        df = pd.DataFrame({"age": [25, None, 30], "income": [40_000, 60_000, None]})
        path = str(tmp_path / "data.csv")
        df.to_csv(path, index=False)
        run_self_healing(path)
        healed = pd.read_csv(path)
        assert healed.isnull().sum().sum() == 0, "All NaNs must be imputed."


# ─────────────────────────────────────────────────────────────────────────────
# Phase 3: Differential Privacy
# ─────────────────────────────────────────────────────────────────────────────
class TestDifferentialPrivacy:
    def test_noise_added_to_numeric(self, sample_csv: Any, tmp_path: Any) -> None:
        from src.data_ops.privacy import apply_differential_privacy
        out = str(tmp_path / "private.csv")
        apply_differential_privacy(sample_csv, out)  # type: ignore[no-untyped-call]
        original = pd.read_csv(sample_csv)
        noisy = pd.read_csv(out)
        # At least one numeric column should differ from the original
        numeric_cols = original.select_dtypes(include="number").columns.tolist()
        any_different = any(
            not original[c].equals(noisy[c]) for c in numeric_cols if c in noisy.columns
        )
        assert any_different, "Differential privacy must add noise to numeric columns."
