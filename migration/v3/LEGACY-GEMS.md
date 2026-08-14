# PĀṬALA V3 — THE LEGACY GEMS (genius ideas from the old/global docs, now in v3)

*2026-08-14 · status: THE EXCAVATED INTELLECT · genius ideas found in the legacy/global vision docs
(markguidance, canonical_reference_map, leapfrog, globalnext, endgame5) that had been left behind. Each:
the idea · why it's genius · where it belongs in v3. This is the intellectual depth the technical spec
doesn't capture.*

---

## GEM 1 — THE T/R/E/C/H/X STATUS TAGS (from `markguidance.md`)
**The idea:** every scholarly claim carries an epistemic status tag:
```
T directly attested in a primary text · R peer-reviewed reconstruction
E empirical/contemporary finding · C structured cross-tradition comparison
H hypothesis/beyond current proof · X contested/unavailable/invalid
```
**Why it's genius:** it's the *content-level* version of the AuthorityVector. The epistemic envelope
tracks WHO reviewed it; the T/R/E/C/H/X tags track WHAT KIND of evidence it rests on. A claim tagged
`[T]` (directly attested) vs `[H]` (hypothesis) is a fundamentally different thing.
**Where in v3:** the Claim layer — each Claim should carry its T/R/E/C/H/X tag alongside the
AuthorityVector. This is the missing "evidence-kind" dimension.

## GEM 2 — THE TWELVE-QUESTION ENQUIRY SCAFFOLD (from `markguidance.md`)
**The idea:** the Recognition Enquiry as a sequence from minimal phenomenology to maximal metaphysics:
```
Q1 Does manifestation occur? → Q2 Is it self-present? → Q3 How does determinacy arise?
→ Q4 What explains memory-as-mine? → Q5 What grounds relation/judgment? → Q6 What shows agency/freedom?
→ Q7 How are error/conceptuality possible? → Q8 How does finite embodiment arise?
→ Q9 Agency at organismic scale? → Q10 Universal subject? → Q11 What is recognition? → Q12 ...
```
**Why it's genius:** it's a *minimal→maximal epistemic ladder* — each question builds on the previous,
and the answer to each is a crux. This IS the crux-generating structure the Question-Growth Engine (E4)
needs.
**Where in v3:** the Argument/Crux layer + expansion E4 (question-growth). The 12 questions are a
ready-made crux scaffold.

## GEM 3 — THE DIALECT-GENEALOGY CORPUS LADDER (from `leapfrog_guide.md`)
**The idea:** don't translate "Tantra" as one corpus. Build the translation engine around a genealogy of
mutually intelligible technical dialects:
```
Trika/Bhairava → Krama/Kālīkula → Kubjikā → Sarvāmnāya/Newar → Kaula/Śākta → Pratyabhijñā → Śaiva Siddhānta
```
Each hop's lexicon feeds the next — "a continuously expanding lexicon rather than forcing the model to
relearn tantric Sanskrit each time."
**Why it's genius:** it's the *lexicon-compounding* ordering. Start with the calibration layer
(Tantrāloka+Jayaratha as the Rosetta corpus), build thousands of glossary entries, then each subsequent
corpus is easier.
**Where in v3:** the harvest plan (GROUND-UP) — the IPVV is one vertical; this is the *horizontal*
corpus-growth strategy.

## GEM 4 — THE ROSETTA-CORPUS PRINCIPLE (from `leapfrog_guide.md`)
**The idea:** Dyczkowski's English gloss is **evidence, not the definition**. Use the well-translated
seed corpus (Tantrāloka etc.) to calibrate the engine, but treat its translations as evidence, never as
the target truth.
**Why it's genius:** it's the anti-theatre principle applied to the corpus. The seed translations train
the engine but don't define the answer — they're evidence to be weighed, like everything else.
**Where in v3:** the TranslationProof layer — the Rosetta corpus provides the parallel-witness evidence,
not the ground truth.

## GEM 5 — THE CONCORDANCE FIRST, LEMMATIZER LAST (from `canonical_reference_map.md`)
**The idea:** start with a full-text SQLite FTS5 concordance — **no Sanskrit lemmatizer needed**.
"Only add lemma-aware retrieval after exact/stem searching becomes a demonstrated bottleneck."
```sql
SELECT work, locator, text FROM passage_fts
WHERE passage_fts MATCH 'visarga' LIMIT 50;
```
**Why it's genius:** it's the anti-overengineering principle for retrieval. A 50-line FTS5 index serves
90% of need instantly; lemma-aware retrieval is added only when it's a demonstrated bottleneck — never
prematurely.
**Where in v3:** the read plane / retrieval layer — the "boring first tool" that beats building a
lemmatizer too early. The concordance is called "the highest-value script."

## GEM 6 — THE THREE-PLACE GEOGRAPHIC NODE (from `canonical_reference_map.md`)
**The idea:** a work's location is NOT one field — it's three distinct, often-different places:
```
claimed_revelation_place (traditional attribution) · historical_center (strong) · witness_location (manuscript evidence)
```
**Why it's genius:** it separates *what a tradition claims* from *where it was interpreted* from *where
manuscripts survive* — with per-field certainty. Much more useful than `location = Kashmir`.
**Where in v3:** the Atlas/Identity layer — the geographic-nodes model is a first-class part of work
identity.

## GEM 7 — PRATYABHIJÑĀ AS A CURRENT, NOT AN ĀMNĀYA (from `canonical_reference_map.md`)
**The idea:** "Pratyabhijñā is best represented in the map as a **philosophical/exegetical current
intersecting Trika, not as another directional Kaula āmnāya.**"
**Why it's genius:** it's a *taxonomy correction* — Pratyabhijñā isn't a competing lineage but a
cross-cutting philosophical current. Getting the ontology right matters for the whole graph.
**Where in v3:** the Tradition/Atlas taxonomy — the relationship between Pratyabhijñā and Trika is a
current-intersecting, not a sibling-lineage.

## GEM 8 — THE SEMANTIC-SHIFT ATLAS / LEXICON DOSSIERS (from `canonical_reference_map.md`)
**The idea:** the glossary is a **semantic-shift atlas** — each lemma is a dossier tracing its trajectory
across traditions (kula: Yoginī-family → Kaula body → cosmic body → Kubjikā mantra-body → Abhinava
kula↔akula polarity), not a flat definition.
**Why it's genius:** it makes *semantic change* a first-class object — exactly the "lemma-through-time"
layer, but at scholarly depth. The `kula/krama/khecarī/visarga` dossiers are gold.
**Where in v3:** the Terminology/Lemma-through-time layer — the dossiers ARE the trajectories.

## GEM 9 — THE INTEGRATION/IDENTITY LAYER + 11 ADAPTERS (from `globalnext.md`)
**The idea:** build the identity/crosswalk objects (Work/Person/Institution/Collection/Manuscript/Edition/
TextInstance/Passage/Token/LexicalSense + external `identifiers` crosswalk) — **never an external DB as
primary key** (`PATA-W-…` survives any external change). Integrate 11 adapters: Wikidata · OpenAlex ·
Crossref · VIAF · ROR · C-SALT · GRETIL · SARIT · PANDiT · NGMCP · IIIF.
**Why it's genius:** it's the "OpenAlex for Sanskrit" made concrete — every imported fact is a versioned,
citable Assertion with source/confidence/status (never overwrite fields).
**Where in v3:** the Atlas/Identity layer + `PATALA-NATIVE-MACHINERY.md` (the 11 adapters are the
identity backbone).

## GEM 10 — THE `patala_*` MCP VERBS (from `globalnext.md`)
**The idea:** expose the graph as verbs so Hermes can drive Pāṭala: `patala_next_action` ·
`patala_get_work_state` · `patala_propose_translation` (**PROPOSE, never ACCEPT**).
**Why it's genius:** it's the "agents propose, humans accept" gate made into an API. Hermes proposes
translations via MCP but can never accept them — the human gate is enforced at the verb level.
**Where in v3:** the Live System / MCP layer (8 verbs) — these `patala_*` verbs are the domain-specific
additions.

## GEM 11 — THE TANTRAKOŚA ORG MAPPING + IKS FUNDING (from `endgame5year.md`)
**The idea:** map the org to the IKS Division's three pillars, which match TANTRAKOŚA exactly:
```
IKS: RESEARCH / EDUCATION / OUTREACH  ↔  TANTRAKOŚA: corpus·API·MCP / courses·Sanskrit / app·lectures·atlas
```
And the funding path: **you + BHU professor + department + Pāṭala infra → IKS proposal** (₹20 lakh grants).
**Why it's genius:** it's the *institutional* go-to-market — not "apply as a tiny startup" but partner
with a university centre to access IKS funding.
**Where in v3:** the Org/Economics layer + the strategic dossier (endgame5).

## GEM 12 — THE CONCENTRIC INGESTION ORDER (from `canonical_reference_map.md`)
**The idea:** the highest-return corpus isn't "everything untranslated" — it's a **concentric ingestion
order**: Trika anchors → Krama → Kubjikā → bridges → Yāmalas → Nepalese syntheses.
**Why it's genius:** it prioritizes by *lexicon-return* — start where each text's terms unlock the next.
**Where in v3:** the harvest plan — complements the dialect-genealogy ladder (GEM 3).

---

## THE LEGACY GEMS → V3 MAP

| Legacy idea | Genius in | Where in v3 |
|---|---|---|
| T/R/E/C/H/X status tags | markguidance | Claim layer (evidence-kind dimension) |
| 12-question enquiry scaffold | markguidance | Argument/Crux + expansion E4 |
| Dialect-genealogy ladder | leapfrog_guide | harvest plan (horizontal corpus growth) |
| Rosetta-corpus principle | leapfrog_guide | TranslationProof (parallel witnesses, not truth) |
| Concordance-first (no lemmatizer) | canonical_reference_map | read plane / retrieval |
| Three-place geographic node | canonical_reference_map | Atlas/Identity |
| Pratyabhijñā as a current | canonical_reference_map | Tradition taxonomy |
| Semantic-shift dossiers | canonical_reference_map | Terminology/lemma layer |
| Integration layer + 11 adapters | globalnext | Atlas/Identity + native machinery |
| `patala_*` MCP verbs | globalnext | Live System / MCP |
| Tantrakośa/IKS org mapping | endgame5year | Org/Economics + strategy |
| Concentric ingestion order | canonical_reference_map | harvest plan |

---

*These are the genius ideas from the legacy/global docs, excavated and mapped into v3. The most
important: the **T/R/E/C/H/X status tags** (the missing evidence-kind dimension for Claims), the
**12-question enquiry scaffold** (a ready-made crux generator), the **dialect-genealogy corpus ladder**
(the horizontal growth strategy), and the **concordance-first principle** (start boring, add lemmatizers
only when demonstrated). None of these was in v3 — now they are.*
