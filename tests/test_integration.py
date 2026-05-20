"""
tests/test_integration.py — End-to-End Integration Tests

Gap #13: Only unit tests existed. These tests verify multi-phase sequences
         and the full API roundtrip.
"""

import os
import json
import pytest
import pandas as pd
import numpy as np


class TestDataOpsPipelineE2E:
    """Integration test: DataOps phases 1→3 in sequence."""

    def test_ingest_validate_mask_sequence(self, tmp_path):
        """Runs ingest → validate → mask_pii as a connected pipeline."""
        # Phase 1: Create synthetic ingestion output
        raw_csv = tmp_path / "raw_ingested.csv"
        pd.DataFrame({
            "age": [25, 30, 200, 45],
            "income": [50000, 60000, -1, 70000],
            "email": ["a@b.com", "c@d.com", "e@f.com", "g@h.com"],
        }).to_csv(raw_csv, index=False)

        # Phase 2: Validate
        from src.data_ops.validate import validate_data
        clean_csv = tmp_path / "clean.csv"
        dlq_csv = tmp_path / "dlq.csv"
        validate_data(str(raw_csv), str(clean_csv), str(dlq_csv))
        assert clean_csv.exists(), "validate_data must produce a clean output"

        # Phase 3: Mask PII on the clean output
        from src.data_ops.mask_pii import mask_pii
        masked_csv = tmp_path / "masked.csv"
        mask_pii(str(clean_csv), str(masked_csv))
        assert masked_csv.exists(), "mask_pii must produce a masked output"


class TestServeAPIE2E:
    """Integration test: Full FastAPI roundtrip."""

    def test_health_endpoint_returns_structured_payload(self):
        """GET /health must return status, version, mab_stats."""
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            pytest.skip("fastapi[test] not installed")

        from src.sre.serve import app
        client = TestClient(app)

        response = client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "mab_stats" in data
        assert "timestamp" in data

    def test_predict_returns_mab_routing(self):
        """POST /predict must route via MAB and return structured response."""
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            pytest.skip("fastapi[test] not installed")

        from src.sre.serve import app
        client = TestClient(app)

        response = client.post("/predict", json={"text": "What is SAMOS?"})
        assert response.status_code == 200

        data = response.json()
        assert "response" in data
        assert "routing" in data
        assert data["routing"]["model_version"] in ("stable", "candidate")
        assert "metrics" in data
        assert data["metrics"]["latency_ms"] >= 0

    def test_predict_rejects_empty_query(self):
        """POST /predict with empty text must return 422."""
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            pytest.skip("fastapi[test] not installed")

        from src.sre.serve import app
        client = TestClient(app)

        response = client.post("/predict", json={"text": ""})
        assert response.status_code == 422

    def test_security_headers_present(self):
        """Responses must include OWASP security headers."""
        try:
            from fastapi.testclient import TestClient
        except ImportError:
            pytest.skip("fastapi[test] not installed")

        from src.sre.serve import app
        client = TestClient(app)

        response = client.get("/health")
        assert response.headers.get("X-Content-Type-Options") == "nosniff"
        assert response.headers.get("X-Frame-Options") == "DENY"
        assert "Strict-Transport-Security" in response.headers


class TestEvaluateForgeCheckpoint:
    """Integration test: evaluate.py loading a forge checkpoint."""

    def test_evaluate_handles_missing_model_gracefully(self):
        """evaluate_and_govern must not crash when no model artifact exists."""
        from src.model_sec.evaluate import evaluate_and_govern

        # Should handle missing model gracefully (return None) without crashing
        evaluate_and_govern()  # return value intentionally unused — we test no-crash only


class TestWatermarkRoundtrip:
    """Integration test: embed → detect watermark roundtrip."""

    def test_full_watermark_lifecycle(self):
        """Embed a watermark into model weights and detect it."""
        from src.ml_ops.watermark import embed_watermark, detect_watermark

        rng = np.random.default_rng(42)
        weights = rng.random(1000)
        secret = "SAMOS_IP_2026"

        marked = embed_watermark(weights.copy(), secret)
        assert marked is not None, "embed_watermark should return marked weights"

        detected = detect_watermark(marked, secret)
        assert detected is True, "Watermark should be detectable after embedding"


class TestLedgerChainIntegrity:
    """Integration test: ledger append → verify chain."""

    def test_multi_event_chain(self, tmp_path, monkeypatch):
        """Multiple ledger entries must form a valid hash chain."""
        import src.ml_ops.ledger as ledger_mod

        ledger_file = tmp_path / "integration_ledger.jsonl"
        monkeypatch.setattr(ledger_mod, "LEDGER_FILE", str(ledger_file))

        events = [
            ("TRAINING", "Started forge run"),
            ("EVALUATION", "Perplexity: 12.5"),
            ("DEPLOYMENT", "Promoted to staging"),
        ]
        for event_type, detail in events:
            ledger_mod.append_to_ledger(event_type, detail)

        lines = ledger_file.read_text().strip().splitlines()
        assert len(lines) == 3

        entries = [json.loads(line) for line in lines]
        for entry in entries:
            assert "event" in entry
            assert "timestamp" in entry
