# migration/v2 — the Pāṭala v2 coherent-system spec

*Proposal (draft for review) for a clean, clear, agent-usable rebuild of the plumbing — not the
scholarship. The scholarship pipeline stays; the names get clear, the layers get codified, and every
store derives from one graph.*

## Files

| File | What it is |
|---|---|
| `PATALA-V2-SPEC.md` | the full proposal: rename map, kernel, transformation registry, stores, execution model, repo layout, build sequence |
| `LAYERS.yaml` | the machine-readable codified layer contract (the spine of v2) — every layer: clear name, legacy code, position, requires/produces, transformation, authority, doc |
| `LAYER-MAPPING.md` | the complete clean map of every layer: new name · mechanism (real files/modules) · process notes · what it needs · relations · vision docs · checkpoints · honest-state table · priority map |
| `MODULES.md` | the reusable module inventory — every module tagged `[REUSE]`/`[PARTIAL]`/`[GOLD-IPVV]`/`[NEW]`, the full Sanskrit→Education lifecycle, the scholar products, the verification plane, and the list of what does NOT exist yet |
| `strategy/` | the NON-technical strategic view: thesis, ecosystem position, partnerships, economics, funding, go-to-market, product doctrine, first-product decision, organisation |
| `goated/` | the curated index of Pāṭala's best standalone documents (the philosophy-engine set, the epistemic/truth set, the retrieval/agentic set, the global/architecture set, the Hermes set, the strategy/product set, the vision set) — with a "read only ten" short list |

## The core idea (one line)

> One event-sourced kernel + one derivation graph + clear names + compiled projections. Docs and the
> site become projections of state, not separate truths.

## The rename (code → clear)

- `T1` → `DraftTranslation` · `L0` → `Tokenization` · `ARGMAP` → `ArgumentOutline`
- `L2` → `Translation` · `L200` → `TranslationProof` · `C1` → `Commentary`
- `THEME` → `Theme` · `EDUCATION` → `Lesson` (SYNTHESIS/ARGUMENT/ESSAY keep their names)

Micro-stages `T1→R1→T2→R2→T3→T3.1→C1` unify onto the same vocabulary:
`DraftTranslation → DraftReview → AlternativeTranslation → Adjudication → FinalTranslation →
FinalProof → Commentary`.

## Why it matters

- **Clear names** → an agent reads the name and knows what it does + where it sits. No lookup.
- **One codified spec** → replaces the 19 hand-maintained "Layer 3 is PARTIAL" docs with a generated
  projection. Status can't drift (it's derived from the live registry).
- **One graph** → the derivation DAG is simultaneously correctness, staleness, scheduler, and retrieval.
  That's the biggest lever.

## Next concrete step (recommended)

1. Get a real reviewer (human or agent) to react to `PATALA-V2-SPEC.md` — especially the rename map
   and the authority semantics (the anti-theatre parts are the ones worth the most scrutiny).
2. Generate the full `LAYERS.yaml` contract and wire `docs_state.py` to render `CURRENT_STATE.md` from
   it. That single artifact is the spine of v2 and the natural first build.
3. Do NOT implement the kernel / projection-compiler until the rename + codify phase is real.
