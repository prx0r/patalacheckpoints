# SANSKRITREE DEEP-DIVE AUDIT — usefulness for Agent 1 (ML/argument) + Agent 2 (L0/corpus)

*2026-08-12. A systematic survey of `/mnt/HC_Volume_106427611/sanskritree` and what each Pāṭala agent
should mine from it. Purpose: stop rediscovering this mount per-session. This is a living index —
update it as assets change.*

---

## 0. The mount at a glance (what exists)

| Asset | Where | Size / scale |
|---|---|---|
| **Concordance index** | `.concordance_index.json` | 132 MB, lemma → passage/token across 168+ texts |
| **`truth/`** | `truth/` | 216 files of scholarly corpus (Ratié, Torella book, Sanderson-adjacent, Dyczkowski, ...) |
| **`saivamap/`** | `saivamap/dossiers/` | structured concept dossiers (vimarśa, prakāśa, kula, akula, spanda, ...) with concordance-verified passages |
| **`corpus/ipvv-anchor/primary/`** | GRETIL ĪPK/ĪPVV, Torella edition+translation (PDF + txt), Pandit translation | edition-addressable verse refs (`Ipk_1,5.11`) |
| **`corpus/targets/`** | canonical_reference_map.md, markguidance.md | the two goldmine docs (glossary + Recognition Enquiry) |
| **`corpus/lexicons/`, `corpus/abhinava/`, `corpus/tantra/`, `corpus/nyaya/`, `corpus/vyakarana_semantics/`, `corpus/mimamsa/`** | topical corpora | per-domain Sanskrit |
| **`translations/_stack/`** | 15 works, each with 00_source…06_c1 layers | the auditable translation pipeline + C1/L0 outputs |
| **`proof/`, `proof_engine/`, `lean/`** | formalization + Lean | (note: Lean bridge is AVOID per Agent-1 guardrails) |
| **`ground_truth/`, `qa_*.json`, `v1_verdicts*.jsonl`** | evals/fixtures | prior adjudication artifacts |

---

## 1. Usefulness for AGENT 1 (ML / argument / themes / CP4)

### A. Published-scholar triangulation for the review gate — DIRECTLY mineable, no fabrication

The single highest-value use. `markguidance.md` + `saivamap/dossiers/` + `truth/torella_book/` give
**independent scholarly corroboration with exact passages quoted**, so evidence vectors can move from
"not collected" to `SCHOLARLY_CORROBORATED`-preliminary WITHOUT inventing citations.

Concrete matches for my existing golds:
- **ARG-004 (prakāśa vs vimarśa):** GRETIL `Ipk_1,5.11` = `prakāśo'rthoparakto'pi sphaṭikādijaḍopamaḥ`
  ("manifestation without vimarśa would be crystal-like, inert") — this is ARG-004's `G4-CRYSTAL`.
  Corroborated by: `saivamap/dossiers/vimarsa.md` (concordance-verified), `markguidance.md` (verdict
  "Established for A"), `truth/torella_book/ch6_ratie_other_streams.txt` + `ch7_ratie_isvarasiddhi.txt`.
- **ARG-002 (vikalpa / non-constructed I):** GRETIL ĪPK kārikā 1 + `markguidance.md` on exclusion
  (`apoha`, ĪPK 1.6.3–8).

### B. Edition-addressable verse grounding (strengthens the review packet)

The GRETIL `gretil_ipv_clean.txt` carries **verse-level addresses** (`Ipk_1,5.11`, `Ipk_1,1.1`, ...).
The v2 review packet currently grounds to L0 *token* spans; this lets it ALSO cite the **edition
address** — a reviewer can open the exact verse. Upgrade: add `verse_ref` (e.g. `Ipk_1,5.11`) alongside
the L0 span in each proposition's `primary_evidence`.

### C. The status-tag discipline (T/R/E/C/H/X) — a mature precedent for my evidence vector

`markguidance.md` uses T (directly attested) / R (specialist reconstruction) / E (empirical) /
C (comparative) / H (hypothesis) / X (contested). This is a working, scholar-facing model of the
non-binary evidence vector I codified. **Align my `MACHINE_PROPOSED → … → INDEPENDENT_REVIEWED` ladder
with it** rather than reinventing — the dossiers already encode which claims are T vs R vs X.

### D. Semantic-shift glossary (canonical_reference_map.md) — feeds semantic-alignment

The glossary warns against single-dictionary semantics: *kula*, *krama*, *śakti*, *vimarśa* have
different senses by tradition/period. This is the *exact* substrate the semantic-alignment layer needs
— it provides gold sense-distinctions (vimarśa-as-reflexive vs vimarśa-as-reflection) that map onto my
`SAME_SENSE / NEAR_SAME / AMBIGUOUS` labels.

### E. What Agent 1 should NOT mine (keep the lane clean)
- `data/atlas/concepts.ts` (the atlas) — Agent 2's translation-facing surface.
- `lean/`, `proof_engine/` — the Lean bridge is AVOID per my guardrails (proves FOL, not Abhinavagupta).
- `frontend/`, `syntheses/` — media/essay, not the argument graph.

---

## 2. Usefulness for AGENT 2 (L0 / corpus / translation factory / CP1)

### A. The concordance index (132 MB) — lexical/construction evidence + difficult-case retrieval
`.concordance_index.json`: lemma → passage/token across 168 texts. Exactly the "difficult-case
evidence" and "historical retrieval" the factory brief calls for. Queryable for morphology/compound/
construction retrieval.

### B. GRETIL + primary editions — the auditable source floor
`corpus/ipvv-anchor/primary/` (GRETIL ĪPK/ĪPVV with verse addresses, Torella ed.+trans., Pandit trans.)
+ `sources/gretil_*` (tantrāloka, tantrasāra, vākyapadīya, nyāyasūtra, ...) + `source-library/tantra/`
+ `sources/` (Akulavīra, Dyczkowski, Manthānabhairava...). These are Agent 2's RAW-SANSKRIT sources
for the L0/RAW-L0 mode and cross-work P0.

### C. The translation stack + STATUS board
`translations/_stack/` (15 works × 00_source…06_c1) + `translations/STATUS.md` is the live pipeline
registry — Agent 2's own completed output, plus which works are `partial`/`pending` (the factory's
next targets). `translations/_stack/ipvv/` holds the C1/L0 layers the golds consume.

### D. Saivamap dossiers — term-policy for translation
`saivamap/dossiers/*.md` give translation policies per concept (e.g. "vimarśa = 'reflexive
apprehension', NEVER merely 'reflection'"). Directly usable as the term-ledger for T2/R2 adjudication.

### E. Existing fixtures/evals
`benchmarks/`, `benchmarks_archive/`, `evaluations/`, `ground_truth/`, `qa_*.json`, `v1_verdicts*.jsonl`,
`protocols/` — prior adjudication runs Agent 2 can reconcile against (avoid re-doing).

### F. Agent 2 should NOT mine
- `proof_engine/`, `lean/` (Agent 1's formalization frontier; not translation).
- `truth/` scholarly essays (those are evidence for Agent 1's argument layer, not translation sources).

---

## 3. Shared / cross-cutting

| Asset | Agent 1 use | Agent 2 use |
|---|---|---|
| `saivamap/dossiers/` | semantic-alignment senses + ARG evidence | translation term-policy |
| `corpus/targets/canonical_reference_map.md` | glossary → alignment | corpus roadmap + ingestion waves |
| `corpus/targets/markguidance.md` | Recognition argument layer | passage priorities |
| `truth/torella_book/` | Ratié corroboration (ARG-004) | primary-text apparatus |
| `.concordance_index.json` | parallel-usage retrieval | difficult-case lexical retrieval |

---

## 4. Immediate high-value actions (mine now)

1. **Agent 1:** Upgrade ARG-004 (and then 002/001) evidence vectors to `SCHOLARLY_CORROBORATED`-preliminary,
   citing GRETIL `Ipk_1,5.11` + the vimarśa dossier + markguidance verdict — no fabrication, exact passages.
2. **Agent 1:** Add `verse_ref` (edition address) to the review-packet propositions alongside L0 spans.
3. **Agent 1:** Map the T/R/E/C/H/X tags into the evidence-hierarchy doc (CLAIMS.md) as a shared precedent.
4. **Agent 2:** Wire the concordance index into the factory's difficult-case retrieval + the RAW-L0 mode's
   lexical evidence.
5. **Shared:** Register this audit in `docs/INDEX.md` so agents stop re-surveying the mount.

---

*Status: this is an audit/index, not a claim. Nothing here is validated scholarship; it maps WHERE
corroborating evidence and sources live so the right agent can mine them under the doctrine.*
