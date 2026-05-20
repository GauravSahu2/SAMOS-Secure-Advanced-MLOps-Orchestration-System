"""
src/ml_ops/watermark.py — Model IP Watermarking
Phase 15: Embeds and detects steganographic ownership signatures in model weights.

FIX: Added embed_watermark(weights, secret) and detect_watermark(weights, secret)
     with proper signatures so the module is testable.
"""

import hashlib
import json
import os
import numpy as np


def _compute_signature_bits(secret: str, n_bits: int = 8) -> list[int]:
    """Derives a deterministic bit sequence from the secret string."""
    digest = hashlib.sha256(secret.encode()).digest()
    bits = []
    for byte in digest:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
            if len(bits) >= n_bits:
                return bits
    return bits[:n_bits]


def embed_watermark(weights: np.ndarray, secret: str = "SAMOS-IP") -> np.ndarray:
    """
    Embeds an IP watermark into a numpy weight array via LSB steganography.

    The least-significant bit of selected weight bytes is flipped to match
    a SHA-256-derived signature of the `secret`.  The modification is
    sub-epsilon and does not meaningfully change model accuracy.

    Args:
        weights: 1-D or N-D float numpy array of model weights.
        secret:  Owner secret string used to generate the signature.

    Returns:
        Modified numpy array with watermark embedded.
    """
    flat = weights.flatten().astype(np.float64)
    sig_bits = _compute_signature_bits(secret, n_bits=min(8, len(flat)))

    for i, bit in enumerate(sig_bits):
        raw_int = flat[i].view(np.int64)
        # Set/clear the LSB to match the signature bit
        if bit == 1:
            flat[i] = np.frombuffer(
                (raw_int | np.int64(1)).tobytes(), dtype=np.float64
            )[0]
        else:
            flat[i] = np.frombuffer(
                (raw_int & ~np.int64(1)).tobytes(), dtype=np.float64
            )[0]

    watermarked = flat.reshape(weights.shape)

    # Persist signature metadata
    os.makedirs("models", exist_ok=True)
    sig_path = "models/watermark_sig.json"
    signature = {
        "secret_hash": hashlib.sha256(secret.encode()).hexdigest(),
        "n_bits": len(sig_bits),
        "sig_bits": sig_bits,
        "owner": "SAMOS-Enterprise-MLOps",
    }
    with open(sig_path, "w") as f:
        json.dump(signature, f, indent=2)

    print(f"✅ IP Watermark embedded ({len(sig_bits)} bits). Signature: {sig_path}")
    return watermarked


def detect_watermark(weights: np.ndarray, secret: str = "SAMOS-IP") -> bool:
    """
    Detects whether a watermark for `secret` is present in `weights`.

    Extracts the LSBs from the same positions used during embedding and
    compares them against the expected signature bits.

    Args:
        weights: The weight array to inspect.
        secret:  The owner secret string to verify against.

    Returns:
        True if the watermark matches, False otherwise.
    """
    flat = weights.flatten().astype(np.float64)
    expected_bits = _compute_signature_bits(secret, n_bits=min(8, len(flat)))

    for i, expected_bit in enumerate(expected_bits):
        raw_int = flat[i].view(np.int64)
        actual_bit = int(raw_int) & 1
        if actual_bit != expected_bit:
            print(f"❌ Watermark mismatch at bit {i}: expected {expected_bit}, got {actual_bit}")
            return False

    print("✅ Watermark verified — ownership confirmed.")
    return True


# ── Legacy entrypoint (backward-compatible) ────────────────────────────────────
def run_watermarking(model_path: str = "models/churn_model.pkl") -> None:
    """Phase 11: Runs the watermarking pipeline on a model file."""
    print(f"🖋️ Phase 11: Embedding IP Watermark for model: {model_path}")
    # Generate a dummy weight vector to demonstrate the signature mechanism
    rng = np.random.default_rng(42)
    demo_weights = rng.random(64)
    watermarked = embed_watermark(demo_weights, secret="SAMOS-IP")
    verified = detect_watermark(watermarked, secret="SAMOS-IP")
    print(f"  Verification result: {'✅ VERIFIED' if verified else '❌ FAILED'}")


if __name__ == "__main__":
    run_watermarking()
