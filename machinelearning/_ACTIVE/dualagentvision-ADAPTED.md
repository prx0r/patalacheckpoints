# DUAL-AGENT VISION — ADAPTED TO OUR ACTUAL INFRASTRUCTURE

*2026-08-12. The vision (`dualagentvision.md`) is the north star. This doc maps it onto what we ACTUALLY
built, showing each checkpoint's real state, and uses the vision's own checkpoint-test to decide what to
build next. The test for every engineering task:

> **Name the checkpoint it advances · the scholarly object it makes more trustworthy · the benchmark/proof
> that demonstrates success. If you can't answer all three, don't build it.**

---

## 1. The state map (vision checkpoint → our real infra)

| Checkpoint | Vision gate | Our actual state | Status |
|---|---|---|---|
| **CP0 BENCHMARK** | measure honestly | `benchmarks/v0/` frozen (MANIFEST/SCHEMA/SPLITS/METRICS + ARG-GOLD-001) | ✅ DONE |
| **CP1 SOURCE PROOF** | certify source→L0 | `verify_l0.py` (P0, honest) + `philproof.py` (the handshake) | 🔶 PARTIAL (P0; P1–P5 not wired) |
| **CP2 RETRIEVAL** | beat baseline on frozen benchmark | `retrieval.py` (BM25/dense/hybrid); old results marked PRE-BENCHMARK | 🔶 NOT RE-BASELINED on v0 |
| **CP3 THEMES** | themes adjudicated | `clusters.json` (machine) + `themes.ts` (separate, not unified) | 🔶 PARTIAL (proposals exist; not accepted) |
| **CP4 ARGUMENT** | real reasoning reconstructed | `gold.py` (ARG-GOLD-001) + `argument.py` (schema) | 🔶 PARTIAL (1 gold; extractor not built) |
| **CP5 VERIFICATION** | claims don't outrun evidence | `lib/verify.ts` (structural) + `essayverify.py` (adversarial) | 🔶 PARTIAL (semantic not model-based) |
| **CP6 SYNTHESIS** | provenance-carrying essay | `essaygen.py` + `essay.py` (claim-graph-canonical) | 🔶 PARTIAL (mechanism; no gold essay) |
| **CP7 WORKBENCH** | explore/develop ideas | — | ⬜ NOT STARTED |
| **CP8 ADVERSARIAL REVIEW** | attack scholarship | partial via verify/counterevidence | ⬜ NOT STARTED (orchestration) |
| **CP9 API/MCP** | tools use the intelligence | `mcp/index.mjs` + `/api/verify/*` | 🔶 PARTIAL (verify tools; arg/theme/essay not exposed) |
| **CP10–12** | collaborative/economic/cross-corpus | — | ⬜ NOT STARTED |

**The honest picture:** CP0 is done; CP1–CP6 have partial infra; CP7+ not started. The vision's "gate"
for each CP is the missing piece everywhere — most checkpoints have *machinery* but not the *proof that
it works* (benchmark-passing, adjudication, or re-baselining).

---

## 2. The checkpoint-test applied to our options (what to build next)

Using the vision's own rule, here's the honest read of each candidate:

| Candidate | Checkpoint | Object it makes trustworthy | Benchmark/proof | Verdict |
|---|---|---|---|---|
| **Re-baseline retrieval on v0** | CP2 | retrieval | run BM25/dense/hybrid on PATALA-RETRIEVAL split S2 | ✅ CLEAR — advances CP2 with a real proof |
| **Grow argument gold to 5–10** | CP4 | argument | hand-build more gold; then test extractor | ✅ CLEAR — the vision's Phase 4 gate |
| **Unify themes.ts + clusters.json** | CP3 | theme | adjudicate memberships against source | ✅ CLEAR — Phase 3 gate |
| **Wire P1–P5 source proof** | CP1 | PhilologicalProof | Vidyut as witness; 0 unknown chars | 🔶 L0 AGENT's lane |
| **Build the essay prose (model-drafted)** | CP6 | essay | needs a gold essay + verifier | 🔴 NOT YET — no gold essay to verify against |
| **More graph abstractions** | — | — | — | ❌ BLOCKED — no checkpoint/object/proof |

**The two clear next moves (both pass the checkpoint-test):**
1. **CP2 — re-baseline retrieval against the frozen benchmark** (the vision's Phase 2 gate; converts our
   PRE-BENCHMARK results into real ones or retires them).
2. **CP4 — grow the argument gold** (the vision's Phase 4; 5–10 hand-built arguments make extraction
   measurable).

---

## 3. The two-agent division, mapped to our infra

### Agent L0 — vertical truth (the vision's Phase 1)
- **Already:** `verify_l0.py` (P0, honest) + the `l0_schema.json`/`l0_coverage.json` contract.
- **Next (vision gate):** make P0 lossless for supported passages (0 unknown chars), then P1–P5.
- **Output:** `PhilologicalProof` objects (not logs) — the `pp:` IDs my `philproof.py` consumes.

### Agent ML (me) — horizontal/upward derivation (the vision's Phases 2–6)
- **Already:** benchmark v0, clusterer, argument schema, ARG-GOLD-001, essaygen, essayverify.
- **Next (vision gates):** re-baseline retrieval (CP2), unify+adjudicate themes (CP3), grow argument gold
  then build the extractor (CP4–5), semantic verification (CP6).

### Shared boundary (contractual, per the vision)
They join at **Passage ID / TranslationDecision ID / PhilologicalProof ID / C1 ID** — never filename,
guessed locator, title, or fuzzy match. **The fabricated-ID failure was exactly this; `cleanup.py` now
enforces exact resolution.**

---

## 4. The anti-weeds rule (from the vision, now the standing rule)

> **Every engineering task must name: (1) the checkpoint it advances, (2) the scholarly object it makes
> more trustworthy, (3) the benchmark/proof that demonstrates success. If it can't answer all three,
> don't build it.**

And the master object is always:
```
SOURCE → L0 → TRANSLATION → COMMENTARY → THEMES → ARGUMENT → SYNTHESIS → WORKBENCH → API
```
each node pointing downward, each status honest (DETERMINISTIC_FACT | MACHINE_PROPOSED | HUMAN_REVIEWED | ACCEPTED).

---

## 5. Where this leaves us (the north star, grounded)

The vision is not aspirational — **CP0–CP6 already have real (if partial) infrastructure.** The remaining
work is NOT building new layers; it's **making each existing checkpoint pass its gate**:

1. **CP2** re-baseline retrieval on v0 (or retire).
2. **CP4** grow argument gold 5–10, then build+gate the extractor.
3. **CP3** unify + adjudicate themes.
4. **CP5** model-based semantic verification (against adversarial examples).
5. **CP6** gold essay (only after CP4–5).

Each is a *proof*, not a *feature*. That's how we reach the bigger vision — one checkpoint making one
more scholarly claim trustworthy enough for the next pipeline to consume — without a rewrite.
