import hashlib
import os

class ZeroTrustGuard:
    """Phase 18: Zero-Trust SecOps - Inter-Phase Handshake."""
    def __init__(self) -> None:
        # SECRET: Must be set via environment variable or injected by HashiCorp Vault.
        # Never hardcode secrets in source code.
        self.secret: str = os.environ.get("SAMOS_ZT_SECRET", "CHANGE-ME-IN-PRODUCTION")  # nosec # noqa
        self.tokens: dict[str, str] = {}

    def issue_token(self, phase_name: str) -> str:
        """Generates a token for a completed phase."""
        print(f"🛡️ Zero-Trust: Issuing token for {phase_name}...")
        token = hashlib.sha256(f"{phase_name}{self.secret}".encode()).hexdigest()
        self.tokens[phase_name] = token
        return token

    def verify_token(self, phase_name: str, token: str) -> bool:
        """Verifies if the predecessor token is valid."""
        expected = hashlib.sha256(f"{phase_name}{self.secret}".encode()).hexdigest()
        if token == expected:
            print(f"✅ Zero-Trust: Handshake Verified for {phase_name}.")
            return True
        else:
            print(f"❌ SECURITY BREACH: Invalid Token for {phase_name}! Blocking Execution.")
            return False

if __name__ == "__main__":
    guard = ZeroTrustGuard()
    token = guard.issue_token("Phase-2-Validation")
    guard.verify_token("Phase-2-Validation", token)
    guard.verify_token("Phase-2-Validation", "MALICIOUS-TOKEN")
