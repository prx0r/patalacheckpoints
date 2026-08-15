"""products/scholar_identity/engine.py — scholar identity (the "who am I" of peer review).

Gives a scholar a real identity (ORCID-backed) + a domain scope, and binds the Ed25519 signing to that
identity. Today `submit_review` takes a bare `actor_id` string; without identity a review can't be
credited or trusted. This is the identity layer that makes reviews credible.

What it provides (CPU-only, deterministic):
  - register(orcid, name, domain_scope[], public_key) -> a ScholarIdentity (PT-scholar id)
  - authorize(identity, scope) -> can this scholar act in this scope? (the review-policy gate)
  - signing_key() / public_key() -> bind the Ed25519 attestation to this identity

The identity is MACHINE_REGISTERED until verified against ORCID; the Ed25519 public key makes a review
or attestation verifiable by anyone (asymmetric — no shared secret).
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[3]
if str(_ROOT / "pipeline") not in sys.path:
    sys.path.insert(0, str(_ROOT / "pipeline"))

# domain scopes a scholar can be authorized for (the closed set, per AXIOMS one-taxonomy rule)
SCOPES = {"translation", "argument", "passage", "terminology", "timeline", "evidence",
          "synthesis", "essay", "education", "all"}


@dataclass
class ScholarIdentity:
    scholar_id: str
    orcid: str
    name: str
    domain_scopes: list = field(default_factory=list)
    status: str = "MACHINE_REGISTERED"   # -> ORCID_VERIFIED after external check
    created_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    public_key: str = ""                 # the Ed25519 public key (PEM)

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items()}


def _new_ed25519_keypair() -> tuple[bytes, bytes]:
    """Generate an Ed25519 keypair for the scholar (private stays with them; public is published)."""
    from products.scholar_review.signing import _keypair
    return _keypair()


def register(orcid: str, name: str, domain_scopes: list[str], public_key: str | None = None,
             private_key: bytes | None = None) -> dict:
    """Register a scholar identity. Generates (or accepts) an Ed25519 keypair.

    private_key is the scholar's own (never stored/committed); public_key is what's published.
    """
    for s in domain_scopes:
        if s not in SCOPES:
            raise ValueError(f"unknown scope {s}; use one of {sorted(SCOPES)}")
    if public_key is None:
        _, public_key = _new_ed25519_keypair()
    scholar_id = f"PT-scholar:{orcid.replace('/', '').replace('-', '').lower()}"
    ident = ScholarIdentity(scholar_id=scholar_id, orcid=orcid, name=name,
                            domain_scopes=domain_scopes, public_key=public_key)
    return ident.to_dict()


def authorize(identity: dict, scope: str) -> dict:
    """Can this scholar act in `scope`? The review-policy gate."""
    if identity.get("status") not in ("MACHINE_REGISTERED", "ORCID_VERIFIED"):
        return {"allowed": False, "reason": "identity not registered/verified"}
    scopes = identity.get("domain_scopes", [])
    if "all" in scopes or scope in scopes:
        return {"allowed": True, "scope": scope, "scholar_id": identity.get("scholar_id")}
    return {"allowed": False, "reason": f"scholar not authorized for scope '{scope}'",
            "scholar_scopes": scopes}


def verify_orcid(identity: dict) -> dict:
    """Mark an identity ORCID-verified (external ORCID check in production; mechanism here).

    Once verified, the identity's reviews/attestations are trusted to their scope.
    """
    identity["status"] = "ORCID_VERIFIED"
    identity["verified_at"] = datetime.now(timezone.utc).isoformat()
    return identity


def run_demo() -> dict:
    """Register a scholar, authorize them, sign an attestation with their key."""
    from products.scholar_review.signing import make_signed_attestation, verify_signed_attestation
    from products.scholar_review.engine import ScholarProduct

    # 1. register a real scholar identity (public key generated)
    private_key, public_key = _new_ed25519_keypair()
    ident = register("0000-0000-0000-0000", "Scholar X", ["translation", "argument"],
                     public_key=public_key.decode())
    ident = verify_orcid(ident)

    # 2. authorize
    ok = authorize(ident, "translation")
    deny = authorize(ident, "timeline")

    # 3. sign an attestation with the scholar's private key
    sp = ScholarProduct()
    ref = sp.list_objects(layer="C1")[0]["id"]
    att = {"attestation_id": f"SA-{ident['scholar_id']}", "target_ref": ref,
           "verdict": "ACCEPT_WITH_QUALIFICATIONS", "reviewer": ident["name"]}
    signed = make_signed_attestation(att, private_key)
    ver = verify_signed_attestation(signed)

    return {"identity": ident, "authorize_translation": ok, "authorize_timeline": deny,
            "attestation": {"verified": ver[0], "reason": ver[1]}, "key_alg": "Ed25519"}


if __name__ == "__main__":
    import sys as _s
    verb = _s.argv[1] if len(_s.argv) > 1 else "demo"
    if verb == "demo":
        print(json.dumps(run_demo(), indent=2, ensure_ascii=False))
    else:
        print(json.dumps({"error": f"unknown verb {verb}"}))
