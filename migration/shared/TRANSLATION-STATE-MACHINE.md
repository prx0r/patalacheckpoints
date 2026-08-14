# WHAT TO BUILD — THE TRANSLATION-STATE MACHINE + THE INTERNAL TRANSLATION INVENTORY

*2026-08-14 · status: BUILD DIRECTIVE · the detailed spec for the per-work translation state machine and
the internal translation inventory — the piece that makes the factory autonomously process all works. This
fills ip-graph's gap: it has no record of which works have which translations.*

---

## WHAT OG PATALA ALREADY HAS (the real state)

**`pipeline/corpus_state.py`** — the per-work translation state machine:
```python
class WorkState:
    t1: str = "NOT_STARTED"   # NOT_STARTED | LEGACY_PRESENT | MODERN_PRESENT | PARTIAL
    l2: str = "NOT_STARTED"
    c1: str = "NOT_STARTED"
    ...
def next_valid_action(s: WorkState) -> dict:
    # LEGACY_T1_PRESENT -> MODERNIZE_L0
    # ... -> the legal next transition per work
```
- Tracks **111 works** through their lifecycle.
- Each work's state: `t1`/`l2`/`c1` = NOT_STARTED → LEGACY_PRESENT → MODERN_PRESENT.
- `next_valid_action(work)` = the single legal next transition (the control plane for Agent 3).

**The translation-state ledger** (`data/corpus/downloads/translation-state-ledger.json`):
- `works`: 111 entries, each with `work_id`, `bibliographic_id`, `source`, and per-layer state.

**The real internal translation inventory (what exists):**
| Inventory | Count |
|---|---|
| Translated `<work>.jsonl` (raw-EN, in `data/corpus/downloads/translations/`) | 71 works |
| T3 finals (the completed translations, in `sanskritree/translations/05_t3_final/`) | 11 works |
| T1 gold (the word-faithful glosses, in `sanskritree/.../ipvv/`) | 28 chunks |
| L200 proof audits | 63 |
| C1 commentaries | 63 |
| The Stk work (new, untranslated, 298 verses) | 1 |

---

## WHAT IP-GRAPH IS MISSING

- **No per-work translation state** — its organism has a `SanskritDoc.status` but not the granular
  `t1`/`l2`/`c1` per-layer tracking.
- **No inventory of which works have which translations** — it doesn't know 71 works are translated, 11
  are T3-final, 28 are T1-gold.
- **No transition logic** (NOT_STARTED → LEGACY_PRESENT → MODERNIZE_L0) — it just runs the loop.

---

## WHAT TO BUILD (the full factorial state machine)

### 1. Adopt OG patala's `corpus_state` as the per-work truth (in ip-graph's organism)

**What:** the `ingestion_organism` should track each work's per-layer state (`t1`/`l2`/`c1`) and use
`next_valid_action()` (from `corpus_state.py`) to decide the legal next transition — not just a flat
`SanskritDoc.status`.

**Why:** autonomy needs the granular state machine. `next_action.py` picks WHICH work; `next_valid_action`
picks WHICH TRANSITION.

### 2. Build the internal translation inventory (the "which translations exist" registry)

**What:** a machine-readable inventory of every work's translation assets:
```
work → t1 (gold/modern/none) → l2 (legacy/modern) → l200 (proof) → c1 (commentary) → t3 (final)
```

**Why:** this is the honest "what exists internally" that ip-graph lacks — the factory can't autonomously
process a work it doesn't know the state of.

### 3. The full factorial state machine (all works, autonomous)

**What:** extend `next_valid_action` to a complete per-work FSM covering ALL 111+ works:
```
SOURCE_PRESENT → T1 (NOT_STARTED → LEGACY_PRESENT → MODERN_PRESENT)
  → L0 (MODERNIZE_L0 if legacy T1)
  → L2 (LEGACY_PRESENT → MODERN)
  → L200 (the proof, only if L2 modern)
  → C1 (commentary)
  → T3 (the final, only when C1 + proof done)
  → COMPLETE
```

**Why:** this is the "full factorial state machine autonomously processing all works" — the thing you
specced. Each work advances through its legal transitions, gated by the review + integrity kernels, driven
by Hermes (the model) + `next_action` (the scheduler).

### 4. The state → ledger → graph bridge

**What:** the updated per-work state flows into the translation-state ledger, then into ip-graph's graph
(works.jsonl) so the site shows each work's honest translation state.

---

## THE ONE-LINE

> **Adopt OG patala's `corpus_state` (the per-work FSM: t1/l2/c1 → next_valid_action) into ip-graph's
> organism, so each of the 111+ works autonomously advances through its legal translation transitions
> (SOURCE → T1 → L0 → L2 → L200 → C1 → T3 → COMPLETE), gated by review + integrity + Hermes — with the
> internal translation inventory (71 jsonl, 11 T3, 28 T1, 63 L200, 63 C1) as the honest state the site
> serves.**

---

## THE BUILD DIVISION

| Build | Who |
|---|---|
| Adopt `corpus_state.next_valid_action` into `ingestion_organism` | agentpatala (has corpus_state) + agentgraph (organism) |
| The internal translation inventory registry | agentpatala (has the data) |
| The full factorial FSM (all works) | both |
| The state → graph → site bridge | both (agentgraph's build-static-site) |

---

*This is the translation-state build directive. OG patala has the real state machine + the real inventory
(71 translated, 11 T3, 28 T1, 63 proof, 63 commentary); ip-graph has the organism loop + the read plane.
The build wires the state machine into the organism so all works process autonomously.*
