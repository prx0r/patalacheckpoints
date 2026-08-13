# SCHOLAR-SOURCE MAP — the corroboration oracle (which scholar/page bears on which proposition)

*2026-08-13. The reusable index of independent published-scholar sources for argument-reference propositions.
**Corroboration is opportunistic and proposition-by-proposition** — a published scholar passage can promote a
matched claim to `SCHOLARLY_CORROBORATED` without a live reviewer, but it is NOT review/adjudication of Pāṭala's
exact object. Each entry is a **candidate `CorroborationEvent`** to be built + false-positive-tested per the
protocol in `DEVPLAN.md` F1 (relation, scope, semantic_relation, independence, method, defeaters). Do NOT treat
"something vaguely similar in Sanderson" as corroborated.*

> **Two axes:** evidence_status (corroboration) is separate from review_status (review of the exact object).

---

## The scholar corpus (all on disk — no network needed)

| Source | Where | Use |
|---|---|---|
| **Sanderson corpus (the entire thing)** | `data/corpus/sources/sanderson/` — `sanderson_manifest.json` (53 works), `Saivism_and_the_Tantric_Traditions_Festschrift_fulltext.txt`, `saiva_exegesis_kashmir.txt`, `encyclopedia_of_religion_1987.txt` (Krama/Trika/Abhinavagupta), `vishvasa_shaiva_age.txt`, `academia_bundles/consolidated/` (213 PDFs), `volumes/` | cross-work Śaiva doctrine, Krama/Trika, argument layer, dating/tradition |
| **Ratié cluster (31 PDFs)** | `sanskritree/corpus/ipvv-anchor/scholarship/` + the full *Le Soi et l'Autre* (`research-library/recognition/books/`) | the recognition/reflexivity argument, the "I", vimarśa, reason/scripture, proof-of-God |
| **Torella IPK ed. + Vṛtti** | `sanskritree/.../primary/torella_ipk.txt` + the Ajaḍapramātṛsiddhi (`sanskritree/sources/muktabodha-lib/AjaDapramAtRsiddhi-M00502-IAST.txt`) | the primary text, the vikalpa / self-luminous analysis |
| **Dyczkowski / Bäumer** | `source-library/tantra/` + `ochema2/sleepyshorts/baumer-*` | Tantrāloka doctrine, accessible scholarship |

---

## ARG-002 (The Non-constructed "I", V2L / ĪPK 1.6.1) — verified citations (recreate the events)

| Prop | Scholar source | Page/span | Relation |
|---|---|---|---|
| G2-OBJ | Torella, IPK ed./trans. (Delhi: Motilal, 2002), kārikā 1.6.1 + Vṛtti + nn. 2, 45 (the kalpanā-definition objection, NB 1.5) | 1.6.1 | DIRECT_SUPPORT |
| G2-TC1 | Torella, IPK 1.6.1 nn. 1, 3 (IPVV II pp. 274, 280: vikalpa = yojana / vicchedana / niścetavya–apohitavya) | pp. 274, 280 | DIRECT_SUPPORT |
| G2-TC2 | Ratié, "Otherness in the Pratyabhijñā Philosophy", *JIP* 35 (2007) | p. 342 fn. 63 | DIRECT_SUPPORT |
| G2-CONC | Ratié, "On Reason and Scripture in the Pratyabhijñā", *Scriptural Authority, Reason and Action* (Vienna: ÖAW, 2013) | pp. 19–22 | DIRECT_SUPPORT |
| G2-IC1 | Ratié, "Otherness...", *JIP* 35 (2007) | p. 342 | DIRECT_SUPPORT |

**Implementation:** `machinelearning/research/patala_ml/gold002.py` per-node `scholarly_corroboration` blocks →
validated by `goldutil.validate_scholarly_corroboration` → `ALL GOLD CONSISTENT`. CLAIMS P-022.

## G4-CRYSTAL (ARG-004, V2H / ĪPK 1.5.11)

| Prop | Scholar source | Page/span | Relation |
|---|---|---|---|
| G4-CRYSTAL | ĪPK 1.5.11 (Torella ed.) + the vimarśa dossier | ĪPK 1.5.11 | DIRECT_SUPPORT |

---

## READY-TO-USE corroboration candidates (fill `CorroborationEvent`s, verify each, then false-positive-test)

These passages are verified to exist and address the claims. Build each as a `CorroborationEvent` per F1.

- **ARG-004** (vimarśa vs prakāśa; svātantrya): G4-TC2/G4-CONC → Ratié *Le Soi et l'Autre* ch. 7 (freedom/
  svātantrya) + *JIP* 35 (2007) p.342; Torella IPK 1.5.11. G4-IC1 (vimarśa = parā-vāk/svātantrya/aiśvarya) → Ratié
  "On Reason and Scripture" pp.19–22 + *Le Soi* ch. 3. Crystal/reflection imagery → Ratié "An Indian Debate on
  Optical Reflections".
- **ARG-001** (order-less support / transcendental): → Ratié "Can One Prove that Something Exists Beyond
  Consciousness?" (the limit — supports the *gap*, not the universal Lord).
- **ARG-005** (interpretive scope local vs systematic): → Ratié's level-distinction (vyavahāra/paramārtha).
- **Universalization (the wager)**: Ratié "Can One Prove..." + "Utpaladeva's Proof of God" support the *limit*
  only. The proof-family transcripts (`research-library`): `prooof` (the S-role does not follow), `observer-proofo`
  (Phen/Siva marked hypotheses) are ready-made falsification fixtures for any universalization overclaim.

---

## Independence classes (never count raw source count as support)

`SAME_AUTHOR · DERIVED_CITATION · INDEPENDENT_AUTHOR · INDEPENDENT_TEXTUAL_ANALYSIS · PRIMARY_EDITION`.
Ratié paper A + Ratié book B + a paper citing Ratié is NOT three independent witnesses. Model
`EvidenceSource{author_id, publication_id, derives_from[]}`.

---

*This map is the corroboration oracle. When building an event: read the cited page, verify the exact quote,
set `relation`/`scope`/`semantic_relation`/`independence`, add `defeaters`, and run the F1 false-positive test.
Never cite a passage you have not verified — fabrication here is the scholarly analogue of the semantic-
paraphrase laundering the argument layer already guards against.*
