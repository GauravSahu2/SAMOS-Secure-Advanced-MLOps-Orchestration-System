"""
====================================================================================================
TRAFFIC ARCHITECT: src/sre/mab_gateway.py
Project: The Autonomous Intelligence Factory
Phase: 23 (MAB Dynamic Traffic Routing)
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

import numpy as np

class MABGateway:
    """Phase 23: Dynamic Deployment - Multi-Armed Bandit (Thompson Sampling)."""
    def __init__(self):
        # Stats for Stable (V1) and Candidate (V2)
        # Success count (1) and Failure count (0)
        self.stats = {
            "stable": {"success": 1, "fail": 1},
            "candidate": {"success": 1, "fail": 1}
        }

    def get_route(self):
        """Samples from Beta distribution to decide route."""
        print("🎰 Phase 23: MAB Gateway calculating optimal traffic route...")
        
        stable_sample = np.random.beta(self.stats["stable"]["success"], self.stats["stable"]["fail"])
        candidate_sample = np.random.beta(self.stats["candidate"]["success"], self.stats["candidate"]["fail"])
        
        route = "stable" if stable_sample > candidate_sample else "candidate"
        print(f"  🚀 Route Selected: {route.upper()} (Stable Score: {stable_sample:.2f}, Candidate Score: {candidate_sample:.2f})")
        return route

    def update_stats(self, route, was_correct):
        """Updates the bandit's knowledge."""
        if was_correct:
            self.stats[route]["success"] += 1
        else:
            self.stats[route]["fail"] += 1
        print(f"  📈 MAB Stats Updated for {route}. Successes: {self.stats[route]['success']}")

if __name__ == "__main__":
    gateway = MABGateway()
    # Simulate 5 requests
    for i in range(5):
        route = gateway.get_route()
        gateway.update_stats(route, was_correct=np.random.choice([True, False]))
