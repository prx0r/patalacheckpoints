# The Three-Version Translation Flow — Full Spec

*2026-08-09. The replacement workflow: three genuinely different translations of every text, reviewed between versions, culminating in a final synthesis. The differences ARE the scholarship — they reveal the interpretation-space, and the adjudications ARE the commentary. "It's hard to cheat that way."*

---

## 1. The principle

One translation can be wrong in ways that look right. Three translations, each composed independently of the others' sentences, cannot be wrong in the same way — where they **agree**, that is the hard core (the text's fixed meaning); where they **differ**, that is the interpretation-space (what the text genuinely allows); and the adjudication of the differences, with evidence, is the commentary. The synthesis (T3) is the culmination: the resolved, justified, final version.

**The flow:**
```
T1 (working translation) → R1 (review of T1)
   → T2 (fresh translation, must differ from T1)
      → R2 (T1-vs-T2 comparison + adjudication + commentary; converges near-final)
         → T3 (the final synthesis — the culmination)
```

**Status labels per text:** `T1-done → R1-done → T2-done → R2-done → T3-FINAL`. The word "complete" is retired; a text is "final" only at T3.

---

## 2. The phases, specified

### Phase 1 — T1 (the working translation)
**What:** the syntax-bound, evidence-aware first translation (the existing pass-1 files — already produced for 15 works).
**Rules (unchanged from PASS_PROTOCOL):** provenance header + time-place-context block; [X]-flags for unresolved readings; validation-sheet items; no silent edits later.
**Artifact:** `{text}_pass1.md` (exists).

### Phase 2 — R1 (the review of T1)
**What:** the peer-review of T1: per crux-verse — the varieties, the most-likely verdict with [G]/[P]/[A] evidence, the natural commentary-seeds.
**Coverage:** at minimum the crux-verses (the [X]-flags, the doctrinally loaded verses, the anchor-divergent verses); the full per-verse review is folded into R2 (which compares anyway).
**Artifact:** the P2 docs (`p2_{text}.md` — exist for all 15 works).

### Phase 3 — T2 (the fresh translation)
**What:** a **genuinely different** translation of the same text, composed **without re-reading T1's sentences**. Only the IAST, the R1 analysis, and the evidence (anchors, glossary, cross-text parallels) are consulted.
**The difference rule ("no repeating passages, words ok") — AMENDED 2026-08-09:**
- **The core requirement: T2 explores alternative INTERPRETATIONS.** Re-composition is not enough — engineered agreement is a failure mode (the first Akulavīra-T2 agreed 14/18; the corrected one found 2 real T1-errors by asking "what else can this mean?"). Each verse is re-derived from the IAST with the alternative-question: the passive vs the active of the compound (pāpabandhavit), the cross-text sense over the clever local one (gamāgame — the KJN 14/136 parallel), the no-emendation construal over the repair (mataṃ = "held as"), the direct address over the generic, the adjective over the noun, the ritual-register over the epistemic.
- **Where a live alternative exists, T2 TAKES it** and marks the fork. Where the text is fixed, T2 composes fresh — and the agreement is the honest hard core.
- **Passages** (sentences/clauses): must be re-composed — no copied sentence-structures.
- **Words** (single lexical items): reuse is allowed — a word that genuinely has one best sense legitimately recurs; the glossary's range-not-default rule governs this.
- **The check:** R2 must be able to OVERTURN T1. A flow that never corrects T1 is a flow not being run.
- **Strategy** (the guarantee of genuine difference): T2 must adopt a **different reading-strategy** from T1. Options:
  - **S1 — the commentary-informed strategy**: T2 renders through the commentary-tradition's voice (Bhāskara's glosses, the Vṛtti/Vivṛti's interpretations) — the doctrine-shaped reading.
  - **S2 — the argument-priority strategy**: T2 renders for the argument's flow — the connective tissue made explicit, the doctrinal terms kept technical.
  - **S3 — the anchor-influenced strategy**: T2 renders with the published translation's choices in view (where an anchor exists) — the scholarly-consensus reading.
  - **S4 — the register-shifted strategy**: T2 renders in a different English register (e.g., T1 formal → T2 plain; T1 analytic → T2 flowing).
  - The strategy is declared in T2's header, and R2 evaluates T1 vs T2 *as strategies*, not just as wordings.
**Anti-cheat rules:**
- T2 is composed blind of T1's text (the T1 file is not re-read; only R1's analysis is).
- If T2's independent composition nonetheless coincides with T1 at the passage level, that coincidence is recorded in R2 as *hard-core evidence* (two independent compositions landing on the same sentence = the text is fixed there).
- T2 may NOT cite T1 as a source; it cites only the IAST, the editions, the anchors, the glossary.
**Artifact:** `{text}_t2.md` — same structure as the pass-1 files (provenance, time-place-context, [X]-flags — with T2's own flags).

### Phase 4 — R2 (the comparison and adjudication)
**What:** the per-verse comparison of T1 vs T2, with the adjudication and the growing commentary. **This phase converges: it should land at the correct finalized reading.**
**Per-verse record:**
```
## v. X
**T1:** ...
**T2:** ...
**Hard core:** (where they agree — ✓, with the note that independent compositions coincided)
**Divergence:** (the difference between the two)
**Adjudication:** the most-likely reading, with [G]/[P]/[A] evidence — or **OPEN** (genuinely interpretable; the interpretation-space recorded, not flattened)
**Commentary:** (grows here — the adjudication's justification, the cross-text links, the anchor-quotes)
```
**The R2 rules:**
- Every divergence is either resolved (with evidence) or marked OPEN — no silent dropping.
- The anchors enter at full strength here: T1-vs-T2-vs-anchor is the three-way check.
- The commentary is extended and justified — this is where the P2 commentary-seeds grow into full notes.
- The convergence check: after R2, per text, the counts — % hard-core, % adjudicated, % OPEN. A text whose OPEN-rate is high is flagged as genuinely interpretable (that's a finding, not a failure).
**Artifact:** `{text}_r2.md`.

### Phase 5 — T3 (the final synthesis)
**What:** the culmination. Not a third independent version — the **resolved** translation: T2's composition carried through R2's adjudications (or T1's where R2 favored it), with the OPEN readings rendered with their alternatives visible (the final version can carry the OPEN flag inline).
**Rules:**
- T3 = the R2-resolved text; every adjudicated divergence is applied; every OPEN divergence is marked inline (the final version stays honest about its genuine openness).
- T3 carries the full apparatus: the provenance, the time-place-context, the R2-summary (the hard-core/adjudicated/OPEN counts), and the commentary for the adjudicated verses.
- T3 is the **final** artifact — the "complete" word may return only here.
**Artifact:** `{text}_t3_final.md`.

---

## 3. What the flow produces (the deliverable stack per text)

| Phase | Artifact | Status-label |
|-------|----------|--------------|
| T1 | `{text}_pass1.md` (exists for 15 works) | T1-done |
| R1 | `p2_{text}.md` (exists for 15 works) | R1-done |
| T2 | `{text}_t2.md` (new) | T2-done |
| R2 | `{text}_r2.md` (new) | R2-done |
| T3 | `{text}_t3_final.md` (new) | **T3-FINAL** |

**The per-text status line** (to be maintained in the atlas): e.g., `Śivasūtra: R1-done (10/78 verses reviewed; C1 applied) → T2 pending`.

---

## 4. The anti-cheat property (why this is hard to fake)

1. **T2 is blind to T1's sentences** — the composition must be fresh or the coincidence is *evidence* (the hard core), not plagiarism.
2. **The strategy-switch guarantees difference** — T1-literal vs T2-commentary-informed cannot produce the same passages by design.
3. **R2 is adversarial to both** — it can overturn T1, overturn T2, or mark OPEN; nothing is inherited.
4. **The anchors are the referee** — where an anchor exists, the three-way comparison (T1/T2/anchor) bounds the adjudication.
5. **The convergence metrics are published** — a text with 100% hard-core is either a simple text or a sign of conformism (checked against the strategies); a text with high OPEN is honestly flagged as interpretable.

---

## 5. Integration with the existing system

- **The three-readings format** maps onto the flow: the verse-level three-readings (literal/contextual/doctrinal) are the *strategies*; the text-level T1/T2/T3 are the *full-text* realization of the same discipline. The verse-level treatments remain the deep-dive format for crux-verses; the flow is the text-level format for everything.
- **The P2 docs** become R1 (already written) — and their commentary-seeds are the R2-commentary's starting material.
- **The glossary** governs the word-level reuse (range-not-default); the flow's hard-core findings feed the glossary (agreement across independent compositions = a sense promoted to "well-attested").
- **The anchors** (the Dyczkowski stack, the round-2 sources, the books as acquired) enter at R1 (as now) and at full strength in R2.
- **The audit rule** (no silent edits) continues: T1 and T2 files are never edited; R2 and T3 record everything.
- **The atlas** carries the per-text status lines; `atlasflaws.md`'s concerns are directly addressed: the flow IS the error-measurement (the hard-core/OPEN rates), the anti-cheat structure counters the self-review bias, and T3-FINAL is the only "complete."

---

## 6. A worked example (the format in miniature)

*Śivasūtra 1.3 — yonivargaḥ kalāśarīram.*

**T1** (literal, existing): "The group of yonis is the body of the kalās."
**R1** (existing P2): the yoni-fork (Bhāskara's four-powers vs Kṣemarāja's māyā) recorded; the four-powers favored for the Bhāskara-focus.
**T2** (strategy S1 — commentary-informed, composed blind of T1): "The congregation of the sources is the embodiment of the energies." (fresh composition; yoni → "sources" per Bhāskara's gloss + the anchor's rendering; kalā → "energies" in the anchor's sense)
**R2:**
- **Hard core:** "group/aggregate" (varga) — both compositions agree independently.
- **Divergence:** "yonis" vs "sources"; "body" vs "embodiment"; "kalās" vs "energies."
- **Adjudication:** "sources" (the anchor + Bhāskara's explicit gloss yonayaḥ śaktayaḥ); "body" (the literal — embodiment is the commentary's word); "kalās" transliterated (the glossary's ruling — the term is technical).
- **Commentary:** the four-powers cross-link (ŚS 2.7's bracket); the domestication lens (the yoni's two faces).
**T3 (final):** "The group of the sources is the body of the kalās" — with the OPEN flag on the yoni-referent (Bhāskara: the four powers; Kṣemarāja: māyā) carried as a footnote.

---

## 7. The immediate execution plan

1. **Spec adopted** — this document becomes the flow's law; the atlas's per-text status lines are created.
2. **T2 begins with the anchored texts** (the ŚS — the anchor makes R2's three-way check possible) — one text run through the full flow end-to-end as the proof.
3. **Then the unanchored complete texts** (Kubjikā, KJN) — T2 with the S1/S2 strategies; the anchors' absence raises the OPEN-rate expected (a finding, recorded).
4. **The openings** (the 10-text batch) — T2 for the openings only; T3 deferred until the texts are completed.
5. **The anchors keep coming** — every book downloaded upgrades the R2-adjudications; the flow is designed so that anchors enter where they exist and the honesty-markers cover where they don't.

---

## 8. The C1 phase (the commentary pass — the next horizon)

After T3-FINAL: **C1** — the commentary pass that "looks at all of this and does its own research on interpretation."

- **Input:** the full stack (T1 + R1 + T2 + R2 + T3 per text).
- **C1's work per text:** (1) take the T3-adjudicated verses and the R2-commentary-chains; (2) do its OWN research — the anchors re-read (the Dyczkowski-stack, the Śaiva Age, the Rājataraṅgiṇī, the prints), the Wikipedia/period-context checks, the cross-text quotations (the TĀ's treatment of each doctrine: the pañcāmṛta in TĀ 29, the mātṛkā in TĀ 3-4, the four-speech in TĀ 15); (3) grow each commentary-note into a full entry: the doctrine, the parallels, the period-context, the OPEN-forks re-examined with fresh evidence; (4) produce the per-text commentary doc (`c1_{text}.md`).
- **C1's independence-rule:** it must NOT merely repeat the R2-chains — it re-derives from the evidence, and it may overturn the T3-readings (a commentary that never challenges its own stack is decoration).
- **The C1-verification flags:** the [X]-items marked in the R2s ("the trivikrama-resonance", "the Anurādhā-nakṣatra", the dating-claims) are C1's first assignments.
