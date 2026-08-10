# Endgame Spec — the Tantra Reader (essays.tantrafiles.xyz)

*The destination. Not to be built now — compiled at the end from the pipeline's outputs. This spec fixes WHAT the site is, WHAT it renders, and WHERE each element comes from, so the translation work we do today already produces the site's content. **See also `docs/endgame2.md` — the revised spec (2026-08-10) reframing the destination as the "Tantra Hub" (the living bibliography + text-reader + translation-workshop + commentary + media), with the FoJin-comparison and the machine-facing/stable-ID plan.***

## 1. The vision

A reader for the tantric corpus with three interlocking layers per text:

1. **The Reader** — the translation, segment by segment (Bilara-style): Sanskrit / translation / notes / alternatives / corpus evidence / glossary.
2. **The Master Map** — the text's internal architecture (the Tantrāloka-map pattern: per-āhnika/per-chapter systemic function, problems, doctrinal target, dependencies, outputs).
3. **The Workbook** — the learning resource (the Tantrāloka-workbook pattern: cumulative units, one escalating question each, three-column method, checkpoints).

Overlaid on all three: **the Reference Map as an interactive graph** — tradition × period × geography nodes with the lemma-trajectories (kula, krama, khecarī...) as edges. Click any term in any translation → its dossier → its loci → the passages.

## 2. The five levels of authority (from the reference map)

| Level | Records | Canonical status |
|---|---|---|
| Source | Sanskrit as in the identified edition/e-text | Immutable snapshot (the concordance corpus) |
| Passage | Stable segment ID (`JKK.2.5`, `KRH.1.1`...) | Immutable identifier |
| Translation | Our present best rendering | Versioned, revisable (T1→T2→T3) |
| Sense | "What kula means here" | Evidence-backed hypothesis (the dossier) |
| Synthesis | "How kula evolved across traditions" | Versioned scholarly reconstruction (the semantic-shift atlas) |

No confidence-percentages. Statuses instead: `verified / citation_corrected / OPEN / not-found` (the FoJin trust-states, adapted).

## 3. What each page renders, and where it comes from

### 3.1 The Reader (per text)
```
┌──────────────────────────────────────────────┐
│  KAULARAHASYA 2.3                            │
│  Sanskrit      [from the e-text, immutable]  │
│  Translation   [T3-FINAL]                    │
│  Notes         [R2's reasoning chain]        │
│  Alternatives  [T2's forks, OPENs]           │
│  [show corpus evidence]  ← concordance query │
│  [glossary]     ← dossier                    │
└──────────────────────────────────────────────┘
```
**Built from:** the T1→T3 files (the translation + the R2 chains + the T2 forks), the concordance (the evidence panel), the dossiers (the glossary popups).

### 3.2 The Master Map (per text)
The Tantrāloka-map template applied to each translated text:
- **Systemic function** — the text's role (e.g. the Kaularahasya: the vāma-mārga's self-defense + the dīkṣā-theology).
- **Internal problems** — the cruxes the R1/R2 flagged.
- **Doctrinal target** — the T3's core claims.
- **Dependencies** — the texts it cites (the Kulapradīpa→Kulārṇava-intertext), the traditions it belongs to.
- **Outputs** — the verse-indexed tables the R2 produces.

**Built from:** the R1/R2 verdicts + the C1 interpretations + the reference map's per-tradition placement.

### 3.3 The Workbook (per text or per tradition)
The Tantrāloka-workbook template:
- Cumulative units, one escalating question each.
- The three columns: what the text claims / what our pipeline established / what remains unproven (the OPENs).
- Checkpoints before moving on.

**Built from:** the C1 plain-English interpretations + the T3 + the reference map's timeline (period, geography, tradition).

## 4. The Reference Map as the connective tissue

The `corpus/targets/canonical_reference_map.md` becomes the site's interactive graph:
- **Nodes:** texts (our translated corpus), traditions (Trika/Krama/Kubjikā/Kaula/Pratyabhijñā/Sarvāmnāya), periods (the 9th–13th-c. timeline), geographies (Kashmir/Oḍḍiyāna/Nepal).
- **Edges:** the lemma-trajectories (kula: lineage→body→totality→Kubjikā-mantra-body→Abhinava's akula-pole), the citations, the semantic shifts.
- **Behavior:** every glossary popup in the Reader is a node in this graph; every parallel in the concordance is an edge.

**Built from:** the report's taxonomy + our concordance's cross-text links + the dossiers we accumulate per lemma.

## 5. The data model (what the pipeline must leave behind)

Per segment (verse/passage), the site needs:
```text
segment_id      JKK.2.5
work            Jñānakārikā
tradition       Kaula (Matsyendra-school)
period          ≤11th c.
sanskrit        [immutable from the e-text]
translation     [T3, versioned]
alternatives    [T2 forks + OPENs]
notes           [R2 reasoning chain]
status          verified / citation_corrected / OPEN / not-found
glossary_refs   [krama → dossier → loci]
parallels       [concordance hits → passage ids]
```
This is exactly the v2 DB schema (passages, translations, alignments, lexical_senses, sense_evidence) + the concordance. **The site is a rendering of the DB; the DB is populated from the markdown by the (future) ingest script.**

## 6. Tech sketch (compile-time only, not now)

- **Data:** the R2 bucket hosts the raw e-texts + the site's JSON (segment-index). The v2 SQLite DB (or a JSON export of it) is the canonical compiled artifact.
- **Static-first:** the site can be a statically-generated renderer (Cloudflare Pages, like tantrafiles-hub already is) — no server needed except the read-only API for comments/annotations.
- **Reader view:** Bilara-style segment rendering from the JSON.
- **Graph:** the reference map rendered client-side (the report's mermaid trajectories → an interactive graph library).
- **Search:** the concordance's index (JSON/SQLite-FTS) powers the evidence panel and the cross-text search.

## 7. What the translation work must keep doing (the site's supply chain)

1. **Translate** (T1→T3) with the concordance for term-evidence → produces the Reader's content.
2. **Adjudicate** (R1/R2) → produces the Notes, the Alternatives, the OPENs, the Master-Map problems.
3. **Interpret** (C1) → produces the Workbook's plain-language units.
4. **Dossier** each lemma as we go (term → our attestations → the report's senses → working policy) → produces the glossary + the graph's edges.
5. **Keep STATUS.md** → the site's "what's translated / what's next" index.

The site is compiled at the end from these five outputs. No web building until the content exists.

## 8. The endgame checklist (compiled when ready)

- [ ] All Hop-1 T3s + the R2-chains (the Reader content)
- [ ] The C1s for each T3'd text (the Workbook content)
- [ ] A Master Map per translated text (the Tantrāloka-map pattern)
- [ ] The dossiers for the core lemmas (kula, krama, khecarī, śakti, visarga...)
- [ ] The concordance index exported (the evidence panels)
- [ ] The reference map's graph data (the interactive sidebar)
- [ ] The compile-script (markdown + DB → site JSON)
