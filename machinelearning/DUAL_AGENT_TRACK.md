# DUAL-AGENT TRACK — the lane split (live)

*2026-08-12. The current two-lane (now three-role) split. Split expertise and context so no agent holds
the other's deep context and none blocks another. Each owns a lane; all write to the same evidence graph
and the same canonical docs. This is the LIVE doc at the path referenced by `docs/INDEX.md`,
`handover/README.md`, and `VISION_AND_NAVIGATION.md` — the original deep version (with each lane's working
method) is archived at `machinelearning/_ARCHIVE/DUAL_AGENT_TRACK.md`.*

---

## 1. The lanes (clean split, no overlap)

| | **Agent 1 — ML / research** | **Agent 2 — corpus compiler + integrity** | **Agent 3 — translation factory** |
|---|---|---|---|
| Direction | horizontal + upward derivation | **vertical truth + corpus integrity** | worker / producer |
| Lane | C1 → themes → arguments → claims → synthesis → review | SOURCE → L0 → corpus state → RAW-L0 factory → versioned L0 → review | RAW-L0 → close translation → adversarial → resolved → C1 |
| Question | does this higher representation legitimately derive from the objects beneath it? | *is this reading licensed by the source? what do we have, where, what state, can every artifact resolve?* | (produces candidate artifacts) |
| Owns | `benchmarks/v0/`, `machinelearning/research/patala_ml/`, ML strategy, retrieval, experiments | `data/corpus/`, `app/`, `lib/`, `pipeline/` (verify_l0, corpus_state, raw_l0, agent3_batch/queue, l0_registry, review_engine), `translations/_stack/ipvv/specs/` | consumes `NEXT_VALID_ACTION`; Hermes execution kernel |
| Checkpoints | CP0, CP2, CP3, CP4 | **CP1** (PhilologicalProof) | — |
| Tests | benchmark eval, retrieval metrics | invariant tests, P0 proof, review-engine idempotence | the factory certificate |

**The load-bearing rule:** Agent 3 never invents a proof Agent 2 hasn't validated; Agent 1 never builds on
structure Agent 2 hasn't exposed. They meet at the **deterministic substrate** (the published corpus +
verify/resolve services + the versioned L0 + the corpus state machine), which is the shared contract.

---

## 2. The shared contract (where they meet)

Both lanes treat these as ground truth:

```text
data/published/ipvv/        the 49-passage lazy store (source + L2 + C1 + immutable ids)
lib/verify.ts               the deterministic verification floor (quote/claim-structure/trace/counterevidence)
data/corpus/themes.ts       deterministic theme proposals
lib/citation.ts             the resolve/immutable-id kernel
data/corpus/graph.ts        the scholarly graph (annotations + evidence roles)
data/corpus/downloads/translation-state-ledger.json   the per-work state + NEXT_VALID_ACTION
data/corpus/downloads/l0-version-registry.json        the immutable versioned L0 registry
```

**Join on Ref IDs only** — Passage ID · PhilologicalProof ID · C1 ID · TranslationDecision ID ·
ReviewEvent ID. Never filename, guessed locator, title, or fuzzy match.

---

## 3. The handoff protocol

- **Agent 2 → Agent 1/3:** "Exposed X" — a structure became machine-queryable (e.g. "the corpus state
  machine is live at `/api/corpus/state`"; "Kramasadbhāva is now RAW-L0 ELIGIBLE").
- **Agent 1/3 → Agent 2:** "Needs X" — a consumer needs data that isn't exposed or validated yet.
- All log to `handover/LOG.md` (one entry per handoff: what, why, file, date, schema snippet).

---

## 4. Guardrails (shared, from the doctrine)

- **A wrong translation is worse than none** — validation is the gate; never let the factory outrun the
  validator.
- **Proof dimensions stay separate** — never a collapsed confidence number.
- **L0 is immutable + versioned** — a fix emits a new version, never edit in place.
- **Agent 2 must not** hand-build ML models, claim results, write C1 / choose interpretive readings
  (Agent 1/3), or promote machine output.
- **Agent 1 must not** edit `data/corpus/`, `app/`, `lib/` scholarly code or re-derive the ontology.
- **Hermes is a replaceable execution kernel, not Pāṭala's epistemic backend.**

---

## 5. The deep reference

The original dual-agent working method (each lane's personal field-tested discipline + the historical
"integrator" framing) is preserved, archived, at `machinelearning/_ARCHIVE/DUAL_AGENT_TRACK.md`. The
current per-lane process workflows are the canonical source: `handover/agent-1-ml/ORIENTATION.md` and
`handover/agent-2-integration/ORIENTATION.md`.
