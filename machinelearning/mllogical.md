# ML LOGICAL — the argument pipeline, made ML-ready with formal structures

*2026-08-12. **Agent 1's (ML) read of the other agent's logical-arguments/hub work** — and what makes it
genuinely *machine-learnable* rather than just tracked. This is the ML-side companion to
`SPEC_LOGICAL_ARGUMENTS_GOLD.md` and `SPEC_PUSHING_METHOD.md`. It does NOT rewrite those specs; it makes
the structures they describe **formal enough to learn over**.*

---

## 0. The honest starting point

The other agent's pipeline is correct in spirit and already tracked:

```
PUSHING (finds a tension, quotes passages)
  → FORMAL LOGICAL ARGUMENT (premises/inference/conclusion, tied to passages)
  → TRUTH ENGINE (PROVED / OUTSIDE_FORMAL / HOLLOW)
  → ESSAY (every claim cites evidence)
  → LEARNING
  → back to PUSHING
```

The hub (`data/corpus/hub.ts`) tracks all of this per source. **The architecture is right.** What's
missing for ML is that the objects are mostly **prose + file pointers** — the argument shape is described
in the spec (§3) but not enforced as data. That's the gap: **a described schema is not a machine schema.**

Two hard truths the other agent's work implicitly assumes but hasn't closed:
1. **The truth engine is a demo** (`nyayaengine.py` = "simulated_lean_check", `nyaya_claims.json` = 817
   bytes). "PROVED in Lean" is aspirational until a real Lean/Pantograph link exists. We must NOT build ML
   on a simulated oracle.
2. **The argument object exists as a spec, not as data.** Until `pt:argument:` records exist with
   structured premises/inference/conclusion, the "compounding pipeline" is a tracking spreadsheet, not a
   learnable corpus.

This document turns the spec into **enforced, addressable, learnable** structures.

---

## 1. Make the argument object a real data type (not a spec)

The spec's §3 shape is good. Enforce it as a typed record in the graph so ML can consume it. This is the
single most important change:

```ts
// Argument — the formal, passage-anchored logical argument (the gold object)
interface Argument {
  id: string;                    // pt:argument:<work>:<slug>
  work_id: string;
  title: string;
  kind: "reductio" | "analogy" | "identity" | "entailment" | "decomposition";
  premises: { text: string; passage_ids: string[] }[];
  inference: "MODUS_PONENS" | "MODUS_TOLLENS" | "DILEMMA" | "ANALOGY" | "ENTAILMENT" | "DECOMPOSITION";
  conclusion: { text: string; passage_ids: string[] };
  tension_id: string;           // the PUSHING question it resolves
  status: "MACHINE_DRAFT" | "REVIEWED" | "PROVED" | "OUTSIDE_FORMAL" | "HOLLOW";
  proof?: { engine: "nyaya" | "lean"; verdict: "PROVED" | "OUTSIDE_FORMAL" | "HOLLOW"; trace: string };
  provenance: string[];         // resolved passage ids
}
```

**Why enforced-typed matters (the ML payoff):**
- `inference` as a closed enum → ML can **classify the argumentative move** (a PATALA-STRUCTURE task:
  "which logical operation does this argument perform?").
- `passage_ids[]` on premises/conclusion → the **retrieval + support** supervision: an argument premise
  *asserts* a passage supports it — that's a claim→support gold pair.
- `kind` as a closed enum → **argument-motif discovery** (the curriculum's relation-motif idea): "show
  every reductio in the IPVV."
- `status` + `proof.verdict` → the honest supervision signal separating *proved* from *bounded* claims.

---

## 2. The truth engine must be an honest, verifiable service — or it's not a floor

The demo `simulated_lean_check()` is dangerous for ML: if we learn "PROVED" from a simulator, we bake in
its errors. The discipline:

- **Until a real Lean/Pantograph link exists, the verdict is a *label*, not a proof.** Record it as
  `proof.verdict` but keep `proof.engine = "manual"` and `status = "REVIEWED"`, never "PROVED".
- **The real floor is the deterministic check that a premise's passage_ids actually resolve** (already
  have `/api/resolve`). That is the machine-checkable part today. Build ML on *that*; the Lean verdict is
  a future enrichment.
- **Concretely:** add a `/verify-argument` service (Agent 1's lane) that deterministically checks, for any
  argument:
  - every `premise.passage_ids[]` and `conclusion.passage_ids[]` resolves via `/api/resolve`;
  - no premise/conclusion is empty;
  - `inference` and `kind` are valid enum values;
  - `status` is consistent with `proof.verdict` (a "PROVED" status without a `lean` trace is a flag).
  This is the **structural floor** — same philosophy as `verify-claim-structure`, extended to arguments.

---

## 3. The argument-corpus tasks (what ML can learn, once §1 + §2 exist)

With typed arguments + a structural verifier, four concrete ML tasks become possible:

| Task | Suite | Input → output | Baseline to beat |
|---|---|---|---|
| **Argument-move classification** | PATALA-STRUCTURE | argument prose → `kind`/`inference` label | majority-class |
| **Premise → support retrieval** | PATALA-EVIDENCE | a premise's text → the passage(s) that support it | BM25 |
| **Argument motif discovery** | PATALA-STRUCTURE | the argument graph → recurring operation patterns | graph community detection |
| **Boundary detection** (which claims are PROVED vs bounded) | PATALA-EVIDENCE | argument text → PROVED / OUTSIDE_FORMAL / HOLLOW | — (needs labels) |

The **premise→support retrieval** is the most immediately valuable and the most honest: the other agent's
work already *asserts* premise↔passage links, so we have gold pairs without inventing any. That's
exactly the "derive fixtures from real structure, don't invent labels" principle I used for the
see_also tasks.

---

## 4. The hub is a graph — make it queryable, not just listable

`hub.ts` is a flat list of outputs per work. For ML it should be a **graph**:
- `pt:hub:<work>:<kind>:<slug>` nodes, with typed edges:
  - `TENSION_OF` (argument ↔ PUSHING question)
  - `DERIVES_FROM` (essay ↔ argument; learning ↔ essay)
  - `CITES` (any output ↔ passage_ids)
- Then "the arguments that bear on recognition" becomes a **graph query**, not a filter.

**Minimal change:** keep the list API, add a `relationships` field per HubOutput + a graph traversal. This
is cheap and makes the hub the substrate for motif/trajectory tasks instead of a catalog.

---

## 5. The compounding loop, made measurable

The other agent's loop says "it compounds." To *prove* it compounds (ML-valuable), attach a metric at each
step:
```
PUSHING       # tensions found
  → ARGUMENT  # premises that resolve · % with all passages resolvable
  → PROOF     # PROVED / OUTSIDE_FORMAL / HOLLOW counts (honest)
  → ESSAY     # claims with resolved evidence
  → LEARNING  # lessons
```
Track these as coverage metrics over the corpus (the `PLATFORM_` "scholarly coverage metrics" idea). Then
"compounds" is a number, not a slogan: *as we add texts, how many tensions→arguments→proofs→essays resolve
and cascade?*

---

## 6. The immediate concrete next steps (Agent 1's lane)

1. **Argument data type** — add `Argument` to the graph types (`data/corpus/graph.ts` is Agent 2's, so
   this lives in the ML lane as `patala_ml/argument.py` reading an `arguments.jsonl` Agent 2 emits, OR as
   a proposed schema handoff to Agent 2). **Decision point: who owns the `Argument` type.** Recommend a
   handoff: Agent 1 proposes the typed schema (this doc), Agent 2 emits the real records from the hub +
   research-library, Agent 1 consumes.
2. **`/verify-argument` structural floor** — deterministic (resolves, non-empty, valid enums, status
   consistency). Cheap, over existing `/api/resolve`.
3. **Premise→support task** — derive from the REAL hub arguments (the reflexive-debate, the Ñāṇavīra
   proof): premise text → its cited passages. Run BM25 baseline. This is the first learnable gold from
   the logical pipeline.
4. **Argument-move classification** — once ~10–20 typed arguments exist, a small classifier vs
   majority-class. Low priority until the corpus is bigger.
5. **Worked example end-to-end (the other agent's suggestion, ML-aware):** take one IPVV reflexivity
   tension → type it as an Argument → run `/verify-argument` → record the honest verdict (NOT a simulated
   Lean "PROVED") → the premise→support retrieval on it. This proves the loop with real data and no
   fabricated oracle.

---

## 7. Guardrails specific to the logical pipeline (for both agents)

- **Never learn "PROVED" from the simulated engine.** Until real Lean exists, treat verdicts as labels
  with `engine: manual` + `status: REVIEWED`. A fake oracle corrupts the supervision signal permanently.
- **Never treat an argument as an assertion Pāṭala stands behind until it's REVIEWED.** "AI proposes ≠
  Pāṭala asserts" applies to arguments exactly as to translations.
- **Keep the MT/IA discipline when arguments cite passages** — an argument premise is an interpretive
  assertion (IA), not a translation decision (MT). Don't let the logical layer silently upgrade an
  interpretive reading to a proof.
- **The premise→support gold is only as good as the passage_ids resolve.** Verify every one.

---

## 8. Bottom line (the ML take)

The logical-arguments pipeline is the right high-value target — **the most *computable* layer of the
whole vision** (formal premises → inference → conclusion is the closest thing to a learnable structure
in the corpus). But it becomes ML-ready only when:

1. the argument object is a **typed, enforced record** (not a spec), with `kind`/`inference` as closed
   enums and `passage_ids` on every premise/conclusion;
2. the truth engine is **honest** (no simulated-oracle "PROVED"); the deterministic floor is
   `/verify-argument` (resolves + valid enums + status consistency), and Lean is a future enrichment;
3. the hub is a **queryable graph** (typed edges), and the compounding loop is **measured** (coverage
   metrics), not asserted.

Then the pipeline yields the most valuable ML supervision Pāṭala can produce: **premise→support pairs
from real scholarship** — gold we didn't have to invent, derived entirely from the other agent's work.
That is the flagship ML win of the logical layer, and it's available the moment the `Argument` type is
real and verified.
