"""
====================================================================================================
TRAFFIC ARCHITECT: src/sre/mab_gateway.py
Project: The Autonomous Intelligence Factory
Phase: 23 (MAB Dynamic Traffic Routing)

FIX APPLIED (Gap #10):
    MAB state is now persisted to Redis (if available). On startup, existing
    Thompson-Sampling statistics are loaded from Redis so learning survives
    container restarts. Falls back to in-memory state if Redis is unreachable.
====================================================================================================

PURPOSE:
    Dynamically routes user traffic between multiple model versions (e.g., Stable vs.
    Candidate) to maximize performance while minimizing risk. It replaces static A/B testing.

ALGORITHM:
    1. THOMPSON SAMPLING: Maintains a Beta Distribution (Success vs. Failure) for each model.
    2. EXPLORATION: Routes a small percentage of traffic to the 'Candidate' to gather data.
    3. EXPLOITATION: Routes the majority of traffic to the currently 'Winning' model.
    4. REAL-TIME UPDATE: Adjusts the distribution instantly based on user feedback/accuracy.

CONNECTION ORDER:
    - INPUT: Ingests model URIs from 'src/model_sec/evaluate.py'.
    - OUTPUT: Serves as the primary routing logic for 'src/sre/serve.py' (Phase 17).
====================================================================================================
"""

import json
import logging
import os

import numpy as np

logger = logging.getLogger("samos.mab_gateway")

# ── Redis configuration ────────────────────────────────────────────────────────
REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
MAB_REDIS_KEY = "samos:mab:stats"

try:
    import redis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class MABGateway:
    """Phase 23: Dynamic Deployment - Multi-Armed Bandit (Thompson Sampling)."""

    def __init__(self) -> None:
        # Default priors (Beta(1,1) = uniform)
        self.stats = {
            "stable": {"success": 1, "fail": 1},
            "candidate": {"success": 1, "fail": 1},
        }
        self.rng = np.random.default_rng(42)
        self._redis = None

        # Attempt to connect and restore state from Redis
        if REDIS_AVAILABLE:
            try:
                self._redis = redis.Redis.from_url(REDIS_URL, decode_responses=True)
                self._redis.ping()
                self._load_state()
                logger.info("🎰 MAB Gateway: Redis connected (%s)", REDIS_URL)
            except Exception as exc:
                logger.warning("🎰 MAB Gateway: Redis unavailable (%s) — using in-memory state.", exc)
                self._redis = None
        else:
            logger.info("🎰 MAB Gateway: redis package not installed — using in-memory state.")

    def _load_state(self) -> None:
        """Restore MAB stats from Redis if they exist."""
        if self._redis is None:
            return
        try:
            raw = self._redis.get(MAB_REDIS_KEY)
            if raw:
                self.stats = json.loads(raw)
                logger.info("  📥 MAB state restored from Redis: %s", self.stats)
        except Exception as exc:
            logger.debug("MAB state load from Redis failed: %s", exc)

    def _save_state(self) -> None:
        """Persist MAB stats to Redis."""
        if self._redis is None:
            return
        try:
            self._redis.set(MAB_REDIS_KEY, json.dumps(self.stats))
        except Exception as exc:
            logger.debug("MAB state save to Redis failed: %s", exc)

    def get_route(self) -> str:
        """Samples from Beta distribution to decide route."""
        logger.debug("MAB Gateway calculating optimal traffic route...")

        stable_sample = self.rng.beta(
            self.stats["stable"]["success"], self.stats["stable"]["fail"]
        )
        candidate_sample = self.rng.beta(
            self.stats["candidate"]["success"], self.stats["candidate"]["fail"]
        )

        route = "stable" if stable_sample > candidate_sample else "candidate"
        logger.debug(
            "Route: %s (stable=%.3f, candidate=%.3f)",
            route.upper(), stable_sample, candidate_sample,
        )
        return route

    def update_stats(self, route: str, was_correct: bool) -> None:
        """Updates the bandit's knowledge and persists to Redis."""
        if was_correct:
            self.stats[route]["success"] += 1
        else:
            self.stats[route]["fail"] += 1

        logger.debug(
            "MAB stats updated: %s → success=%d, fail=%d",
            route, self.stats[route]["success"], self.stats[route]["fail"],
        )
        self._save_state()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    gateway = MABGateway()
    # Simulate 5 requests
    for _i in range(5):
        r = gateway.get_route()
        gateway.update_stats(r, was_correct=gateway.rng.choice([True, False]))
    print(f"Final stats: {gateway.stats}")
