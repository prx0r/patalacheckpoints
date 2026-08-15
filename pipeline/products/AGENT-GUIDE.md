# PĀṬALA PRODUCTS — Agent Reference (how to use each engine)

*The authoritative usage guide for the standalone product engines. Each product is one folder under
`pipeline/products/`, fully self-contained (stdlib + shared IPVV loader + the deterministic
`review_engine` reducer). All hydrate from **real IPVV data**. No Next.js/MCP/network in the engines.*

---

## 0. Quick orientation

| Product | Folder | Catalog # | Proof | Depends on |
|---|---|---|---|---|
| Review + Attestation + Audit | `scholar_review/` | #7 #8 #14 | 11/11 | `_shared/ipvv` + `review_engine` |
| Translation Proof | `translation_proof/` | #2 | 6/6 | `_shared/ipvv` |
| Argument | `argument/` | #5 | 6/6 | `_shared/ipvv` |
| Crux | `crux/` | #6 | 4/4 | `argument` |
| Research Packet | `research_packet/` | #9 | 5/5 | `_shared/ipvv` + networkx |
| Comparison | `comparison/` | #13 | 3/3 | `crux` |
| Evidence Independence | `evidence_independence/` | evidence | 5/5 | corroboration registry + OpenCitations |
| Claim | `claim/` | #4 | 7/7 | IPVV C1 → proposition |
| Context Bundle | `context_bundle/` | #16 | 6/6 | composes argument/crux/claim/packet |
| Passage / Reading | `passage/` | #3 | 6/6 | IPVV passages + KG2Code query |
| Benchmark | `benchmark/` | #15 | 5/5 (+ inspect_ai 1.000) | real samples → inspect_ai |
| Passage Workbench | `passage_workbench/` | #3 workbench | 5/5 | disagreements → durable review gate |
| Terminology | `terminology/` | — | 6/6 | trajectories.json + terms.json |
| Timeline | `timeline/` | — | 5/5 | historyTimeline.json |

**Total: 80/80 PASS on real data.** Every engine is runnable from any cwd (each adds `pipeline/` to
`sys.path` itself).

---

## 1. Run everything (the verification)

```bash
cd /root/patalacheckpoints
for p in scholar_review translation_proof argument crux research_packet comparison evidence_independence claim context_bundle passage benchmark passage_workbench terminology timeline; do
  echo "--- $p ---"; python3 pipeline/products/$p/test.py | grep SUMMARY
done
```

Each `test.py` is a deterministic proof (asserts invariants, exit 0 = pass). No model calls, safe on
the shared box.

---

## 2. Importing in code (the pattern)

All engines are importable as `products.<name>.engine`. You only need `pipeline/` on the path OR to run
from the patala root:

```python
import sys
sys.path.insert(0, "/root/patalacheckpoints/pipeline")

from products.scholar_review.engine import ScholarProduct
from products.translation_proof.engine import translation_proofs
from products.argument.engine import arguments
from products.crux.engine import crux_between
from products.research_packet.engine import research_packet
from products.comparison.engine import compare_between
```

---

## 3. scholar_review — Review #7 · Scholar Attestation #8 · Audit #14

**File:** `pipeline/products/scholar_review/engine.py`

### 3.1 The class
```python
from products.scholar_review.engine import ScholarProduct, verify_attestation

sp = ScholarProduct()                      # hydrates 80 real objects (goldchain + C1 + assertions)

# — review: machine proposes, authorized scholar submits —
sp.propose_review("V2-L-sastho-vimarsa-smrti-apohana:c1", "ACCEPT", "candidate")
sp.submit_review("scholar-A", "scholar", "*", ref, "ACCEPT", "sound")   # scholar_kind MUST be human-capable
# Raises PermissionError if actor_kind == "machine" (machine can never promote)

# — adversarial panel (anti-groupthink) —
sp.panel_review(ref, ["r1","r2","r3"], "j1", findings=[
    {"reviewer":"r1","opinion":"SUPPORT"},
    {"reviewer":"r3","opinion":"CONCERN","severity":"BLOCKING","text":"..."}])
#   -> {"verdict": {"verdict":"BLOCKED", "dissent":{...}, "blocking_findings":1}}

# — signed attestation (content-hash + signature, tamper-detected) —
att = sp.attest(ref, "scholar-A", "ACCEPT_WITH_QUALIFICATIONS", "reviewed")
#   -> {"attestation": {...}, "verified": [True, "VERIFIED"]}
verify_attestation(att["attestation"])   # (True, "VERIFIED")

# — zero-write counterfactual —
sp.simulate_review(ref, "REJECT")        # does NOT mutate the real ledger

# — read surfaces —
sp.list_objects(layer="C1")              # [ {id, layer, status, review_state} ]
sp.object_state(ref)                     # {effective_state, reviews, dependencies, ...}
sp.impact(ref)                           # {directly_affected, potentially_affected, unaffected}

# — audit (Pāṭala audits itself) —
sp.audit()   # {objects, layers, reviews_in_ledger, attestations_signed, attestations_verified, unreviewed_objects}
```

### 3.2 CLI
```bash
python3 pipeline/products/scholar_review/engine.py audit
python3 pipeline/products/scholar_review/engine.py list_objects '{"layer":"C1"}'
python3 pipeline/products/scholar_review/engine.py panel '{"target_ref":"...","reviewers":["r1","r2","r3"],"judge":"j1","findings":[...]}'
python3 pipeline/products/scholar_review/engine.py attest '{"target_ref":"...","reviewer":"scholar-A","verdict":"ACCEPT_WITH_QUALIFICATIONS"}'
```

### 3.3 Decisions
`ACCEPT | REVISE | REJECT | ABSTAIN`. Verdicts: `ACCEPT_WITH_QUALIFICATIONS | ACCEPT | REJECT | ABSTAIN`.

### 3.4 Anti-theatre rules (non-negotiable)
- A **machine** actor can PROPOSE but NEVER submit a state-changing review (enforced → `PermissionError`).
- Reviews are **append-only**; a REJECT does not delete, a REVISE does not overwrite.
- Attestations are content-addressed + signed; tampering breaks `content_hash`.

---

## 4. translation_proof — Translation Proof #2 (the moat)

**File:** `pipeline/products/translation_proof/engine.py`

```python
from products.translation_proof.engine import translation_proofs

proofs = translation_proofs()                                  # all 49
one = translation_proofs("pt:passage:ipvv:chunkD-memory-pramana.md")[0]

one["audit_vector"]        # 10 dims: SOURCE_COVERAGE, TARGET_GROUNDING, MORPHOLOGY, SYNTAX,
                           #         NEGATION, MODALITY, TERM_CONSISTENCY, SEMANTIC_ENTAILMENT,
                           #         PARALLEL_WITNESS, HUMAN_REVIEW
one["publication_gate"]    # {"decision":"BLOCKED","blocking_dimensions":["SOURCE_COVERAGE"]}
one["content_hash"]        # sha16 of {id, source, l2_text}
one["source_identity"]     # {witness, source_hash, source_chars}
```

**Critical:** there is NO single "quality %" score. The gate BLOCKs on any failing dimension. Treat
`audit_vector` as a vector, never aggregate it.

**CLI:** `python3 pipeline/products/translation_proof/engine.py [passage_id]`

---

## 5. argument — Argument #5

**File:** `pipeline/products/argument/engine.py`

```python
from products.argument.engine import arguments

args = arguments()                                   # all 49
one = arguments("ARG:pt:passage:ipvv:chunkD-memory-pramana.md")[0]
# keys: argument_id, work_id, thesis, premises[], inference{}, defeaters[], source_refs[], status
```

**CLI:** `python3 pipeline/products/argument/engine.py [argument_id]`

---

## 6. crux — Crux #6

**File:** `pipeline/products/crux/engine.py`

```python
from products.crux.engine import crux_between

cx = crux_between("ARG:pt:passage:ipvv:chunkA-svatyandya.md",
                  "ARG:pt:passage:ipvv:chunkB-eligibility-gita.md")
# keys: position_a, position_b, shared_premises[], crux_a_asserts[], crux_b_asserts[], crux_count, interpretation
```

**CLI:**
```bash
python3 pipeline/products/crux/engine.py "ARG:...A" "ARG:...B"   # the crux
python3 pipeline/products/crux/engine.py                          # list argument ids
```

---

## 7. research_packet — Research Packet #9

**File:** `pipeline/products/research_packet/engine.py` — requires **networkx**.

```python
from products.research_packet.engine import research_packet

pkt = research_packet("eternal self memory")   # or research_packet(q, max_sources=8)
# keys: question, retrieval{method,graph_nodes,graph_edges}, matched_passages[], count
# retrieval.method == "lexical_seed + PathRAG_flow"
# matched_passages[].{passage_id, work_id, immutable_id, relevance_hits, flow_score,
#                    source_chars, has_l2, has_c1, status}
```

**CLI:** `python3 pipeline/products/research_packet/engine.py "eternal self memory"`

---

## 8. comparison — Comparison #13

**File:** `pipeline/products/comparison/engine.py`

```python
from products.comparison.engine import compare_between

cmp = compare_between("ARG:pt:passage:ipvv:chunkA-svatyandya.md",
                      "ARG:pt:passage:ipvv:chunkB-eligibility-gita.md")
# keys: a, b, classification ("AGREEMENT" | "REAL CRUX"), shared[], divergent{a_asserts[], b_asserts[]}, note
```

**CLI:** `python3 pipeline/products/comparison/engine.py "ARG:...A" "ARG:...B"`

---

## 8b. evidence_independence — the evidence-independence product (SOURCE_ECHO)

**File:** `pipeline/products/evidence_independence/engine.py`

```python
from products.evidence_independence.engine import independence_report, corroborated_propositions

props = corroborated_propositions()                  # real corroborations, grouped by proposition
r = independence_report(live=True)                   # live OpenCitations+Crossref
r = independence_report(live=False)                  # offline deterministic (author-identity + dedup)
# per proposition: {n_corroborations_recorded, n_unique_sources, duplicate_sources, target_doi,
#                   independence{status, per_source[{source, independence}], echo_detected}}
```

**CLI:** `python3 pipeline/products/evidence_independence/engine.py live|offline`

**Honest notes:** dedups identical sources (real data has 6 recorded → 2 unique); live classification is
`UNAVAILABLE`/`OPEN` when OpenCitations is unreachable, never fabricated. Output is MACHINE_PROPOSED
evidence for the review gate, never truth.

---

## 9. Wired surfaces (already pointing at these engines)
### MCP (`mcp/index.mjs`) — spawns the engines, no code duplication
| MCP verb | Engine |
|---|---|
| `patala_scholar_list/audit/object/impact/panel/simulate/attest` | `scholar_review/engine.py` |
| `patala_translation_proof` | `translation_proof/engine.py` |
| `patala_argument` | `argument/engine.py` |
| `patala_crux` | `crux/engine.py` |
| `patala_research_packet` | `research_packet/engine.py` |
| `patala_compare` | `comparison/engine.py` |

### API (Next routes)
- `GET /api/scholar?verb=...` → `scholar_review/engine.py`
- `GET /api/products?verb=...` → the per-product engines

---

## 10. Honest limits (do not claim these as done)

- **No live LLM/auditor calls.** Engines are deterministic. Live auditors (xCOMET/MQM/Vidyut) for
  Translation Proof, formal validity checking (ASPIC+/AIF) for Argument, and semantic embeddings are
  **not** wired.
- **TranslationProof SOURCE_COVERAGE** is structural (full passage source vs its L2 summary), so it
  currently reads low (e.g. 0.09) and the gate honestly BLOCKs. A token-aligned coverage is future work.
- **Production signed-auth** (cosign/ORCID/C2PA + transparency log) is not in the demo attestation.
- **Durable ledger persistence** — the ledger re-hydrates from IPVV per call; a Postgres projection is
  future integration.
- **Research Packet** uses PathRAG flow; HippoRAG/ToG-2 modes exist in `lib/retrieval.py` but are not
  all wired here.

---

## 11. The dependency DAG (kept acyclic)

```
_shared/ipvv.py ──► translation_proof
                ──► argument
argument ──► crux ──► comparison
scholar_review  (uses review_engine reducer + _shared/ipvv)
research_packet (uses _shared/ipvv + networkx)
```

When in doubt: import `products._shared.ipvv` directly to read the real substrate
(`ipvv.passages()`, `ipvv.goldchain()`, `ipvv.assertions()`, `ipvv.c1_body(p)`, `ipvv.passage_id(p)`).
