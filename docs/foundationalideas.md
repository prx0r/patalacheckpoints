The biggest game-changer is to decide **now** that every translation, note, manuscript witness, term occurrence, lecture, and article is ultimately attached to a stable passage/text identity rather than being loose page content. Bilara's immutable segment-ID approach is a very strong precedent: root text, translation, comments, markup, and variant readings can all coexist against the same stable segment. ([GitHub][1])

I'd build these foundations before adding lots more content:

1. **Passage-level identity from day one.** Every verse/prose segment gets a permanent ID like `th:kubjikamata:3.14`. Never make URL structure itself the canonical identity. Then translations, audio, comments, variants, citations, and AI retrieval all hang from it. If segmentation later changes, keep aliases rather than breaking IDs.

2. **A real provenance ledger.** Every claim should know where it came from:

   ```text
   Sanskrit reading → GRETIL / edition X
   manuscript variant → NGMPP A41/3 fol. 27v
   translation → Hanneder 1998 p. 54
   interpretation → Ratié 2011
   site translation → model + prompt version + human edits
   ```

   This is probably more important than your eventual vector database. An agent should be able to answer not just **what** it believes but **why**.

3. **Model textual witnesses properly now.** Don't store one magic `sanskrit` field. Use:

   ```text
   WORK
      ↓
   WITNESSES
      ├ manuscript A
      ├ manuscript B
      ├ edition X
      └ e-text Y
           ↓
        READINGS
   ```

   TEI already has mature conventions for encoding witnesses, lemmas, readings, critical apparatus, and linking manuscript facsimiles to transcription. Building your internal model so it can export TEI later saves an enormous migration. ([Text Encoding Initiative][2])

4. **Separate transcription, normalized Sanskrit, and edited text.** This will matter once you touch manuscripts:

   ```text
   diplomatic transcription
   normalized transcription
   editorial reading
   ```

   Do not overwrite one with another. TEI specifically supports combining transcription with digital facsimiles and recording editorial intervention. ([Text Encoding Initiative][3])

5. **Make terminology a first-class object.** Don't wait until you have thousands of translations. Start collecting:

   ```text
   śakti
   kula
   krama
   vimarśa
   prakāśa
   visarga
   khecarī
   āveśa
   uccāra
   śūnya
   ```

   But don't define one global meaning. Store:

   ```text
   lemma
   textual occurrence
   proposed sense
   tradition
   date
   translator rendering
   commentary gloss
   evidence
   ```

   Eventually this becomes the historical semantic engine we discussed.

6. **Translation alignment should be many-to-many.** Don't assume Sanskrit verse 12 = English sentence 12. A translator may split, merge, omit, or reorder material. Build actual alignment objects:

   ```text
   source passage(s)
        ↕
   translation segment(s)
   ```

   Then you can compare Dyczkowski, Singh, Bäumer, your translation, etc., without forcing them into identical segmentation.

7. **Claims and annotations should be citable objects.** If somebody comments:

   > Jayaratha appears to interpret *kula* here technically rather than genealogically.

   give that annotation its own ID, author, evidence, revision history, status and discussion. Then scholarly commentary becomes reusable by the API rather than trapped in a Disqus-like comments section.

8. **Build contributor identity/review history properly.** Scholar profiles should eventually support ORCID. Separate:

   ```text
   contributor
   reviewer
   editor
   translator
   transcriber
   lecturer
   automated process
   ```

   A translation could then visibly show:

   > AI-assisted draft → corrected by A → reviewed by B → unresolved note by C.

   That could become a genuinely compelling scholarly workflow.

9. **Design for critical editions, even if you're not producing them yet.** TEI's apparatus model explicitly represents alternate readings and witnesses and supports interactive editions where readers choose readings. ([Text Encoding Initiative][2]) So later your reader can have:

   ```text
   EDITED TEXT
   [show variants]

   śaktir ...
      A: śaktiḥ
      B: śaktim
      KSTS: śaktir
   ```

   Starting with the right schema makes this cheap later.

10. **Make "related" relationships evidence-bearing.** Your atlas will become much more useful if edges aren't generic:

```text
Tantrasadbhāva
   ── quoted by ──▶ Tantrāloka

Text A
   ── probable borrowing ──▶ Text B

Text C
   ┈ conceptual parallel ┈ Text D
```

Each edge should have:

```text
relationship_type
scholarly_source
confidence
relevant passages
```

That eventually becomes an extraordinary research graph.

11. **Create a quotation/reuse detector.** This could become one of the site's signature tools. As texts enter the corpus, automatically detect Sanskrit n-gram/fuzzy overlaps and produce candidate borrowings:

```text
EXACT MATCH
13 pādas

PROBABLE ADAPTATION
82% lexical overlap

SHARED FORMULA
common across 17 texts
```

Humans validate the interesting ones. Over years you begin reconstructing textual transmission computationally.

12. **Track negative knowledge.** This sounds boring but will make your bibliography trustworthy:

```text
complete English translation:
NO COMPLETE TRANSLATION LOCATED

checked:
2026-08-10

searched:
WorldCat
Google Scholar
publisher catalogues
Academia
specialist bibliography

superseded if:
new edition discovered
```

Otherwise "untranslated" claims decay rapidly.

13. **Build saved research collections.** A researcher should eventually be able to create:

> "Krama cognition project"

and collect passages, terms, papers, manuscript images, annotations, translations and queries. Private first; optionally publish later. That's potentially an institutional paid feature.

14. **Everything import/export friendly.** From day one provide JSON. Later add:

* TEI XML
* CSV
* BibTeX/RIS
* Zotero
* IIIF links
* Markdown

TEI is especially worth designing around because it already models primary sources and critical apparatus in ways scholarly editors recognize. ([Text Encoding Initiative][2])

15. **Treat generated AI output as a separate evidence class.** Never let it silently become corpus truth:

```text
HUMAN-ASSERTED
SOURCE-DERIVED
MACHINE-DERIVED
MACHINE-SUGGESTED
```

A machine-generated lemma, translation, date, relationship or parallel can become human-validated later.

The feature I think could become the site's **killer interaction** is a research sidecar beside every Sanskrit passage:

```text
KUBJIKĀMATA 3.14

Sanskrit              Translation
─────────────────────────────────

SELECT: khecarī

[Meaning]
[Occurrences 47]
[Same period 11]
[Same tradition 18]
[Commentarial glosses 4]
[Published renderings 6]
[Parallel passages 9]
[Manuscript variants 2]
[Scholarship 7]

Ask about this passage →
```

That one interface naturally grows as your corpus grows. At first it may only have dictionary + translation + bibliography. Later it gains morphology, parallels, manuscript variants, commentary and historical semantic analysis. **You don't redesign the product—the evidence density increases.**

And I'd make one more foundational decision now: keep your internal schema **richer than your UI**. The UI can remain beautifully simple like `chaining.dev`, while underneath you preserve TEI-compatible witnesses, stable segments, provenance and relationships. That avoids the classic digital-humanities failure mode where a gorgeous reader later has to be rebuilt because the data was stored as Markdown blobs.

The things I'd actually implement **before translating another 100 texts** are therefore just:

**stable IDs → provenance → witness/source model → many-to-many translation alignment → term occurrences → resource/bibliography objects → versioned annotations.**

Everything exciting we've discussed—MCP, audits, semantic history, parallel detection, scholar collaboration, TTS, manuscript comparison, institutional workspaces—can grow cleanly out of those seven foundations.

[1]: https://github.com/suttacentral/bilara-data?utm_source=chatgpt.com "GitHub - suttacentral/bilara-data: Content for Bilara translation webapp. · GitHub"
[2]: https://tei-c.org/Vault/P5/4.8.0/doc/tei-p5-doc-bak/en/html/TC.html?utm_source=chatgpt.com "13 Critical Apparatus - The TEI Guidelines"
[3]: https://www.tei-c.org/release/doc/tei-p5-doc/en/html/PH.html?utm_source=chatgpt.com "12 Representation of Primary Sources - The TEI Guidelines"
