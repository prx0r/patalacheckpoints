# FUNCTIONALITY — the tools & product layer of the vision

*2026-08-12. The vision docs about **what Pāṭala builds and does**: the machinery, the interfaces, the
product projections of one scholarly core. This folder indexes (assigns, does NOT rewrite) the existing
docs under this lens — the functional capabilities and how they relate to the scholarly core, the
scholars who use them, and the economics that sustain them.*

---

## WHY THIS LENS MATTERS

Pāṭala's functionality is **one scholarly core rendered as many interfaces** (Vision 03) — NOT a pile of
separate apps. Every tool is a projection of the same evidence graph. The functionality folder is the
map of those projections and the machinery that powers them.

---

## THE FUNCTIONAL LAYERS (the projections + the machinery)

### The machinery (the core that powers everything)
| Function | Canonical doc | What it is |
|---|---|---|
| **The scholarly factory** | `onboarding/README.md` (Stages) + `THE_COMPANION.md` | Sanskrit → proof → translation → C1 |
| **The discovery engine (Pushing)** | `skills/push-text` + `research-library/pushing/` | hound a text with "why" to find its arguments |
| **The Philosophy IR** | `machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md` | argument-under-interpretation (the heart of CP4–5) |
| **The ML layer** | `handover/agent-1-ml/ML-MECHANICS-REFERENCE.md` | benchmark, retrieval, extraction, the Nyāya gate |
| **The skills (workflows)** | `skills/*/SKILL.md` (7) | translate-work, write-commentary, push-text, validate-passage, ... |
| **The agent system** | `handover/SYSTEM.md` + `AGENTS.yaml` | who does it + tracked progress (template→instances) |

### The interfaces (the product projections)
| Projection | Canonical doc | What it is |
|---|---|---|
| **The translation lab** | `docs/endgame1.md` | machine-assisted critical translation |
| **The Tantra Hub** | `docs/endgame2.md` + `ENDGAME_SITE_SPEC.md` | living bibliography + reader + workshop + commentary + media |
| **Pāṭala Review (adversarial)** | `docs/vision/vision-06-adversarial-review.md` | attack a thesis; the research compiler |
| **The New Scholar workbench** | `docs/vision/vision-07-new-scholar.md` | structured inquiry in the research graph |
| **The Media layer** | `docs/vision/vision-09-media-and-cross-tradition.md` | essays / shorts / video / AI-teacher (Workengestation + Renderio) |
| **The API / MCP** | `apideas.md` + `machinelearning/mcp` | machine access to the scholarly intelligence |

### The foundations (the invariants everything hangs on)
| Function | Canonical doc | What it is |
|---|---|---|
| **Stable identity** | `docs/foundationalideas.md` | every artifact attaches to a passage ID |
| **Provenance** | `docs/endgame4.md` §8-10, `docs/endgame5year.md` | claim → translation → Sanskrit → manuscript witness |

---

## HOW THIS LAYER RELATES TO THE OTHERS (the interdependencies)

```
THE SCHOLARLY CORE (the truth)      ←  the spine every tool renders (Layer 2 of CORE-BIBLE)
    ↕
FUNCTIONALITY (the tools)           ←  the projections + machinery
    ↕
SCHOLARS (the human layer)          ←  the tools give scholars the workbench; scholars give the data
    ↕
ECONOMICS (the sustainability)      ←  tools + scholar data → revenue → more tools + fellowships
```

**The rule (from the anti-weeds doctrine):** every piece of functionality must resolve to a grounded
claim. A tool that renders content which can't trace to the source is theater regardless of how
polished. Functionality serves the scholarly core; it never replaces it.

---

## THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala's functionality is one scholarly core rendered as many projections — the machinery (factory,
pushing, philosophy-IR, ML, skills, agent system) and the interfaces (translation lab, Tantra Hub,
Pāṭala Review, New Scholar workbench, media layer, API/MCP) — where every tool is a projection of the
same evidence graph, every tool gives the scholars the workbench that produces the expert data, and no
tool is allowed to render content that doesn't resolve to the source.**
