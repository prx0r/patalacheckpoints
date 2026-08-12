# THE VISION & NAVIGATION — start here (for any new agent)

*2026-08-12. The single entry point. It gives the VISION (what we're building and why), the LOGICAL
PROGRESSION (in what order the ideas unfold), and the NAVIGATION (where everything lives). Read this
first; it tells you which docs to open and in what order. `docs/INDEX.md` is the flat reference; this
is the map with a compass.*

---

## 1. THE VISION (one paragraph)

We are building a **computable scholarly tradition**: a single evidence graph over Sanskrit sources
(source → translation → decision → commentary → theme → claim → essay → pedagogy), where every layer
is machine-queryable, every claim resolves to its source, and any reader — scholar or beginner — can
enter at the depth they need. The IPVV (Abhinavagupta's Vivṛtivimarśinī) is the flagship; the
architecture is agnostic and generalizes to any text (Tantra now, then Yogic/Vedānta, Buddhism/Greek/
Nyāya later). **One trustworthy scholarly core, rendered as many media projections** (essays, shorts,
video, AI-teacher) — see Vision 09.

The two engines that make it real:
- **PUSHING** — mechanically hound a text with "why" to expose its deepest arguments (the discovery).
- **LOGICAL ARGUMENTS AS GOLD** — turn those penetrations into auditable, strength-graded
  truth-packets (the formalization), which essays cite and learning teaches.

## 2. THE LOGICAL PROGRESSION (the order of ideas)

Read these in order — each builds on the last:

```
STEP 1 — THE CORPUS (the substrate)
  49 IPVV passages, source + L2 + C1 + themes, published in Pāṭala.
  → docs/PHASE1_IPVV_CORPUS_PROCESS_NOTES.md + machinelearning/IPVV-STACK-INTEGRATION.md

STEP 2 — THE VERIFICATION FLOOR (make it trustworthy)
  /api/resolve + /api/verify/* — every claim resolves; nothing unanchored is served.
  → docs/INDEX.md (the map) + the API routes

STEP 3 — THE HUB (organize by source)
  Every primary source tracks ALL its outputs (essays, arguments, pushing, learning).
  → machinelearning/COMPOUNDING_RESEARCH_SYSTEM.md + data/corpus/hub.ts

STEP 4 — PUSHING (the discovery engine)
  How to deep-dive a text mechanically. The question-DNA + the agent spec.
  → ../research-library/pushing/PUSHING_GUIDE.md + AUTONOMOUS_PUSHING_AGENT_SPEC.md
    + QUESTIONNAIRE_REAL_DNA.md

STEP 5 — COMPARATIVE (ask every text the same deep questions)
  The agnostic core + tradition modules → a cross-text comparative matrix.
  → ../research-library/pushing/SPEC_COMPARATIVE_PUSHING.md

STEP 6 — LOGICAL ARGUMENTS AS GOLD (the formalization)
  Penetrations → auditable, strength-graded truth-packets → essays.
  → machinelearning/SPEC_LOGICAL_ARGUMENTS_GOLD.md + SPEC_ARGUMENT_TRUTH_PACKET.md
  → (deepened) machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md — the CP4 target: the
    philosophical IR (Commitment, derivational Proposition, ResearchQuestion, frame, alignment,
    regime), built gold-first so the ontology is forced by evidence, then evaluated multi-way
    (ASPIC / Nyāya / semantic / formal) under a profile.

STEP 7 — THE ML LAYER (make it learnable + verifiable)
  Benchmark → retrieval baselines → the THEMES experiment → vertical fidelity.
  → machinelearning/MLUSEINPATALA.md + DEVPLAN.md + SPEC_CONSOLIDATED_BUILD.md

STEP 8 — THE PRODUCT VISION (the multi-resolution endgame)
  ORIGINAL/READ/GUIDE/STUDY/CRITICAL — one graph, many projections.
  → machinelearning/VISION-COMPUTABLE-TRADITION.md + MLVISION.md

STEP 9 — THE MEDIA LAYER + CROSS-TRADITION ENGINE (Vision 09)
  The scholarly core rendered as shorts/video/essays/AI-teacher (Workengestation = written voice,
  Renderio = video), then reproduced across traditions (Tantra → Yogic → Vedānta → Greek) —
  same machinery, new content each time.
  → docs/vision/vision-09-media-and-cross-tradition.md
```

## 3. THE NAVIGATION (where everything lives)

| Home | What it holds | Canonical entry |
|---|---|---|
| **Pāṭala repo** (`/root/projects/patala`) | the site/app: data model, API, reader, MCP, ML strategy | `README.md` → `docs/INDEX.md` |
| **Sanskritree specs** (`.../_stack/ipvv/specs/`) | the scholarly factory specs + full onboarding | `THE_COMPANION.md` |
| **Research-library** (`/root/projects/research-library`) | the essays, the PUSHING method, the comparative work | `pushing/PUSHING_GUIDE.md` + the essays in `recognition/` |

**The three docs every agent MUST read first (in order):**
1. **This file** (the vision + progression).
2. **`docs/INDEX.md`** (the flat canonical reference — the single source of truth per concern).
3. **`THE_COMPANION.md`** (sanskritree) — the full-system technical onboarding.

> **Then, to see the whole vision as one zoomable map:** `docs/vision/CORE-BIBLE.md` — one vision
> chunked into 6 layers (sentence → paragraph → derivation graph → checkpoints → domain lenses →
> specs/gold/data). Every vision doc is a zoom-level of that ONE core, not a separate product.

## 4. THE TWO TRACKS (context engineering)

There are two agents (see `machinelearning/DUAL_AGENT_TRACK.md` and the operational
`machinelearning/CONTEXT_ENGINEERING.md`), and they SHARE the vision context until the
specialization splits near the end:

```
SHARED CONTEXT (both agents, the foundation)
  This vision file · docs/INDEX.md · THE_COMPANION.md
  The corpus (PHASE1 notes) · the hub · the verification floor
     ↓  (the split point — after the substrate, the lanes diverge)
AGENT 1 — ML/RESEARCH                AGENT 2 — INTEGRATION/CONTENT
  owns: MLUSEINPATALA, DEVPLAN,        owns: hub, PUSHING, comparative,
  benchmark, retrieval, experiments,   logical-args specs, the reader,
  vertical-fidelity, mllogical         API/MCP, the essays, the Sanskrit
```

The shared context is everything up to STEP 3 (corpus + verification + hub). After that, each agent
goes deep on its own lane, meeting again at the comparative matrix + the argument truth-packet.

## 5. THE REVIEW CHECKLIST (what a new agent should verify)

- [ ] You can state the vision in one paragraph (§1).
- [ ] You know the 8-step progression and where each step lives (§2).
- [ ] You've read the 3 must-read docs (§3).
- [ ] You know which lane you're on (ML vs integration) and what you own (§4 + DUAL_AGENT_TRACK.md).
- [ ] You know the current state (what's done vs pending) — see `docs/INDEX.md` + the audit.

---

*This file is the compass. `docs/INDEX.md` is the map. Read this, then the map, then go deep on your
lane.*
