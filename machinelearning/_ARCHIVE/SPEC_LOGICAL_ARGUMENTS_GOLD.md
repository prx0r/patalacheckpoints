# SPEC — LOGICAL ARGUMENTS ARE THE GOLD (the compounding pipeline)

*2026-08-12. The highest-value output of the whole system. Logical arguments — formal,
passage-anchored, provable-where-possible — are what make Pāṭala a *computable scholarly tradition*
rather than a translation site. This ties the truth engine (nyāya/Lean), the PUSHING discovery, and
the published corpus into one compounding loop.*

---

## 1. The thesis

> **PUSHING finds tensions → formal logical arguments resolve/analyze them → essays get written from
> the arguments → lessons teach the essays. It all compounds and tracks on the source hub.**

The essays and logical arguments in `research-library/` (the reflexive-debate, the Ñāṇavīra proof,
`apoha-partition-formal`, the `FORMALIZATION-OF-RECOGNITION` AM0) are the proof this works. The
vision: once the corpus is machine-readable (passages + C1s + themes + resolve + hub), this becomes
automatable.

---

## 2. The compounding loop (each step tracked)

```
                    ┌───────────────────────────────┐
                    │  PUSHING enquiry (discovery)  │  finds a tension, quotes the passages
                    └──────────────┬────────────────┘
                                   │  resolve passages (/api/resolve + published store)
                                   ▼
                    ┌───────────────────────────────┐
                    │  FORMAL LOGICAL ARGUMENT      │  ← THE GOLD
                    │  premises · inference · concl │  tied to passages
                    │  tied to the truth engine     │
                    └──────────────┬────────────────┘
                                   │  prove/analyze (nyāya/Lean where formalizable)
                                   ▼
                    ┌───────────────────────────────┐
                    │  ESSAY (from the argument)    │  every claim cites argument + passages
                    └──────────────┬────────────────┘
                                   ▼
                    ┌───────────────────────────────┐
                    │  LEARNING (from the essay)    │  lessons, guides
                    └──────────────┬────────────────┘
                                   │
                                   └──► back to PUSHING the next tension
```

All steps write to the source hub (`/api/hub`): `pt:hub:<work>:<kind>:<slug>` with `passage_ids`.
Nothing is orphaned; everything resolves.

---

## 3. The argument object (the machine shape)

```text
pt:argument:<work>:<slug> {
  work_id
  title
  kind: "reductio" | "analogy" | "identity" | "entailment" | "decomposition"
  premises:   [ { text, passage_ids } ]
  inference:  "the typed move"
  conclusion: { text, passage_ids }
  tension_id:  the PUSHING question it resolves
  provenance:  derivation (resolved passages)
  status:      "MACHINE_DRAFT" → "REVIEWED" | "PROVED" | "OUTSIDE_FORMAL"
  proof:       optional — the nyāya/Lean trace where formalizable
}
```

The `proof` field ties it to the truth engine: `PROVED` (Lean), `OUTSIDE_FORMAL` (empirical),
`HOLLOW` (unsayable) — the truth-compressor's honest verdicts.

---

## 4. The truth-engine link

The `nyayaengine.py` (NYĀYA → LEAN decomposition, the "truth compressor") already exists as a
scaffold. It maps to the argument object:
- a formal argument's premises/conclusion become the Lean claim to prove;
- `ground_truth/nyaya_claims.json` supplies formal claim data;
- the verdict (`PROVED`/`OUTSIDE_FORMAL`/`HOLLOW`) is attached to the argument.

This is the "logical arguments are the gold" machine: it turns a PUSHING-found tension into a formal
claim that is either proved or honestly bounded.

---

## 5. The compounding payoff

| Capability | Before | After |
|---|---|---|
| "What are the tensions in IPVV?" | manual reading | PUSHING enquiry (discovered) |
| "Are they real?" | scholarly judgment | formal argument (premises + inference) |
| "Can they be proved?" | — | truth engine (PROVED / OUTSIDE_FORMAL / HOLLOW) |
| "What does it mean?" | — | essay from the argument |
| "Teach me" | — | lesson from the essay |
| "Where do I start?" | — | epistemic PageRank over the source hub |

Every new machine-readable text adds more: more PUSHING enquiries, more tensions, more arguments,
more essays, more lessons — all tracked, all compounding.

---

## 6. Immediate steps (todos)

- [ ] **Argument object schema** (Agent 1) — `pt:argument:` per §3, added to the graph + hub.
- [ ] **Truth-engine link** (Agent 1) — connect argument objects to `nyayaengine.py`/Lean; record
      the PROVED/OUTSIDE_FORMAL/HOLLOW verdict.
- [ ] **A worked example** — pick one IPVV tension from PUSHING-IPVV (e.g. the reflexivity claim),
      resolve its passages, formalize the argument, run it through the engine, write the essay.
      This proves the loop end-to-end.
- [ ] **Hub wiring** (Agent 2) — ensure the argument objects land on `/api/hub` with passage_ids.
