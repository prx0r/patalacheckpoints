# CRITICAL AUDIT — ip-graph: what's REAL vs THEATER (the honest, executed review)

*2026-08-14 · status: THE HONEST REVIEW · agentpatala's critical audit of ip-graph, done by RUNNING the
code and reading the assertions — not trusting the docs. Every claim below is verified by execution.
This is not a takedown — it's the anti-theatre doctrine applied to the lab, so we build on what's real.*

---

## 1. THE TEST SUITE: 82/84, and its own failure reveals the truth

**Ran `scripts/run-tests.py`: 82/84, not the claimed "75/75".**
- **`theatre_check_all` FAILS.** Its own message:
  > *"The lab has 37 experiments proven on real data; 44 prove mechanism only (synthetic). The fix is the
  > graduation test (real data through the whole stack)."*
- **So the honest count is 37 REAL / 44 SYNTHETIC — not "75 fully built."** The docs say "30 fully built";
  the test's own audit says 37 real, 44 mechanism-only.

## 2. The "real graph" is the DOYLE corpus, not Sanskrit

The `data/graph/graph.json` the graduation test uses:
- **490 nodes**: Libertarianism, Mind Body Problem, Value, Quantum, Entropy, Superposition...
- **0 Sanskrit refs** (no Stk, IPVV, Bhāvopahāra, Tantrāloka)
- So "graduation_test_real_data" proves the mechanisms on the **free-will science corpus**, NOT real Pāṭala
  Sanskrit. It's "real data" — but not OUR data.

## 3. The translation tests are CIRCULAR (hand-fed, then asserted)

```python
good.source_analysis = {"morphology": "PASS"}      # hand-SET the value
v = good.audit_vector()
check("good translation: SOURCE_COVERAGE >= 0.99", v["SOURCE_COVERAGE"] >= 0.99)  # assert it back
```
The test **sets the field, then asserts the container returns it.** Nothing generates a translation. Same
pattern in `kernel_validation_suite.py` (hand-sets `good.source_analysis = {"morphology":"PASS"}`).

## 4. The kernels are mostly CONTAINERS + READS, not GENERATORS

| Kernel | What it actually is |
|---|---|
| `translation.py` | **empty container** (audit_vector, publication_gate) — translates NOTHING |
| `translation_variant.py` | `add(translator, text)` — you HAND-FEED the variants; it compares, doesn't generate |
| `vidyut_l0.py` | has a **fallback SLP1 word-splitter** (vidyut IS installed, but the fallback path exists and may be what runs) |
| `pushing_miner.py` | reads markdown + regex-mines cruxes (legit for the HUMAN LOGICVID gold, but no new generation) |
| `hermes_exec.py` | **ORPHANED** — the Hermes execution path is built but **imported by NOTHING** |

## 5. THE BIGGEST FINDING: Hermes is NOT wired to generation

- `hermes_exec.py` (the real `hermes -z` execution path) is **imported by nothing** — it's dead code.
- **Nothing in ip-graph calls Hermes for the actual LLM generation** (translation, commentary, essays,
  pushing).
- The kernels that SHOULD generate (translation, translation_variant) are hand-fed containers.
- **The correct pattern is `translate_passage.py`** (agentpatala's, in `/root/projects/patala/migration/v3/`)
  — real Hermes generation: T1 + close + reading + commentary via `model.py` → `hermes -z`.

## 6. WHAT IS ACTUALLY REAL (not theater)

These are genuinely solid and worth building on:
- **`epistemic.py`** — the 4-axis Authority + ceiling invariant (real, honest)
- **`review.py`** — the herdr reducer + human gate (real, tested)
- **`staleness.py`** — the blast-radius walker (real, correct)
- **`scholar_review.py`** — the adversarial panel + CiteCheck (real)
- **`source_registry.py`** — the rights/health source registry (real)
- **`evidence_ledger.py`** — the typed-evidence ledger (real)
- **`vidyut_l0.py`** (the deterministic normalization, when vidyut is used)
- **The organism loop design** (`ingestion_organism.py`) — the priority-queue autonomy is RIGHT
- **The Tantrāloka full-stack test** (9/9) — theme→essay→education→pedagogy→products on real Tantrāloka
  data — this one genuinely wires real data end-to-end

## 7. THE DECISION

**Hermes should power GENERATION; `.py` kernels should power REDUCTION.** ip-graph has this backwards:
- The `hermes_exec.py` (for generation) is orphaned.
- The translation kernels (which should generate) are empty containers.
- The deterministic kernels (review/staleness/evidence — correctly `.py`) are solid.

**The fix:** wire `hermes_exec.py` into the translation/variant/essay kernels (or better, adopt
`translate_passage.py`), so the organism actually GENERATES via Hermes instead of hand-feeding containers.
Keep the deterministic `.py` reducers (they're correct as `.py`).

---

*This is the honest audit. ip-graph has REAL machinery (the reducers, the registry, the organism loop, the
Tantrāloka full-stack) and THEATER (the circular translation tests, the orphaned hermes_exec, the
Doyle-corpus "real" graph). The correct architecture: Hermes for generation, `.py` for reduction.*
