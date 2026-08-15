# scholar_identity — the scholar's "who am I" (peer-review identity)

Gives a scholar a real identity (ORCID) + a domain scope, and binds the Ed25519 attestation signing to
it. A review/attestation can't be credited without identity.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/scholar_identity/test.py   # 7/7 proof
PYTHONPATH=pipeline python3 pipeline/products/scholar_identity/engine.py demo
```

## Engine API
```python
from products.scholar_identity.engine import register, verify_orcid, authorize
ident = verify_orcid(register("0000-0000-0000-0000", "Scholar X", ["translation","argument"]))
authorize(ident, "translation")   # -> {allowed: True}
```

## Honest limits
- Uses a synthetic ORCID for demos (never a real person's).
- The identity is MACHINE_REGISTERED until verified against ORCID (external check).
