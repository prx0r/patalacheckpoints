# AGENT 2 (INTEGRATION / L0) — CHECKPOINTS & GOALS

*2026-08-12. The Agent-2 leading doc. Breaks the shared vision (`CHECKPOINTS.md`) into THIS lane's
concrete goals. **Agent 2 owns CP1 (PhilologicalProof).** Read `AGENTS.md` + `AGENTS-DOCTRINE.md` +
`handover/CHECKPOINTS.md` first.*

---

## THE LANE (what Agent 2 owns)

```
CP1 PHILOLOGICAL PROOF REAL   →  [converge with Agent ML at CP4]
```

**Agent 2's question, always:** *is this reading licensed by the source?* It produces `PhilologicalProof`
objects (not logs), and joins with Agent ML on `Ref` IDs (passage / proof / C1), never fuzzy.

---

## GOAL CP1 — PhilologicalProof v1

**Where you are (already the CLOSEST major checkpoint):**
- V2/V3: **35/35 P0 PASS**, 0 unknown source chars, exact spans, complete classification.
- P2 Vidyut witnesses already exist across ~104k records.

**What CP1 means (NOT "machine proves translation correctness"):**
> Every material source→L0 translation decision can expose what is mechanically proven, linguistically
> supported, unresolved, or editor-dependent.

**Finish in order:**
```
P0 exact source coverage       ✅ done
P1 segmentation/sandhi         Vidyut
P2 morphology                  Vidyut + Heritage ensemble
P3 lexical sense               gold fixtures → ranker benchmark
P4 alignment                   gold alignment → baseline/model benchmark
P5 syntax/referents            later / selective high-risk
```

**The structure to freeze NOW:**
```ts
interface PhilologicalProof {
  proof_id: string; passage_id: Ref; source_span_ids: Ref[];
  source_integrity: ProofDimension; extraction_coverage: ProofDimension;
  segmentation: ProofDimension; morphology: ProofDimension; syntax: ProofDimension;
  alignment: ProofDimension; lexical_sense: ProofDimension;
  open_issues: PhilologicalIssue[];
  tool_witnesses: ToolWitness[];
  review_events: ReviewEventId[];
}
interface ProofDimension {
  status: "PROVED" | "SUPPORTED" | "CONFLICT" | "OPEN" | "UNCHECKED" | "REVIEWED";
  evidence_ids: string[];
}
```
Do NOT invent `confidence: .93`. `REVIEWED` means actual human review, not code.

**Why it matters:** this immediately becomes `/verify-translation` — "upload your Sanskrit translation
and Pāṭala shows exactly where philological judgment enters." That is already a scholar product.

---

## GOAL CP1 — the concrete sequence

```
1. Heritage ensemble → P2 disagreement analysis   (run Heritage over all Vidyut CONFLICT + UNANALYZED
                                                   + a stratified control: ~500 CONFIRMED, ~500 AMBIGUOUS_SUPPORTED)
                                                   → a Vidyut×Heritage confusion matrix + disagreement report
2. lexical gold (~50–100 fixtures incl. NO-UNIQUE-SENSE abstention cases) → ranker benchmark
   (baselines: most-common gloss / local L0 gloss / embedding) before ranker.py becomes a witness
3. alignment gold (held-out from manually checked L0 pairs) → alignment benchmark
```

**Do NOT:** wander into essay logic · promote ranker.py to P3 without a human-reviewed gold + baseline eval.

---

## THE SHARED BOUNDARY (how the lanes converge at CP4)

Agent 2 certifies the source floor; Agent ML derives upward. The join is contractual:
```
Passage ID · PhilologicalProof ID · C1 ID · TranslationDecision ID
```
**Never** by filename, guessed locator, title string, or fuzzy match. The fabricated-ID failure
permanently established this.

At CP4, the vertical object both lanes produce together:
```
"I claim X"
because:
    C1 says ...        (Agent ML)
    L2 renders ...     (Agent ML)
    Sanskrit span is ... (Agent 2's source)
    PhilologicalProof says ...  (Agent 2)
```

---

## THE GUARDRAILS (Agent 2 specific)

- Output `PhilologicalProof` objects, not logs.
- The 5 proof dimensions each carry an honest status; no collapsed confidence number.
- `extraction_coverage: OPEN` (unclassified source chars) is NOT `lexical_sense: OPEN` — never conflate.
- Keep the frozen P0 extractor; only fix reproducible loss bugs.
- Update `CLAIMS.md` (P-001) + the handover honestly as each P1–P4 sub-capability crosses its gate.
