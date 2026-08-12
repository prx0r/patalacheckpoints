# WHAT'S NEXT — close the open threads, build the recommendation layer

*2026-08-12. The open threads we never closed, and the concrete next builds for Pāṭala. Written
concise because the context is tight. Each item names the gap, the build, and who owns it.*

---

## 1. OPEN THREADS WE NEVER CLOSED

| Thread | Status | What's missing |
|---|---|---|
| **The 6 downloaded IPV/IPK sources** | files on disk in sanskritree, IPK/Vivṛti registered in bibliography + spines — **but the IPV (Vimarśinī) + 1921 scan are NOT registered** | register them as hub/resources + wire into the IPVV context (root kārikā + Vṛtti + IPV parallel beside the passage) |
| **Related-texts / "similar sources" recommendation** | **never built** | the Netflix-style rail: given a passage/work, recommend the root / parallel / commentary / opposing / scholarship |
| **Comparative matrix** | spec'd (`SPEC_COMPARATIVE_PUSHING.md`) but no data | `comparative.ts` + `/api/comparative` + first seed run |
| **The argument truth-packet** | spec'd, not built | the `pt:argument:` schema + `/verify-argument` + one worked example |
| **L200 → graph annotations** | L200 files exist (65), not ingested into the graph | L200 decisions/MT as annotations |
| **PARALLELS** (cross-text witnesses per theme) | not built | the comparative evidence layer |
| **IPVV 1.5.11 vs the 49-passage store** | 1.5.11 is a separate hand-authored unit; the store is chunk-level | reconcile — the 49 store is the canonical substrate; 1.5.11 is the rich exemplar |

---

## 2. THE RECOMMENDATION LAYER (the biggest missing product feature)

**The idea:** given any passage or work, recommend the related texts — exactly the "Netflix but for
related works" you described. Deterministic first (the relations graph + spines already have the
data), then ML-similarity later.

### 2.1 Deterministic related-rail (ship first — data already exists)

Given a work or passage, return a ranked rail:

```
RELATED for IPVV 2.4 (the reflexion claim)
  · IPK 1.5.11            (ROOT_TEXT — the kārikā it comments on)      ← via resolve/spines
  · IPV (Vimarśinī)       (parallel commentary on the same kārikā)    ← via the spines
  · Tantrāloka            (DOCTRINAL_PARALLEL — the same doctrine)     ← via the relations graph
  · the Buddhist source   (OPPOSING_POSITION — the opponent)           ← via source-layer
  · Ratié, Otherness      (SCHOLARSHIP — the adjudicator)              ← via the bibliography
```

Ranking rule: **relation type × confidence × shared terms**, not flat tags. This is deterministic
and uses the existing `relations.ts` + `canonical-spines.ts` + `bibliography`.

**Build:** `/api/recommend?work=<id>` + `/api/recommend?passage=<id>` + an MCP tool
(`recommend_related`). Data: a `data/corpus/recommend.ts` that assembles the rail from the spines +
relations + hub. Cheap, high-value, in Agent-2's lane.

### 2.2 Passage-level recommendation (the "because you read X")

The passage-level version: "Because you read IPVV 2.4 (reflexion)…" → next passage in the argument
(CONTINUES_ARGUMENT), the root kārikā, the parallel, the opponent. This is the frozen integration
build-order's "related rail" step. Uses the passage C1's `see_also` + RELATED + shared terms.

### 2.3 ML-similarity later (Agent-1's lane)

Once the embedding index exists (the ML plan's Q2/Q3), add semantic similarity ranking over the
deterministic rail — the rail is the curated seed; embeddings refine it. Do NOT build this before
the deterministic rail.

---

## 3. THE DOWNLOADED SOURCES — what we were going to do

The 6 IPV/IPK sources were acquired to **anchor the IPVV against the root kārikā + Vṛtti + the
parallel Vimarśinī**. The plan was: wire them into the **context pack** so each IPVV passage shows
its root text beside it. That's still open:

| Source | Role | State |
|---|---|---|
| GRETIL IPK+Vṛtti (`gretil_utipk_pu/au.txt`) | **root kārikā + Vṛtti** the IPVV comments on | on disk; bibliography has IPK; **not wired into the passage context** |
| GRETIL IPV (`gretil_ipv_clean.txt`) | the **parallel Vimarśinī** (Abhinava's shorter) | on disk; **not registered as a hub/resource** |
| Torella IPK (text + pdf) | critical ed. + EN | on disk; bibliography has it |
| 1921 IPV scan | historical citation | on disk; not usable as text (front-matter OCR) |
| Pandey Bhāskarī III (EN IPV) | comparison only | on disk; bibliography has IPV w/ Bhāskarī |

**The build:** (1) register GRETIL IPV + the scans as resources/crosswalks in the bibliography; (2)
wire IPK+Vṛtti + IPV into `/api/context/passages/:id` so each IPVV passage shows its root kārikā +
Vṛtti + IPV parallel (the "context alignment" step from the dev plan). This is the transformative
IPVV-scholar feature and it's deterministic (the mapping is the spines + source ranges).

---

## 4. THE PRIORITY (what to build next, in order)

Given the ML agent is on Q1–Q3 (benchmark/tokenizer/baselines), my lane's highest-value closes are:

1. **The deterministic related-rail** (`/api/recommend` + MCP) — the biggest missing product feature;
   reuses existing data; gives every passage/work a recommendation rail.
2. **Context alignment** — wire IPK+Vṛtti+IPV into `/api/context` so each IPVV passage shows its
   root text. Closes the downloaded-sources thread.
3. **Comparative matrix** — `comparative.ts` + `/api/comparative` + first seed run (feeds Agent-1's
   Q5/Q6).
4. **Argument truth-packet schema** + `/verify-argument` + one worked example (the Q4 slice).

These are all in my lane, all deterministic, all build on the existing substrate, and none collide
with the ML agent's benchmark/retrieval work.

---

## 5. The recommendation doc — write it as the product spec

Create `docs/api/recipes/recommend-related.md` (or a `SPEC_RECOMMENDATION.md`) that specifies the
related-rail: ranking rule (relation × confidence × shared terms), the deterministic source (spines
+ relations + hub + C1 see_also), the passage vs work variants, and the later ML-similarity
refinement. This is the concrete "how do we recommend similar sources" answer.
