# Atlas Flaws — the honest review and the counter-strategy

*2026-08-09. The self-audit of the translation workflow, and the plan to counter its flaws. Written to be read by any future agent BEFORE trusting the corpus.*

---

## Part I. The flaws (the honest review)

### The verdict
The workflow is good as a **candidate-generation** system — the best possible without human eyes — but it is **not yet a verification system**, and the docs have overstated how verified things are. "P2 COMPLETE" in the atlas is the most misleading string in the project.

### The flaws, in order of severity

1. **Zero human Sanskritists have touched the corpus.** The "peer review" is self-review: the same model, same context, same biases. The varieties-and-verdicts P2 format has the form of judgment without the independence. The one genuine reading-correction (C1, ŚS 1.13) came from the anchor, not from self-review — the tell that self-review rarely overturns anything.
2. **Verification coverage ≈ 15–20%, presented as done.** 10 of 78 ŚS sūtras anchor-checked; the Kubjikā, Kulānanda, Unmattabhairava, most of the KJN, all of the 10-text batch have **zero external check**. The P2 docs are crux-sampling, not completion.
3. **The [X]-backlog is structural.** The corrupt pādas need the prints (Chatterjee, Bagchi, KSTS 4/6) — not held. Some pass-1 translations were made *through* the corruption (the Kulasāra soma-myth, Kubjikā 1.21) — a fraction of the corpus is reconstruction wearing translation's clothes.
4. **No error measurement exists.** No sampled mismatch-count against an anchor, no classified error-rate. The CP1 "defensible rate" was never applied to this batch — and the docs don't state its absence.
5. **The emendations "recommended" in the P2 docs** (nirlakṣaṇam, yena jñātaṃ, saṃgama) are confident guesses presented in an adjudicating format.
6. **The blind-translation rule was violated in spirit.** The anchors were read *while* translating (their renderings quoted into the files). Fine as a check-layer; the docs imply more independence than existed.
7. **The glossary can become an echo chamber.** A registered default ("nirañjana = stainless+unmanifest") pre-loads every future text; context-sensitivity — what philology insists on — is what a fixed glossary erodes. It should record *range*, not *default*.
8. **"6 complete texts" is true but misleading** — complete in pass-1 form, largely unverified. The word "complete" will mislead a future agent.
9. **Document proliferation** — 15 pass-1 files + 7 P2 docs + 2 audit docs + glossary + atlas; no automatically-maintained status file.

### The scale (what this actually is)
**15 works touched in this program** (6 complete in pass-1 form: Śivasūtra+Bhāskara, Akulavīratantra, Kulānanda, Unmattabhairavahṛdaya, Kubjikātantra, Kaulajñānanirṇaya; 9 with openings: the 10-text batch minus the two counted above, plus the Spanda Vivṛti opening). **~1,600–1,800 verses** of pass-1 translation, of which **~10% is anchor-verified** and **~0% is human-reviewed**. Plus the earlier phases (Spandakārikā, Vijñānabhairava, Siddhitrayī, Nyāyasūtra renders) — another ~340 verses, some with real verification (the CP1/CP2 defensible-rate work).

---

## Part II. The counter-strategy — more anchors, less guesswork

*The user's hypothesis is right: the LLM's guesswork is inversely proportional to the evidence available. Every anchor added moves the corpus from "candidates" toward "verified." The order below is the execution plan.*

### Tier 0 — free, do immediately (no books needed)
1. **The error-measurement**: sample 20–30 verses from each anchored text (ŚS vs Dyczkowski; Akulavīra vs the archive translation), compare verse-by-verse, classify every mismatch (agree / lexical / doctrinal / error), publish the rate per text. This converts "we think it's fine" into a number.
2. **The prints from archive.org**: the Bagchi 1934 KJN volume (the full KJN + Akulavīra + Kulānanda bundle) is downloadable — collate every corrupt pāda against it. The single biggest [X]-resolution available now.
3. **The Lakshmanjoo Śiva-Sutras OCR** (the scan on disk) → the Vimarśinī-anchor for free via Google Vision.
4. **The two-model review**: a second LLM (different architecture) reviewing the P2 docs cold — catches at least the confirmation-bias layer. Free; weakens flaw #1 meaningfully.

### Tier 1 — the anchor-books (the user's downloads)
5. **Mukhopadhyaya/Dupuis, KJN** — unlocks the KJN's full per-verse verification (our longest unanchored complete text).
6. **Torella, ĪPK with the Vṛtti** — unlocks the Hop-5 chain (and our Siddhitrayī work gets its reference).
7. **Jaideva Singh, Śiva Sūtras** (or the OCR'd Lakshmanjoo) — the Vimarśinī-side of the ŚS.
8. **Dyczkowski, A Journey in the World of the Tantras** — the Kaula-commentary evidence for the T2-cluster's practices (the cīna-kramas, the pañcāmṛta, the kumārīs).
9. **Avalon's Karpūrādistotra** — ✅ already downloaded (round-2); the Kālīkula-hop anchor in hand.

### Tier 2 — the anchor-use strategy (how to make anchors do more)
10. **The TĀ as the doctrinal oracle**: the 11 Dyczkowski volumes are an anchor for *doctrine*, not just the TĀ-text — every doctrinal claim in our batch (pañcāmṛta, mātṛkā, the bhāva-triple, the yoni) should be checked against TĀ's treatment (TĀ 3, 15, 29, 31 — on disk). This multiplies the anchor coverage without new books.
11. **Anchor-proximate prioritization**: translate texts that have ANY published translation (even partial) before untranslated ones — the leapfrog made stricter. The untranslated frontier (Kubjikā, Kulānanda, the 10-text batch) waits until the anchored corpus is verified and its glossary is calibrated.
12. **The scholarship-as-anchor**: Sanderson's Śaiva Age (✅ on disk) for the dating/taxonomy claims; the Rājataraṅgiṇī (✅) for the Kashmir history; the torella_book chapters (✅) for the Krama/Pratyabhijñā. The period-essays should be written *from* these, not from Wikipedia alone.
13. **The glossary as range-not-default**: reformat the period-glossary entries as "attested senses with citations" rather than single renderings — context-sensitivity preserved.

### Tier 3 — the human layer (the only real fix)
14. **One human pass on one complete text** — the ŚS is the candidate (anchored, complete, 78 sūtras). A Sanskritist's corrections calibrate the whole pipeline's error-profile.
15. **The status-field language**: per-text status (P1-complete-unverified / P2-partial / P3-verified) replacing the word "complete" in the atlas.

### The principle
The corpus should be labeled by what it is: **candidate translations with honesty markers and a growing verification layer.** The anchors are the verification. Every book downloaded, every print collated, every error-measurement published moves the corpus up the ladder. The workflow itself does not need redesign — it needs its final layers, and accurate labels in the meantime.
