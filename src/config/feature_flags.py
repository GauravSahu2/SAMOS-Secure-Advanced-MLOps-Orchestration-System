"""
src/config/feature_flags.py

Enterprise feature flag management.
Allows safe, dynamic rollout of experimental features without code redeployment.
Falls back to environment variables if Redis is unavailable.
"""
import os
import logging
import redis

logger = logging.getLogger(__name__)

class FeatureFlags:
    def __init__(self):
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        try:
            self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
            # Test connection
            self.redis.ping()
            self._use_redis = True
        except redis.ConnectionError:
            logger.warning("Feature Flags: Redis unavailable. Falling back to environment variables.")
            self._use_redis = False

    def is_enabled(self, flag_name: str, default: bool = False) -> bool:
        """
        Check if a feature flag is enabled.
        Priority: Redis > Environment Variable > Default
        """
        if self._use_redis:
            try:
                val = self.redis.get(f"flag:{flag_name}")
                if val is not None:
                    return val.lower() in ("true", "1", "yes")
            except redis.RedisError:
                pass # Fallback to env var if Redis fails mid-flight
        
        env_val = os.environ.get(f"FLAG_{flag_name.upper()}")
        if env_val is not None:
            return env_val.lower() in ("true", "1", "yes")
            
        return default

flags = FeatureFlags()
