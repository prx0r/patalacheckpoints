# MASTER INTEGRATION DEVPLAN — ONE organism (patala factory + ip-graph read plane)

*2026-08-14. THE canonical build plan, synthesized from four deep parallel reviews of patala v2, patala v3,
my ip-graph NAVIGATION files, and my SPECs. This is the single source of truth for the final integration:
**patala has the mature TRANSLATION FACTORY (SOURCE→T1→L0→L1/L2→L200→C1, real workers, committed objects);
ip-graph has the modern READ PLANE + ORGANISM + VALIDATION kernels.** The build wires them into ONE
autonomous organism — never rebuild, always integrate.*

---

## THE ONE ARCHITECTURE (what we're building)

```text
WRITE SIDE (patala — mature, real)          READ SIDE (ip-graph — modern, built)
  object_registry (SOURCE 32039 · T1 · L0        my projection compiler (context_compiler,
  · L1L2 · L200 · C1, committed)                  build-static-site, already reads the registry)
  factory workers (t1/l0/l1_l2/l200/c1)         → immutable content-addressed bundles (R2/CDN)
  L200 derivational-audit (the moat)             → my read plane (bundle_router MCP + seo + fts)
  C1 commentary (the philosophical frame)        → Astro site + Cloudflare edge
  corpus_state (111-work ledger)                 my organism (next_action + factory_pool + hermes)
      │                                            + my validation (TranslationProof + scholar_review)
      └────────── ONE autonomous organism ───────────┘
   patala PRODUCES translations/proofs/commentaries; ip-graph VALIDATES + SERVES them.
```

**The one rule (SPEC-00):** the repo/Atlas is a COMPILER producing immutable, independently addressable read
artifacts. Compute on write, read from bytes. A new text must NOT rebuild the whole corpus.

---

## THE VERIFIED REALITY (from the four reviews — what actually exists)

### Patala's mature TRANSLATION FACTORY (REAL, committed objects)
- **T1** transliteral gloss: 397 committed objects / 25 works ✅
- **L0** token floor (vidyut): 815 committed / 12 works ✅
- **L1/L2** readable prose: worker exists; L1L2-translate is the generative engine ✅
- **L200** derivational-audit: 11 committed (fixtures) + 63 hand-authored IPVV gold ⚠️ machine-scale gap
- **C1** commentary: worker + frozen C1-SPEC, 4 committed + 63 IPVV gold ⚠️
- **corpus_state**: 111-work ledger, next_valid_action control plane ✅
- **The L200 spec is FROZEN** (8 sections, MT/IA classifier, audit-is-stricter-than-prose) ✅
- **The schema.py collision**: the two systems MUST run in separate processes (enforced)

### My ip-graph READ PLANE + ORGANISM (REAL, validated)
- **Read plane**: context_compiler (12/12) · fts_search (9/9) · bundle_router MCP (16/16) · seo (13/13) ·
  build-static-site (already compiles the registry) · rebuild-on-commit (compute-on-write) · Astro site ·
  edge worker ✅
- **Organism**: ingestion_organism (10/10) · next_action (7/7) · factory_pool (10/10) · hermes_exec
  (agentic generation, 6/6) · self_healing (8/8) · evidence_ledger (9/9) · integrity_gate (8/8) ·
  iteration_confidence (5/5) · pushing_miner (7/7) · commentary_lift (5/5) ✅
- **Epistemic core**: TranslationProof (11-dim, gate BLOCKS) · scholar_review (panel+citecheck) ·
  canonical_contracts (parity with OG authority) · staleness (blast-radius) ✅

### The specs (already complete — apply them, don't re-spec)
- **SPEC-00** (compiler/factory), **SPEC-16** (translation proof-carrying), **SPEC-18** (complete pipeline,
  3 products validated), **SPEC-49** (frozen stack + Rust policy), **SPEC-13** (staleness toolbox).

---

## THE HONEST GAPS (what's NOT built — the actual work)

### The 7 real gaps (from the reviews)
1. **Machine L200/C1 at corpus scale** — the derivational-audit + commentary produce only fixtures; the
   63+63 IPVV gold is hand-authored, not machine. THE highest-leverage gap (v2 STEP 2).
2. **Live TranslationProof auditors** (xCOMET/MQM/OTTAWA/ByT5/Heritage/Vidyut lattice) — the proof
   generators/auditors from SPEC-16 are NOT wired; `translation.py.generate()` hand-fills from bool().
3. **The Translation Audit Compiler** (SPEC-16 §30) — `patala translate-proof SOURCE TRANSLATION` CLI doesn't exist.
4. **The real read-plane INFRASTRUCTURE** — R2 push, Neon Postgres, Cloudflare deploy. Currently a LOCAL
   simulation (bundles to disk, FTS in DuckDB, Astro un-deployed). Deployment = the SPEC-00 premise unmet.
5. **Signed human attestation (gap E)** — blocks the marketplace.
6. **Context paging (gap A)** + the 5 missing kernels (misconception, question_growth, enquiry,
   design_provenance, graph_stable).
7. **Text-Fabric substrate + CTS + Stencila schema-compiler** (SPEC-18 build order steps 2-3).

---

## THE BUILD PHASES (the canonical order — from the v2 GROUND-UP + SPEC-00 §25)

### PHASE 0 — RECONCILE THE RECORD [do first — everything rests on it]
- Regenerate `layers/*.md` to reality (L00-L07+L09 built, L08 empty).
- Reconcile the dual layer-taxonomy (00-09 vs L00-L12) → pick ONE.
- Resync GAPS.md (drop "no read plane" claims).
- **Fix the count drift** (44 kernels in lib/, docs say 43/40/37).

### PHASE 1 — THE SUBSTANCE: ingest the IPVV gold into the registry [the highest-leverage build]
- **Bulk-ingest the 63 L200 + 63 C1 IPVV golds** into the registry with Derivation edges (mirror
  `ingest_ipvv_argmap_golds.py`). This makes the moat REAL on real data.
- Then run the L200/C1 workers on the Tantrāloka root (the Mona Lisa) at corpus scale.

### PHASE 2 — CONVERGE THE KERNEL (kill the divergent defs)
- Promote `python/patala_core/authority.py` (non-scalar AuthorityVector) to canonical (my
  `canonical_contracts.py` already has parity).
- Add `derivation.py · events.py+reducers.py · gates.py · staleness.py` (the 9 [NEW] items).
- Wire ledger→Postgres; stop the site reading `data/atlas/*.ts`.

### PHASE 3 — THE TRANSLATION AUDIT COMPILER (SPEC-16 §30, the moat made live)
- Wire the real proof generators (ByT5/Heritage/Vidyut/skrutable lattice) + auditors (xCOMET/GemSpanEval/
  OTTAWA/entailment/term/MQM) into `TranslationProof`.
- Build `patala translate-proof SOURCE TRANSLATION → translation-proof.json` (13 sections).
- Ingest Mitrasamgraha/MITRA as the benchmark + error-family validators.

### PHASE 4 — THE READ PLANE INFRASTRUCTURE (SPEC-00 §9-20, the deploy)
- Push the compiled projections to R2 (content-addressed); serve via Cloudflare CDN.
- Stand up Neon Postgres + the `artifacts/aliases/relations/passages/works` schema.
- Deploy the Astro site + Worker (`/api` + `/mcp`) + Hyperdrive.
- Wire the projection DAG + incremental rebuild (add doc → rebuild only affected, NOT whole corpus).

### PHASE 5 — THE ORGANISM AT REAL SCALE
- Wire the autonomous loop: `next_action` (decide) + patala factory (produce) + `factory_pool` (parallel)
  + `hermes` (generate) + my gates (verify) → commit → serve.
- The Tantrāloka full-corpus production (Phase 1 of this, at scale).
- The organism feedback (learner probes → cruxes → re-prioritize).

### PHASE 6 — CLOSE THE SECURITY + PRODUCT GAPS
- Gap E (signed attestation), Gap A (context paging), the 5 missing kernels, Layer-08 domains.

---

## THE INTEGRATION SEAM (who does what)

- **patala**: the write-side factory (SOURCE→EDUCATION DAG, workers, registry, L200/C1 production).
- **ip-graph (me)**: the read plane (compile→bundles→MCP→SEO→site) + the organism (decide→generate→verify→
  commit) + the validation kernels (TranslationProof, scholar_review, integrity, evidence).
- **The rule**: reuse, never rebuild. patala's factory is real; my read plane + organism is real. The build
  is the INTEGRATION (already partially wired: `build-static-site.py` reads the registry read-only).

## Proofs / resolution
- Patala v3: `migration/v3/` (V3-BUILD-SPEC, PRODUCTS, L200/C1 specs, workers)
- Patala v2: `migration/v2/` (LAYERS.yaml, GEMS, GROUND-UP-PLAN) + `docs/NORTHSTAR.md` (thesis)
- My read plane + organism: `lib/` (context_compiler, bundle_router, seo, ingestion_organism, factory_pool)
- My specs: `specs/SPEC-{00,16,18,49,13}.md`
- The sub-plans: `devplans/` (TRANSLATION-PRODUCTION, READ-PLANE-ORGANISM, TANTRALOKA-PRODUCTION)
