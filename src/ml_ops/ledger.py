import hashlib
import json
import datetime

class ModelLedger:
    """Phase 16: Immutable Governance - Blockchain-lite Ledger."""
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0', event="GENESIS")

    def create_block(self, proof, previous_hash, event, metadata=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': str(datetime.datetime.now()),
            'event': event,
            'metadata': metadata or {},
            'proof': proof,
            'previous_hash': previous_hash
        }
        self.chain.append(block)
        return block

    def get_previous_hash(self):
        return self.hash(self.chain[-1])

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def record_event(self, event, metadata):
        print(f"⛓️ Ledger: Recording immutable event: {event}...")
        prev_hash = self.get_previous_hash()
        self.create_block(proof=100, previous_hash=prev_hash, event=event, metadata=metadata)
        print(f"  ✅ Block #{len(self.chain)} added to the chain.")

if __name__ == "__main__":
    ledger = ModelLedger()
    ledger.record_event("BIAS_AUDIT_PASSED", {"model": "V2.1.0", "acc_gap": "0.02"})
    ledger.record_event("MODEL_PROMOTED", {"target": "PRODUCTION"})
