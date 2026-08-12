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

## ALREADY CAPTURED (no re-import — cross-check only)

- `saivamap/dossiers/` (11 term dossiers) — already the source of `data/atlas/concepts.ts` + `data/terms.json`
- `corpus/targets/*` — already consolidated in `data/corpus/targets/` + `docs/corpus/TARGETS-INDEX.md`
- `corpus/ipvv-anchor/` chunk maps + IPVV passages — already in `data/published/ipvv/`

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
