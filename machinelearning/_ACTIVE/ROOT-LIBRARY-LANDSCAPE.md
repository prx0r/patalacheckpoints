# ROOT LIBRARY & META-DOCS — the landscape (and the one real gap)

*2026-08-12. A survey of the root-level library + meta docs that were already in the repo (some from
other sessions, some from R2): `onboarding/`, `skills/`, `docs/vision/`, `apideas.md`,
`research-library/pushing`, `docs/INDEX.md`. The question: how does this connect to the live agent
system (`AGENTS.yaml` template→instances, `STATE.yaml`, `flow.py`) we built in `handover/`?*

---

## 1. WHAT'S ALREADY THERE (the landscape)

| Piece | What it is | Status |
|---|---|---|
| **`onboarding/README.md`** | a staged read: STAGE 0 gate (doctrine) → 1 vision → 2 map → 3 full system → the specialization gate (L0 vs ML) | solid, existing on-ramp |
| **`skills/`** (7 SKILL.md) | Claude-style agent skills: `translate-passage`, `translate-work`, `assemble-stack`, `write-commentary`, `validate-passage`, `push-text`, `use-api` — each a named workflow a model can load | real workflows, each with the epistemic rules baked in |
| **`docs/vision/` + `docs/endgame*.md`** | the numbered vision arc (Vision 01–08: translation-lab → Tantra Hub → one scholarly infrastructure → economics → 5-year → **Pāṭala Review → New Scholar → Scholar Economics**) + foundational strategy (NORTHSTAR, foundationalideas, positioningpartners) | the strategic north star |
| **`docs/INDEX.md`** | the flat canonical reference — the single source of truth per concern; flags `[ARCHIVED]` | the canonical map |
| **`apideas.md`** | the Tantra Hub research API proposal (stable IDs, translation registry, provenance envelope) | a product proposal |
| **`research-library/pushing/`** | the pushing/enquiry work (the Logicvid method, truth-packets) | the discovery engine |
| **`experiments/`** | per-work pushing milestones (e.g. kramasadbhava 1.8) | active work |

---

## 2. THE ONE REAL GAP (honest finding)

**The `skills/` system and the `docs/vision/` arc are NOT wired into the live agent system we built in
`handover/`.** Specifically:

1. **`docs/INDEX.md` + `onboarding/` do not reference the agent system** (`AGENTS.yaml`, `STATE.yaml`,
   `flow.py`, `handover/SYSTEM.md`). A new agent following `onboarding/` would not know the live
   checkpoint flow exists.
2. **The `skills/` SKILL.md files are not connected to the live state.** They are static workflows — a
   skill like `translate-work` describes the T1→C1 flow, but nothing tells an agent "run this skill,
   then update CP1 via `flow.py`."
3. **The vision arc and the checkpoint ladder are two separate maps** — `docs/vision/INDEX.md` (Vision
   01–08, product/strategic) and `handover/CHECKPOINTS.md` (CP0–CP12, engineering). Both are real; neither
   references the other.

**The insight:** the repo has TWO parallel meta-layers that don't meet:
```
LAYER A (the scholarly product):  vision docs → skills (workflows) → pushing → the corpus
LAYER B (the agent system):       AGENTS.yaml → instances → STATE.yaml → flow.py → checkpoints
```
They describe the SAME work from two sides (what to do vs. who does it + track it), but nothing joins them.

---

## 3. WHY THIS MATTERS (the connection to our work)

The `skills/` system is actually **the natural payload of the agent system.** Our live instances
(agent1/agent2) are the *who*; the skills are the *how*; the vision arc is the *why*. A full system joins
them:
```
VISION (docs/vision + VISION_AND_NAVIGATION)   why
   ↓
SKILLS (skills/*.SKILL.md)                      how — the workflows an agent runs
   ↓
AGENT SYSTEM (instances + STATE.yaml + flow.py) who + tracked progress
   ↓
CHECKPOINTS (CP0–CP12)                          what's left, measured
```

---

## 4. THE MINIMAL INTEGRATION (no overengineering — just close the gap)

The honest, cheap move is NOT to rewrite anything — it's to **make the two layers reference each other**:

1. **`docs/INDEX.md` + `onboarding/README.md`**: add one line pointing at `handover/SYSTEM.md` + the
   live flow (`flow.py status`), so a new agent knows the checkpoint system exists.
2. **Each `SKILL.md`**: add one `metadata.hermes` line noting which checkpoint the skill advances (e.g.
   `translate-work` → CP1, `push-text` → CP4, `write-commentary` → CP3). No behavior change — just a join.
3. **`docs/vision/INDEX.md`**: add one line mapping the vision arc to the checkpoint ladder
   (e.g. Vision 06 Pāṭala Review → CP5/CP8, Vision 07 New Scholar → CP7).
4. **`handover/CHECKPOINTS.md`**: add a "see also" note pointing at the skills + vision arc.

**That's it.** Four one-line joins, no new architecture, no dependencies. It makes the existing system
coherent without overengineering — and it's exactly what the doctrine wants (each layer names what it
advances).

---

## 5. WHAT I AM NOT PROPOSING (the overengineering to avoid)

- **Not** building a skill-loader/registry into `flow.py` (the skills are Claude-style SKILL.md, loaded
  by the model; they don't need our tooling).
- **Not** merging the vision arc into the checkpoint ladder (two legitimate maps, one product one
  engineering).
- **Not** routing skills through STATE.yaml (skills are static workflows, not checkpoint progress).

---

## 6. THE ONE-SENTENCE CARRY-FORWARD

**The repo already has two mature parallel meta-layers — the scholarly product (vision docs + skills +
pushing) and the agent system (template→instances + STATE.yaml + flow.py) — and they describe the same
work but don't reference each other. The minimal, non-overengineered fix is four one-line joins
(docs/INDEX + onboarding point to the agent system; each SKILL.md names its checkpoint; the vision index
maps to the CP ladder; CHECKPOINTS.md points at the skills). The skills are the natural payload of the
agent system — joining them costs nothing and makes the whole thing coherent.**
