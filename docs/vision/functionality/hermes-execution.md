# THE VISION × HERMES MAP — how the execution kernel realizes the Pāṭala vision

*2026-08-12. The mapping between the **canonical vision** (`docs/vision/`) and the **Hermes execution
kernel** (`handover/hermes/`). The thesis: **Hermes is Pāṭala's replaceable execution kernel; the vision is
what Pāṭala IS.** This doc shows which vision files Hermes operationalizes, and where *other* tech is still
needed. It is the bridge from the strategic vision layer to the execution lane.*

---

## THE MASTER MAPPING

| Vision doc / lens | What the vision says | How Hermes operationalizes it | Other tech needed (beyond Hermes) |
|---|---|---|---|
| **Vision 01 — translation lab** (`endgame1.md`) | machine-assisted critical translation, auditable | **A3 translation factory**: `kanban` + `cron` + `--worktree` + `patala-translate` skill (T1→L2→C1 via `pipeline/model.py`) | the L0 source floor (Agent 2's `verify_l0` — Pāṭala-owned) |
| **Vision 02 — Tantra Hub** (`endgame2.md`) | living bibliography + reader + workshop | Hermes `sessions`/`memory` for editorial state; MCP serves the hub | the site (Next.js) is Pāṭala-owned |
| **Vision 03 — one scholarly infra, many interfaces** | one evidence graph, several projections | **Hermes = one execution kernel under every projection** — the replaceable substrate | the epistemic graph (Pāṭala-owned) |
| **Vision 04 — economic thesis** (`endgame4.md`) | scarce assets = source + rights + provenance + expert judgment | Hermes is *infrastructure*, NOT the moat — it disappears; Pāṭala keeps the scarce assets | the scholar network + correction data (Pāṭala-owned) |
| **Vision 06 — Pāṭala Review** (`vision-06-adversarial-review.md`) | adversarial review + research compiler (the mega-product) | **A4 review scheduling** (kanban + cron + `patala_propose_review`) + **the executable-corrections loop** (`handover/hermes/PEER-REVIEW.md`) — machine pre-review compresses the paper; scholar Workbench is the surface | the review/dependency engine (Pāṭala-owned); the Workbench UI (Pāṭala-owned) |
| **Vision 07 — New Scholar** (`vision-07-new-scholar.md`) | the scholar works in the research graph (structured inquiry) | the **Scholar Workbench + AI copilot** (a constrained patala profile that can't accept/promote) | the workbench UI (Pāṭala-owned) |
| **Vision 08 — Scholar Economics** (`vision-08-scholar-economics.md`) | paid adjudication, ORCID/CRediT credit, ownership | ORCID crosswalk (review credit → ORCID); Contributor ID ↔ ORCID | ORCID/ROR/Crossref infra (external, interop) |
| **Vision 09 — Media layer** (`vision-09-media-and-cross-tradition.md`) | the core rendered as essays/video/AI-teacher | **A6 projection** skills (`publish`, etc.) render the graph | Workengestation / Renderio (external) |
| **Vision 10 — Market Entry** (`vision-10-market-entry-and-partnerships.md`) | BHU/global partners, funding, go-to-market | the executable-corrections dataset = a demo + funding metric ("63 Pratyabhijñā propositions reviewed") | the institutional network (external) |
| **Vision 11 — Śiva Before Abhinava** (`expansion/vision-11-siva-before-abhinava.md`) | the genealogy corpus | A3 factory + A2 corpus compiler ingest the new corpora | the source acquisition (Muktabodha/GRETIL — already on disk) |
| **The functionality lens** (`functionality/README.md`) | one core rendered as many interfaces | the execution kernel under all of it | — |
| **The scholars lens** (`scholars/README.md`) | "AI proposes, scholar adjudicates" | **the peer-review system IS this** (`PEER-REVIEW.md`) | — |

---

## THE THREE-VECTOR VIEW (how Hermes + vision + other-tech compose)

```
THE VISION (what Pāṭala IS)          THE EXECUTION (Hermes)          THE ECOSYSTEM (other tech)
─────────────────────────            ─────────────────────           ─────────────────────────
Vision 06 Review (mega-product)  ↔   A4 scheduling + corrections  ↔   OpenReview · Crossref · ORCID
Vision 07 New Scholar (workbench)↔   Scholar copilot profile      ↔   (Workbench UI = Pāṭala-owned)
Vision 01 Translation lab       ↔   A3 factory (kanban+cron)     ↔   L0 floor = Pāṭala-owned
Vision 03 one-infra-many-UI     ↔   the execution kernel          ↔   the epistemic graph = Pāṭala-owned
Vision 08 Scholar economics     ↔   review credit / trajectories  ↔   ORCID · ROR · Crossref
Vision 09 Media                 ↔   A6 projection skills          ↔   Workengestation · Renderio
Vision 04 Economics (the moat)  ↔   (disappears — infra)          ↔   scholar network + corrections = Pāṭala-owned
```

---

## WHERE OTHER TECH IS NEEDED (beyond Hermes — the Pāṭala-owned layer)

Hermes provides execution. Pāṭala must still build (these are NOT in Hermes, and they're the moat):

1. **The epistemic graph + ledger** (`data/corpus/`, `corpus_state.py`) — Pāṭala-owned.
2. **The source/proof floor** (`verify_l0.py`, the 63/63 IPVV + L0 for other works) — Pāṭala-owned.
3. **The review/dependency engine** — `ReviewEvent` as a graph mutation + downstream recomputation
   (`handover/hermes/PEER-REVIEW.md` Phase 3) — Pāṭala-owned.
4. **The Scholar Workbench UI** (Vision 07) — Pāṭala-owned.
5. **The MCP capability layer** (`patala_*` tools, PROPOSE-not-ACCEPT) — Pāṭala-owned.
6. **The executable-corrections dataset** (the moat) — Pāṭala-owned, from Hermes trajectories + ReviewEvents.

And the interop targets (external, integrate-not-build): OpenReview/Kotahi (review workflow), Hypothesis
(annotation), DocMaps/PReF (review-process interchange), COAR Notify (external events), ORCID/ROR (identity),
Crossref/DataCite (PIDs), OpenAlex/OpenCitations (global graph), JATS (article export).

---

## THE ONE-SENTENCE CARRY-FORWARD

**The Pāṭala vision is what the epistemic graph IS (Review, New Scholar, translation, media, economics);
Hermes is the replaceable execution kernel that operationalizes every vision projection (kanban, cron,
worktree, skills, sessions); and the moat — source floor, review/dependency engine, Scholar Workbench,
MCP capability layer, executable-corrections dataset — is the Pāṭala-owned layer built on top of both,
interoperating with the existing scholarly-infrastructure ecosystem rather than rebuilding it.**
