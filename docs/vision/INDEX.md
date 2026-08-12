# PĀṬALA VISION — INDEX

*2026-08-12. The canonical map of Pāṭala's vision/strategy/product docs. One place to see the whole
strategic picture. This index is the single gate for "what is the vision" — add any new vision doc
here and in `docs/INDEX.md`.*

---

## How to read this

- **Canonical** = read/trust for that concern.
- **THE CORE BIBLE (`docs/vision/CORE-BIBLE.md`) = the top-level map** — one vision chunked into 6
  zoomable layers (sentence → paragraph → graph → checkpoints → domain lenses → specs/gold/data). Start
  there for the whole picture, then zoom into any layer here.
- The vision unfolds as a **sequence (Vision 01 → 09)**. Read in order for the full arc.
- Each doc is its own file; none is superseded — they are complementary layers of one vision.
- Original, un-numbered strategy docs (NORTHSTAR, foundationalideas, positioningpartners) are
  canonical but sit outside the numbered sequence; they are cross-referenced below.

---

## The numbered vision sequence

| # | Doc | Focus (one line) |
|---|---|---|
| **01** | `docs/endgame1.md` | The translation-laboratory endgame — machine-assisted critical translation from witnesses to auditable publication. |
| **02** | `docs/endgame2.md` | Endgame Spec 2 — the **Tantra Hub**: living bibliography + text-reader + translation-workshop + commentary + media. The current destination reframe. |
| **03** | `docs/endgame3.md` | Endgame Spec 3 — **one scholarly knowledge infrastructure, several interfaces** (not separate projects). |
| **04** | `docs/endgame4.md` | Endgame Spec 4 — the **economic thesis**: scarce assets = source data + rights + provenance + expert judgment. |
| **05** | `docs/endgame5year.md` | Endgame Spec 5 — **2026–2031 strategic window** (manuscript digitisation money, IKS funding, DH, AI). |
| **06** | `docs/vision/vision-06-adversarial-review.md` | **Pāṭala Review** — adversarial scholarly review + the research compiler (scholar-facing API mega-product). *(new, from R2)* |
| **07** | `docs/vision/vision-07-new-scholar.md` | **The New Scholar** — workbench, perspective collector, research-graph scholarship. *(new, from R2)* |
| **08** | `docs/vision/vision-08-scholar-economics.md` | **Scholar Incentives & Economics** — paid adjudication, ORCID/CRediT credit, ownership. *(new, from R2)* |
| **09** | `docs/vision/vision-09-media-and-cross-tradition.md` | **The Media Layer & Cross-Tradition Engine** — the scholarly core rendered as shorts/video/essays/AI-teacher (Workengestation = written voice, Renderio = video), then reproduced across traditions (Tantra → Yogic → Vedānta → Greek). |
| **10** | `docs/vision/vision-10-market-entry-and-partnerships.md` | **Market Entry & Partnerships** — academic partners (BHU + global scholars), funding/fellowship sources, institutional models, outreach, low-cost pilots, legal/IP, metrics. *(new, from R2)* |
| **11** | `docs/vision/vision-11-siva-before-abhinava.md` | **Śiva Before Abhinava** — the genealogy of Śaiva ideas as the next major corpus: six chronological corpora (Rudra→Śiva→Pāśupata→Early Tantra→Bhairava/Kaula→Kashmir) + three cross-cutting graphs (concept, cosmology, argument), ending at Abhinavagupta and connecting into IPVV. *(new, from R2)* |

---

## The top-level map (start here)

| Doc | Focus |
|---|---|
| **`docs/vision/CORE-BIBLE.md`** | **THE CORE BIBLE** — one vision chunked into 6 zoomable layers (sentence → paragraph → graph → checkpoints → domain lenses → specs/gold/data). The top-level gate: read this, then zoom into any numbered vision below. |
| `machinelearning/_ACTIVE/PATALA-ENGINE-ROADMAP-12MO.md` | The 12-month philosophy-engine roadmap (the strategic reference; gold-first build order + 8 benchmark tasks + crux algorithm). |

## The three lenses (the human/tool/value folders)

| Lens | Folder | The vision viewed as… |
|---|---|---|
| **Functionality** | `docs/vision/functionality/README.md` | the tools + machinery + interfaces (the projections of one core) |
| **Scholars** | `docs/vision/scholars/README.md` | the human layer — the contributors whose judgment is the moat, and their new role |
| **Economics** | `docs/vision/economics/README.md` | the sustainability — scarce assets, funding channels, the flywheel |

Each folder assigns the existing docs (content untouched) + the relationships. They are the same vision
at Layer 4 of the CORE-BIBLE, seen through what we build / who does it / what sustains it.

---

## Map to the engineering checkpoint ladder (CP0–CP12)

The vision arc (above) is the *product/strategic* view; the checkpoint ladder
(`handover/CHECKPOINTS.md`) is the *engineering* view of the same work. Rough mapping:

| Vision | Checkpoints it lands on |
|---|---|
| 01 translation-lab / 02 Tantra Hub | CP1 (source proof) → CP6 (synthesis) |
| 03 one scholarly infrastructure | the whole ladder (CP0–CP12) |
| 04 economic thesis / 08 scholar economics | CP10–CP12 (collaborative + economic + cross-corpus) |
| 05 five-year strategic window | sequencing of CP1–CP6 |
| 06 Pāṭala Review (adversarial review) | CP5 (verification) + CP8 (adversarial review) |
| 07 New Scholar (workbench) | CP7 (workbench) → CP9 (API/MCP) |
| 11 Śiva Before Abhinava (cross-corpus genealogy) | CP1 (per-corpus source proof, reused) → CP12 (cross-corpus) |

**Where the live agent system tracks this:** `handover/SYSTEM.md` (template → instances) +
`handover/STATE.yaml` via `python3 handover/flow.py status`.

---

## The site spec (the concrete destination)

| Doc | Focus |
|---|---|
| `docs/ENDGAME_SITE_SPEC.md` | The Tantra Reader (essays.tantrafiles.xyz) — what the site is, what it renders, where each element comes from. Note: `endgame2.md` reframes this as the Tantra Hub. |

---

## Foundational / strategic (the deep vision, un-numbered)

| Doc | Focus |
|---|---|
| `docs/NORTHSTAR.md` | The strategic plan for a scholarly intelligence layer for tantric textual heritage (the 1.19cr-manuscript Gyan Bharatam context, positioning between layers). The deepest strategy doc. |
| `docs/foundationalideas.md` | The foundational idea: every artifact attaches to a stable passage/text identity (Bilara/immutable-segment precedent). |
| `docs/positioningpartners.md` | Positioning & partners — the connective research layer. |

---

## Development plans (the how, not the vision)

| Doc | Focus |
|---|---|
| `docs/nextdev.md` | The minimal formal primitives everything hangs off. |
| `docs/nextdev2.md` | Pāṭala development plan (forward). |
| `docs/DEV_PLAN.md` | Development plan (API-first, bibliography-first). |
| `docs/DEV_PLAN_AGNOSTIC_CONTRACT.md` | The agnostic-contract dev plan (ML lane). |

---

## ML / product-resolutions vision (the multi-resolution endgame)

| Doc | Focus |
|---|---|
| `machinelearning/VISION-COMPUTABLE-TRADITION.md` | The computable-scholarly-tradition vision (ORIGINAL/READ/GUIDE/STUDY/CRITICAL projections). |
| `machinelearning/MLVISION.md` | ML vision (big picture). |
| `machinelearning/EDUCATION_VISION.md` | The graph-native teaching engine vision. |
| `machinelearning/PATALA_AS_LIBRARY_ENGINE.md` | Pāṭala as the engine for the `.meta/` Library (4 wings as register-projections). |
| `docs/LEARNING_STRATEGY.md` | The learning/education strategy. |

---

## Update protocol

When you add a vision doc: give it the next `vision-NN-<topic>.md` number, add a header (title +
provenance + `see docs/vision/INDEX.md`), add it to this table, and add it to `docs/INDEX.md`. The
sequence and this index are the single source of truth for "what is the vision."
