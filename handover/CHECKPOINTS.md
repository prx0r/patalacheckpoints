# CHECKPOINTS — the shared leading doc for BOTH agents

*2026-08-12. The one-screen truth: what the two agents are driving toward, in order. **No new higher
layer is built until the lower scholarly object it consumes has crossed its validation gate.** Read
`AGENTS.md` + `AGENTS-DOCTRINE.md` first; this is the execution map.*

---

## THE FIVE CHECKPOINTS (the whole plan)

```text
CP0  BENCHMARK REAL
CP1  PHILOLOGICAL PROOF REAL      (Agent L0)
CP2  EVIDENCE RETRIEVAL REAL      (Agent ML)
CP3  THEMES REAL                  (Agent ML)
CP4  ARGUMENTS REAL               (both — they CONVERGE here)
      ↓
     [semantic verification → adversarial review → essays → API/MCP]
```

**The one sentence (keep everyone out of the weeds):**
> The next five checkpoints are Benchmark → Philological Proof → Retrieval → Accepted Themes → Real
> Arguments. No new higher layer is built until the lower scholarly object it consumes has crossed its
> validation gate.

---

## THE SEVEN CANONICAL CONTRACTS (freeze these; everything else sits on top)

```text
1. Ref                       the universal reference type — every ID must resolve
2. ReviewState / ReviewEvent the honest status ladder
3. BenchmarkFixture / BenchmarkRun   the frozen evaluation objects
4. PhilologicalProof         the source→L0 proof
5. EvidenceCandidate / EvidenceUse   retrieval returns scholarly candidates, not strings
6. Theme / ThemeMembership   the accepted-theme object
7. Proposition / Inference / Grounding / Defeater   the argument layer
8. DebateFrame / SemanticAlignment   the anti-fake-contradiction layer (see SEMANTIC-COMMENSURABILITY.md)
```

**8. DebateFrame / SemanticAlignment — the newest, and one of the most important.** Every argument is
*argument-under-a-frame*. Before comparing two positions, require: same DebateFrame? same target
proposition? semantic alignment adequate? scope compatible? Only then test contradiction. This makes
viruddha a graph operation (does H support ¬S after alignment?), not a keyword hack, and prevents the
fake contradictions that pollute argument comparison, counterevidence, and theme clustering. Full spec:
`machinelearning/SEMANTIC-COMMENSURABILITY.md`.

### Ref (the most important — both agents share it)
```ts
interface Ref {
  id: string;
  type: "WORK" | "PASSAGE" | "SOURCE_SPAN" | "L0" | "TRANSLATION" | "C1" |
        "THEME" | "PROPOSITION" | "INFERENCE" | "PHILOLOGICAL_PROOF" | "EVIDENCE";
  version?: string;
}
```
**Invariant: every ID placed into a canonical Pāṭala object must resolve.** No fabricated IDs, no fuzzy
locator silently promoted. (The fabricated-ID bug permanently established this.)

### BenchmarkFixture + BenchmarkRun (CP0)
```ts
interface BenchmarkFixture {
  fixture_id: string; benchmark_version: string;
  task: "PASSAGE_RETRIEVAL" | "TERM_RETRIEVAL" | "CLAIM_SUPPORT" | "COUNTEREVIDENCE" |
        "ARGUMENT_EXTRACTION" | "FIDELITY";
  inputs: Ref[]; expected: unknown; provenance: Ref[];
  review_state: "CANDIDATE" | "SINGLE_REVIEWED" | "DOUBLE_REVIEWED" | "ADJUDICATED";
  split: "DEV" | "EVAL_ONLY" | "ARGUMENT_FAMILY_HELD_OUT" | "WORK_HELD_OUT";
  allowed_training_use: boolean;
}
interface BenchmarkRun {
  run_id: string; benchmark_version: string; git_commit: string;
  model_or_method: string; config_hash: string;
  predictions: Ref; metrics: Record<string, number>; error_analysis: Ref;
}
```
**Gate: no model "works" unless there is a `BenchmarkRun` demonstrating it.**

---

## THE CHECKPOINT GATES (what each "REAL" means)

| CP | Real means | Owned by |
|---|---|---|
| **CP0 BENCHMARK** | ~40–50 retrieval queries + 20–30 evidence pairs + 5–10 arguments + 20–30 fidelity pairs, all human-checked, with the Fixture contract | ML |
| **CP1 PHILOLOGICAL** | every source→L0 decision exposes PROVED/SUPPORTED/CONFLICT/OPEN/REVIEWED per dimension; P0✅, P1–P4 via Vidyut+Heritage+gold | L0 |
| **CP2 RETRIEVAL** | BM25 vs dense vs hybrid beats trivial baseline on frozen retrieval fixtures; returns `EvidenceCandidate` objects | ML |
| **CP3 THEMES** | 3 of the 9 proposals genuinely adjudicated into `AcceptedTheme` (membership inspected, not clustering-asserted) | ML |
| **CP4 ARGUMENT** | ARG-GOLD-001..010 real propositions; extractor tested blind against them; the vertical object "I claim X because C1 says / L2 renders / span is / proof says". **Target shape = the philosophical IR** (`machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md`): every proposition carries a Commitment (who asserts) + derivational `derived_from`; a ResearchQuestion per argument; Attack vs Defeat split; three-level SemanticAlignment for comparative cases. **Built gold-first — the ontology is forced by the gold, not designed empty.** | **both converge** |

**ACTIVE NOW (2026-08-12): CP4 is live.** Agent 1 is building **ARG-003 (reductio) · ARG-004
(conceptual-distinction) · ARG-005 (ambiguous)** with the IR shape. ARG-001/002 done + consistent.
Progress tracked live in `handover/STATE.yaml` via `flow.py update agent1 CP4 <status>`. See
`handover/agent-1-ml/INDEX.md` (current work) + `handover/agent-1-ml/ORIENTATION.md` (the process).

---

## THE TWO-AGENT RESPONSIBILITIES (the next month)

### Agent L0 — ONLY CP1 (PhilologicalProof)
```
Heritage ensemble → P2 disagreement analysis
→ lexical gold → ranker benchmark
→ alignment gold → alignment benchmark
```
Do NOT wander into essay logic. The `PhilologicalProof` contract is the deliverable:
```ts
interface ProofDimension { status: "PROVED"|"SUPPORTED"|"CONFLICT"|"OPEN"|"UNCHECKED"|"REVIEWED"; evidence_ids: string[]; }
```
No invented `confidence: .93`.

### Agent ML — ONLY CP0, CP2, CP3, CP4
```
finish benchmark gold population → benchmark retrieval → adjudicate 3 themes → grow Argument Gold → test actual extraction
```
Do NOT build the essay generator further. Do NOT build full Bayesian propagation. Do NOT promote the
Nyāya gate to semantic verification yet — **Nyāya waits until real `Inference` objects exist.**

---

## WHERE THE NYĀYA GATE FITS (the honest placement)

The Nyāya gate does NOT wire onto arbitrary claims. It plugs in at **CP4**, once real `Proposition` /
`Inference` objects exist — as the audit of the *inference* (and the `Defeater` types: COUNTEREVIDENCE /
RIVAL_READING / COUNTEREXAMPLE / FAILED_PREMISE / SCOPE_PROBLEM). Until then it stays `NYAYA_GATE_CANDIDATE`.

---

## THE CONVERGENCE OBJECT (the first complete vertical scholarly object)

At CP4, an argument proposition can finally say:
```
"I claim X"
because:
    C1 says ...
    L2 renders ...
    Sanskrit span is ...
    PhilologicalProof says ...
```
That is the first complete vertical scholarly object — and everything after (semantic verification,
adversarial review, essays, workbench, API/MCP) is a *composition* of objects we already know are
trustworthy, not speculative architecture.

---

## THE AGENT-SPECIFIC BREAKDOWNS

- **Agent ML (CP0/CP2/CP3/CP4):** `handover/agent-1-ml/CHECKPOINTS-ML.md`
- **Agent 2 / L0 (CP1):** `handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md`

Each breaks this shared vision into that lane's concrete goals, gates, and guardrails.

## SEE ALSO (the parallel layers this ladder joins)

- **The live agent system (who + tracked progress):** `handover/SYSTEM.md` (template `agent0` → live
  instances) + `handover/STATE.yaml` via `python3 handover/flow.py status`.
- **The skills (how the work is done):** `skills/*/SKILL.md` — each skill names the checkpoint it
  advances (e.g. `translate-work` → CP1, `push-text` → CP4, `write-commentary` → CP3).
- **The product vision arc (why):** `docs/vision/INDEX.md` — Vision 01–08 mapped onto this ladder
  (e.g. 06 Pāṭala Review → CP5/CP8, 07 New Scholar → CP7).
