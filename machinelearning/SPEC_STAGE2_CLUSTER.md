# SPEC — STAGE 2: CLUSTER all 63 IPVV C1s (the machine-proposal layer)

*2026-08-12. The next build in the logical order (LOGICAL-ORDER.md): scale the hybrid-graph pilot from
25 to all 63 C1s, producing overlapping communities (the machine proposals that themes then adjudicate
editorially). Owned by Agent 1 (ML). This spec is the plan; the code + tests are built in
`machinelearning/research/patala_ml/`.*

---

## 1. The goal

Take the 63 C1 read/ renderings (the published passages' C1 bodies) and produce **overlapping
communities** from the **hybrid relation graph** — the same mechanism the pilot proved on 25 C1s, scaled
to all 63, production-grade and testable.

```
63 C1s
  → hybrid relation graph (See also + shared KEY TERMS + sequence)
  → community detection (Louvain, overlapping)
  → candidate neighborhoods (machine proposals)
```

## 2. The hybrid relation graph (from the pilot's corrected design)

**The two structured signals** (NOT shared body-words — the pilot proved those over-connect = noise):
1. **Curated `See also` edges** — the C1s' explicit relational links (from `c1_source.related_passages`
   / the `See also` field).
2. **Shared KEY TERMS** — two C1s citing the same technical lemma.

Edge weight (following the pilot):
```
w = w_seealso·(1.0 if linked) + w_terms·jaccard(key_terms)
```
with the pilot's default weighting (curated edges dominate; shared terms as support).

## 3. Community detection

- **Louvain** (python-louvain) over the graph — the pilot favored graph community detection over
  HDBSCAN because the C1s are already relation-linked.
- **Overlapping:** a C1 can belong to several communities. Louvain is non-overlapping by default, so we
  get overlap by **multi-assigning borderline nodes** (a node whose top-2 community memberships are
  within a threshold is assigned to both) — matching the "themes overlap, not partition" rule.

## 4. The output — a ClusterProposal

```ts
interface ClusterProposal {
  cluster_id: string;        // e.g. CL-1
  member_c1_ids: string[];   // the C1s
  strengths: Record<string, number>;   // membership strength per member
  edge_evidence: { a: string; b: string; type: "see_also" | "shared_term"; weight: number }[];
  // why is C1-X in this cluster? → answerable from edge_evidence
}
```

## 5. Validation (the tests)

| Test | What it proves |
|---|---|
| **graph-connectivity** | every C1 is in ≥1 cluster; no isolated orphans (except genuine singletons) |
| **overlap-preserved** | the known multi-theme C1s (V2O, V2L) appear in ≥2 clusters |
| **evidence-trace** | every membership has a readable edge_evidence (no member without a justifying edge) |
| **known-cluster-recovery** | the pilot's known clusters (memory, causal, pramāṇa, vimarśa) are recovered |
| **determinism** | same input → same clusters (fixed seed) |

## 6. The acceptance test (what "done" means)

```
Given the 63 C1s, the clusterer produces overlapping communities such that:
  · ≥1 member per cluster, evidence-traced
  · V2O/V2L appear in ≥2 clusters (overlap)
  · the known memory/causal/pramāṇa/vimarśa neighborhoods are recovered
  · reproducible (fixed seed)
```

---

## 7. What feeds this (dependencies)

- **C1 bodies + key terms + see-also:** already loaded by `patala_ml/corpus.py` (PassageDoc has
  `c1_body`, `key_terms`, `see_also`).
- The corpus is the **49 published passages**; their C1s are the 63 rendering — the clusterer uses the
  C1 id (chunk-derived) as the node id, so it maps back to passages for resolve.

## 8. What this feeds (downstream)

- **Stage 3 — THEMES:** the editor accepts/merges/splits these proposals into named themes.
- **Stage 4 — ARGUMENTS:** each theme's member C1s become an argument's premises.
- **The retrieval/eval lane:** cluster assignments are a new relation feature + a PATALA-STRUCTURE task.

## 9. Non-goals (keep it scoped)

- NOT building the THEMES editorial layer (that's the human-adjudication step, later).
- NOT touching the Pāṭala app (`data/corpus/`, `app/`). This is pure ML research in my lane.
- NOT optimizing beyond Louvain for now — graph-ML embeddings are a later, benchmark-gated experiment.

---

## 10. BUILD RESULT (verified 2026-08-12) — the V2/V3-vs-V1 finding

Building and inspecting the actual output revealed a **genuine, useful structural finding**:

**The V2/V3 C1s cluster cleanly into the recognized IPVV themes** (V2/V3-only scope):
| Cluster | Members | Theme |
|---|---|---|
| CL-0 | V2A, V2B, V2C | Memory / self-cognition |
| CL-1 | V2D, V2E, V2F, V2G | Jñānaśakti / external-cognition / the Buddhist |
| CL-2 | V2H, V2I, V2J, V2K | Vimarśa / language |
| CL-3 | V2L, V2O, V2P, V2R, V2S + V3F, V3I | Order-less support / unity |
| CL-4 | V3C, V3D, V3E, V3I, V3J, V3K, V3L, V3M | Pramāṇa / cosmology |
| CL-7 | V3F, V3N, V3O, V3P | Grace / liberation |
| CL-8 | V3G, V3H | Causality |

**The V1 block (28 C1s, the upoddhata/purvapaksa dialectic) does NOT cluster usefully** — it's a
dense commentary cross-reference block where the shared see_also graph mega-clusters (13–16 member
noisy groups). Tuning the shared-term threshold doesn't help (it only adds generic-V1 connections).
**The honest fix:** the emitter (`experiments/emit_clusters.py`) clusters V2/V3 for themes and flags
V1 for **editorial partitioning** — over-tuning the graph to force V1 would produce fake structure.

**Deliverables:** `data/published/ipvv/clusters.json` (the V2/V3 proposals, mapped, with coherence +
overlap + edge evidence) + `clusters.report.txt` (the editorial report). 14/14 cluster tests pass.

**This is the "actually useful" output** — clean V2/V3 themes an editor can accept/merge, with the
V1 block honestly deferred rather than force-clustered.
