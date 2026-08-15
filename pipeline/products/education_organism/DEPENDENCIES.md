# DEPENDENCY + COMPLETENESS MANIFEST — the whole session's work

*2026-08-15 · the full dependency and completeness audit of everything built this session: the
education-serving organism, the derivation chain + audit, the site + API, and the smellycock
integration. Every dependency resolved, every surface verified. This is what the smellycock owner pulls.*

---

## 1. THE PRODUCT (`pipeline/products/education_organism/`)

| File | Deps (module) | Present? |
|---|---|---|
| `engines/education.py` | stdlib only | ✅ |
| `engines/organism.py` | stdlib only | ✅ |
| `engines/organism_loop.py` | stdlib only | ✅ |
| `engines/misconception.py` | **→ `staleness`** (present in engines/) | ✅ |
| `engines/pedagogy.py` | stdlib only | ✅ |
| `engines/memory.py` | stdlib only | ✅ |
| `engines/segment_key.py` | stdlib only | ✅ |
| `engines/reconciliation.py` | stdlib only | ✅ |
| `engines/staleness.py` | stdlib only | ✅ |
| `README.md` / `AGENT-GUIDE.md` / `VISION.md` | — | ✅ |

**Verified: all 9 engines import cleanly; `misconception → staleness` resolves.**

## 2. THE CORE MACHINERY (`serveragent3/kernels/`)

16 kernels, all stdlib-only, **16/16 import OK**:
`object_registry` · `gates` · `generation` · `education` · `organism` · `organism_loop` ·
`misconception` · `pedagogy` · `memory` · `segment_key` · `reconciliation` · `staleness` ·
`ingestion_organism` · `next_action` · `source_registry` · `integrity_gate`.

## 3. THE SCRIPTS (`serveragent3/scripts/`) — all run OK

`run-tests` (22/22) · `test-e2e` (5/5) · `test-gems-integration` (5/5) · `run-organism-loop` ·
`run-ingestion-organism` · `tutor-agent` · `learner-log` · `compile-education` · `compile-og-learning` ·
`link-derivation-chain` · `audit-resolve` · `serve-education` (API) · `check.py` (drift).

## 4. THE LIVE SURFACES

| Surface | Deps | Status |
|---|---|---|
| Astro static site (`smellycock/web/`) | `astro ^5.0.0` (+ esbuild/sharp) | ✅ built, 10 pages |
| Site server (:8080) | stdlib `http.server` | ✅ HTTP 200 |
| Education API (:8787) | stdlib `http.server` + `sqlite3` | ✅ HTTP 200 |
| Learner store | SQLite (`learner.db`) | ✅ |

## 5. THE SMEL LYCOCK INTEGRATION

- `MANIFEST.json`: **27 implementation entries** (incl. education_organism product + GEM kernels) — the owner's resolver finds it.
- `check.py --status`: **PASS**
- `check_epistemic.py --status`: **PASS** (25 products, 8 layers reconciled)

## 6. THE ENDGAME PROOF

The audit resolver still traces an education claim to source:
```
EDUCATION → ESSAY → SYNTHESIS → ARGUMENT → C1 → L200 → L2 → L1 → L0 → T1 → SOURCE ✅
```

## 7. WHAT THE OWNER NEEDS TO RUN

```bash
# the product (all deps included, stdlib-only)
cd /root/patalacheckpoints
PYTHONPATH=pipeline python3 -c "import sys; sys.path.insert(0,'pipeline/products/education_organism/engines'); import education,organism,organism_loop,misconception,pedagogy,memory,segment_key,reconciliation,staleness; print('engines OK')"
# the verification + audit
python3 /root/serveragent3/scripts/run-tests.py        # 22/22
python3 /root/serveragent3/scripts/test-e2e.py         # 5/5
python3 /root/serveragent3/scripts/audit-resolve.py    # claim → source
# the live site + API
cd /root/smellycock/web && PATALA_WEB_ROOT=/root/smellycock/web npx astro build
python3 /root/serveragent3/scripts/serve-education.py 8787
# the gates
cd /root/smellycock && python3 check.py --status && python3 check_epistemic.py --status
```

**Every dependency is included; every surface is verified; nothing is left dangling.**
