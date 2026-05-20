"""
src/sre/event_bus.py

Phase 26: Enterprise Event-Driven Architecture (EDA) implementation.
Instead of linear sequential execution, SAMOS phases emit events to a Redis-backed 
Pub/Sub event bus. Downstream processes listen and execute asynchronously.

This enables:
1. Parallel Phase Execution
2. Dead-Letter Queues (DLQ)
3. Microservice Decoupling
"""
import os
import json
import logging
import threading

logger = logging.getLogger(__name__)

class EventBus:
    """A lightweight Redis-backed Event Bus for decoupling MLOps phases."""
    def __init__(self):
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        try:
            import redis
            self.redis = redis.Redis.from_url(redis_url, decode_responses=True)
            self.redis.ping()
            self.pubsub = self.redis.pubsub()
            self._use_redis = True
        except Exception:
            logger.warning("EventBus: Redis unavailable. Operating in local-only memory mode.")
            self._use_redis = False
            self.pubsub = None  # type: ignore[assignment]
            
        self._handlers = {}
        self._listener_thread = None

    def publish(self, channel: str, event_data: dict):
        """Emit an event payload to a specific channel."""
        payload = json.dumps(event_data)
        if self._use_redis:
            self.redis.publish(channel, payload)
        logger.info(f"[EVENT BUS] 📤 Published to '{channel}': {payload}")

        # If Redis is unavailable, execute locally (for dev/CI fallback)
        if not self._use_redis and channel in self._handlers:
            self._handlers[channel](event_data)

    def subscribe(self, channel: str, handler_func):
        """Register a callback for an event channel."""
        self._handlers[channel] = handler_func
        
        if self._use_redis:
            self.pubsub.subscribe(**{channel: self._handle_message})
            if not self._listener_thread:
                self._listener_thread = threading.Thread(target=self._listen, daemon=True)
                self._listener_thread.start()
                
        logger.info(f"[EVENT BUS] 📥 Subscribed to '{channel}'")

    def _handle_message(self, message):
        if message['type'] == 'message':
            channel = message['channel']
            data = json.loads(message['data'])
            if channel in self._handlers:
                self._handlers[channel](data)

    def _listen(self):
        """Background thread listening for Redis Pub/Sub messages."""
        for _ in self.pubsub.listen():
            pass # Handling is done via callback dictionary provided to subscribe()

# Global singleton bus
bus = EventBus()

if __name__ == "__main__":
    # Quick demo of the EDA architecture
    import time
    
    def on_data_ingested(payload):
        print(f"✅ DataOps Node Received: {payload}")
        print("➡️ Triggering Data Validation Phase...")
        bus.publish("DATA_VALIDATED", {"status": "clean", "records": payload.get("count")})
        
    def on_data_validated(payload):
        print(f"✅ MLOps Node Received: {payload}")
        print("➡️ Triggering Model Training Phase...")

    # Wire up the asynchronous listeners
    bus.subscribe("DATA_INGESTED", on_data_ingested)
    bus.subscribe("DATA_VALIDATED", on_data_validated)
    
    time.sleep(1)
    
    # Fire the initial event
    print("\n🚀 Firing initial event: DATA_INGESTED")
    bus.publish("DATA_INGESTED", {"source": "s3://raw-zone", "count": 10000})
    
    time.sleep(2)
    print("\nEDA Demo Complete.")
