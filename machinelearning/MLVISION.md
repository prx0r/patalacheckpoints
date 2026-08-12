# PĀṬALA ML VISION — from layered scholarship to a self-improving scholarly intelligence

*2026-08-12. The big picture: how the ML strategy (`MLUSEINPATALA.md`), the corpus architecture
(`IPVV-STACK-INTEGRATION.md`), and the site vision (`NORTHSTAR.md`, `ENDGAME_SITE_SPEC.md`) compose into
one coherent thing — and how that thing becomes bigger than FoJin, bigger than any RAG/GraphRAG layer,
into an engine whose value compounds. Companion to the frozen `MLUSEINPATALA.md` (the *what-to-build*);
this is the *why-it-forms-a-whole-and-where-it-can-go*. **The concrete product it all serves — the
computable scholarly tradition with the epistemic gearbox, misconception maps, and concept journeys — is
`VISION-COMPUTABLE-TRADITION.md`; read that for what the machine ultimately renders.***

---

## 0. The thesis in one line

> **Pāṭala's edge is not better retrieval. It is that the corpus itself encodes critical scholarship as
> supervised data — so every generation layer (translation, commentary, theme, essay, lesson, and the
> "gen-z" renderings) is a *checked transformation* over evidence, not an LLM guess.**

FoJin made retrieval trustworthy (11% → 98% served-trustworthy via deterministic guards). That is the
floor. **The bigger-than-FoJin move is to make *the entire scholarly pipeline* — not just answers —
trustworthy, provenance-bound, and — most importantly — a *training signal*.** FoJin answers questions
about a canon. Pāṭala learns the *structure of scholarly reasoning itself* and can then reason about any
premodern text.

---

## 1. How it all works together (the machine)

The ML strategy and the corpus are the same machine seen from two sides.

### The one graph, many controlled projections
```
                       THE SCHOLARLY GRAPH (one source of truth)
  Sanskrit span · reading · decision · C1 · theme · claim · essay · lesson
                     (every node addressable; every edge typed + evidenced)

   EXPOSE (deterministic, free)         INFER (learned, benchmark-gated)
   /verify-quote  /verify-claim-structure   ColBERT retrieval · graph embeddings
   /trace-dependency  /find-counterevidence   theme discovery · entailment
   /resolve                                  Vertical Fidelity classifier
```

- **EXPOSE** is the deterministic floor: it never hallucinates, because it returns explicit edges
  already in the graph. It is the platform (the API/MCP surface any tool can call).
- **INFER** proposes; the benchmark gates it; **human review promotes it**; and once promoted it becomes
  *new explicit structure* — which the next INFER round then learns over. **The floor and the inference
  feed each other.** That closed loop is the self-improving engine.

### The loop (the flywheel)
```
evidence graph
   → deterministic EXPOSE services (always trustworthy)
   → ML INFER proposals (theme, parallel, entailment, counterevidence, simplification)
   → fixed benchmark + held-out test (empirical gate)
   → human review (measured: inter-rater, edit burden)
   → promoted structure back into the graph  (provenance preserved)
   → richer supervision for the next round
```
Each turn the graph gets denser and the supervision richer — and the benchmark stays fixed, so
improvement is *measured*, not felt.

---

## 2. How it achieves the vision we laid out

| Vision element | Where it is built | How ML completes it |
|---|---|---|
| **Reader is the product** (nextdev2) | `app/read/[work]/[locator]` — phrase-clickable, decisions, C1 toggle | C1 retrieval (Phase 3/4) lets the reader *find* related passages; late-interaction handles Sanskrit terms |
| **Reference Map / concept graph** (ENDGAME §4) | `data/atlas/concepts.ts` + term trajectories | graph embeddings + hyperbolic space put traditions/concepts in a learnable geometry; cross-work themes discover new edges |
| **Master Map / Workbook** (ENDGAME §2–3) | C1s + themes + argument maps | Vertical Fidelity guarantees the Workbook's simplification never distorts the C1/essay it derives from |
| **"Choose your depth"** (CRITICAL/C1/GUIDE/GEN-Z) | the stacked layers + `SPEC_EDUCATION.md` | the depth ladder IS the paired-transformation dataset; Vertical Fidelity is the check that each depth is faithful |
| **Provenance-preserving generation** (PLATFORM_…) | `/verify-*`, `/trace-dependency`, the DAG | the epistemic compiler catches *scope strengthening / attribution error / lost negation* across any generation |
| **The moat: verified graph, not GraphRAG** (NORTHSTAR) | the corpus + review graph | the benchmark + measured human review turn "expert-approved" into a *defensible, publishable dataset* |
| **Machine-access via MCP/API** (FoJin pattern) | `mcp/index.mjs`, the URNs | the EXPOSE services + themes/parallels tools make the graph callable by any AI |

---

## 3. The "this is it" flags — the items that were the real destination

Across the project several things were flagged as genuinely special. They are not features; they are the
**core of the bigger-than-FoJin claim**.

### 3a. The layered supervision is a new kind of dataset
The reviewer's framing, frozen: **Pāṭala is not making AI "understand Sanskrit better"; it is making
scholarly reasoning itself supervised data.** The chain
`source → reading → decision → commentary → theme → claim → pedagogy` is a supervision signal almost no
corpus has. FoJin has cross-canon *alignment*; Pāṭala has cross-*layer* derivation — a strictly richer,
more general object.

### 3b. Vertical Fidelity — the cross-domain benchmark
The depth ladder (`L2 → C1 → Theme → Guide`, plus the GEN-Z renderings) gives **controlled positive
pairs**, and the corruption set (NEGATION_LOSS, SCOPE_STRENGTHENING, CERTAINTY_INFLATION,
ATTRIBUTION_ERROR, BOUNDARY_ERASURE, AGENT_SWAP) gives hard negatives. This is *not* Sanskrit-specific:
**"does simplification preserve meaning across explanation depths"** is a general NLP problem. A clean
benchmark here is a contribution any lab can use — the piece that lets Pāṭala matter beyond the field.

### 3c. The σ-flip / felt-to-ground honest limit (the philosophical spine)
The IPVV work is anchored on a real philosophical limit: the felt→ground step is *argued, not closed*
(the universalization is the wager). **The ML layer inherits this honesty as a design principle** — the
epistemic compiler refuses to let a claim's scope exceed its evidence. The engineering enforces the
philosophy: no boundary-erasure, no attribution-error. That alignment — philosophy and provenance
agreeing — is what makes the whole thing cohere rather than being "a GNN on a canon."

### 3d. GEN-Z / education as the real product surface
The endgame treats the "how we teach it" layer (EDUCATION, `SPEC_EDUCATION.md`) as downstream of the
stack. **But the GEN-Z rendering is the *stress test***: if you can faithfully simplify the recognition
thesis for a teenager *without* losing the boundary ("this passage does not by itself prove universal
identity"), you have proven the whole pipeline preserves meaning. Education is not a bolt-on; it is the
**verification that depth-conservation works** — and the most human-facing proof of the system's value.

---

## 4. How this becomes bigger than FoJin

FoJin: trustworthy RAG over an aggregated Buddhist canon — retrieval + verification guards + MCP. A
finished, impressive *reader/answer platform*. **Pāṭala's ceiling is structurally higher**:

| | FoJin | Pāṭala (at full build) |
|---|---|---|
| Core object | aligned passages across canons | **layered scholarly derivation** (supervision) |
| Trust | citation guard → 98% served-trustworthy | **+ claim-support + cross-layer fidelity + provenance DAG** |
| Generality | Buddhist canon | **any premodern text** (the stack is tradition-agnostic) |
| Learnable asset | embedding index | **the derivation structure itself as training data** |
| Research output | an eval harness | **a cross-domain benchmark (Vertical Fidelity) + the supervision-dataset thesis** |
| Compounding | more aligned pairs | **more promoted scholarly structure → richer supervision → better inference** |

**The compounding difference:** FoJin's flywheel adds aligned pairs. Pāṭala's flywheel adds *promoted
scholarly structure* — which is both the product (verified graph) and the training signal (supervision).
Each expert-validated decision makes the next round of inference better. That is a **self-improving
scholarly intelligence**, not a corpus.

**Becoming the standard:** the real moat (NORTHSTAR) is *trusted collaborative standard adoption* —
stable IDs, crosswalks, validation histories, a scholar network. The ML layer amplifies this: a fixed,
public benchmark + measured inter-rater agreement + reproducible experiments is what makes institutions
and other AI systems *depend on* Pāṭala's verified graph rather than their own. **You become the layer
others build on** — the same way Crossref/OpenAlex became infrastructure, but with a supervised-reasoning
capability they don't have.

---

## 5. The trajectory (what "achieving + going beyond" looks like)

### Stage 1 — Trusted scholarship (now → Phase 2A)
Finish publication; benchmark suite; EXPOSE services. The site is verifiable; the API is callable;
FoJin-parity on trust. **Not yet differentiated — but the foundation.**

### Stage 2 — Supervised reasoning (Phases 3–5)
Retrieval + THEMES + claim-verification + **Vertical Fidelity** on real data. Now the corpus *learns*
scholarly reasoning. The Vertical Fidelity benchmark is published — a first external artifact.

### Stage 3 — Transfer (Phase 6+, cross-work)
Train on IPVV, transfer to a held-out work (Tantrāloka, Kubjikā, Krama). **This is the "bigger than the
source" moment:** if the learned *structure of reasoning* transfers to a text the model never saw, Pāṭala
is no longer about one canon — it is a **general engine for premodern philosophical text**. That is the
research claim that would matter.

### Stage 4 — The platform (the eventual ceiling)
The EXPOSE + INFER + benchmark + review stack is exposed as **first-class APIs and MCP tools** any
institution or AI uses. Pāṭala becomes the *verification + supervision infrastructure* for the field —
where FoJin is a destination, Pāṭala becomes **the rail the whole field runs on** (open commons +
paid reliability/compute, the NORTHSTAR economic thesis).

---

## 6. The five questions that stay true at every stage

```
Can explicit scholarly structure improve retrieval?
Can models discover relationships experts accept without erasing disagreement?
Can we detect when interpretation outruns source support?
Can we preserve semantic content moving from critical scholarship to beginner explanation?   ← GEN-Z
Can provenance improve reasoning reliability?
```

Any new ML idea must answer one of these (and name the benchmark + baseline). If it can't, it doesn't
get built. This keeps the vision from collapsing into novelty-chasing.

---

## 7. Bottom line

The ML strategy and the corpus are one machine: **EXPOSE the scholarship deterministically, INFER over
it under a fixed benchmark, promote via measured human review, and let the promoted structure enrich the
supervision.** That closed loop is what achieves the vision — the reader, the reference map, the
workbook, the depth ladder, the GEN-Z renderings all become *verified transformations over one graph*.

**Bigger than FoJin** because FoJin is trustworthy answers over a canon, while Pāṭala becomes
**self-improving scholarly intelligence over any premodern text** — with a cross-domain benchmark
(Vertical Fidelity) and a transfer result as the eventual proof. The philosophical honesty (the
felt→ground boundary) and the engineering honesty (the provenance floor) are the same discipline, and
that coherence is the thing no "applied GraphRAG" can copy.

The destination is not a bigger corpus. It is:
> **a machine that learns how scholarship reasons, and verifies every claim it lets out.**

---

## PROGRESS (2026-08-12) — the substrate is now real

The layered-supervision claim is no longer just the thesis; it is wired into Pāṭala:
- 49 IPVV passages published (lazy JSON) with **source + L2 + C1 (`verse_commentary[]`, V1
  multi-C1) + c1_source** — the multi-resolution ladder is machine-queryable.
- **THEMES exposed** (`/api/themes` + `get_themes` MCP) — deterministic proposals from shared
  technical lemmas across C1s.
- **The deterministic verification floor is live** (`/api/verify/{quote,claim-structure,
  trace-dependency,counterevidence}` + MCP tools) — "AI proposes ≠ Pāṭala asserts" is now machine
  access, not just a rule.
- Benchmark seed documented (`BENCHMARK_HANDOVER.md`) so the INFER phases start from real fixtures.

The vision's *projection-over-evidence* is now buildable on real data: ORIGINAL / READ / GUIDE /
STUDY / CRITICAL can each resolve to the same canonical passage.
