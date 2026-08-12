# AGENT 1 (ML) — CHECKPOINTS & GOALS

*2026-08-12. The Agent-1 leading doc. Breaks the shared vision (`CHECKPOINTS.md`) into THIS lane's
concrete goals. **Agent ML owns CP0, CP2, CP3, CP4.** Read `AGENTS.md` + `AGENTS-DOCTRINE.md` +
`handover/agent-1-ml/SESSION-2026-08-12.md` first.*

---

## THE LANE (what Agent ML owns)

```
CP0  BENCHMARK REAL   →  CP2 RETRIEVAL REAL  →  CP3 THEMES REAL  →  CP4 ARGUMENT REAL (converge w/ L0)
```

**Do NOT:** build the essay generator further · build full Bayesian propagation · promote the Nyāya gate
to semantic verification yet. Nyāya waits until real `Inference` objects exist.

---

## GOAL CP0 — Benchmark genuinely real

**Now:** benchmark framework exists + ARG-GOLD-001 + retrieval fixtures. **Gold population is thin.**

**Target (human-checked, not just directories):**
```
PATALA-RETRIEVAL   ~40–50 reviewed queries
PATALA-EVIDENCE    ~20–30 claim↔evidence judgments
PATALA-STRUCTURE   5–10 real hand-reconstructed arguments
PATALA-FIDELITY    ~20–30 transformations + adversarial corruptions
```
**Freeze:** the `BenchmarkFixture` + `BenchmarkRun` contracts (see CHECKPOINTS.md §7).
**Gate:** no model "works" without a `BenchmarkRun`.

**Current state (honest):** retrieval has 1 fixture file; structure has ARG-GOLD-001; evidence has the
12-fixture Nyāya-gate gold; fidelity has 0. → grow all toward the targets.

---

## GOAL CP2 — Evidence retrieval becomes trustworthy

**Now:** passages/C1/terms/relations/resolve exist. Retrieval quality is NOT yet a benchmarked capability.

**Build:** run against CP0 — BM25 vs dense vs hybrid (vs late-interaction later) for questions like
"find passages supporting X" / "find uses of vimarśa" / "find passages challenging claim C."

**Freeze the `EvidenceCandidate` contract** — retrieval returns scholarly candidates, NOT strings:
```ts
interface EvidenceCandidate {
  candidate_id: string; query_id?: string; target_claim_id?: string;
  passage_id: Ref; source_span_ids?: Ref[];
  relation: "SUPPORT_CANDIDATE" | "CONTRADICT_CANDIDATE" | "QUALIFY_CANDIDATE" | "PARALLEL_CANDIDATE" | "UNKNOWN";
  retrieval_method: string; retrieval_score?: number;   // ranking score, NOT truth score
  status: "MACHINE_PROPOSED" | "REVIEWED" | "ACCEPTED" | "REJECTED";
}
```
**Gate:** a production method must beat the trivial baseline on frozen retrieval fixtures.

---

## GOAL CP3 — Themes become real scholarly objects

**Now:** 9 graph proposals + `themes.ts` lemma-topics, but NO unified editorial Theme layer.

**Do NOT build another clustering algorithm.** Unify the representation first (`Theme` + `ThemeMembership`
contracts — see CHECKPOINTS.md §7).

**Immediate target:** adjudicate **3 of the 9 proposals** — Order-less Support, Vimarśa, Pramāṇa — into
`AcceptedTheme` objects. A theme is accepted because someone inspected members/exclusions/boundary/
tensions/evidence — NOT because clustering found it.

**Gate:** the 3 themes are `EDITOR_REVIEWED`/`ACCEPTED` with real review events.

---

## GOAL CP4 — Real argument reconstruction (the big one)

**Now:** ArgumentProposal schema exists; automatic reconstruction does not. One gold object (ARG-GOLD-001).

**Grow gold** to ARG-GOLD-001..005 then 010, covering:
```
clear inference · implicit inference · objection/reply · reductio ·
ambiguous reconstruction · NO-SAFE-RECONSTRUCTION case (the abstain case)
```

**Freeze the argument contracts** — proposition nodes + inference nodes, NOT one giant object:
- `Proposition` (TEXTUAL_CLAIM / INTERPRETIVE_CLAIM / IMPLICIT_PREMISE / CONCLUSION / OBJECTION /
  QUALIFICATION · explicitness · grounding · boundary · status)
- `Inference` (premise_ids / conclusion_ids · scheme NYAYA_ANUMANA/REDUCTIO/TRANSCENDENTAL/... · rationale ·
  defeaters · status)
- `Grounding` (passage_id · source_span_ids · c1_id · l200_assertion_id · philological_proof_ids)
- `Defeater` (COUNTEREVIDENCE / RIVAL_READING / COUNTEREXAMPLE / FAILED_PREMISE / SCOPE_PROBLEM)

**This is where the Nyāya machinery plugs in** — as an audit of the `Inference`, once real Inference
objects exist. Not onto arbitrary claims.

**Gate:** extractor evaluated blind against the gold (proposition F1, grounding precision, relation F1,
abstention), a simple baseline included.

---

## THE NEXT-FOUR-BUILDS QUEUE (Agent ML, concrete)

```
1. finish benchmark gold population   (CP0 — grow evidence + structure + fidelity fixtures)
2. benchmark retrieval                (CP2 — BM25/dense/hybrid vs trivial baseline on CP0)
3. adjudicate 3 themes                (CP3 — Order-less Support, Vimarśa, Pramāṇa → AcceptedTheme)
4. grow Argument Gold 001–010 + test actual extraction   (CP4)
```

**The convergence:** at CP4, an argument proposition can say "I claim X because C1 says / L2 renders /
Sanskrit span is / PhilologicalProof says" — the first complete vertical scholarly object, joining Agent
ML's derivation to Agent L0's proof.

---

## THE GUARDRAILS (Agent ML specific)

- Route EVERYTHING through the frozen benchmark. No model "works" without a `BenchmarkRun`.
- The Nyāya gate stays `NYAYA_GATE_CANDIDATE` until real `Inference` objects exist.
- Do NOT pursue the Lean bridge (proves FOL tautologies, not Abhinavagupta).
- Do NOT build the essay layer / Bayesian propagation / more clustering.
- Join on `Ref` IDs — never fuzzy. Update `CLAIMS.md` + `theatre_check.py` honestly as you go.
