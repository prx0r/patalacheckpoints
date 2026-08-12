# SANSKRITREE → PĀṬALA IMPORT MANIFEST (the full audit + where it lands)

*2026-08-12. The consolidated result of the full sanskritree audit: what is DIRECTLY USEFUL to Pāṭala,
where it should be imported, and what is noise/aspirational (excluded). **Pāṭala already owns the
canonical/lexicon/corpus layer** (concepts.ts, terms.json, the targets DB, published passages) — the
genuine net-new imports are: (1) not-yet-ingested primary texts, (2) the argument-layer analytical docs
in `truth/`, (3) Lean design lessons only.*

---

## THE VERDICT (one line)

> Pāṭala is the downstream consumer of sanskritree. The canonical/lexicon/corpus layer is already
> captured; the real net-new value is the **not-yet-ingested primary texts** + the **argument-layer
> analytical docs in `truth/`** + **Lean design lessons**.

---

## IMPORT — primary texts (data/corpus/passages/) — NOT yet ingested

| Text | Source | Why |
|---|---|---|
| Kiraṇatantra (clean IAST) | `source-library/tantra/siva-corpus/kiranatantra_clean.txt` | Śaiva Siddhānta, control group |
| Mālinīvijayottara (clean IAST) | `source-library/tantra/siva-corpus/malinivijayottara_clean.txt` | Trika anchor |
| Kramasadbhāva (IAST) | `sources/round3/kramasadbhava_IAST.txt` | the Krama packet #1 |
| Jayadrathayāmala | `sources/round3/jayadrathayAmala_*.txt` | Kālīkula flagship (later) |
| Ciñciṇīmatasārasamuccaya | `sources/round3/cincinmatasarasamuccaya_IAST.txt` | the bridge text |
| Timirodghāṭana | `sources/round3/timirodghAtana_gretil.txt` | archaic Kaula |
| Pramāṇavārttika | `sources/gretil2/raw_pramanavarttika.txt` | Buddhist control |
| Padārthadharmasaṃgraha | `sources/gretil2/raw_padarthadharmasamgraha.txt` | Vaiśeṣika control |
| Kaulajñānanirṇaya | `sources/round2/bagchi_kjn_1934.txt` | the KJN corpus |
| Vākyapadīya / Nyāyasūtra / Tarkasaṃgraha | `sources/gretil_*.txt` | philosophical control texts |

**Note:** many (kubjikāmata, maharthamanjari, kramasadbhava) already have Pāṭala jsonl — do not re-ingest.

---

## IMPORT — argument-layer analytical docs (machinelearning/ + docs/vision/scholars/) — THE NEW VALUE

**For Agent 1 (the argument layer) — under the doctrine's experimental discipline (mark MACHINE_PROPOSED, not settled):**
| Doc | What | Where |
|---|---|---|
| `truth/TANTRALOKA_MASTER.md` (+ REFERENCE/REREAD/VOLUMES_1-11) | verse-by-verse claim extraction | `machinelearning/_ACTIVE/` (argument ground) |
| `truth/sambandhasiddhi_translation.md` | Utpaladeva argument reconstruction | `data/corpus/passages/` |
| `truth/isvarasiddhi_translation.md` | Utpaladeva proof-of-God | `data/corpus/passages/` |
| `truth/apoha-partition-formal.md` | apoha formal argument | `machinelearning/` |
| `truth/torellalogic.md` | Torella's IPVV logic | `machinelearning/` |
| `truth/dharmakirti_apoha.txt`, `dharmakirti_self.txt` | Buddhist epistemology control | `machinelearning/` |
| `truth/utpaladeva_proof_of_god.txt` | Pratyabhijñā argument | `machinelearning/` |
| **Candidate (experimental/speculative):** `RASA_THESIS`, `mepit-formal-thesis`, `inexternalism_formal`, `subtle_body_formal`, `COMPENDIUM`, `SYNTHESIS` | cross-disciplinary theory | `machinelearning/_ACTIVE/` (flagged, not settled) |

**For docs/vision/scholars/ (reference):**
| Doc | What |
|---|---|
| `truth/torella_synthesis.md` + `torella_book/` (9 chapters) | the most important secondary source for the IPVV argument layer |
| `abhinavagupta/` curated PDFs (Dharmakīrti apoha, Utpaladeva's Proof of God, Vimarśa/reflexivity) | argument-layer secondary sources |
| `ipvv-anchor/MANIFEST.md` | edition/anchor registry |

---

## IMPORT — bibliography augmentation (data/atlas/bibliographySeed.ts)

- `ipvv-anchor/scholarship/` (30 Ratié/Torella PDFs) → as citation records
- `corpus/contrastive/` (Sāṅkhya/Vedānta PDFs) + `corpus/mimamsa/` + `corpus/lexicons/` (Amarakośa, Śabdasāgara) → as bibliographic anchors, NOT files

---

## IMPORT — reference docs (docs/corpus/)

- `ref/{sourceref,targetslogic,archiveref,graphref,mechanicsref}.md` — where-to-get-texts decision trees + graph architecture theory
- `corpus/learning/REFERENCE_TANTRALOKA_MASTER_MAP.md`
- `corpus/abhinava/README.md` — the Abhinava work×role map

---

## IMPORT — Lean design lessons only (machinelearning/proofs/)

- `ref/goldfeedback.md` — 14 architecture corrections incl. Lean Layer B/C schema fixes (already referenced by SANSKRITREE-LEAN-REVIEW.md)
- `proof_engine/{fol_lean_bridge,decomposition}.py` — as reference
- **Do NOT import** `lean/`, `Pantograph/`, `proof_engine_lean/` as a working capability — confirmed aspirational (no running proofs, no gold).

---

## IMPORT — reusable ENGINE (do NOT rebuild): the translation-QA scaler + fidelity taxonomy

`translations/tools/` is a mature, evaluated engine whose Task-2 scholarly-fidelity taxonomy maps ~1:1
onto Agent 1's contrast-set/verification vocabulary. Reuse, not duplicate:
- `qa_scaler.py` — deterministic+heuristic flagger (INFERENCE_TOO_COMPRESSED, MISSING_PREMISE,
  LOGIC_INVERSION, TERM_POLICY_DRIFT, ...). Task 1 = READER QA; Task 2 = SCHOLARLY FIDELITY QA
  (`POLARITY_CHANGE / SPEAKER_CHANGE / UNLICENSED_INFERENCE / TERM_SENSE_DRIFT /
  UNRESOLVED_SOURCE_DEPENDENCY / ...`).
- `qa_v1_harness/gold/eval/compare.py` + `V1_THREE_CONDITION_FINDINGS.md` — the honest falsification
  result (prose-only 2/17 recall; dominant bucket B = over-logged human stall, not evaluator failure).
- `qa_v2_fidelity.py` — the Task-2 licensing checker over the L2→L200→map→L1→L0→Sanskrit stack.
- **Alignment decision:** Agent 1's contrast-set corruption types should align to this taxonomy
  (POLARITY_CHANGE→NEGATE, SPEAKER_CHANGE→SWAP_SPEAKER, UNLICENSED_INFERENCE→inference-integrity,
  UNRESOLVED_SOURCE_DEPENDENCY→BROKEN_REF, TERM_SENSE_DRIFT→REPLACE_TERM_SENSE). Where: reference in
  `handover/SANSKRITREE-AUDIT.md`; consume in the contrast-set work.

## IMPORT — corroboration already consumed by ARG-004 (proposition-level)

`saivamap/dossiers/vimarsa.md` + GRETIL `gretil_ipv_clean.txt` `Ipk_1,5.11` + `truth/torella_book/`
(Ratié) were used to fold ARG-004 → `SCHOLARLY_CORROBORATED_PRELIMINARY` (the crystal/inert component
only). See `benchmarks/v0/ARG-GOLD-REVIEW-PACKET-v2.md`. Template for mining ARG-001/002/003/005.

## IMPORT — the source-material graph + source-library (outside sanskritree)

The corroboration campaign's scholar material is NOT only in sanskritree. The graph of traditions →
scholar papers → essays → source material lives at:
- **`/root/projects/.meta/`** — `TRADITION-GRAPH.md` (9 traditions → source/RO/essays/site), `SCHOLARS.md`
  (scholar → books+essays), `SOURCE-RESOURCES.md` (the on-disk source material + action items),
  `SOURCE-MANUAL.md`.
- **`/root/projects/source-library/`** — the actual material: `tantra/` (abhinavagupta, utpaladeva-ipk,
  ksemaraja, jayaratha, lakshmanjoo, dyczkowski, matter-of-wonder `extracted-passages.md`, hareesh-blog),
  `consciousness/scholars/` (29 dirs: biernacki, utpaladeva, dharmakirti, husserl, metzinger...), plus
  platonism/sufism/occult/buddhism/frontier.
- **Use for Agent 1:** scholar corroboration (Ratié reason-revelation at
  `source-library/tantra/source/ratie_reason_revelation/`, Biernacki matter-of-wonder extracted
  passages, Utpaladeva). Register in `docs/INDEX.md` (done).

---

## IMPORT — semantic-shift atlas (LEMMA→SENSE) as structured data

`benchmarks/v0/semantic-shift-atlas.json` — the canonical_reference_map glossary materialized as
machine-readable data: **16 lemmas × 25 senses**, each with tradition / period / sense /
translation_policy / evidence / semantic_warning. Feeds:
- **Agent 1 (semantic-alignment):** the sense-distinctions (e.g. vimarśa Pratyabhijñā vs Krama) map onto
  the SAME/NEAR/DIFFERENT alignment labels — the seed for the semantic-alignment gold.
- **Agent 2 (term-policy):** the translation_policy field per tradition → the T2/R2 term-ledger.
Model: `LEMMA → SENSE{tradition, period, locus, policy, explanation, parallel, status}`. Principle:
*semantic consistency is the goal, not lexical uniformity.*

---

## IMPORT — concordance index (132 MB, 505 texts) as retrieval evidence

`.concordance_index.json` — lemma→passage/token across 505 texts. Agent 1: parallel-usage retrieval
for semantic-alignment. Agent 2: difficult-case lexical retrieval for the factory.

---

## ALREADY CAPTURED (no re-import — cross-check only)

- `saivamap/dossiers/` (11 term dossiers) — already the source of `data/atlas/concepts.ts` + `data/terms.json`; NOW ALSO consumed as corroboration for ARG-004 (§ above).
- `corpus/targets/*` — already consolidated in `data/corpus/targets/` + `docs/corpus/TARGETS-INDEX.md`
- `corpus/ipvv-anchor/` chunk maps + IPVV passages — already in `data/published/ipvv/`

---

## IMPORT — the truth/ full classification (216 files, three epistemic classes)

`handover/SANSKRITREE-TRUTH-CLASSIFICATION.md` — the complete scan of `truth/`:
- **Class 1 (GENUINE SCHOLARSHIP, citable):** torella_book (Ratié/Baumer/Cuneo/Rastogi/Tripathi), Torella
  synthesis/logic, Dharmakīrti, isvarasiddhi/sambandhasiddhi, TANTRALOKA_*, abhinavagupta_* essays,
  Biernacki, Rastogi, Utpaladeva → **the corroboration mine for ARG-001..005** (ARG-004 already folded).
- **Class 2 (RIGOROUS FRONTIER SYNTHESIS, MACHINE_PROPOSED, NOT citable):** Recognition Enquiry
  (markguidance/deep-research-report — the paper candidate), Aperture framework, unified framework,
  valence/QRI, whattheheckis*, rasa, subtle-body, geometry/music → research scaffolding only.
- **Class 3 (NOISE / EXCLUDED):** chittick/ficino/shaw/steiner/iamblichus/law-of-one/ochema/channeling,
  syntheses/* (mystical) — out of scope unless Vision-11 cross-tradition needs them.

Register in `handover/SANSKRITREE-AUDIT.md` + this manifest so it's durable.

---

## NOISE / EXCLUDED (do not import)

- `syntheses/*` entirely (mystical/tech synthesis — out of scope for evidence-grounded Pāṭala)
- `truth/{law-of-one, cassiopaean, ochema, shaw theurgy, chittick/ficino/sufi/plotinus comparanda, steinerbook, redditidealims}` — channeling/mystical
- Empty scaffolds: `corpus/nyaya/*`, `corpus/tantra/*/`, `corpus/vyakarana_semantics/`, `saivamap/{trika,krama,kaula,...}`

---

## THE ONE-SENTENCE CARRY-FORWARD

**Pāṭala already owns the canonical/lexicon/corpus layer (concepts/terms/targets/published); the full
sanskritree audit found the genuine net-new imports are the not-yet-ingested primary texts
(`data/corpus/passages/`), the argument-layer analytical docs in `truth/` (→ `machinelearning/` for Agent
1, under the experimental doctrine), and the Lean design lessons only (→ `machinelearning/proofs/`) —
everything else is either already captured or noise to exclude.**
