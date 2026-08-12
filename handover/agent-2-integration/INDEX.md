# Agent 2 — INTEGRATION/CONTENT LANE INDEX

*The one living pointer for Agent 2's current state — done / in-progress / next. Update this as you
work. Append-only history lives under this folder; this file is the single "what is true right now"
source for the integration lane.*

---

## Lane

- **Role:** integration + scholarly content + docs + Sanskrit substrate.
- **Owns:** `data/`, `app/`, `lib/`, `pipeline/`, the reader/API/MCP, the factory,
  `translations/_stack/ipvv/specs/` + process notes.
- **Rule:** "AI proposes ≠ Pāṭala asserts." Expose scholarly structure as addressable data (schema
  snippets), keep the L200/C1 discipline, preserve provenance.
- **Do NOT:** build ML models or claim results (that's Agent 1); over-engineer the reader before the
  data/API is complete.

---

## Current state (2026-08-12)

### Done
- **Corpus published** — 49 IPVV passages as lazy-JSON (`data/published/ipvv/`), single source of
  truth via `getPublishedTranslation()` for both `/read` and `/api/resolve`. 21 tests pass.
- **Deterministic substrate** — C1 wired (`c1.verse_commentary[]`), c1_source derived (63 total),
  themes exposed (`/api/themes` + `get_themes`), hub + spines + journey + analyst + recommend exposed
  (`/api/…` + MCP).
- **Verification floor** — `lib/verify.ts` (`/api/verify/{quote,claim-structure,trace-dependency,
  counterevidence}`) + `lib/citation.ts` (`/api/resolve` + immutable ids).
- **API/docs** — `docs/openapi.yaml` (34 paths), `docs/api/README.md` (35 routes), `docs/api/mcp.md`
  (21+ MCP tools).

### In progress / next (in order)
1. **L0 P0 proof (BUILT, near-pass)** — `pipeline/verify_l0.py` (P0 deterministic, no NLP deps) emits
   per-chunk `.l0.proof.json` + aggregate. Coordinate model repaired (dual chunk/line), 4 tokenizer
   bugs fixed. Status: **V2/V3 11/35 PASS**, V1 legacy 0/28. Remaining: unmarked quote-initial tokens
   (`"now (idānīṃ)` — V2) + a V1 legacy-format extractor pass → goal **63/63 P0 PASS**. Full record:
   `docs/BUILD_NOTES_L0_P0.md`. Schema: `translations/_stack/ipvv/specs/l0_schema.json` +
   `l0_coverage.json`. Then wire Vidyut as P1/P2 witness (non-authoritative), then hand clean
   certificates to Agent 1.
2. **Deterministic related-rail** — `/api/recommend` + `recommend_related` MCP (biggest missing product
   feature; reuses spines/relations/hub/C1 see_also; no collision with Agent 1).
3. **Context alignment** — wire GRETIL IPK+Vṛtti+IPV into `/api/context` so each IPVV passage shows its
   root kārikā + parallel (closes the downloaded-sources thread).
4. **Comparative matrix** — `comparative.ts` + `/api/comparative` + first seed (feeds Agent 1's Q5/Q6).
5. **Argument truth-packet** — `pt:argument:` schema + `/verify-argument` + one worked example.
6. **PARALLELS** — typed (`supports/qualifies/contradicts`) cross-text witnesses, addressable.
7. **L200 → graph annotations** — keep the MT/IA split.
8. **Schema-version pin** — `data/published/ipvv/version.json` (protects Agent 1's eval validity).

Full thread list: `WHAT_NEXT_PATALA.md`.

---

## Open threads (flagged)
- The 6 downloaded IPV/IPK sources: IPV (Vimarśinī) + 1921 scan are NOT yet registered as
  hub/resources.
- IPVV 1.5.11 (hand-authored rich exemplar) vs the 49-passage chunk store — keep the 49 as canonical
  substrate; reconcile 1.5.11 as the exemplar.
- Recommended related-rail spec (`docs/api/recipes/recommend-related.md`) not yet written as the
  product spec.

---

## Protocol
- Log every data-carrying handoff to `handover/LOG.md` with a schema snippet; bump the version pin on
  shape changes; keep provenance (never overwrite originals).
