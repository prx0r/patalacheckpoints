# scholar_review — Review #7 · Scholar Attestation #8 · Audit #14

A **standalone** peer-review + attestation engine over REAL IPVV objects. No Next.js, no MCP, no
network — pure Python (stdlib + `review_engine` reducer + shared IPVV loader).

## Products in this module
- **Review (#7)** — adversarial panel (anti-groupthink, dissent surfaced, BLOCKED on any blocking
  finding) + typed-dependency reducer + impact report.
- **Scholar Attestation (#8)** — content-addressed, deterministically signed, tamper-detected.
- **Audit (#14)** — Pāṭala audits itself: every object/review/attestation resolves.

## Run
```bash
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 pipeline/products/scholar_review/test.py   # 11/11 proof
PYTHONPATH=pipeline python3 pipeline/products/scholar_review/engine.py demo
```

## Engine API
```python
from products.scholar_review.engine import ScholarProduct
sp = ScholarProduct()
sp.panel_review("V2-L-sastho-vimarsa-smrti-apohana:c1", ["r1","r2","r3"], "j1",
                findings=[{"reviewer":"r3","opinion":"CONCERN","severity":"BLOCKING"}])
sp.submit_review("scholar-A", "scholar", "*", ref, "ACCEPT", "sound")
sp.attest(ref, "scholar-A", "ACCEPT_WITH_QUALIFICATIONS", "reviewed")
sp.audit()
```

## Wiring later (not done here)
- API: `GET /api/scholar?verb=...` (thin proxy to `engine.py`)
- MCP: `patala_scholar_*` verbs (spawnSync -> engine.py)
- Production signed-auth (cosign/ORCID/C2PA + transparency log) — schema ready, key plumbing external.

## Honest limits
- Demo signing key; production auth external.
- Ledger re-hydrates per call from IPVV; durable persistence is a later integration.
