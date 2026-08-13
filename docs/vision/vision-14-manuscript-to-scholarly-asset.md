# VISION 14 — THE MANUSCRIPT-TO-MACHINE-READABLE SCHOLARLY ASSET (Muktabodha, but derived)

*2026-08-13. The vision that turns the whole factory into a **granular, provenance-bearing, API-exposed
scholarly asset**: every text becomes a Pāṭala-derived version — fully translated, metadata-tagged
(school, time period, lemmas), machine-readable, and exposed as gorgeous structured data. This makes
Pāṭala the natural home for **manuscript onboarding** — upload a manuscript, it auto-processes through
the whole stack, is labeled, and tells you exactly what transformation it needs.*

---

## 1. THE ONE-LINE VISION

> **Pāṭala is not a translation website. It is the engine that turns any raw Sanskrit/manuscript input
> into a high-quality, machine-readable, provenance-bearing scholarly object — and exposes it as
> gorgeous, queryable data via an API.**

The mental model that unlocks it: **"Muktabodha, but derived."** Muktabodha gives you scanned e-texts.
Pāṭala gives you *processed, verified, enriched* texts — every one with its school, time period,
lemmas, argument structure, and provenance, all machine-readable and API-exposed.

### The deeper frame: a canonical machine-reference layer

Pāṭala is not just a Sanskrit tool — it is heading toward being the **canonical machine-readable
reference layer for the Śaiva textual tradition first, then Vedic, then Greek**. This is not a hope;
it is structurally true of the architecture:

```text
              UNIVERSAL PĀṬALA CORE (language-agnostic)
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
 SanskritCompiler    GreekCompiler     PaliCompiler
       │                 │                 │
       ▼                 ▼                 ▼
      T1                T1                T1
       └─────────────────┼─────────────────┘
                         ▼
       L0 → ARGMAP → L2 → L200 → C1 → THEME → ESSAY → epistemic graph
```

The layer stack (SOURCE→T1→L0→ARGMAP→L2→L200→C1) is **language-agnostic by design**: only the
front-end compiler (segmentation, morphology, lemmatisation, technical lexicon) is Sanskrit-specific.
L0 is the portable boundary — once a text reaches L0, the rest of Pāṭala need not know whether it
originated in Sanskrit, Greek, or Pāli. (This is the GlossLM argument, imported as a vision doc:
*"every language-specific compiler must emit a standardized semantic/philological intermediate
representation"* — not "every tradition needs its own entire Pāṭala stack".)

So the vision is precise: **Śaiva/Sanskrit is the proving ground that hardens the universal kernel;
the same factory then consumes Vedic and Greek with language-specific front-ends, all feeding one
canonical machine-readable reference layer exposed through the same API.** That is the moat — not
"we have Sanskrit text" (many do), but "we hold the *derived, verified, enriched* reference state
across the whole tradition, machine-readable and queryable."



## 2. WHAT "A PĀṬALA VERSION OF A TEXT" MEANS

For every input we hold both, and they are **distinct and honestly labeled**:

```text
INPUT (raw, external)
  - the archive.org / GRETIL / scan / manuscript / another project's e-text
  - provenance: who made it, its edition, its license

      ↓  (the factory's derived stack)

PĀṬALA VERSION (our derived engine output)
  - SOURCE → T1 (word-gloss) → L0 (structured) → ARGMAP → L2 (readable)
    → L200 (audit) → C1 (commentary) → THEME → ESSAY
  - enriched with: school, sub-school (śākhā), working period, author/attribution,
    parsing register, lemmas, term-senses, argument graph, review state
  - fully machine-readable, versioned, provenance-bearing, API-exposed
```

The key rule (already our doctrine): the Pāṭala version is **derived from** the input, never silently
conflated with it. `source_type` distinguishes `clean_etext` / `ocr` / `manuscript_scan` / `imported`.
The factory's honesty discipline (never claim a derived reading is the source) is what makes this a
trustworthy asset, not just a dump.

---

## 3. THE GRANULAR QUALITY LADDER (why this is valuable)

The per-work signal we just built (`source_ready.py` — CLEAN / READY / PRIORITY) is the seed of
something much richer. The full ladder per text:

```text
INPUT QUALITY
  raw_scan          — image/PDF, needs OCR
  ocr_done          — text extracted, needs review
  clean_etext       — machine-readable, trustworthy (GRETIL/TITUS)
  imported          — from another project, needs re-derivation

FACTORY STATE
  source_registered — in the queue
  t1                — word-gloss done
  l0                — structured representation done
  l2 / l200 / c1    — translation + audit + commentary
  reviewed          — scholar/MACHINE_PROPOSED → adjudicated

ENRICHMENT
  lemma_indexed     — lemmas + term-senses resolved
  metadata_tagged   — school, śākhā, period, author, register
  argument_mapped   — propositions/inferences/cruxes
  bibliography_linked — atlas record, translation status, rights
```

Every text carries a **quality fingerprint** — a single object that says "here's exactly how far this
text has been processed, and what's still needed." That's the granularity you're excited about, and it
is exactly what manuscript onboarding and API consumers need.

---

## 4. MANUSCRIPT ONBOARDING (the auto-ingest path)

The end-state interaction:

```text
User uploads a manuscript (PDF / image-scan / Devanagari e-text / another project's export)
        ↓
1. INGEST     — extract text (OCR if image; reuse the OCR pipeline idea we documented)
        ↓
2. DETECT     — language/script (IAST? Devanagari? mixed?), source quality
        ↓
3. LABEL      — produce the quality fingerprint:
                  "this is a Devanagari scan, OCR needed, 90% likely = Tantrasadbhāva,
                   school = Trika/Bhairava env., likely ~9th c., no complete English"
        ↓
4. ROUTE      — decide the transformation needed:
                  → clean_etext? go straight to T1
                  → scan? route to OCR then T1
                  → already translated? import + re-derive, don't retranslate
        ↓
5. PROCESS    — push through the whole stack (SOURCE→T1→L0→ARGMAP→L2→L200→C1→THEME→ESSAY)
        ↓
6. EXPOSE     — become a full Pāṭala version, API-queryable, provenance complete
```

The **"what transformation does it need"** step is the key differentiator: the system doesn't just
dump text in — it *diagnoses* the input and routes it through the right pipeline, exactly like
`source_ready.py` does today (it already tells you CLEAN/DIRTY and READY).

---

## 5. THE API EXPOSURE (gorgeous data)

Everything above is worthless if it isn't queryable. The vision: a first-class read API over the
derived state:

```text
GET /texts/{work}                     → the Pāṭala version: all layers + metadata + provenance
GET /texts/{work}/layers/T1           → word-gloss
GET /texts/{work}/layers/L0           → structured representation
GET /texts/{work}/lemmas              → lemma index + term-senses
GET /texts/{work}/argument            → proposition/inference graph
GET /texts/{work}/bibliography        → atlas: school, period, translations, rights
GET /texts/{work}/quality             → the quality fingerprint (how far processed)
GET /manuscripts/{id}/routing         → "this needs OCR then T1"
```

Each object is versioned, provenance-bearing, and machine-readable. That's the "gorgeous data" — 
structured, queryable, trustworthy. The factory's registries + ledger + atlas are already the raw
materials for this API; they just need a thin read layer (which is also the `patala_*` MCP verb bridge
we already scoped for Hermes).

---

## 6. HOW THIS CONNECTS TO EXISTING PROJECTS (reuse-first, not rebuild)

Per the anti-build doctrine, Pāṭala should **link with** the mature ecosystem, not reimplement it:

| Existing system | What Pāṭala does with it | What Pāṭala adds |
|---|---|---|
| **Muktabodha** | Ingests their scanned e-texts | Derives the full translated/enriched version they don't have |
| **GRETIL / TITUS / SARIT** | Source of clean e-texts | Processing, verification, enrichment, argument graph |
| **Sanskrit Library / Ambuda** | Sanskrit tooling, lemmatizers | Bundles their analyses as `AnalysisWitness[]` (ensemble, disagreement-preserving) |
| **DCS / corpus** | Lemma + collocation data | Term-sense + lemma index woven into the derived version |
| **IFP / EFEO** | Critical editions + translations | Links their editions; keeps provenance honest (never conflates) |

The value we hold is not "we have Sanskrit text" (many do) — it's **"we have *derived*, *verified*,
*enriched* text, with school/period/lemmas/argument structure, provenance-bearing and API-exposed."**
That's the moat.

---

## 7. WHY THIS FITS THE EXISTING FACTORY (it's not a new build — it's a wrapper)

We already have ~90% of this built:

- **The derived stack** — SOURCE→T1→L0→ARGMAP→L2→L200→C1→THEME→ESSAY (Era A)
- **The compiler/intake** — `register_sources.py`, `corpus_state.py` (Era B + this session's work)
- **The bibliography** — atlas with school/period/translations (this session's work)
- **The quality signal** — `source_ready.py` (CLEAN/READY/PRIORITY, just built)
- **Provenance + integrity** — versioned registry, hash-chained event ledger
- **Self-healing queue** — factory loop + auto-intake

**The layer below the factory** (the missing one this vision needs): the **source resolver** —
see `docs/vision/source-resolution/source-resolver-design.md`. It distinguishes Work → Edition →
Witness → Surrogate → Transcription → E-text → SOURCE with an **authority ladder** (DISCOVERED → …
→ SCHOLAR_CONFIRMED), using the Sanskrit-specific authority stack (NCC, NMM/Pandulipi, NGMCP, SARIT,
GRETIL, Muktabodha) + book catalogs + IIIF — and never auto-promotes from fuzzy matching. The v1 of
this is `pipeline/verify_editions.py` (archive.org + GRETIL attestations, recorded honestly as
statements about evidence).

What's missing is the **thin read API layer** over all of it (`patala_*` verbs / an HTTP read API),
plus the **manuscript-ingest + routing step** (OCR + detection + label, built on the OCR pipeline idea
we documented). So this vision is a **wrapper + API**, not a rewrite.

---

## 8. THE IMPLEMENTATION ORDER (depth before width)

```text
E0  Freeze the granular quality model (input_quality × factory_state × enrichment)  [mostly done]
E1  Complete the bibliography for the ~20 CLEAN-but-unlabeled works (gap from source_ready.py)
E2  Read API over existing registries/ledger/atlas  (patala_get_work_state, etc.)
E3  Manuscript ingest: detection + labeling + routing  (reuse OCR idea; validate quality first)
E4  Lemma index woven into the derived version
E5  Argument graph exposure
E6  Import adapters (Muktabodha / other projects) with honest provenance
E7  Full API exposure + MCP bridge (Hermes)
```

**Do NOT build the whole ingest/API at once.** Prove the granular model on the existing corpus first
(E0–E2), then add manuscript ingest (E3) once OCR quality is validated — exactly the discipline we've
been following.

---

## 9. THE CARRY-FORWARD

> **Pāṭala becomes the engine that turns any raw Sanskrit input (including manuscripts) into a
> high-quality, machine-readable, provenance-bearing scholarly version — school, period, lemmas,
> argument structure, all tagged — exposed as gorgeous queryable data via an API. "Muktabodha, but
> derived." The factory already does the derivation; the next steps are the read API (E2), completing
> the bibliography gap (E1), and the manuscript-ingest routing layer (E3) once OCR quality is proven.**
