# PĀṬALA V3 — THE MECHANISMS (the exact machinery, from the mastered lab)

*2026-08-14 · status: THE MECHANISM SPEC · the actual, load-bearing mechanisms of the Verified Epistemic
OS (from `MASTER-KNOWLEDGE-BASE.md` + `lib/` + the experiments), each with its core mechanism, its
invariant/gate, and the exact algorithm. This is the depth behind `LAYERS.yaml` (v3) — not just what each
kernel is, but HOW it works and what makes it honest.*

---

## THE 5 ARCHITECTURALLY LOAD-BEARING MECHANISMS (the ones that make the whole thing real)

### M1. THE EPISTEMIC CEILING INVARIANT — the honesty law
**Kernel:** `lib/epistemic.py` · **Proof:** validate-stack (0 violations across the real graph)

> **A derived object's authority may never exceed what its parents' evidence legitimately supports.**

The mechanism that keeps the graph from becoming a hallucination dump. Every object carries an
`EpistemicEnvelope` (the 4-axis Authority: generation · evidence · review · publication) with a
`projection ceiling ≤ parent` invariant. A machine-proposed claim can never claim to be
scholar-corroborated just by being derived.

**The invariant:** `projection_ceiling(child) ≤ allowed_projection(parents)`. If violated, the graph is
lying — the test fails.

### M2. THE HUMAN PUBLICATION GATE — only humans make truth
**Kernels:** `review.py` (herdr reducer) · `organism_loop.py` · `agent_delivery.py` · `evolve.py`

> **Agents propose. Only humans authorize canonical truth.**

The state machine: `state + event/evidence → deterministic reducer → next state`. Nothing promotes
without evidence; only the human transition can reach `ADJUDICATED`. This is why the organism is
"agents propose, humans adjudicate" — the anti-theatre core made mechanical.

### M3. THE DAG STALENESS / BLAST-RADIUS — the self-maintaining property
**Kernel:** `lib/staleness.py` · **Proof:** validate-layer03-05 (PHYSICS retraction → FREE_WILL)

> **A source change flags every downstream object stale, and computes the rebuild order.**

The dependency graph is simultaneously correctness, staleness propagator, and rebuild scheduler. RKA
blast-radius: retracting one premise flags all downstream layers (real test: PHYSICS retraction flags
the FREE_WILL argument). This is what makes the organism self-maintaining — nothing silently goes
stale, nothing recomputes unnecessarily.

### M4. THE REVIEW REDUCER + ANTI-GROUPTHINK PANEL — evidence-gated promotion
**Kernel:** `lib/scholar_review.py` · **Proof:** cross-review + review-bias (37.1% bias survived)

> **A deterministic reducer promotes only on evidence; a panel resists groupthink.**

Adversarial panel: N independent reviewers debate, a judge delivers the verdict. Anti-groupthink:
dissent is reported, never forced into consensus. CiteCheck: every citation verified, phantom citations
flagged. Bias-robust: 37.1% reviewer bias survived the audit — the mechanism works even when reviewers
are biased.

### M5. THE EDUCATION / ORGANISM MOAT — wrong-answer → known-neighbor
**Kernels:** `education.py` · `pedagogy.py` · `organism.py` · `organism_loop.py`
**Proof:** education-organism + pedagogy + organism-loop (8/8, 7/7, 10/10)

> **A learner's wrong answer maps to a KNOWN epistemic neighbor, and the pedagogy targets the weakest
> skill.**

The education moat: wrong answer → the known misconception graph (not a generic "try again"). Pedagogy
runs a mastery reducer targeting the weakest skill. The organism loop (10-stage consumer→research
machine) closes the flywheel: learner confusion → reveals source ambiguity → source-repair → re-teach.
This is unscrapeable + self-improving — the rarest moat.

---

## THE 7 ALGORITHMS (the exact retrieval/reasoning machinery)

| Algorithm | arXiv | Status | The exact mechanism |
|---|---|---|---|
| **PathRAG** | 2502.14902 | ⭐ IMPLEMENTED (`retrieval.py`) | flow-based pruning: `S(vi)=Σ α·S(vj)/|N(vj)|, α=0.7`; path reliability; ascending-reliability prompting |
| **HippoRAG** | 2405.14831 | ⭐ IMPLEMENTED | Personalized PageRank (PPR); **hub-bias finding documented** |
| **KG2Code** | 2607.22652 | ⭐ IMPLEMENTED (`query.py`, **Bet 2**) | KG→executable code DSL: `resolve/neighbors/path/evidence` |
| **ToG-2** | 2407.10805 | GAP | alternating graph + context retrieval (adopt into trace/investigate) |
| **SubgraphRAG** | 2503.09287 | GAP | smallest useful subgraph (combine with bounded-context) |
| **GFM-RAG** | 2509.24276 | GAP | graph foundation model (`export_gfm_graph()` interop) |
| **HyperGraphRAG** | 2505.07426 | GAP (**Bet 1**) | n-ary/hypergraph structure (keep Argument non-flat) |

**Only 3 of 7 are coded** (PathRAG/HippoRAG/KG2Code). **Bet 1 = HyperGraphRAG** (the argument graph must
stay non-flat — n-ary relations). **Bet 2 = KG2Code** (executable queries, promoted to `lib/query.py`).

---

## THE KERNEL INVARIANTS (what makes each of the 17 kernels honest)

| Kernel | Invariant / gate |
|---|---|
| `epistemic.py` | projection ceiling ≤ parent (the honesty law) |
| `schema.py` | every object validates against one schema (kills divergence) |
| `review.py` | nothing promotes without evidence; only human → ADJUDICATED |
| `scholar_review.py` | citation must resolve; blocking finding blocks |
| `staleness.py` | retraction flags all downstream stale |
| `query.py` | deterministic verifiable trace (KG2Code) |
| `retrieval.py` | (HippoRAG is hub-biased — known finding) |
| `translation.py` | publication blocked on any hard-dim fail (the moat) |
| `certificate.py` | factors from validated subsystems (compounding) |
| `discovery.py` | value = load-bearing × weak-verified × contested (Research Value Score) |
| `education.py` | education is a projection of the graph |
| `organism.py` | consumer = sensor for comprehension failure |
| `organism_loop.py` | agents propose; human_authorize = only path to truth |
| `pedagogy.py` | targets weakest skill (mastery reducer) |
| `evolve.py` | only better+distinct candidates promote (MAP-Elites, Pareto incl. cost) |
| `agent_delivery.py` | human gate for canonical truth |
| `essay_ingest.py` | essay = derivation input, not dead prose |

---

## THE 8 LAWS (the organism's constitution — deeper than the 3 planes)

```text
1  epistemic honesty        (eigenius + envelope) — a claim is HOW it's known
2  deterministic promotion  (herdr) — reducers gate, not agents
3  self-maintaining staleness (RKA) — nothing silently goes stale
4  temporal truth           (graphiti + Merkle) — history is replayable
5  publishable provenance   (PROV-K) — every claim traces to source
6  executable retrieval     (KG2Code + PathRAG + HippoRAG) — query the graph, not prose
7  reactive documents       — source change → prose recompiles
8  verified self-knowledge  — the system proves WHY it is what it is
```

---

## THE 6 UNCONSIDERED FRONTIERS (the future the lab already sees)

| # | Frontier | What it is |
|---|---|---|
| A | OS-dreams-in-public | the system reasons openly |
| B | counterfactual-engine (whole-graph) | what-if across the entire graph |
| C | cross-organism-learning | learner error → source-repair |
| D | verifier-as-rival | a hostile debater verifies |
| E | temporal-scholarship | scholarship across time |
| F | epistemic-provenance-of-the-system-itself | the system proves its own construction |

---

## THE HONEST STATE (from STATE.yaml)

**Every layer VALIDATED except 07-surfaces (DISCOVERED).** "VALIDATED = prototype, not production." The
gaps (A-G):
- **A context-paging** — NOT built
- **B execution-branching** — ✅ BUILT
- **C deterministic-replay** — ✅ BUILT
- **D content-addressed run-traces** — NOT
- **E signed human attestation** — **NOT (critical before marketplace)** — agent_delivery uses plain
  `human_authorize()`
- **F workspace isolation** — NOT
- **G local-first nodedb** — cloned, NOT

**The theatre truth:** 24 PROVEN on real data / 26 PROVEN-MECHANISM (synthetic) / 0 UNPROVEN. The
data-grounded tests: validate-stack, validate-layer03-05, validate-essay-ingest, pathrag, hipporag,
kg2code, crux-compiler. **The fix = the graduation test.**

---

## THE ROADMAP (the exact priorities)

- **P0 — the graduation test** (the #1 next milestone): ONE claim end-to-end on real evidence (the
  two-stage free-will as an IPVV stand-in), then MUTATE a premise and verify the whole organism reacts
  (staleness → reactive essay → pedagogy → signed re-release). `validate-stack.py` starts it.
- **P1 — close gaps:** E signed attestation (before marketplace) · A context-paging · the 3 remaining
  adapters (openalex, s2orc, xaif).
- **P2 — deepen:** LOGICVID gold → enquiry graph · enquiry-discovery → pedagogy · MAP-Elites on real
  translation · essay-ingest on a full source.

---

## THE RESOLVE CHAIN (how an agent finds anything in the lab)

```text
Question → TRACEABILITY-MAP.md (vision+layer) → KERNELS-INDEX.md (kernel) → the validating
experiment (scripts/) → the source repo (ecosystem/ or arXiv) → the spec (specs/) → the doc (docs/)
```

**The 5 most important things to know:**
1. `validate-stack.py` is the only real end-to-end pipeline
2. the epistemic ceiling invariant is the load-bearing law
3. the human publication gate is everywhere
4. staleness blast-radius is the self-maintaining mechanism
5. the graduation test is the #1 next step

---

*This is the mechanism depth for v3 — the exact machinery behind the layer contract. The 5 load-bearing
mechanisms (epistemic ceiling, human gate, staleness, anti-groupthink review, education moat) are what
make the organism honest and real. The algorithms (PathRAG/HippoRAG/KG2Code) are the retrieval/reasoning
core. This is what a from-scratch build implements — see `LAYERS.yaml` (v3) for where each lives.*
