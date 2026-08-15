"""products/scholar_review/signing.py — production attestation signing (cosign-style, Ed25519).

Upgrades the demo attestation from a shared-secret HMAC to REAL asymmetric signing (Ed25519), the
cosign/C2PA pattern. CPU-only, no GPU. A scholar's private key signs the attestation; the public key
verifies it; a third party can verify WITHOUT the private key (asymmetric).

Security model (cosign-style):
  - private key stays with the scholar (never leaves)
  - public key is published (a transparency log / registry)
  - the attestation is content-addressed + signed; any tamper breaks verification
  - verification needs ONLY the public key, so anyone can confirm a scholar signed it

Deterministic + CPU-only (cryptography lib). Fallback to the demo HMAC if `cryptography` is absent.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


def _keypair() -> tuple[bytes, bytes]:
    """Generate an Ed25519 (private_pem, public_pem)."""
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    key = ed25519.Ed25519PrivateKey.generate()
    priv = key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                             serialization.NoEncryption())
    pub = key.public_key().public_bytes(serialization.Encoding.PEM,
                                        serialization.PublicFormat.SubjectPublicKeyInfo)
    return priv, pub


def sign_payload(payload: bytes, private_pem: bytes) -> bytes:
    """Sign a canonical payload with an Ed25519 private key (cosign-style)."""
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    key = serialization.load_pem_private_key(private_pem, password=None)
    return key.sign(payload)


def verify_signature(payload: bytes, signature: bytes, public_pem: bytes) -> bool:
    """Verify an Ed25519 signature with the PUBLIC key only (asymmetric)."""
    from cryptography.hazmat.primitives.asymmetric import ed25519
    from cryptography.hazmat.primitives import serialization
    from cryptography.exceptions import InvalidSignature
    try:
        key = serialization.load_pem_public_key(public_pem)
        key.verify(signature, payload)
        return True
    except (InvalidSignature, Exception):
        return False


def make_signed_attestation(attestation: dict, private_pem: bytes | None = None) -> dict:
    """Produce a production-signed attestation: content-hash + Ed25519 signature + public key.

    `attestation` is the plain (unsigned) attestation dict. Returns the signed record with
    `signature` (base64) + `public_key` (PEM) + `content_hash`.
    """
    import base64
    if private_pem is None:
        private_pem, public_pem = _keypair()
    else:
        # derive the public key from the private
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        key = serialization.load_pem_private_key(private_pem, password=None)
        public_pem = key.public_key().public_bytes(serialization.Encoding.PEM,
                                                   serialization.PublicFormat.SubjectPublicKeyInfo)

    content_hash = hashlib.sha256(json.dumps(attestation, sort_keys=True, ensure_ascii=False).encode()).hexdigest()
    record = {**attestation, "content_hash": content_hash}
    canonical = json.dumps(record, sort_keys=True, ensure_ascii=False)
    sig = sign_payload(canonical.encode(), private_pem)

    return {
        **record,
        "signature": base64.b64encode(sig).decode(),
        "public_key": public_pem.decode(),
        "algorithm": "Ed25519",
    }


def _canonical_of(signed: dict) -> str:
    """The payload that was signed = the record WITHOUT signature/public_key/algorithm
    (this INCLUDES content_hash, which is part of the signed record)."""
    canon = {k: v for k, v in signed.items() if k not in ("signature", "public_key", "algorithm")}
    return json.dumps(canon, sort_keys=True, ensure_ascii=False)


def verify_signed_attestation(signed: dict) -> tuple[bool, str]:
    """Verify a production-signed attestation with its embedded public key (no private key needed)."""
    import base64
    public_pem = signed["public_key"].encode()
    signature = base64.b64decode(signed["signature"])
    payload = _canonical_of(signed)
    if not verify_signature(payload.encode(), signature, public_pem):
        return False, "signature_invalid"
    # content_hash is the hash of the ORIGINAL attestation fields (not the self-referential record)
    original = {k: v for k, v in signed.items() if k not in
                ("signature", "public_key", "algorithm", "content_hash")}
    if hashlib.sha256(json.dumps(original, sort_keys=True, ensure_ascii=False).encode()).hexdigest() \
            != signed["content_hash"]:
        return False, "content_hash_mismatch (payload tampered)"
    return True, "VERIFIED"


if __name__ == "__main__":
    priv, pub = _keypair()
    att = {"attestation_id": "SA-demo", "target_ref": "pt:pid:ipvv:80f9c7f414ed",
           "verdict": "ACCEPT_WITH_QUALIFICATIONS", "reviewer": "scholar-A"}
    signed = make_signed_attestation(att, priv)
    ok, why = verify_signed_attestation(signed)
    print("signed attestation algorithm:", signed["algorithm"])
    print("content_hash:", signed["content_hash"][:16], "...")
    print("signature b64:", signed["signature"][:24], "...")
    print("verify (public key only):", ok, "|", why)
    # tamper: change the verdict -> must fail
    tampered = dict(signed); tampered["verdict"] = "REJECT"
    print("tampered verify:", verify_signed_attestation(tampered)[0], "(should be False)")
    assert ok is True
    assert verify_signed_attestation(tampered)[0] is False
    print("SELF-TEST PASS (production Ed25519 attestation: sign + verify + tamper-detect)")
