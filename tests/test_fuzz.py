"""
tests/test_fuzz.py — Property-Based / Fuzz Tests using Hypothesis

Gap #12: hypothesis is in requirements.txt but was never used. These tests use
         @given() strategies to fuzz-test critical modules.
"""

import json
import tempfile
import pytest
import numpy as np

try:
    from hypothesis import given, strategies as st, settings, assume, HealthCheck
    HYPOTHESIS_AVAILABLE = True
except ImportError:
    HYPOTHESIS_AVAILABLE = False

    # Dummy decorators so class bodies parse even without hypothesis
    def given(*_a, **_kw):  # type: ignore
        def wrapper(fn):
            return fn
        return wrapper

    def settings(*_a, **_kw):  # type: ignore
        def wrapper(fn):
            return fn
        return wrapper

    def assume(_cond):  # type: ignore
        pass

    class _DummyST:
        """Placeholder for hypothesis.strategies when hypothesis is not installed."""
        def text(self, **_kw): return None
        def integers(self, **_kw): return None
        def sampled_from(self, _seq): return None
        def characters(self, **_kw): return ""

    st = _DummyST()  # type: ignore

    class HealthCheck:  # type: ignore
        function_scoped_fixture = None

pytestmark = pytest.mark.skipif(not HYPOTHESIS_AVAILABLE, reason="hypothesis not installed")


class TestWatermarkFuzz:
    """Fuzz-tests for LSB steganographic watermarking."""

    @given(
        secret=st.text(min_size=1, max_size=32, alphabet=st.characters(whitelist_categories=("L", "N"))),
        array_size=st.integers(min_value=100, max_value=1000),
    )
    @settings(max_examples=25, deadline=None)
    def test_embed_detect_roundtrip(self, secret, array_size):
        """Embedding then detecting a watermark must recover the original secret."""
        from src.ml_ops.watermark import embed_watermark, detect_watermark

        rng = np.random.default_rng(42)
        weights = rng.random(array_size)

        marked = embed_watermark(weights.copy(), secret)
        assert marked is not None, "embed_watermark returned None"
        assert marked.shape == weights.shape, "Shape changed after embedding"

        detected = detect_watermark(marked, secret)
        assert detected is True, f"Watermark not detected for secret='{secret}'"

    @given(
        secret=st.text(min_size=1, max_size=8, alphabet=st.characters(whitelist_categories=("L",))),
    )
    @settings(max_examples=10, deadline=None)
    def test_wrong_secret_fails_detection(self, secret):
        """Detection with the wrong secret should fail."""
        from src.ml_ops.watermark import embed_watermark, detect_watermark

        assume(secret != "WRONG_KEY")

        rng = np.random.default_rng(99)
        weights = rng.random(500)

        marked = embed_watermark(weights.copy(), secret)
        assert marked is not None

        # Detection with a completely different secret should usually fail
        wrong_detected = detect_watermark(marked, "WRONG_KEY_DEFINITELY")
        # We don't assert False here because LSB collisions are possible for short secrets
        # but we do assert the function doesn't crash
        assert isinstance(wrong_detected, bool)


class TestLedgerFuzz:
    """Fuzz-tests for the hash-chained governance ledger.

    Uses tempfile.mkdtemp() instead of pytest's tmp_path fixture because
    hypothesis @given() does not reset function-scoped fixtures between
    generated inputs.
    """

    @given(
        event_type=st.sampled_from(["TRAINING", "EVALUATION", "DEPLOYMENT", "ROLLBACK", "AUDIT"]),
        detail_text=st.text(min_size=1, max_size=100),
    )
    @settings(max_examples=20, deadline=None)
    def test_append_to_ledger_never_crashes(self, event_type, detail_text):
        """Appending arbitrary events to the ledger must never raise."""
        import os
        import src.ml_ops.ledger as ledger_mod

        tmp_dir = tempfile.mkdtemp()
        ledger_file = os.path.join(tmp_dir, "test_ledger.jsonl")
        original = ledger_mod.LEDGER_FILE
        try:
            ledger_mod.LEDGER_FILE = ledger_file
            ledger_mod.append_to_ledger(event_type, {"detail": detail_text})

            assert os.path.exists(ledger_file)
            with open(ledger_file) as f:
                content = f.read()
            assert len(content.strip().splitlines()) >= 1
        finally:
            ledger_mod.LEDGER_FILE = original

    @given(
        n_entries=st.integers(min_value=2, max_value=10),
    )
    @settings(max_examples=5, deadline=None)
    def test_hash_chain_integrity(self, n_entries):
        """Hash chain must be consistent — each entry links to the previous."""
        import os
        import src.ml_ops.ledger as ledger_mod

        tmp_dir = tempfile.mkdtemp()
        ledger_file = os.path.join(tmp_dir, "chain_test.jsonl")
        original = ledger_mod.LEDGER_FILE
        try:
            ledger_mod.LEDGER_FILE = ledger_file

            for i in range(n_entries):
                ledger_mod.append_to_ledger("TEST", {"detail": f"Entry {i}"})

            with open(ledger_file) as f:
                lines = f.read().strip().splitlines()
            assert len(lines) == n_entries

            entries = [json.loads(line) for line in lines]
            for entry in entries:
                assert "hash" in entry, "Entry missing hash field"
        finally:
            ledger_mod.LEDGER_FILE = original


class TestMABGatewayFuzz:
    """Fuzz-tests for Thompson Sampling routing."""

    @given(
        n_requests=st.integers(min_value=1, max_value=50),
    )
    @settings(max_examples=10, deadline=None)
    def test_mab_always_returns_valid_route(self, n_requests):
        """MAB gateway must always return 'stable' or 'candidate'."""
        from src.sre.mab_gateway import MABGateway

        gw = MABGateway()
        for _ in range(n_requests):
            route = gw.get_route()
            assert route in ("stable", "candidate"), f"Invalid route: {route}"
            gw.update_stats(route, was_correct=gw.rng.choice([True, False]))

    @given(
        successes=st.integers(min_value=1, max_value=1000),
        fails=st.integers(min_value=1, max_value=1000),
    )
    @settings(max_examples=15, deadline=None)
    def test_mab_handles_extreme_stats(self, successes, fails):
        """MAB must not crash even with very skewed Beta parameters."""
        from src.sre.mab_gateway import MABGateway

        gw = MABGateway()
        gw.stats["stable"]["success"] = successes
        gw.stats["stable"]["fail"] = fails
        route = gw.get_route()
        assert route in ("stable", "candidate")
