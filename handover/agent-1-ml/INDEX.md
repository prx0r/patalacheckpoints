# Agent 1 — ML/RESEARCH LANE INDEX

*The one living pointer for Agent 1's current state — done / in-progress / next. Update this as you work.
Append-only history lives under this folder; this file is the single "what is true right now" source for
the ML lane.*

> **LEADING CHECKPOINT DOC: `handover/CHECKPOINTS.md`** (the shared 5-checkpoint plan + 7 canonical
> contracts) + **`handover/agent-1-ml/CHECKPOINTS-ML.md`** (this lane's goals: CP0/CP2/CP3/CP4).
> Read those before the current-state below.

---

## Agent 1 = the WHOLE philosophical-intelligence lane (NOT a single experiment)

Agent 1's program is the full upward derivation — from corpus/C1 to a machine-readable
philosophical/research intelligence layer. ASPIC was one small CP4/CP5 experiment inside it (~5% of the
endgame). The real program:

```
CORPUS / C1 → RETRIEVAL → THEME/CLUSTER → PROPOSITION EXTRACTION → ARGUMENT RECONSTRUCTION
  → SEMANTIC ALIGNMENT → DIALECTICAL RELATIONS → FORMAL/NYĀYA/ASPIC EVALUATION
  → CRUX EXTRACTION → SYNTHESIS → SCHOLAR WORKBENCH / REVIEW
```

**The Agent 1 thesis:** *can we transform a textual corpus into an auditable graph of claims, arguments,
interpretations, disagreements and cruxes — while preserving exactly where interpretation entered?*

## Where Agent 1 stands (honest state table)

| Layer | State |
|---|---|
| CP0 benchmark infrastructure | **done** |
| CP2 retrieval | **partial** |
| CP3 clustering/themes | **partial — no accepted themes yet** |
| CP4 argument IR | **early but real** |
| Gold arguments | **model-critiqued, still scholarly candidates** |
| Automatic argument extraction | **not working yet** (proposition lexical F1 ~0.36, inference recovery 0) |
| Semantic alignment | **early / schema + fixtures** |
| Dialectical graph | **emerging from gold review** (RESPONDS_TO / ATTACKS / UNDERCUTS / …) |
| ASPIC adapter | **first pilot only** (proxy-supported; real-engine re-run OPEN) |
| Nyāya evaluator | **not properly exercised on reviewed IR** |
| Crux computation | **not built/validated** |
| Synthesis | **mostly future** |
| Workbench / Review | **future** |

## The Agent 1 roadmap (in order)

1. **Finish the five golds properly** — the model review forced real IR corrections (inference vs
   dialectical, grounding vs inference, `support_scope`, reconstruction commitment, warrant placement,
   ARG-003 demotion). ARG-002 v2 is the first clean case; 001/004/005 revised around the same discipline.
2. **Build the real argument extractor** — split into A proposition extraction / B argument
   reconstruction / C systematic interpretation (not one monolithic extractor).
3. **Return to CP3 themes/clustering** — machine clusters exist; NO accepted themes. Establish whether
   useful thematic structure is inducible from C1/corpus and adjudicable.
4. **Build semantic alignment properly** — same target/sense/scope/level/modality before contradiction.
5. **Build the dialectical graph** — RESPONDS_TO / ATTACKS / UNDERCUTS / REBUTS / UNDERMINES /
   QUALIFIES / CONCEDES / DISTINGUISHES, separate from internal inference (pūrvapakṣa/siddhānta).
6. **Run multiple evaluators over the same IR** (ASPIC / Nyāya / formal → EvaluationRun; no one is "truth").
7. **Crux extraction** — the minimal disputed dependency the disagreement turns on (+ counterfactual).
8. **Synthesis** — debate graph → strongest positions → unresolved questions → essays/briefs (CP6).
9. **Scholar Workbench / Review** — scholar edits graph → recompute (the "philosophy OS").

---

## Lane

- **Role:** ML + eval + retrieval + the research story.
- **Owns:** `machinelearning/` (doctrine, benchmark, DEVPLAN, experiments), the curriculum, statistical
  rigor, leakage rules.
- **THE GOVERNING RULE (read `AGENTS.md` + `machinelearning/AGENTS-DOCTRINE.md` FIRST):**
  *nothing is real because code exists; it's real only when independent gold + blind eval + metric +
  human adjudication show it.* A tested schema ≠ a result. Route everything through the frozen benchmark.
- **Rule (frozen):** no INFER model is adopted until it beats a baseline on a fixed held-out set.
- **Do NOT:** edit `data/corpus/`, `app/`, `lib/` (Agent 2's ontology); re-derive Agent 2's structures
  (philproof internals, verify_l0); port the F1–F8/D1–D5/B1–B6 ontology (rejected — doesn't fit Pāṭala).

---

## Current state (2026-08-12) — THE HONEST PICTURE

> **Read `handover/agent-1-ml/SESSION-2026-08-12.md` first** — the full session record. This INDEX is the
> living summary. **The vision this feeds:** `docs/vision/CORE-BIBLE.md` (Layer 3 = checkpoints) — my
> CP4 work is the ACTIVE item there; update it via `handover/flow.py` at session end.

### 🔴 THE ACTIVE WORK RIGHT NOW (this is the live task)
**The scholar-corpus foundation (S0) is the forward work.** The ML vertical is frozen + peer-review-clean; the
pivot is turning the on-disk published-scholar corpus (Sanderson/Ratié/Torella/Bäumer) into a
provenance-addressable corroboration oracle — **no live reviewer needed** — by **borrowing mature open tools**
(GROBID/Zotero/OpenAlex/OpenCitations/RO-Crate/PaperQA2/Inspect/INCEpTION/Recogito) and adding only the **epistemic
dependency graph** (SourceAssertion → CorroborationEvent → Proposition → Argument → Crux → Synthesis → ReviewEvent
→ dependency). **Start with the Inspect AI prototype** (port one existing benchmark + the laundering mutations).
**HANDOVER: `handover/agent-1-ml/HANDOVER-2026-08-13.md`** (read this first).
```
Built this session:
  ARG-003  reductio                (V2-O ordered-support regress, 8 nodes/4 infs)   ✅
  ARG-004  conceptual-distinction  (vimarśa vs prakāśa, V2-H, 6/4)                 ✅
  ARG-005  interpretive scope      (V3-I: local vs systematic, 5/3, 2 Positions,    ✅
            3-level SemanticAlignment; retyped from AMBIGUOUS after review)
  Build 4  primitive extractor run BLIND vs all 5 golds → BenchmarkRun             ✅
            (baseline lexical-overlap F1 0.36, inference recovery 0.0; Task-A bound,
             metric BOUNDED as baseline-v0)
  Gate #3  VERTICAL OBJECT v0 (HARDENED) — one proposition (ARG-001 G-TC2) with EVERY edge  ✅
            TYPED + honest resolution: exact L0 grounding_refs (no fuzzy search for gold),
            GroundingLink{relation,resolution,review_state} per edge, proof marked STALE (not
            resolved), C1/L2 at SPAN_LEVEL, missing IR fields surfaced (not retrofitted).
            patala_ml/vertical.py + benchmarks/v0/vertical/vertical-v2o-g-tc2.json. FROZEN v0.
            ✅ NOW FULLY RESOLVED: Agent 2 regenerated the authoritative P0 proof → proof edge
               STALE → EXACT / REFERENCE_RESOLVED (on_disk_PASS True, roundtrip PASS, 0 unresolved).
               The auditable Sanskrit→C1 chain closes end-to-end. Cross-lane handoff logged.
  Review applied (REVIEW-2026-08-12-MODEL-1, independent model review): ARG-001/002/004/005 REVISE,      ✅
             ARG-003 REJECT_AS_TEXTUAL_GOLD -> demoted to ALT_RATIONAL_RECONSTRUCTION (regress not
             licensed). Corrections applied: regress/transcendental removed (ARG-001), parā-vāk/
             knower identifications are GROUNDING not inference (ARG-001/004), ARG-005 objection is a
             dialectical RESPONDS_TO + systematic reading needs cross-passage grounding, ARG-002 v2 is
             the clean py-aspic target. Status = MODEL_INDEPENDENT_REVIEWED (NOT specialist-reviewed).
             ReviewEvent: benchmarks/v0/review/REVIEW-2026-08-12-MODEL-1.json · IR findings:
             machinelearning/_ACTIVE/IR-REVIEW-FINDINGS.md.
Honest status: golds are MACHINE_PROPOSED/CANDIDATE — NOT yet independently reviewed.
```
Built this session (cont.) — the CP3 / theme layer + retrieval readiness:
  Theme discovery  recall-first pipeline over IPVV/C1 → 100% coverage (63/63, 0 unassigned)     ✅
                   (patala_ml/theme_discovery.py; theme-map-ipvv-v0.json; THEME-MAP-IPVV-REPORT.md)
  Theme review     THEME-REVIEW-001..003 (model): Order-less Support=LOCAL_THEME(REVISE),          ✅
                   Vimarśa=CONCEPT_TERM_FAMILY(RETYPE), Pramāṇa=DOCTRINAL_PROBLEM_DOMAIN(RETYPE)
                   → the three are NOT the same kind → CP3 kind-taxonomy validated
  Theme packet     THEME-ADJUDICATION-PACKET.md (kind taxonomy + coarse sense-tagging)            ✅
  Stage A          Semantic-alignment harness built + baseline falsified (0/8; ablation isolates        ✅
                   the failure to encoder/representation space, not context windows). Next: cross-
                   encoder pair classifier / Sanskrit-aware embedding (see RETRIEVAL-NEUROSYNTHETIC-VISION.md)
  ASPIC pilot      ARG-002 v2 → minimal local fallback (real engine 503): vikalpa accepted          ✅
                   w/o defeater, defeated with G2-TC2; EvaluationRun recorded; converse fixed;
                   REPRESENTATIONAL_FIDELITY=PARTIAL, SEMANTIC=PROXY_SUPPORTED, BET=OPEN
  Vertical object  proof edge now reference_resolution=EXACT + semantic_support=MACHINE_PROPOSED    ✅
  Doctrine         Axiom 11 (git worktree discipline) + GIT-INCIDENTS.md (4cc78d1 recorded)        ✅
Next (see `NEXT-STEPS.md` revision 6): **the Pāṭala Review vertical is FROZEN and peer-review-clean relative to
the current objects** — the synthesis (weakest-governs, `SYN-INF-001` reconstructed + UNRESOLVED), monotone EO,
one provenance-linked essay + SentenceEvidenceAudit (6 laundering/paraphrase mutation classes caught), and a
deterministic k-core structural hierarchy + Louvain stability ablation (P-019 v2; Louvain empirically stable at
11 communities on the 63-node graph). **Agent 1 is on hold; the next move is Agent 2 / the autonomous factory**
(registry idempotency → single-writer lock → Hermes cleanup → stable passage_id+hash binding → bounded batching →
ASCII-avagraha → OCR→SOURCE_BLOCKED → crash/resume + adversarial tests → Sanskrit-only replay certificate → a small
Kramasadbhāva unattended canary, then a generic L0 controller reused across T1/R1/T2/R2/T3/T3.1/C1). Deferred
roadmap (xAIF/SEPIO/nanopub/TantraFact) = record, not queue.

**The source of this task:** `handover/agent-1-ml/ORIENTATION.md` Phase 4 + `NEXT-STEPS.md` + the vision
(`docs/vision/CORE-BIBLE.md` Layer 3 / `handover/CHECKPOINTS.md` CP4).

### The pivot this session: epistemic hardening (not building more)
We built a full ML spine (cluster→argument→essay→gold-chain), then an audit exposed it was mostly
structurally-elegant-but-hollow. We pivoted to: frozen benchmark + enforced doctrine + honest relabeling
+ one genuinely measured result (the Nyāya gate).

### What is REAL (the honest set)
- **`benchmarks/v0/`** — the frozen evaluation substrate (the most valuable thing we built).
- **The Nyāya gate** (`nyayagate.py`) — measured: detection 0.80, false-positive 0.00, abstain 0.50.
- **The L0 proofs** (Agent 2's `verify_l0.py`) — V2/V3 35/35 P0 PASS, verified. The gold chain now
  consumes these.
- **The clusterer** (`cluster.py`) — real graph topology; MACHINE_PROPOSED themes.

### What is HOLLOW (admitted, do not present as results)
- `strength.py` (BayesianEvidencePrimitive — uncalibrated, no epistemic role)
- `argument.py` (schema; `gate` slot empty)
- The essay layer (`essaygen/essayplan/...` — scope creep, the endpoint not the machine)
- `aifgraph.py` (no real propositions), `c1metrics.py` (unvalidated thresholds)
- `builders.py` comparison — **RETIRED as CIRCULAR**

### In progress / next (in order — the real work)
1. **🔴 CP3 theme acceptance** — run the model review of the theme map, cross the kind/sense
   adjudication into `ACCEPTED_THEME` (Order-less Support=LOCAL_THEME, Vimarśa=CONCEPT_TERM_FAMILY,
   Pramāṇa=DOCTRINAL_PROBLEM_DOMAIN). `THEME-REVIEW-001..003` are the model judgments; a human/model
   confirmation promotes them.
2. **Semantic alignment** — the foundational symbolic layer. The theme reviews surfaced the exact
   relations to model (vimarśa NEAR_SAME, sphurattā AMBIGUOUS, pramāṇa NEAR_SAME / anumāna AMBIGUOUS).
   Freeze SemanticAlignment v0 from those actual annotations, THEN build the alignment machinery.
3. **Independent gold review → the FIRST auditable argument** (ARG-002 v2) — unlocks real py-aspic +
   crux + dialectical. Do NOT block CP3/alignment on this (the reviewer: build experimentally, mark
   ENGINEERING_VALIDATED ≠ SCHOLARLY_VALIDATED).
4. **CP2 retrieval over Pāṭala objects** — index Sanskrit lemmas + C1 + argument objects;
   BM25/dense/late-interaction baseline (the "neural layer" of the microscope vision).
5. **Then** viruddha as a graph op + the extractor (split A/B/C).

**Do NOT:** build the essay layer / Bayesian propagation / more clustering · hack viruddha into the
frozen gate · build extraction/crux as if the gold were already validated (mark it ENGINEERING_VALIDATED,
not SCHOLARLY_VALIDATED) · present `reference_resolution=EXACT` as semantic entailment.

---

## Key files (the doctrine + the state)

### The governing doctrine (read first)
- `AGENTS.md` (repo root) — auto-loaded; the ONE RULE + read-order.
- `machinelearning/AGENTS-DOCTRINE.md` — the master anti-theatre rule.
- `machinelearning/CLAIMS.md` — the project's self-audit ledger (P-001..P-008).
- `machinelearning/COMPONENT-CONTRACTS.md` — the 9-field anti-theatre contracts.
- `machinelearning/AGENT1-HANDOVER.md` — the working doctrine (axioms, errors, tone).
- `machinelearning/theatre_check.py` — the mechanical gate (run before claiming "done").

### The vision + plan
- `machinelearning/dualagentvision.md` + `-ADAPTED.md` — the north star + checkpoint map (CP0–CP12).
- `machinelearning/DEVPLAN.md` — the consolidated execution plan (priority: gold review → extractor → gate; **§5 = the neural/retrieval Phase D**).
- `machinelearning/_ACTIVE/RETRIEVAL-NEUROSYNTHETIC-VISION.md` — the "semantic microscope" vision (Stages A–E) + the comprehensive review of retrieval frameworks vs current state.
- `machinelearning/MLUSEINPATALA.md` — the frozen strategy.

### The truth-engine goldmine (external)
- `machinelearning/TRUTHENGINE-FULL-AUDIT.md` — the 22-doc inventory (Nyāya gate = best asset, unwired).
- `machinelearning/TRUTHENGINE_TO_PATALA_MAPPING.md` — reuse mechanisms, reject the ontology.
- `machinelearning/SANSKRITREE-LEAN-REVIEW.md` — the honest verdict: don't build on Lean.
- Runtime: `/root/projects/.meta/misc/truth-engine/` (code + docs-active).

### The research lane
- `machinelearning/research/` — the 26-module package + 10 test files (339 passing).
- `machinelearning/mlcurriculum.md` — the verified 26-paper curriculum.
- `benchmarks/v0/` — the frozen substrate (MANIFEST/SCHEMA/SPLITS/METRICS + gold).

---

## Guardrails reminder
Never edit the deterministic substrate (`data/published/`, `lib/verify.ts`, `data/corpus/themes.ts`,
`lib/citation.ts`, `data/corpus/graph.ts`) — consume it through the shared contract. The philproof/verify_l0
internals are Agent 2's lane; my consumer (`philproof.py`, `build_goldchain.py`) reads their output. Join on
Passage ID / Proof ID / C1 ID — never fuzzy.

## THE ACTIVE NEXT-STEPS DOC (current execution)
- **`handover/agent-1-ml/NEXT-STEPS.md`** — the exact how-to for the next session: build ARG-GOLD-002..005
  (transcendental/objection-reply/reductio/conceptual-distinction/ambiguous) with the
  DebateFrame/SemanticAlignment layer, the per-build gates, the falsification self-check, and the guardrails.
