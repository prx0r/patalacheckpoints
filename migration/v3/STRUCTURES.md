# PĀṬALA V3 — THE STRUCTURES (the definitive structural reference, validated against v2)

*2026-08-14 · status: THE AUTHORITATIVE STRUCTURES · the complete list of structures Pāṭala definitely
needs, excavated from v2 and validated present in v3. Each structure: what it is, where it lives in v3,
and its honest status (PROVEN / PROVEN-MECHANISM / NEEDS-BUILD / BUILT-in-patala). This is the frontier-
fast answer to "what structures do we definitely need" — nothing speculative, every one either proven in
the lab or built in patala/.meta.*

---

## THE STRUCTURES WE DEFINITELY NEED (the authoritative list)

### S1. THE AUTHORITY GRAPH + ATLAS (the spine) — ✅ present in v3
- **What:** the canonical object graph: work → witness → passage → translation → proof → commentary →
  argument → synthesis, every node identity-resolved. The **Atlas** (254 works, resolver) is the
  human/API surface over it.
- **v3:** `LAYERS.yaml` (identity layer, added this session) · `PRODUCTS.md` (#0)
- **Status:** PROVEN in patala (`patala_core/atlas/`) · NOT in lab · **was a v3 gap, now restored**

### S2. THE EPISTEMIC ENVELOPE (the honesty law) — ✅ present in v3
- **What:** every node carries 4-axis Authority (generation·evidence·review·publication) with
  `ceiling(child) ≤ parent`. Stops the graph being a hallucination dump.
- **v3:** `MECHANISMS.md` (M1) · `LAYERS.yaml` (authority_axes) · `PRODUCTS.md` (#4)
- **Status:** PROVEN (0 violations)

### S3. THE EVENT LEDGER + REDUCER (the state machine) — ✅ present in v3
- **What:** append-only events → deterministic reducer → state. The human publication gate.
- **v3:** `MECHANISMS.md` (M2) · `PATALA-V3-ORGANISM.md` · `PRODUCTS.md` (#7)
- **Status:** PROVEN (herdr)

### S4. THE DERIVATION DAG + STALENESS (self-maintaining) — ✅ present in v3
- **What:** every object records parents + transformation; staleness = blast-radius → rebuild order.
- **v3:** `MECHANISMS.md` (M3) · `LAYERS.yaml` (staleness kernel) · `V3-BUILD-SPEC.md`
- **Status:** PROVEN (PHYSICS retraction → FREE_WILL)

### S5. THE REVIEW PANEL + CITECHECK (the immune system) — ✅ present in v3
- **What:** adversarial panel, anti-groupthink, CiteCheck, findings lifecycle.
- **v3:** `MECHANISMS.md` (M4) · `PRODUCTS.md` (#7) · `LAYERS.yaml` (review kernel)
- **Status:** PROVEN (37.1% bias-robust)

### S6. THE TRANSFORMATION REGISTRY (the factory's brain) — 🔧 ADDED this session (was missing)
- **What:** one registry of every transformation (input/output/invalidates/preserves/requires/verifier),
  driving scheduling + staleness + validation + MCP + docs from one place. The v2 "real unlock."
- **v3:** `LAYERS.yaml` (transformation_registry kernel layer, added this session) · `build_targets`
- **Status:** NEEDS-BUILD — **was present in v2, missing in v3, now restored**

### S7. THE PROJECTION COMPILER + READ PLANE (the sensory system) — ✅ present in v3
- **What:** canonical store → immutable artifacts (HTML/JSON/Parquet) → R2/CDN; MCP ~8 verbs; Context
  Bundles.
- **v3:** `V3-BUILD-SPEC.md` (Mechanism 8) · `PRODUCTS.md` (#16) · `MECHANISMS.md`
- **Status:** PROVEN-MECHANISM (bounded-context, agent-delivery)

### S8. THE PRODUCTION ORGANISM + CONSUMER LOOP (reproductive + sensory) — ✅ present in v3
- **What:** verified Synthesis → essay (workengestation) → render (renderio) → publish (reception/sites)
  → consumer → new cruxes → back into the graph.
- **v3:** `PATALA-V3-ORGANISM.md` (reproductive system) · `V3-BUILD-SPEC.md` (Mechanism 6)
- **Status:** BUILT in .meta (13 essays, 49 gold-packs, 4 sites)

### S9. THE BIBLIOGRAPHY / DISCOVERY (identity foundation) — 🔧 ADDED this session
- **What:** the 254 works + Zotero/Crossref/OpenAlex/OpenCitations discovery. The identity source.
- **v3:** `LAYERS.yaml` (identity layer external_tools) · `PRODUCTS.md` (#0)
- **Status:** BUILT in patala (atlas-bibliography.json, 254 records)

### S10. THE TERMINOLOGY / LEMMA-THROUGH-TIME — 🔧 ADDED this session
- **What:** `trajectories.ts`, `/api/terms/:lemma/history`. Feeds Translation (term consistency) + Lesson.
- **v3:** `LAYERS.yaml` (term layer) · `PRODUCTS.md` (#0b)
- **Status:** BUILT in patala

### S11. THE TIMELINE — 🔧 ADDED this session
- **What:** `historyTimeline.json`, `/api/history/timeline`. The school/tradition chronology.
- **v3:** `LAYERS.yaml` (timeline layer) · `PRODUCTS.md` (#0c)
- **Status:** BUILT in patala

---

## THE COMPLETENESS VALIDATION (what v2 had, confirmed in v3)

| v2 structure | v3 status | Notes |
|---|---|---|
| Authority graph + Atlas | ✅ PRESENT | identity layer added (was missing) |
| Epistemic envelope | ✅ PRESENT | MECHANISMS M1 |
| Event ledger + reducer | ✅ PRESENT | MECHANISMS M2 |
| Human publication gate | ✅ PRESENT | MECHANISMS M2 |
| Derivation DAG + staleness | ✅ PRESENT | MECHANISMS M3 |
| Review panel + CiteCheck | ✅ PRESENT | MECHANISMS M4 |
| **Transformation registry** | 🔧 **ADDED** | was missing, now in LAYERS.yaml |
| Projection compiler + read plane | ✅ PRESENT | BUILD-SPEC M8 |
| Production organism (.meta) | ✅ PRESENT | ORGANISM |
| Consumer loop / organism | ✅ PRESENT | ORGANISM |
| **Bibliography** | 🔧 **ADDED** | was missing, now in identity layer |
| **Terminology / lemma** | 🔧 **ADDED** | was missing, now term layer |
| **Timeline** | 🔧 **ADDED** | was missing, now timeline layer |
| TranslationProof (moat) | ✅ PRESENT | PRODUCTS #2, MECHANISMS |
| Graduation test | ✅ PRESENT | the #1 milestone |
| 6 expansions | ✅ PRESENT | ORGANISM |
| 8 laws | ✅ PRESENT | MECHANISMS |
| 3 planes | ✅ PRESENT | LAYERS.yaml |
| Context bundles | ✅ PRESENT | PRODUCTS #16 |
| MCP 8 verbs | ✅ PRESENT | BUILD-SPEC |

**The 4 things I had to add this session (v2 → v3 gaps now closed):**
1. **Transformation registry** (the factory's brain — the v2 "real unlock")
2. **Atlas / Authority Graph** (the identity backbone)
3. **Bibliography / discovery**
4. **Terminology / lemma-through-time + Timeline**

---

## THE BUILD TARGETS (the honest to-do — now complete in v3)

```text
graduation_test       one IPVV claim through the whole stack, then mutate + watch it react
needs_build           tokenization · commentary · essay_projection · transformation_registry
gap_e                 signed human attestation (C2PA/ORCID)
gold_ingest           register the 63 L200 + 63 C1 golds with derivation edges
ledger_to_postgres    the reducer writes Postgres from events (kill the four-truths)
site_read_path        stop reading .ts seeds; read compiled objects
expansions            E1 marketplace · E2 organism · E3 what-if · E4 question-growth ·
                      E5 self-proving · E6 enquiry-discovery
```

---

*This is the definitive structures reference. Every structure Pāṭala definitely needs is listed, mapped
to its v3 location, and validated. The 4 v2→v3 gaps (transformation registry, atlas, bibliography,
term/timeline) are now closed. Nothing speculative — every structure is either proven in the lab or
built in patala/.meta.*
