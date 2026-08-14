# LAYER 11 — ORG & ECONOMICS

> **STATUS: DESIGN — credit/market/partnership strategy is aspirational, not built** (derived live state — see `docs_state.py`)


*Part of the `NAVIGATION.md` layer map (the master tree / spine). The human + economic structure: agents, Hermes, scholars, money.*

## 1. What it is
The organizational + economic layer: who the agents are, how Hermes runs the work, how scholars are
credited and paid, and how Pāṭala positions in the ecosystem.

## 2. Purpose
Turn epistemic quality into a durable moat and a sustainable economic model. Align incentives so that
scholar corrections, provenance, and review data compound into something competitors can't copy.

## 3. External tools used
Hermes (execution kernel) · OpenAlex/Crossref (identity) · ORCID/ROR/CRediT (credit) · OpenReview/COAR
Notify (publishing). See `external-tools.md`.

## 4. Data
- `AttributionEvent` — the accounting atom (scholar credit: DIRECT_QUOTE / PARAPHRASED_POSITION / ...).
- `RightsState` — per-work copyright/quote/derivative policy.
- `external_identifier` — ORCID/ROR/VIAF crosswalks.
- The question/understanding graph (Q) — the behavioral moat.

## 5. Processes
```
Revenue → scholarly attribution graph → transparent contribution accounting
  (commissioned review · expert adjudication · licensed commentary · course contribution)
```
**Credit ≠ permission** — attribution and copyright are separate. Public = index/citation infrastructure;
deep = controlled corpus (`globalaccess.md`).

## 6. Implementations
- `AGENTS.md` — the agent architecture + Hermes wiring + operating axioms.
- `~/.hermes/profiles/patala/MEMORY.md` — the Hermes patala profile memory.
- `docs/global/globalpartnerships.md` — the 4 partner classes + integration-first adapters.
- `docs/vision/vision-08-scholar-economics.md` — the scholar economics.
- `docs/endgame4.md` — the economic thesis (the 84000 story).

## 7. Docs
- `docs/global/globalpartnerships.md` — the integration/identity strategy.
- `docs/global/globalaccess.md` — open-reference / controlled-corpus.
- `docs/global/HERMES-CALLING.md` — the correct way to call Hermes.
- `docs/vision/vision-08-scholar-economics.md` — scholar economics + credit.
- `docs/vision/vision-10-market-entry-and-partnerships.md` — go-to-market.
- `docs/endgame4.md` · `docs/endgame5year.md` — economics + strategic window.
- `NAVIGATION.md` — the master tree / spine / resolver.
