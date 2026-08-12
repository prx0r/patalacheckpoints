# EXPANSION — the Śiva genealogy + corpus-acquisition lens

*2026-08-12. The vision docs about **expanding Pāṭala beyond the IPVV**: walking the braided history of
Śaiva ideas backward from Abhinavagupta, and acquiring the open, legally-available primary Sanskrit +
scholarly-translation corpus that makes that computationally tractable. This folder indexes (assigns,
does NOT rewrite) the existing docs under this lens. Companion to the Economics lens
(`docs/vision/economics/README.md`) and the numbered vision sequence (`docs/vision/INDEX.md`).*

---

## WHY THIS LENS MATTERS

The IPVV is the crown, but Abhinavagupta does not arise against a blank background. The durable question
Pāṭala can uniquely answer is **"How did the world of Abhinavagupta become possible?"** — and that
requires modeling the *genealogy of Śaiva ideas*, not a single lineage, and acquiring the corpus that
makes the question computable rather than speculative.

The key correction (from the vision): **there is no simple straight genealogy** (`Vedic Rudra → Śiva →
Pāśupata → Tantra → Abhinava`). The evidence gives a **braided history** — Vedic Rudra traditions,
emerging Rudra-Śiva theology, epic/Purāṇic religion, ascetic Pāśupata currents, lay Śivadharma,
Siddhānta/Mantramārga, Bhairava/Śākta systems, Kaula/Krama/Trika, and philosophical Kashmirian exegetes
repeatedly interacting and reorganizing one another. Early Śaivism itself was already plural.

## The corpus plan (the recoverable dependency network)

The computational chain (from the manifest):
```
Brahmayāmala (7th/8th c) ──► wider Vidyāpīṭha/Śākta substrate ──► Siddhayogeśvarīmata
                                                                    ├─► Mālinīvijayottara ─┐
                                                                    └─► Kālī/Krama ────────┴─► Abhinavagupta (MVV/Tantrāloka)
                                                                                                 ├─ Pratyabhijñā: Somānanda → Utpaladeva → IPVV
                                                                                                 └─ Bhairava: Svacchanda / Netra
```

**Build order (NOT historical chronology — bootstrap on existing human gold first):**
```
TIER 0  INGEST EXISTING HUMAN GOLD   SYMT (Törzsök), MVT (Vasudeva), Tantrasadbhāva (Bang),
                                     Brahmayāmala (Hatley/Kiss), Śivadṛṣṭi 1-3 (Nemec), Kiraṇa (Goodall), Niśvāsa
TIER 1  INGEST COMPLETE SANSKRIT     Svacchanda+Ks, Netra+Ks, Kubjikāmata, Kālīkulapañcaśatikā, Kramasadbhāva,
                                     Devīdvyardhaśatikā, Mahānayaprakāśa, Śrīkhacakrapañcakastotra, Śivadṛṣṭi, MVV
TIER 2  TRANSLATE THE HOLES          Kālīkulapañcaśatikā, Kramasadbhāva, remaining MVV/Śivadṛṣṭi/Tantrasadbhāva, Svacchanda, Netra
TIER 3  MANUSCRIPT-SCALE FLAGSHIPS  Jayadrathayāmala, remaining Brahmayāmala, Devyāmala
```

**The key insight:** a ready-made electronic **Krama corpus** already exists (Muktabodha/INDOLOGY:
Kālīkulapañcaśatikā + Kramasadbhāva + Devīdvyardhaśatikā + Mahānayaprakāśa + Jñānanetra). Ingesting the
Krama packet first establishes terminology, ontology, deity graph and translation memory — so when Pāṭala
hits the 24,000-verse Jayadrathayāmala, it already knows the Krama language.

## The acquisition ethics (from the manifest)

- **Open/legal only.** Every entry is a verified freely-accessible scholarly edition/translation, or a
  public-domain scan/transcription. Unauthorized recent-book piracy mirrors are **excluded**.
- **Do not re-translate what human scholars already covered.** e.g. Brahmayāmala chapters 1–3/21/39–40/
  45–46/55/73/83/99 already have critical editions/translations — those are *existing human gold*, not a
  translation frontier.
- **License-aware.** Commercial editions (e.g. Nemec's Śivadṛṣṭi, Dyczkowski's Manthānabhairava) are
  referenced but not pirated; prioritize free primary infrastructure first.

## The EXPANSION docs (assigned, canonical originals untouched)

| Doc | Focus |
|---|---|
| `vision-11-siva-before-abhinava.md` | **The vision** — the genealogy of Śaiva ideas as the next major corpus (six chronological corpora + three cross-cutting graphs: concept, cosmology, argument). |
| `vision-11-siva-before-abhinava-corpus-manifest.md` | **The acquisition plan** — the open-source inventory (15 works) + the tiered build order + the request for a machine-readable download manifest (canonical_id, Sanskrit URL, translation URL, format, chapters, edition, date, citations-in-Abhinava, status). |

## How this connects to the current work

The 63/63 IPVV source floor is exactly the machinery reused to ingest these corpora: the L0 adapter +
`verify_l0.py` (proven format-agnostic on two IPVV formats) + the L200 audit + the vertical-object chain.
The first *second* work ingested here is what actually demonstrates cross-work generalization (the honest
caveat recorded in CLAIMS.md P-001). The genealogy maps to CP12 (cross-corpus).

## The on-disk corpus (what we already have — 2026-08-12)

Most of the śiva corpus is **already on disk**, not just in the plan. The ref-able indexes:

- **`data/corpus/downloads/siva-corpus-inventory.json`** — 15 L0-able `_stack/` works (kramasadbhava
  VALID 563, kubjikā T1-unvalidated, sivasutra through C1, etc.) + the source libraries (Muktabodha 500,
  round2/3, gretil) + the translation-pipeline state.
- **`data/corpus/downloads/siva-corpus-download-manifest.json`** — the 15 works with source/translation
  URLs + status.
- **The compiled corpus-targets DB** — `data/corpus/targets/` (sources.json, targets.json, leads.json,
  anchors.json, index.json) built by `pipeline/build_corpus_targets_db.py`, with the master map in
  **`docs/corpus/TARGETS-INDEX.md`** (the one-place index of every target, lead, source, and the two
  goldmine docs).
- The **untranslated registers** (`corpus/targets/untranslated.md`, `untranslated2.md`,
  `untranslated3.md`, `targetacquired.md`) are the ranked, on-disk-vs-[ACQ] translation roadmap.

**THE TWO GOLDMINE DOCS (read before translating/acquiring):**
- `sanskritree/corpus/targets/canonical_reference_map.md` — the master substrate: taxonomy/timeline,
  the canonical corpus with ingestion waves, **the semantic-shift glossary** (the fix for cross-work term
  misreading), the auditable translation architecture, the 18-month roadmap.
- `sanskritree/corpus/targets/markguidance.md` — the Recognition Enquiry: passage dossiers, the A/B/C
  thesis levels, cross-tradition mapping (the argument-layer goldmine).

**Cross-work L0 finding (honest):** a legacy T1 (kramasadbhāva) extracts via the shared tool (209
tokens) and passes `verify_l0.py` with 0 overlaps/fragments/dups, but full P0 needs a small
editorial-classification extension for the mixed raw-verse+gloss+metadata format — the exact seam
P-001 flagged. This is the seam the autonomous-translation agent (agent3) must address when built.

---

## THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala's expansion is the genealogy of Śaiva ideas — walking backward from Abhinavagupta through a
braided history (not a single lineage), bootstrapping on existing human scholarly gold (SYMT/MVT/
Tantrasadbhāva/Brahmayāmala/Śivadṛṣṭi), then ingesting complete open Sanskrit corpora (the Krama packet
first), then translating the high-leverage holes — so that the question "How did the world of Abhinavagupta
become possible?" becomes computable, using the 63/63 source-integrity machinery already built. Next
concrete step: turn the manifest into a machine-readable download manifest the repo can pull automatically.**
