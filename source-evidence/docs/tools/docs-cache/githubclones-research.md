Yes — this is the right layer. I searched for **individual researchers/devs building strange one-off things on top of the corpora**, and this is already much better than the mainstream-tool list.

### 1. `joyboseroy/darshana-graph` — probably the biggest immediate goldmine

This is extremely close to Pāṭala conceptually. One person has assembled a **text-grounded comparative Indian-philosophy graph** across Vedānta, Nyāya, Vaiśeṣika, Sāṃkhya, Yoga, Jainism and a huge Buddhist corpus. The repo includes raw corpus acquisition, OCR conversion, resumable scraping, ID collision repair, LLM tagging, disagreement detection, stylometric comparison, auditing and Hugging Face export. ([GitHub][1])

The files alone are worth raiding:

```text
scrape.py
scrape_new.py
scrape_tattvartha.py
scrape_nimbarka.py

convert_gita.py
convert_muller.py
convert_madhva.py
convert_prabhupada_1972.py

extract_gambhirananda.py

fix_duplicate_ids.py
tag_corpus.py
audit_tagged.py
embedding_disagreement_finder.py
stylometric_comparison.py
prepare_hf_dataset.py
inventory.py
test_sources.py
```

Most interestingly, its tagging architecture is:

```text
real passage
   ↓
LLM classification
   ↓
CLOSED concept vocabulary
   ↓
CLOSED relation vocabulary
   ↓
reject anything outside vocabulary
   ↓
audit
```

rather than “ask an LLM to invent a graph.” ([GitHub][1])

That is exactly the discipline we want for a **candidate-generation layer beneath Pāṭala's stronger epistemic gates**.

It also has something very Pāṭala-ish already: its audit detects cross-school “tensions” by finding concept pairs for which schools assert different relation types. ([GitHub][1])

### Even more interesting: this repo has spawned side-projects

The README points to:

```text
joyboseroy/darshana-temporal-analysis
joyboseroy/vada-simulator
```

The first reportedly adds temporal attribution, structural-homology experiments, diachronic sense disambiguation and a much larger graph; the second is a **citation-grounded multi-agent debate simulator where agents representing philosophical schools are prevented from fabricating citations**. ([GitHub][1])

That second one is almost tailor-made for the Pāṭala argument/education layer.

**This developer deserves a dedicated repo-family audit.**

---

## 2. `joyboseroy/emptiness-graph`

This is even more conceptually aligned.

It is a tiny hand-authored **typed philosophical graph of emptiness** across Theravāda, Prajñāpāramitā, Madhyamaka and Yogācāra. It currently has a passage layer plus a separately curated philosophical layer. ([GitHub][2])

The architecture:

```text
corpus_manifest.jsonl
concepts.jsonl
edges.jsonl
passages.jsonl
passage_edges.jsonl
```

That's almost a miniature Pāṭala.

The interesting distinction is:

```text
PHILOSOPHICAL GRAPH
hand-authored

vs

PASSAGE INDEX
automatically generated
```

The author explicitly refuses to let automated extraction define the philosophical relations. ([GitHub][2])

That is very close to our:

```text
candidate
≠
adjudicated assertion
```

### Their edge taxonomy is worth studying

They distinguish things like:

```text
negates
presupposes
implies
is_identical_to
is_coextensive_with
depends_on
is_ground_of

refutes
extends
applies_method_of
deconstructs

tensions_with
reframes_as
is_conventional_expression_of
is_ultimate_level_of
is_precursor_of

enables
is_obstacle_to
is_antidote_to
```

and deliberately distinguish, for example, an ontological `negates` relation from dialectical `refutes`. ([GitHub][2])

That should go straight into the comparative audit against our current relation vocabulary.

More importantly, unresolved disagreement is represented as **`tensions_with` rather than forced reconciliation**. ([GitHub][2])

That is pure Pāṭala philosophy-engine thinking.

---

# 3. `tylergneill/pramana-nlp`

The Pāṇḍitya guy has another buried treasure.

This is a **Sanskrit pramāṇa corpus created specifically for computational analysis**, assembled from:

* GRETIL
* SARIT
* private collections
* heterogeneous `.htm`
* `.xml`
* `.doc`
* other source formats. ([GitHub][3])

It isn't merely a dataset.

He left behind all the ugly **philological ETL micro-tools**:

```text
transform.py
validate_text.py
segmentation pipeline
metadata spreadsheets
cleaned texts
document segmentation
word segmentation
topic-model inputs
similarity analysis
```

`transform.py` actually **daisy-chains XSL transformations** across heterogeneous scholarly files, while `validate_text.py` checks textual structure, bracket usage and suspicious character patterns. ([GitHub][3])

This is exactly what I meant by finding people's old research code.

### More importantly: its corpus is pramāṇa

Not generic Sanskrit.

So it potentially gives us pre-cleaned computational material for the exact intellectual lineage around:

```text
Nyāya
Buddhist pramāṇa
epistemology
logic
```

that feeds the Pratyabhijñā argument work.

The repo has **14 stars** and was archived in March 2026. ([GitHub][3])

That's exactly our target category: valuable scholarly work that's finished enough to contain real infrastructure but obscure enough nobody has productized it.

---

# 4. His `vatayana.info` work is another rabbit hole

The `pramana-nlp` README says the processed corpus later powered an **intertextuality search interface** called Vātāyana. ([GitHub][3])

That is worth tracing because intertextuality detection is directly relevant to:

```text
passage A
   ↓ possible reuse
passage B

quotation
parallel
allusion
adaptation
shared formula
```

Pāṭala absolutely needs this eventually.

I'd particularly hunt its similarity algorithms rather than rebuild passage-parallel discovery ourselves.

---

# 5. `joyboseroy`'s corpus acquisition code may save us ridiculous amounts of time

This deserves separating from the graph itself.

The developer already wrote source-specific conversion/scraping logic for:

```text
Bilara / SuttaCentral
Gita repositories
Sacred-texts
Wisdomlib
Müller SBE
DJVU OCR
scanned PDFs
Tattvārthasūtra
Nimbārka commentary
Madhva
Gambhirananda
```

and built the scrapers to resume where appropriate. ([GitHub][1])

In other words, instead of:

```text
Pāṭala agent:
"How do I ingest Wisdomlib?"
```

we may already have:

```text
scrape_tattvartha.py
scrape_nimbarka.py
```

to learn from.

Likewise Bilara ingestion gives us a ready pattern for ingesting SuttaCentral's structured Buddhist material.

This is exactly the sort of code we should pull into:

```text
patala-ingest/adapters/
```

after checking licenses and provenance.

---

# 6. `graphGita`

This one is smaller and somewhat rougher, which is useful.

Bhaskar Tripathi built a personal experiment attempting to transform the Bhagavad Gītā into a **knowledge graph**, with graph exploration and plans for comparing hundreds of interpretations. The implementation uses ordinary Python data pipelines and graph-oriented storage/visualization concepts rather than sophisticated scholarly infrastructure. ([GitHub][4])

The part I care about is not its philosophical accuracy.

It's the product experiment:

```text
same root passage
        ↓
many interpretations
        ↓
relations / agreement / conflict
        ↓
graph navigation
```

That's basically one early version of our Compare product.

I would **mine UI/query ideas, not ingest its epistemology**.

---

# 7. `xr843/fojin`

This is more developed now, but still essentially an individual-builder project rather than a legacy scholarly institution.

FoJin has assembled **10,500+ Buddhist texts from 613 sources**, with Sanskrit/Pāli/Tibetan/Chinese material, full-text search, parallel reading, semantic search, RAG and a knowledge graph. ([GitHub][5])

For Pāṭala the interesting question isn't “should we use their RAG?”

It's:

> **How the hell did one developer normalize 613 Buddhist sources?**

That's the gold.

I would inspect:

```text
source registry
canonical identifiers
document normalization
cross-canon matching
language mapping
parallel text relationships
ingestion adapters
Elasticsearch mappings
citation retrieval
```

because this potentially saves enormous work on our Buddhist counterargument corpus.

---

# 8. `mmehner/sanskrit-editing-suite`

GitHub surfaced a tiny personal repository literally called **`sanskrit-editing-suite`** associated with Sanskrit critical editing.

This is exactly the sort of thing that doesn't appear in “best Sanskrit software” lists. The repository is tiny (~185 KB in GitHub metadata), so I would treat it as a **micro-tool candidate**, not an ecosystem.

I haven't verified enough of its implementation yet to recommend adopting it; it's on the next code-audit pile rather than the “use now” pile.

---

# 9. `SriramKrishnan8/dcs_sh_alignment`

This one from the earlier pass actually **does belong in your new category**.

It isn't DCS itself.

It's one person's research project trying to align:

```text
Digital Corpus of Sanskrit
        ↕
Sanskrit Heritage Reader
```

The important asset isn't another parser.

It's the **cross-parser disagreement dataset**.

And the same researcher has related alignment work extending across multiple Sanskrit analysis systems.

That is perfect training/evaluation material for:

```text
PAT-LING-001

surface Sanskrit
      ↓
system A analysis
system B analysis
system C analysis
      ↓
agreement matrix
      ↓
Pāṭala candidate analysis
```

rather than pretending any single analyzer is authoritative.

---

# 10. Oliver Hellwig's personal `sanskrit` repo

This one's older but easy to overlook because everyone knows DCS while fewer people inspect Hellwig's personal repository.

It contains:

```text
corpus/
dcs/data/
papers/
texts/
translations/
```

specifically for **quantitative research on Sanskrit/Vedic Sanskrit**. ([GitHub][6])

That means there may be derived data and experimental corpora that never became obvious features of the public DCS interface.

For our “go as far back as possible” work this is particularly interesting.

---

# 11. Weird OCR/student projects — mostly don't adopt them, but raid experiments

GitHub turns up a bunch of tiny Sanskrit manuscript OCR projects such as:

```text
Suyashkb/VedOCR
ari2612sarkar/ManuVision
NoiceHax/DivyaLipi-AI
Suganthi-23/Digitizing-Sanskrit-Manuscripts-using-OCR-and-Image-Processing
Samuela31/Sanskrit-Manuscripts-Revival-Using-Deep-Learning-Techniques
Sharzzz001/Sanskrit-OCR
```

The last, for example, is a small EasyOCR-based pipeline for turning Sanskrit images into machine-readable output. ([GitHub][7])

I **wouldn't adopt these as OCR foundations**.

What they're useful for is discovering:

* datasets people found,
* preprocessing recipes,
* deskew/threshold combinations,
* page segmentation assumptions,
* handwriting/image samples,
* scripts people tested,
* failure cases.

For Gyan Bharat-scale manuscript ingestion, small student repos are often more useful as **experiment indexes** than dependencies.

---

# 12. The Tibetan side has similar hidden engineering we can steal

One example: the Esukhia Derge Kangyur/Tengyur repositories contain very practical scripts/workflows for:

```text
page + folio anchoring
line numbering
correction suggestions
normalized vs diplomatic forms
checking photographed scans
TEI export
splitting huge volumes into individual works
```

while preserving links to physical witnesses. ([GitHub][8])

That's valuable because Tibetan Buddhist projects have already confronted problems Pāṭala will encounter with Indian manuscript witnesses:

```text
raw witness
≠
normalized reading
≠
corrected text
```

Their implementation patterns are likely more useful than another generic TEI standard document.

---

# The one I'd attack first

It is **`joyboseroy`'s entire account**, not one repository.

Look at what this person has independently started constructing:

```text
darshana-graph
       │
       ├── ingestion
       ├── parallel commentary
       ├── passage grounding
       ├── closed relation ontology
       ├── disagreement discovery
       ├── stylometry
       └── evidence quotes
             │
             ├── darshana-temporal-analysis
             │      ├── diachronic senses
             │      └── temporal attribution
             │
             └── vada-simulator
                    ├── philosophical agents
                    ├── real citations only
                    └── citation fabrication rejection

emptiness-graph
       │
       ├── concepts
       ├── typed philosophical edges
       ├── tensions
       ├── passage grounding
       └── graph-constrained retrieval
```

This is almost a **parallel independent evolutionary branch of Pāṭala**. ([GitHub][1])

But Pāṭala has the stronger architecture because we're additionally doing:

```text
Sanskrit L0
translation provenance
evidence-use objects
claim-strength ceilings
argument reconstruction
review events
scholar adjudication
stable IDs
cross-text synthesis
proof-of-understanding education
```

So I don't want to replace Pāṭala with this.

I want to **strip-mine it**.

### The most valuable things to steal immediately

1. **All source adapters/scrapers** from `darshana-graph`.
2. Its **closed-vocabulary candidate tagging** technique.
3. Its **disagreement/tension finder**.
4. `embedding_disagreement_finder.py`.
5. Its **inventory + source-health tooling**.
6. Tyler Neill's **GRETIL/SARIT heterogeneous cleaning pipeline**.
7. Tyler's pramāṇa **metadata + segmented corpus**.
8. `emptiness-graph`'s **typed relation taxonomy** as a comparison against ours.
9. `vada-simulator`'s **citation-enforcement mechanics**.
10. `darshana-temporal-analysis`'s **diachronic sense machinery**.

This is much closer to the search strategy I think you wanted: **find the random researcher who solved 30% of one Pāṭala subsystem for their PhD/paper/weekend project, then absorb the useful machinery instead of recreating it.**

And there are clearly more. The next productive sweep is not searching `"Sanskrit NLP"` at all; it's traversing the **GitHub accounts, forks, citations and dependencies of Neill, Bose Roy, Hellwig, Sriram Krishnan and similar computational-Indology researchers**. That's where I expect the truly obscure motherlode to be.

[1]: https://github.com/joyboseroy/darshana-graph "GitHub - joyboseroy/darshana-graph: A text-grounded knowledge graph of Indian philosophy, covering Hindu darshanas, the Buddhist Pali Canon, and Jain philosophical texts · GitHub"
[2]: https://github.com/joyboseroy/emptiness-graph "GitHub - joyboseroy/emptiness-graph: A typed philosophical knowledge graph of Buddhist emptiness teachings · GitHub"
[3]: https://github.com/tylergneill/pramana-nlp "GitHub - tylergneill/pramana-nlp: data, metadata, tools, and LDA experiments on a corpus of Sanskrit philosophy texts · GitHub"
[4]: https://github.com/bhaskatripathi/graphGita?utm_source=chatgpt.com "GitHub - bhaskatripathi/graphGita: First scientific re-interpretation of Bhagwad Gita with Knowledge Graphs improved with Monte Carlo Tree Search · GitHub"
[5]: https://github.com/xr843/fojin?utm_source=chatgpt.com "GitHub - xr843/fojin: Buddhist Digital Text Platform — 10,500+ texts, 613 sources, trilingual cross-canon, AI Q&A (RAG), knowledge graph, full-text search · GitHub"
[6]: https://github.com/OliverHellwig/sanskrit?utm_source=chatgpt.com "GitHub - OliverHellwig/sanskrit: Data for the quantitative study of (Vedic) Sanskrit · GitHub"
[7]: https://github.com/Sharzzz001/Sanskrit-OCR?utm_source=chatgpt.com "GitHub - Sharzzz001/Sanskrit-OCR: Converts images of Sanskrit text to English Text · GitHub"
[8]: https://github.com/Esukhia/derge-tengyur?utm_source=chatgpt.com "GitHub - Esukhia/derge-tengyur: Digital Derge Tengyur · GitHub"
