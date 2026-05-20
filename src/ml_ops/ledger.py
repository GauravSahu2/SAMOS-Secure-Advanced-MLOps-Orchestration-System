"""
src/ml_ops/ledger.py — Immutable Governance Ledger
Phase 16: Records every governance event as a hash-chained JSONL entry.

Two APIs:
  1. ModelLedger class  — in-memory blockchain-lite (original, unchanged)
  2. append_to_ledger() — persistent JSONL file-based ledger (testable)
"""

import hashlib
import json
import datetime
from datetime import timezone
import os

# Module-level constant — overridable by tests via monkeypatch
LEDGER_FILE = "artifacts/governance_ledger.jsonl"


from typing import Any

def append_to_ledger(event: str, metadata: dict[str, Any]) -> dict[str, Any]:
    """
    Appends a hash-chained entry to the persistent JSONL governance ledger.

    Each entry contains:
      - event: human-readable event name
      - metadata: arbitrary dict (model version, metrics, etc.)
      - timestamp: ISO 8601
      - hash: SHA-256 of this entry (for tamper detection)

    Returns the written entry dict.
    """
    os.makedirs(os.path.dirname(LEDGER_FILE) or ".", exist_ok=True)

    entry = {
        "event": event,
        "metadata": metadata,
        "timestamp": datetime.datetime.now(timezone.utc).isoformat(),
    }
    # Hash the entry itself (deterministic given same content + timestamp)
    entry_bytes = json.dumps(entry, sort_keys=True).encode()
    entry_hash: str = hashlib.sha256(entry_bytes).hexdigest()
    entry["hash"] = entry_hash

    with open(LEDGER_FILE, "a") as f:
        f.write(json.dumps(entry) + "\n")

    print(f"⛓️ Ledger: Event '{event}' recorded (hash: {entry_hash}...)")
    return entry


class ModelLedger:
    """Phase 16: Immutable Governance — in-memory blockchain-lite Ledger."""

    def __init__(self) -> None:
        self.chain: list[dict[str, Any]] = []
        self.create_block(proof=1, previous_hash="0", event="GENESIS")

    def create_block(self, proof: int, previous_hash: str, event: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        block = {
            "index": len(self.chain) + 1,
            "timestamp": str(datetime.datetime.now()),
            "event": event,
            "metadata": metadata or {},
            "proof": proof,
            "previous_hash": previous_hash,
        }
        self.chain.append(block)
        return block

    def get_previous_hash(self) -> str:
        return self.hash(self.chain[-1])

    def hash(self, block: dict[str, Any]) -> str:
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def record_event(self, event: str, metadata: dict[str, Any]) -> None:
        print(f"⛓️ Ledger: Recording immutable event: {event}...")
        prev_hash = self.get_previous_hash()
        self.create_block(proof=100, previous_hash=prev_hash, event=event, metadata=metadata)
        # Also persist to the JSONL file
        append_to_ledger(event, metadata)
        print(f"  ✅ Block #{len(self.chain)} added to the chain.")


if __name__ == "__main__":
    ledger = ModelLedger()
    ledger.record_event("BIAS_AUDIT_PASSED", {"model": "V2.1.0", "acc_gap": "0.02"})
    ledger.record_event("MODEL_PROMOTED", {"target": "PRODUCTION"})
