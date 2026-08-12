# PĀṬALA CORPUS TARGETS — the master index (the consolidated goldmine)

*2026-08-12. The one-place map of every translation target, lead, source, and scholarly reference across
patala + sanskritree. This consolidates the formerly-scattered docs (the `corpus/targets/*` mess, the
`truth/` leads, the `ref/` logic, the `sources/round{2,3}/` manifests, the `_meta/` audits) into a queryable
structure + links to every original. **Agents: read this before translating or acquiring anything.**

---

## THE DATABASE (machine-readable, built from the scattered docs)

`pipeline/build_corpus_targets_db.py` compiles everything into `data/corpus/targets/`:

| File | What | Contents |
|---|---|---|
| `sources.json` | downloaded source files | 64 files from sources/round{2,3}/ + gretil2/ + root |
| `targets.json` | actionable RAW-L0 targets | 21 works, prioritized (Krama packet first) |
| `leads.json` | register I/II/III leads | 39 tracked leads (the untranslated registers + acquisition board) |
| `anchors.json` | translation anchors/status | 16 from translation_status_audit.md (which texts already have English) |
| `index.json` | master doc index | 26 source docs + their links + existence |

Query: `python3 pipeline/agent3_queue.py --registry` (targets) · `--leads` (leads) ·
`python3 pipeline/audit_translation_pipeline.py` (existing T1/R1/T2/R2/T3/C1 works).

---

## THE TWO GOLDMIINE DOCS (read these first — they are the substrate)

> **Imported to patala (2026-08-12):** the goldmine + method docs now live locally in `docs/corpus/` so
> agents read the copied version, not the mount. The sanskritree originals remain the record (never edit
> them); the local copies are the read-first references. Also imported: `translation_atlas.md`,
> `tradition_anchors.md`, `translation_flow_spec.md`, `leapfrog_guide.md`, `leapfrog_map.md`,
> `atlasflaws.md`.

### 1. `docs/corpus/canonical_reference_map.md` (the MASTER substrate, 1355 lines)
The single most important reference for the autonomous translator. Contains:
- **Taxonomy & timeline** — the Trika/Krama/Kubjikā/Kaula/Spanda/Pratyabhijñā/Sarvāmnāya ecosystem, as a
  *network with transfer-nodes*, not six separate schools.
- **The canonical corpus** — anchors (A+), expansion (A), frontier (B) with ingestion priority.
- **The ingestion waves** (the precise order): Semantic anchors → Krama core → Kubjikā root → Kubjikā
  expansion → Bridge layer → Large syntheses → Sarvāmnāya.
- **THE SEMANTIC-SHIFT GLOSSARY** — the fix for cross-work term misreading: *kula, akula, krama, śakti,
  spanda, vimarśa, parāmarśa, prakāśa, visarga, anuttara, khecarī, mālinī, mātṛkā, svātantrya*... each with
  tradition/period sense + evidence + semantic warning. **Do not build a single "Tantric dictionary"; build
  an evidence graph where a lemma has different senses per text/tradition/period.**
- **The auditable architecture** — Bilara's immutable segment IDs; "recoverability" not "87% confidence";
  the concordance-first tooling; the tool map (Muktabodha/GRETIL/Vidyut/Heritage/DCS/Ambuda/Bilara).
- **The 18-month roadmap** to a versioned canonical reference (library → atlas → timeline → glossary →
  semantic atlas → evidence graph → explainers).

### 2. `docs/corpus/markguidance.md` (the Recognition Enquiry — the argument-layer goldmine, 253 lines)
The philosophical-research substrate (feeds Agent 1 / the argument layer, not just translation):
- **Passage dossiers** with the A/B/C thesis levels: **A** reflexive presence (prakāśa-vimarśa) ·
  **B** diachronic subjectivity & memory-ownership · **C** universal identity (the contested frontier).
  "A does not automatically entail B, B does not entail C."
- **The decisive passages**: ĪPK 1.4.4-8, 1.5.11-14, 1.6.3-8, 1.7.3-6, 2.4.14-19; Ajaḍapramātṛsiddhi 9-17,
  22-26; Vākyapadīya 2.19, 2.143-152, III.3; Tantrāloka 5.62-63, 9.154-205, 10.108; Spandakārikā.
- **Cross-tradition mapping** (which tradition advances which question), **the status-tag discipline**
  (T text / R reconstruction / E empirical / C comparison / H hypothesis / X contested), and **the
  50-70 verse passage-book deliverable**.
- **The gaps** (epistemic-to-ontological slide, memory-argument strength, universalization, status of
  relation, process vs witness) — exactly the places specialists push back.

### 3. `docs/corpus/sivaqueue-translation-guide.md` (the SECOND corpus — "Śiva before Abhinava", 425 lines)
The **untranslated-Śaiva translation guide**, researched as a distinct second corpus beyond the
Kaula/Kubjikā/Trika/Krama census. Source: R2 `sanskritree/sivaqueue` (2026-08-12). Contents:
- **100 untranslated Śaiva targets** with honest status labels (**U** no English translation · **P**
  partial · **EN-gap** French/other exists · **U?** verify before claiming first translation), across the
  Pāśupata/Śivadharma → early Mantramārga → Śaiva Siddhānta → Aṣṭaprakaraṇa → ritual-manual → Kashmirian
  frontier.
- **14 translation-memory guides (G1–G14)** — critical Sanskrit + specialist English editions (Niśvāsa,
  Śivadharmaśāstra, Parākhya, Kiraṇavṛtti, Tattvasaṃgraha, Pāśupatasūtra, ...) to ingest as the
  translation-memory layer BEFORE translating any of the 100.
- **The 15-first priority sequence** (Pañcārthabhāṣya → Śivadharma corpus → early Skandapurāṇa →
  Niśvāsaguhyasūtra → early Siddhānta → Nareśvaraparīkṣā → Kiraṇavṛtti 7-12 → Hṛdayaśiva Prāyaścittasamuccaya).
- **The architecture**: the "Śiva Source Tree" (Rudra → Abhinavagupta), a per-work `work_id/date/
  tradition/translation_status/source_witnesses/translation_guides/reuse_relations` record, and the
  **translation-neighbourhood** rule — route each target through a historically-appropriate G-guide so a
  model never renders `pāśa = "bondage"` from the dictionary alone. Same-lemma ≠ same-concept.
- **Carry-forward**: build Niśvāsamukha + Niśvāsa + the translated early-Śaiva editions as a permanent
  translation-reference layer before translating these works.

---

## THE SOURCE DOCS (the originals this index compiles — never edit these, they are the record)

### Registers & acquisition (sanskritree/corpus/targets/)
| Doc | What |
|---|---|
| `untranslated.md` | register I — the 20 highest-value targets |
| `untranslated2.md` | register II — the sources behind the famous sources (+ the Bhartṛhari/Nyāya strategic correction) |
| `untranslated3.md` | register III — the next 20 (#41-60) + the 6 roadmap discoveries |
| `targetacquired.md` | the acquisition board — ACQ / LANDED / MS-request / locate |
| `round2_sources.md` | round-2 sources — verification + commentary anchors |
| `translation_status_audit.md` | the don't-duplicate register (which texts already have English) |
| `translation_atlas.md`, `canonical_reference_map.md`, `tradition_anchors.md`, `leapfrog_map.md`, `leapfrog_guide.md`, `markguidance.md`, `markguidance.md`, `atlasflaws.md`, `nonsaivatranslate.md`, `batch_9_plan.md` | the strategic/method docs |

### Downloaded sources (sanskritree/sources/)
| Manifest | What |
|---|---|
| `round2/MANIFEST.md` | round-2 verification + commentary sources |
| `round3/MANIFEST.md` | round-3 acquisitions (vishvasa raw-path) |
| `gretil2/MANIFEST.md` | GRETIL acquisitions |

### Other leads (sanskritree/)
| Doc | What |
|---|---|
| `ref/targetslogic.md` | targets logic |
| `truth/rasaleads.md`, `truth/rasa-top-leads.md` | the rasa-thesis leads (note: may be a different project) |
| `translations/_meta/*` | the translation-process audits (PASS2_ROUND2_AUDIT, etc.) |

### patala generated data (data/corpus/downloads/)
| File | What |
|---|---|
| `siva-corpus-download-manifest.json` | the 15-work Śiva corpus manifest |
| `siva-corpus-inventory.json` | on-disk corpus inventory |
| `sivaqueue-translation-guide.md` (`docs/corpus/`) | the second-corpus "Śiva before Abhinava" guide (100 targets + G1-G14 translation memory), from R2 `sanskritree/sivaqueue` |
| `translation-pipeline-inventory.json` | existing T1/R1/T2/R2/T3/C1 works (the easy wins) |
| `translation-state-ledger.json` | the corpus-state ledger (NEXT_VALID_ACTION) |
| `translation-targets DB` (`data/corpus/targets/`) | the compiled database |

---

## THE ONE-SENTENCE CARRY-FORWARD

**The corpus goldmine is now consolidated: 64 sources + 21 actionable targets + 39 leads + 16 anchors +
26 indexed source-docs, anchored by the canonical reference map (taxonomy, ingestion waves, the semantic-
shift glossary that prevents cross-work term misreading) and the Recognition Enquiry (the argument-layer
dossiers) — and every agent should read those two goldmine docs and the DB before translating or acquiring
anything.**
