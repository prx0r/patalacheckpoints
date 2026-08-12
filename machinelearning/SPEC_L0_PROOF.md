# L0 PROOF SPEC — proof-carrying philological translation

*2026-08-12. The goal is NOT "the machine proves the English translation is true" (no system can do
that for philosophical Sanskrit). What we CAN build is much stronger than ordinary translation QA:*

> **a proof-carrying philological translation where every mechanically checkable step is actually
> checked, and every non-mechanical step is isolated as an explicit scholarly judgment.**

That gives very high confidence in L0 and makes errors extremely visible.

The stack to build:

```text
SOURCE
↓
P0 byte/character integrity proof
↓
P1 reversible segmentation proof
↓
P2 morphological analysis certificate
↓
P3 syntactic / kāraka analysis certificate
↓
P4 Sanskrit↔L0 alignment certificate
↓
P5 lexical-sense justification
↓
P6 proposition-preservation tests
↓
P7 independent translation comparison
↓
HUMAN-ADJUDICATED PHILOLOGICAL CERTIFICATE
```

---

## 1. P0 — prove you actually translated the source

This part **can be mathematically exact**.

For every passage record:

```text
source_sha256
source_start_char
source_end_char
source_exact
normalization_function
normalized_sha256
```

Then verify:

```text
extract(original, start, end) == source_exact
```

and hash it.

No L0 record is accepted unless it resolves to exact source bytes/characters.

That proves:

> **Nothing was silently invented, skipped, reordered, or sourced from the wrong text.**

This should be the first "proof."

---

## 2. P1 — reversible Sanskrit segmentation

This can also get remarkably close to a proof.

You have Sanskrit such as a sandhied/compound form and propose:

```text
surface
↓
segment A
segment B
segment C
```

Then require the reverse operation to regenerate the original surface form.

Useful existing Sanskrit infrastructure:

**Sanskrit Heritage / Heritage.py**
[http://github.com/hrishikeshrt/heritage](http://github.com/hrishikeshrt/heritage)

It exposes segmentation/morphological analysis, parsing, declension, conjugation and dictionary lookup, and it can use the Sanskrit Heritage Platform locally.

**Skrutable**
[http://github.com/tylergneill/skrutable](http://github.com/tylergneill/skrutable)

Provides Sanskrit transliteration plus sandhi and compound splitting from Python.

**Samsaadhanii/UoH parser wrapper**
[http://gist.github.com/hrishikeshrt/231e91dbc364b50916f1d465afee18bb](http://gist.github.com/hrishikeshrt/231e91dbc364b50916f1d465afee18bb)

This exposes the Samsaadhanii Sanskrit parser from the command line and supports prose/verse inputs and different morphological/parser configurations.

Use **two independent analyzers** where possible.

Then the certificate can say:

```json
{
  "surface": "...",
  "segmentation": ["...", "..."],
  "heritage_accepts": true,
  "samsaadhanii_accepts": true,
  "roundtrip_surface_match": true
}
```

The most important check is not model confidence. It is:

```text
split
→ morphological forms
→ sandhi recomposition
→ EXACT ORIGINAL
```

If exact recomposition fails, flag it.

That gives something genuinely proof-like.

---

## 3. P2 — morphology certificate per Sanskrit token

Each Sanskrit unit should get a structured analysis:

```text
surface
lemma
POS
case
number
gender

or:

root
tense/mood
voice
person
number

compound analysis
```

Sanskrit Heritage can return structured morphological analyses and semantic-role parses.

The Digital Corpus of Sanskrit is also valuable as an external morphological corpus; Ambuda publishes a cleaned version under CC BY.
[http://github.com/ambuda-org/dcs](http://github.com/ambuda-org/dcs)

Sanskrit NLP literature makes clear why this matters: segmentation, morphology, compounds and dependency structure are upstream bottlenecks for Sanskrit NLP, especially because of sandhi, free word order and rich morphology.

So for an L0 entry like:

```text
tasya
→ "of him"
```

you can require:

```text
analyzer:
  lemma: tad
  case: genitive
  number: singular
  gender/context: ...
```

Then:

```text
English relation "of X"
↔ Sanskrit genitive
```

becomes mechanically compatible.

This still doesn't prove the English choice is *best*, but it proves it isn't grammatically impossible.

---

## 4. P3 — syntax / kāraka certificate

This is the next major upgrade.

For every clause reconstruct something like:

```text
VERB
├── agent
├── patient
├── instrument
├── locus
├── qualifier
└── subordinate relation
```

Sanskrit dependency parsing is an active NLP task, including graph-based and transition-based parsing and explicit evaluation of verse versus prose-order (*anvaya*) inputs.

This gives a way to test catastrophic translation errors:

```text
AGENT_SWAP
OBJECT_SWAP
NEGATION_SCOPE
MODIFIER_ATTACHMENT
CASE_ROLE_MISMATCH
VERB_ARGUMENT_LOSS
```

These are much more important than whether one English gloss sounds slightly odd.

For IPVV save two objects:

```text
surface_parse
anvaya_parse
```

because Sanskrit philosophical prose often becomes much clearer in construed order.

---

## 5. P4 — Sanskrit ↔ L0 alignment proof

This is where the existing L0 becomes incredibly useful.

Each English L0 item should be aligned to exact Sanskrit units:

```text
S1 S2 S3
 ↓  ↘
E1   E2
```

Use the deterministic alignment as the canonical one, then run an independent neural aligner as an **audit witness**.

A usable existing project is **awesome-align**:
[http://github.com/neulab/awesome-align](http://github.com/neulab/awesome-align)

It extracts token-level bilingual alignments using multilingual contextual representations and can be fine-tuned on parallel corpora.

Another useful research system is XLM-Align:
[http://github.com/CZWin32768/XLM-Align](http://github.com/CZWin32768/XLM-Align)

It trains cross-lingual models with explicit word-alignment objectives.

But **don't trust an English–Sanskrit pretrained aligner blindly** — cross-lingual alignment quality varies substantially by language/script and task.

Instead, we now have a route to train/calibrate one.

---

## 6. Mitrasamgraha could give a Sanskrit–English calibration corpus

This is very timely.

**Mitrasamgraha** was released in 2026 with **391,548 Classical Sanskrit–English bitext pairs**, plus post-corrected validation and test sets; the authors specifically highlight persistent difficulty with philosophical concepts, compounds and layered figurative language. ([arXiv][10])

Paper:
[http://arxiv.org/abs/2601.07314](http://arxiv.org/abs/2601.07314)

That means we could eventually:

```text
Mitrasamgraha
+ human-reviewed IPVV alignments
↓
Sanskrit-English alignment model
↓
independent audit of L0 alignments
```

Crucially, train on other material and test on held-out IPVV.

Then agreement between:

```text
human/L0 alignment
Heritage morphology
dependency parse
learned bilingual aligner
```

is strong independent evidence.

Not proof—but meaningful triangulation.

---

## 7. Build an actual `PhilologicalProof` object

This is what Pāṭala is missing.

```json
{
  "id": "PP-IPVV-V2L-0042",

  "source": {
    "span_id": "S42",
    "exact_hash_verified": true
  },

  "segmentation": {
    "tokens": ["..."],
    "roundtrip_verified": true,
    "heritage_supported": true,
    "secondary_parser_supported": true
  },

  "morphology": [
    {
      "token": "...",
      "lemma": "...",
      "analysis": "...",
      "status": "VERIFIED"
    }
  ],

  "syntax": {
    "predicate": "...",
    "agent": "...",
    "patient": "...",
    "negation": "...",
    "status": "EDITOR_REVIEWED"
  },

  "alignment": {
    "source_span_ids": ["..."],
    "target_span_ids": ["..."],
    "automatic_witness_agrees": true
  },

  "lexical": {
    "rendering": "...",
    "sense_evidence": ["dictionary...", "parallel..."],
    "status": "PREFERRED"
  },

  "obligations": {
    "source_coverage": "PASS",
    "target_coverage": "PASS",
    "polarity": "PASS",
    "agency": "PASS",
    "number": "PASS",
    "modality": "PASS",
    "unlicensed_addition": "PASS"
  },

  "review": "EDITOR_APPROVED"
}
```

Now **"verified translation" means something concrete**.

---

## 8. Define proof obligations

This is the key conceptual move.

Instead of one impossible question:

> "Is this translation correct?"

ask a set of much smaller questions that are increasingly machine-checkable.

For every L0 unit:

```text
O1 SOURCE
Does its Sanskrit span exist exactly?

O2 COVERAGE
Is every Sanskrit semantic unit accounted for?

O3 NO-ADDITION
Does every English semantic unit have a source anchor
or SUPPLIED designation?

O4 MORPHOLOGY
Is the chosen grammatical interpretation licensed?

O5 ROLE
Are agent/patient/instrument/etc preserved?

O6 POLARITY
Is negation preserved?

O7 QUANTIFICATION
Are eka/sarva/anya/etc preserved correctly?

O8 MODALITY
Are possibility/necessity/optative relations preserved?

O9 COREFERENCE
Do pronouns/demonstratives resolve consistently?

O10 TERM SENSE
Does the chosen lexical sense have evidence?

O11 COMPOUND
Is the compound interpretation morphologically possible?

O12 CLAUSE STRUCTURE
Does the English proposition preserve the Sanskrit dependency structure?
```

Then:

```text
12/12 obligations satisfied
```

has an actual meaning.

Much better than:

```text
confidence = 0.97
```

---

## 9. Some obligations can be genuinely deterministic

Separate:

```text
MACHINE-PROVED
```

from:

```text
MACHINE-CHECKED
```

from:

```text
SCHOLAR-ADJUDICATED
```

### Machine-proved

```text
source hash matches
character range matches
all tokens covered
no target span orphaned
recomposition == source
quote substring exact
```

These can be effectively binary.

### Machine-checked

```text
morphological analyzer licenses parse
dependency parser licenses relation
word aligner independently agrees
lexical database contains sense
```

These are tool outputs, not proofs of correctness.

### Scholar-adjudicated

```text
this is the intended morphology
this compound has this semantic relation
this referent is X
this technical sense is preferable
this implicit subject should be supplied
```

This distinction is critical.

---

## 10. Use multiple independent Sanskrit analyzers as a "proof ensemble"

This is probably the easiest immediate win.

Run every L0 source phrase through:

```text
Sanskrit Heritage
Samsaadhanii
existing L0 parse
```

and optionally sandhi/compound tooling such as Skrutable. Heritage supports morphology, parsing and grammatical generation; Skrutable supports sandhi/compound splitting.

Produce:

```text
CONSENSUS
all agree

DISAGREEMENT
two analyses differ

UNPARSED
none accept
```

Then prioritize:

```text
DISAGREEMENT + meaningful translation decision
```

for human inspection.

That is enormously more efficient than rereading 100,000 L0 records manually.

---

## 11. Round-trip grammar checking is especially attractive

Given:

```text
surface Sanskrit
↓
segmentation
↓
lemma + morphology
```

use a morphological generator to regenerate the forms.

Heritage exposes declension and conjugation generation as well as analysis.

Test:

```text
surface:
abhāsate

analysis:
√bhās ...
↓
generator
↓
expected surface forms
```

and check whether the source form is among them.

For nominal forms, same idea.

This gives **analysis→generation round-trip validation**.

That's very close to a proof obligation:

> If my morphological parse were correct, could the grammar generate the actual observed form?

If no → definite problem.
If yes → parse remains possible.

---

## 12. Do the same with sandhi

Another strong property test:

```text
source surface
↓ split
A + B
↓ apply sandhi engine
surface'
```

require:

```text
normalize(surface') == normalize(source surface)
```

This is excellent because it converts part of philological analysis into a **reversible computation**.

The `skrutable` toolkit provides sandhi/compound splitting functionality, while Sanskrit Heritage provides Sanskrit grammatical analysis/generation.

---

## 13. Then add cross-translation witnesses

Also a powerful external check unavailable to ordinary MT.

For important passages:

```text
YOUR L0
YOUR L2
Pandey
Torella
Ratié
other relevant translation
```

Automatically classify divergences:

```text
NEGATION
AGENCY
TERM
NUMBER
REFERENT
MODALITY
CLAUSE_SCOPE
ADDITION
OMISSION
```

Agreement is not proof.

But disagreement is **high-value evidence that something deserves inspection**.

This turns existing scholarship into an adversarial test suite.

---

## 14. Eventually create a proof certificate readers can inspect

Imagine clicking:

> **Why should I trust this translation?**

and seeing:

```text
SOURCE INTEGRITY       ✓ exact
SEGMENTATION           ✓ reversible
MORPHOLOGY             ✓ Heritage + parser
SYNTACTIC ROLES        ✓ reviewed
L0 ALIGNMENT           ✓ complete
NEGATION               ✓ preserved
AGENCY                 ✓ preserved
TARGET ADDITIONS       ✓ none unmarked
TERM SENSE             ✓ evidence
EXTERNAL COMPARISON    △ 1 disagreement
HUMAN REVIEW           ✓ editor
```

Then click any line.

That's vastly more meaningful than saying:

> "AI-assisted translation checked by humans."

---

# The implementation to start with

Do **not** try to build the complete semantic proof.

Build **Philological Proof v0**:

```text
1. SOURCE HASH / SPAN PROOF
2. TOKEN COVERAGE
3. REVERSIBLE SEGMENTATION
4. HERITAGE MORPHOLOGY
5. SECOND PARSER CROSS-CHECK
6. ANALYSIS→GENERATION ROUND TRIP
7. L0 TOKEN ALIGNMENT
8. UNSUPPORTED ENGLISH TOKEN DETECTOR
9. NEGATION / NUMBER / CASE / VERB FEATURE CHECKS
10. disagreement queue
```

Use:

```text
Heritage.py
http://github.com/hrishikeshrt/heritage

Skrutable
http://github.com/tylergneill/skrutable

Samsaadhanii CLI wrapper
http://gist.github.com/hrishikeshrt/231e91dbc364b50916f1d465afee18bb

Ambuda DCS data
http://github.com/ambuda-org/dcs

awesome-align
http://github.com/neulab/awesome-align

Mitrasamgraha paper
http://arxiv.org/abs/2601.07314
```

This fits the existing architecture perfectly.

We don't end up claiming:

> **"the machine proved Abhinavagupta means X."**

We can legitimately claim something much more precise:

> **"Every mechanically decidable transformation from the source string through segmentation,
> morphology, grammatical analysis and alignment has a reproducible certificate; remaining semantic
> choices are individually exposed as adjudicated philological decisions."**

That is about as close to a **proof-carrying translation** as is responsibly possible—and it gives
much stronger peace of mind about L0 than another LLM translation pass ever could.

---

## 15. VERIFIED INFRASTRUCTURE SURVEY (checked 2026-08-12 — reuse, don't rebuild)

Every external link in this spec was fetched and verified alive. The key finding: **most of the
"proof" machinery already exists and is mature — we should consume it, not rebuild it.** This is the
"check each github link as priority so we don't rebuild things" deliverable.

### A. ⭐ Vidyut (Ambuda) — THE one to adopt first
`https://github.com/ambuda-org/vidyut` — MIT, Rust core + first-class Python bindings (`pip install vidyut`), 130★, active. **This single project covers P0–P2 (and much of P3) out of the box:**

| Vidyut crate | What it does | Maps to |
|---|---|---|
| `vidyut-lipi` | transliteration (all scripts) | (input normalization) |
| `vidyut-sandhi` | apply/undo sandhi (`चैव → च एव`) | **P1 reversible segmentation** |
| `vidyut-cheda` | segment text into words **+ annotate morphology** | **P1 + P2 morphology** |
| `vidyut-prakriya` | generate words with derivations per Pāṇini | **P1 round-trip / analysis→generation** |
| `vidyut-kosha` | compact word→inflection store | P2 lookup |
| `vidyut-chandas` | meter identification | verse classification |

**Recommendation:** use `vidyut-cheda` + `vidyut-sandhi` as the P1/P2 analysis engine, and
`vidyut-prakriya` for the P1/P11 round-trip regeneration check. This is far better maintained and
faster than calling the Heritage web mirror per token. It's also **the cleanest cross-check**: Vidyut
(rule-based, Pāṇinian) vs Heritage vs Samsaadhanii = the "proof ensemble" of §10.

### B. The Sanskrit Heritage stack
- **Heritage.py** `https://github.com/hrishikeshrt/heritage` — GPL v3, `pip install heritage`. Python interface to Sanskrit Heritage (web mirror or local). Morphological analysis, sandhi, declensions, conjugations, lexicon search, and **semantic-role parse** (the Reader Assistant — relevant to P3 kāraka). Use as the *second* independent analyzer (§10 ensemble). GPL v3 — **note the license** if the result is embedded/distributed.
- **Samsaadhanii/UoH CLI wrapper** (gist `231e91dbc...`) — a working wrapper for the University of Hyderabad SCL parser (morphology + dependency graph, prose/verse/Vedic modes). Use as the *third* ensemble member. **Caveat:** the gist requires a local `samsaadhanii/scl` install + the WX encoding path; heavier to set up.

### C. Alignment (P4 audit witness)
- **awesome-align** `https://github.com/neulab/awesome-align` — BSD-3-Clause, mBERT-based neural word aligner. Produces `i-j` Pharaoh-format alignments. The practical choice for the P4 audit witness.
- **XLM-Align** `https://github.com/CZWin32768/XLM-Align` — MIT, `microsoft/xlm-align-base` on HF. Word-alignment oriented pretraining. Stronger but heavier (needs its own harness); awesome-align is the simpler first pick.

### D. Data / calibration corpora
- **Mitrasamgraha** `https://arxiv.org/abs/2601.07314` (Jan 2026) — **391,548** classical Skt→EN bitext pairs + 5,587 val + 5,552 test, post-corrected; explicitly flags philosophical/compound difficulty. Ideal calibration corpus for the P4 learned aligner. **Note the authors include the IPVV translators (Nehrdich, Sandhan, Goyal)** — highly relevant to our domain.
- **ambuda-org/dcs** `https://github.com/ambuda-org/dcs` — sanitized Digital Corpus of Sanskrit (CC BY 4.0). For morphological corpus lookups.
- **tokushige-koyasan/dcs-corpus** — 270 DCS texts as **lemmatized CoNLL-U** + machine-restored plain text (CC BY 4.0). Potentially the best morphological training/validation corpus (lemmatized, dependency annotations).

### E. Reuse decision (avoid rebuild)
- **P0 (source hash/span)** — build ourselves; it's 30 lines over our immutable T1 (no external tool).
- **P1 (segmentation) + P2 (morphology) + P11 (round-trip)** — **adopt Vidyut**, cross-check with Heritage + (optionally) Samsaadhanii.
- **P3 (syntax/kāraka)** — Samsaadhanii parser or Heritage semantic-role parse; also see UD_Sanskrit-UFAL + KISS parsing data + the dependency-parsing paper (`2004.08076`) for the anvaya vs surface question.
- **P4 (alignment)** — awesome-align now; calibrate/train later with Mitrasamgraha + our human-reviewed L0/L2.
- **P6/P8–P12 (obligation checks)** — mostly our own logic over the above outputs + the verification floor (`/api/verify/*`).

> **Don't rebuild** what Vidyut already does well. The Pāṭala-specific contribution is the
> **certificate + obligation layer** (the `PhilologicalProof` object, §7, and the MACHINE-PROVED /
> MACHINE-CHECKED / SCHOLAR-ADJUDICATED distinction, §9) over these engines — plus the provenance
> spine tying every check to our immutable T1/L0. That is the genuinely new work.

---

## 16. P0–P7 FEASIBILITY vs THE ACTUAL L0 DATA (reviewed 2026-08-12)

Assessment of each proof layer against the real `translations/_stack/ipvv/` data (35 chunks, 102,157
tokens; 96.42% PARSED, 3.58% AMBIGUOUS, 2 FAILED). **The binding constraint is the L0 coordinate bug,
not the external tools.**

| Layer | Feasible now? | What blocks it |
|---|---|---|
| **P0 source hash/span** | ⚠ Blocked by L0 bug | `char_start/char_end` are absolute-in-full-chunk but `source_text` is per-line → **can't** prove `extract == source_exact` against `source_text` as stored. Content (`raw_fragment`) IS correct (slice matches). Fix the extractor's coordinate system first, then P0 is ~30 lines. |
| **P1 reversible segmentation** | ✅ Tool-ready, data-blocked | Vidyut `vidyut-cheda`/`vidyut-sandhi` + `vidyut-prakriya` do this today. But L0's own segmentation is incomplete: **247/267 lines have token-span gaps**, so L0 itself isn't yet lossless. Two-sided: fix L0 losslessness AND add the Vidyut round-trip witness. |
| **P2 morphology** | ✅ Ready | Vidyut `vidyut-cheda` annotates morphology; Heritage cross-checks. Our L0 `lemma_iast` is only ~half-populated (AMBIGUOUS tokens have empty lemma) — morphology cert must fill these. |
| **P3 syntax/kāraka** | 🔶 Build | Samsaadhanii parser (gist) or Heritage semantic-role parse; heavy setup. UD_Sanskrit + KISS data exist for eval. This is the biggest lift. |
| **P4 alignment (L0↔Skt)** | ⚠ Tool-ready, data-needs | awesome-align needs tokenized parallel input; our L0 has gloss↔lemma pairs but no clean parallel file yet. Build `source | iast-lemma` parallel lines from L0 → run aligner as audit witness. |
| **P5 lexical-sense** | 🔶 Build | Needs the term-sense registry (partly in `TRANSLATION_PROTOCOL.md` §4 + graph `pt:sense`). Not a tool problem — a data/schema step. |
| **P6 proposition-preservation + O1–O12** | 🔶 Build | Deterministic checks over the alignments + verification floor. Reuses `/api/verify/*`. Valuable but downstream of P0–P4. |
| **P7 cross-translation witnesses** | ✅ Ready data | Pandey/Torella/Ratié translations + our L0/L2 exist. Divergence classification is our own logic. |

**Recommended build order (v0):**
1. **Fix `t1_extract.py` coordinate system** (per-line spans, or absolute + `full_text`) → unblocks P0.
2. **`verify_l0.py` full-chunk lossless proof** (the P0/P1 foundation) + close the 247/267 gaps.
3. **Adopt Vidyut** (`vidyut-cheda` + `vidyut-sandhi`) as the P1/P2 engine + Heritage cross-check → the
   §10 proof ensemble.
4. **`PhilologicalProof` object + obligation checks (O1–O12)** over the above → the readable certificate.
5. Later: P3 (Samsaadhanii/Heritage roles), P4 (awesome-align + Mitrasamgraha calibration), P7 (witness
   divergences).

---

[1]: https://github.com/hrishikeshrt/heritage "Heritage.py -- Python Interface to The Sanskrit Heritage Site"
[2]: https://github.com/tylergneill/skrutable "Skrutable -- Sanskrit transliteration + sandhi/compound splitting"
[3]: https://gist.github.com/hrishikeshrt/231e91dbc364b50916f1d465afee18bb "Samsaadhanii Parser CLI wrapper"
[4]: https://github.com/ambuda-org/dcs "Sanitized data from the Digital Corpus of Sanskrit"
[5]: https://arxiv.org/abs/2308.08807 "Linguistically-Informed Neural Architectures for Sanskrit"
[6]: https://arxiv.org/abs/2004.08076 "Neural Approaches for Data Driven Dependency Parsing in Sanskrit"
[7]: https://arxiv.org/abs/2101.08231 "Word Alignment by Fine-tuning Embeddings on Parallel Corpora"
[8]: https://arxiv.org/abs/2106.06381 "Improving Pretrained Cross-Lingual Language Models via Self-Labeled Word Alignment"
[9]: https://arxiv.org/abs/2002.03518 "Multilingual Alignment of Contextual Word Representations"
[10]: https://arxiv.org/abs/2601.07314 "Mitrasamgraha: A Comprehensive Classical Sanskrit Machine Translation Dataset"
