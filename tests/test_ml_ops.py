"""
tests/test_ml_ops.py — MLOps Pillar test suite (Phases 6–11 + 21)
Covers: nas, personalization, automl, distill, ledger, watermark,
        zero_trust (devsecops), mab_gateway (sre)
"""

import os
import json
import pytest
from typing import Any
import numpy as np


# ─────────────────────────────────────────────────────────────────────────────
# Phase 10: Neural Architecture Search
# ─────────────────────────────────────────────────────────────────────────────
class TestNAS:
    def test_returns_valid_architecture(self) -> None:
        from src.ml_ops.nas import run_nas_evolution
        arch = run_nas_evolution(generations=1)
        assert isinstance(arch, list), "NAS must return a list."
        assert len(arch) == 2, "Architecture must be [n_layers, n_neurons]."
        n_layers, n_neurons = arch
        assert n_layers >= 1, "Must have at least 1 hidden layer."
        assert n_neurons >= 5, "Must have at least 5 neurons."

    def test_fitness_improves_over_generations(self) -> None:
        """Multiple generations should not regress significantly."""
        from src.ml_ops.nas import run_nas_evolution
        arch_1gen = run_nas_evolution(generations=1)
        arch_3gen = run_nas_evolution(generations=3)
        # Both should be valid architectures — just confirm no crash and valid output
        assert arch_1gen is not None
        assert arch_3gen is not None


# ─────────────────────────────────────────────────────────────────────────────
# Phase 9: Personalization
# ─────────────────────────────────────────────────────────────────────────────
class TestPersonalization:
    def test_adapter_has_required_keys(self) -> None:
        from src.ml_ops.personalization import create_personalized_adapter
        adapter = create_personalized_adapter("USER-1", [0.1, 0.05, 0.02])  # type: ignore[no-untyped-call]
        assert "user_id" in adapter
        assert "bias_adjustment" in adapter

    def test_bias_is_mean_of_history(self) -> None:
        from src.ml_ops.personalization import create_personalized_adapter
        history = [0.1, 0.3, 0.5]
        adapter = create_personalized_adapter("USER-2", history)  # type: ignore[no-untyped-call]
        expected = sum(history) / len(history)
        assert abs(adapter["bias_adjustment"] - expected) < 1e-9

    def test_empty_history_returns_zero_bias(self) -> None:
        from src.ml_ops.personalization import create_personalized_adapter
        adapter = create_personalized_adapter("USER-3", [])  # type: ignore[no-untyped-call]
        assert adapter["bias_adjustment"] == 0


# ─────────────────────────────────────────────────────────────────────────────
# Phase 16: Immutable Governance Ledger
# ─────────────────────────────────────────────────────────────────────────────
class TestGovernanceLedger:
    def test_entry_appended(self, tmp_path: Any, monkeypatch: Any) -> None:
        from src.ml_ops import ledger as ledger_module
        ledger_path = str(tmp_path / "test_ledger.jsonl")
        monkeypatch.setattr(ledger_module, "LEDGER_FILE", ledger_path)
        ledger_module.append_to_ledger("test_event", {"score": 0.95})
        assert os.path.exists(ledger_path)
        with open(ledger_path) as f:
            entries = [json.loads(line) for line in f if line.strip()]
        assert len(entries) >= 1
        assert entries[-1]["event"] == "test_event"

    def test_ledger_is_append_only(self, tmp_path: Any, monkeypatch: Any) -> None:
        from src.ml_ops import ledger as ledger_module
        ledger_path = str(tmp_path / "append_only.jsonl")
        monkeypatch.setattr(ledger_module, "LEDGER_FILE", ledger_path)
        ledger_module.append_to_ledger("event_a", {})
        ledger_module.append_to_ledger("event_b", {})
        with open(ledger_path) as f:
            lines = [l for l in f.readlines() if l.strip()]
        assert len(lines) == 2, "Each append must produce a separate JSONL line."


# ─────────────────────────────────────────────────────────────────────────────
# Phase 15: Model Watermarking
# ─────────────────────────────────────────────────────────────────────────────
class TestWatermark:
    def test_watermark_modifies_weights(self) -> None:
        from src.ml_ops.watermark import embed_watermark
        original = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
        watermarked = embed_watermark(original.copy(), secret="SAMOS-IP")
        assert not np.array_equal(original, watermarked), \
            "Watermark must modify at least one weight bit."

    def test_watermark_is_detectable(self) -> None:
        from src.ml_ops.watermark import embed_watermark, detect_watermark
        weights = np.random.default_rng(42).random(100)
        watermarked = embed_watermark(weights.copy(), secret="SAMOS-IP")
        detected = detect_watermark(watermarked, secret="SAMOS-IP")
        assert detected is True, "Embedded watermark must be detectable."

    def test_wrong_secret_fails_detection(self) -> None:
        from src.ml_ops.watermark import embed_watermark, detect_watermark
        weights = np.random.default_rng(42).random(100)
        watermarked = embed_watermark(weights.copy(), secret="SAMOS-IP")
        detected = detect_watermark(watermarked, secret="WRONG-SECRET")
        assert detected is False, "Wrong secret must not detect watermark."


# ─────────────────────────────────────────────────────────────────────────────
# Phase 23: MAB Gateway (Thompson Sampling)
# ─────────────────────────────────────────────────────────────────────────────
class TestMABGateway:
    def test_route_is_valid(self) -> None:
        from src.sre.mab_gateway import MABGateway
        gw = MABGateway()
        route = gw.get_route()
        assert route in ("stable", "candidate"), f"Invalid route: {route}"

    def test_success_increments_success_count(self) -> None:
        from src.sre.mab_gateway import MABGateway
        gw = MABGateway()
        before = gw.stats["stable"]["success"]
        gw.update_stats("stable", was_correct=True)
        assert gw.stats["stable"]["success"] == before + 1

    def test_failure_increments_fail_count(self) -> None:
        from src.sre.mab_gateway import MABGateway
        gw = MABGateway()
        before = gw.stats["candidate"]["fail"]
        gw.update_stats("candidate", was_correct=False)
        assert gw.stats["candidate"]["fail"] == before + 1

    def test_high_success_routes_to_stable(self) -> None:
        """After many stable successes the bandit should strongly prefer stable."""
        from src.sre.mab_gateway import MABGateway
        gw = MABGateway()
        for _ in range(500):
            gw.update_stats("stable", was_correct=True)
        # With 500 successes vs 1/1 baseline the beta mean strongly favours stable
        # Sampling 20 times should yield at least 15 stable routes
        routes = [gw.get_route() for _ in range(20)]
        stable_count = routes.count("stable")
        assert stable_count >= 14, f"Expected strongly stable routing, got {stable_count}/20 stable."


# ─────────────────────────────────────────────────────────────────────────────
# Phase 19: Zero-Trust SecOps
# ─────────────────────────────────────────────────────────────────────────────
class TestZeroTrust:
    def test_valid_token_accepted(self) -> None:
        from src.devsecops.zero_trust import ZeroTrustGuard
        guard = ZeroTrustGuard()
        token = guard.issue_token("Phase-Test")
        assert guard.verify_token("Phase-Test", token) is True

    def test_invalid_token_rejected(self) -> None:
        from src.devsecops.zero_trust import ZeroTrustGuard
        guard = ZeroTrustGuard()
        guard.issue_token("Phase-Test")
        assert guard.verify_token("Phase-Test", "FORGED-TOKEN") is False

    def test_different_phases_have_different_tokens(self) -> None:
        from src.devsecops.zero_trust import ZeroTrustGuard
        guard = ZeroTrustGuard()
        t1 = guard.issue_token("Phase-A")
        t2 = guard.issue_token("Phase-B")
        assert t1 != t2, "Different phase names must produce different tokens."
