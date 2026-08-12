# ARG-GOLD REVIEW PACKET v2 — primary-Sanskrit grounded

*Rebuilt 2026-08-12. This packet replaces the v1 basis. The change: every proposed proposition is now
grounded **directly to primary Sanskrit + its L0 analysis floor**, not through the L2. The L2 appears
only as labeled secondary interpretive context and is **never required for a review decision**. This
removes the derivational circularity the first review (MODEL-1) flagged — the L2 was produced *from*
the very argument maps being reviewed.*

**The question a reviewer now answers:**

> Does this proposed argument follow from the **primary textual evidence**?

…not:

> Does this proposed argument agree with an interpretive layer partly derived from the same reconstruction?

---

## The evidence ladder (explicit for every argument)

```text
PRIMARY SANSKRIT
    ↓
EXACT SOURCE SPANS / IDs            (resolvable L0 token ids)
    ↓
L0 TOKEN + ANALYSIS FLOOR           (lemma/morphology, P0 proof status)
    ↓
OPTIONAL CLOSE / LITERAL GLOSS      (secondary, labeled, non-authoritative)
    ↓
PROPOSED PROPOSITIONS
    ↓
PROPOSED INFERENCES
```

**Technical rule (hard):** every proposition points downward to primary-source evidence *without
requiring L2 as an intermediate authority.*

```text
Proposition  --GROUNDED_IN-->  L0 / SourceSpan  -->  Sanskrit        (correct)
Proposition  --->  L2  --->  prior interpretive reconstruction      (rejected)
```

---

## How to review each argument

Each argument is presented in the same A–H structure:

```text
A. REVIEW TARGET      what proposition/inference is being judged
B. PRIMARY SOURCE     Sanskrit passage, stable passage/span IDs, edition/provenance
C. L0 EVIDENCE        exact tokens per proposition, lemma/morphology, P0 status, uncertainty markers
D. MINIMAL RENDERING  only enough English to make review practical (NOT itself the gold)
E. PROPOSED ARGUMENT  propositions, commitment/speaker, inference(s), conclusion
F. DERIVATION MAP     P1 ← Sanskrit span X ; P2 ← span Y ; I1 ← P1 + P2 + warrant W
G. KNOWN RISKS        MODEL-1 objections, ambiguous parse, reconstruction vs extraction, scope
H. REVIEW QUESTIONS   4 separate questions + ACCEPT / REVISE / REJECT / ABSTAIN
```

### Explicitness labels (used throughout — a reviewer may accept grounding but reject a reconstruction)

```text
TEXTUALLY_EXPLICIT          the Sanskrit states it directly
TEXTUALLY_SUPPORTED         supported by the Sanskrit as a reading, not stated verbatim
RECONSTRUCTED_NECESSARY     required to make the inference work (a reconstruction)
INTERPRETIVE_EXTENSION      goes beyond the passage (identification/synthesis claim)
```

### The four review questions (not a single vague ACCEPT)

1. **Textual grounding:** Are the proposed propositions licensed by the Sanskrit?
2. **Attribution:** Are they attributed to the correct speaker / position (siddhānta vs pūrvapakṣa)?
3. **Reconstruction:** Is the proposed inference a defensible reconstruction rather than an imported argument?
4. **Alternatives:** Is there a materially plausible rival reading or reconstruction that should remain open?

Record **ACCEPT / REVISE / REJECT / ABSTAIN** for *each of the four* (a scholar may accept the Sanskrit
grounding but reject the reconstruction).

### Prior machine review — how to read it

For each argument, the **MODEL-1** verdict is shown under **PRIOR MACHINE REVIEW**. It is:

```text
PRIOR MACHINE REVIEW
not evidence
not adjudication
useful only as a list of objections to inspect
```

Do not let it anchor your verdict. If MODEL-1 said REJECT, inspect *why* — but decide on the Sanskrit.

---

## Status

- **Basis:** v2 — primary-Sanskrit grounded; every proposition has ≥1 resolving primary span.
- **Machine gate:** `check_review_packet.py` passes (every proposition resolves; every inference ref resolves; L2-dependence ZERO).
- **Status ladder:** MACHINE_PROPOSED → FOUNDER_REVIEWED → INDEPENDENT_REVIEWED → SPECIALIST_REVIEWED → ADJUDICATED.
  The five remain CANDIDATE. A MODEL review exists (MODEL-1) — `MODEL_INDEPENDENT_REVIEWED`, NOT `INDEPENDENT_REVIEWED`.
  After ONE clean argument crosses `INDEPENDENT_REVIEWED`, it becomes the target for the external formal-evaluator (py-aspic) pilot.
- **Reviewer needed:** independence from the builder + competence to falsify reconstruction errors. A Sanskrit /
  Indian-philosophy PhD, postdoc, teacher, or advanced researcher is sufficient for a first pass.

---

## ARG-002 — The Non-constructed I (objection → reply, V2-L)

### A. REVIEW TARGET
The objection→reply argument: reflexive awareness ('I') is linguistically expressed, yet is **not** a
conceptual construction (vikalpa). Target: proposition G2-CONC + the distinction it rests on.

### B. PRIMARY SOURCE
- **Passage:** `pt:passage:ipvv:chunkV2-L-sastho-vimarsa-smrti-apohana.md`
- **Edition:** Torella's ĪPK, sixth vimarśa (smṛti/apohana śaktis), kārikā 1:
  > ahaṃpratyavamarśo yaḥ prakāśātmāpi vāgvapuḥ / nāsau vikalpaḥ sahyukto dvayākṣepī viniścayaḥ
- **Source:** `M00021` lines 8405–9200 (T1 primary, `02_t1/chunkV2-L-sastho-vimarsa-smrti-apohana.md`).

### C. L0 EVIDENCE
| Prop | Span (resolvable) | Lemma |
|---|---|---|
| G2-OBJ | `chunkV2-L-sastho-vimarsa-smrti-apohana:L31:T112` | vikalpatvāśaṅkā (the vikalpa-construction objection is raised) |
| G2-TC2 | `chunkV2-L-sastho-vimarsa-smrti-apohana:L28:T87` | ahaṃ ('I') |
| G2-TC2 | `chunkV2-L-sastho-vimarsa-smrti-apohana:L28:T88` | pratyavamarśo (reflexive awareness) |
| G2-TC2 | `chunkV2-L-sastho-vimarsa-smrti-apohana:L29:T93` | vikalpaḥ (negated: nāsau vikalpaḥ) |

P0 proof: the chunk's L0 floor passes P0 (exact spans, lossless). No L0 uncertainty/conflict markers
were flagged for these spans.

### D. MINIMAL RENDERING
"I-reflexive-awareness which, though of the nature of manifestation, has word as its body — that is
not a conceptual construction; joined to both, it is a determination that invokes both [the object and
the word]." (kārikā 1; literal, for review convenience only — not itself the gold.)

### E. PROPOSED ARGUMENT
| Prop | Explicitness | Speaker | Text |
|---|---|---|---|
| G2-OBJ | TEXTUALLY_EXPLICIT | objector | If reflexive awareness is joined to linguistic form, why is it not simply vikalpa? |
| G2-TC1 | TEXTUALLY_SUPPORTED | siddhānta | vikalpa operates by combining / differentiating / determining contents. |
| G2-TC2 | TEXTUALLY_EXPLICIT | siddhānta | The 'I'-awareness is not one more constructed relation. |
| G2-CONC | RECONSTRUCTED_NECESSARY | siddhānta | Linguistic articulation does not show self-awareness is produced by conceptual determination. |
| G2-IC1 | INTERPRETIVE_EXTENSION | reviewer | Abhinavagupta preserves a distinction between reflexive awareness and the operations that articulate it. |

Inference: **G2-INF1** (CONCEPTUAL_DISTINCTION) — G2-TC1 + G2-TC2 → G2-CONC.
Warrant (carried on the InferenceRule, per IR-F-04): being expressible in language does not entail being
a product of conceptual determination (articulation ≠ construction).

### F. DERIVATION MAP
```
G2-OBJ   ←  L31:T112  (vikalpatvāśaṅkā)
G2-TC2   ←  L28:T87 (ahaṃ) + L28:T88 (pratyavamarśo) + L29:T93 (vikalpaḥ negated)
G2-CONC  ←  L28:T88 (pratyavamarśo as vāgvapuḥ) + L29:T93 (nāsau vikalpaḥ)   [reconstructed]
G2-INF1  ←  G2-TC1 + G2-TC2 + warrant (articulation ≠ construction)
```

### G. KNOWN RISKS
- **MODEL-1 (PRIOR MACHINE REVIEW):** REVISE (MINOR). Note: the reconstructed warrant ('articulation ≠
  construction') belongs on the InferenceRule, not as an ordinary Proposition — applied here.
- **Reconstruction vs extraction:** G2-CONC is RECONSTRUCTED_NECESSARY — it is the conclusion the
  objection→reply forces, not a sentence found verbatim.
- **Scope:** the passage preserves reflexive awareness *distinct from* construction; it does not by
  itself establish a universal single subject.

### H. REVIEW QUESTIONS
1. Textual grounding: ______
2. Attribution: ______
3. Reconstruction: ______
4. Alternatives: ______

**DECISION:** ACCEPT / REVISE / REJECT / ABSTAIN (circle one, per question)

### CURRENT EVIDENCE VECTOR (honest, not a binary gold label)

```
state                        SCHOLARLY_UNREVIEWED · HIGH_CORROBORATION pending
primary_text_grounding       strong (all props → resolvable L0 spans)
morphology                   supported (L0 floor P0-clean)
published_scholar_corrob     not yet collected (step 2, requires source care)
model_reconstruction_agree   not yet run blind (step 3)
rival_reading                present (see G. scope note: no universal-subject claim)
attribution_confidence       high for siddhānta/pūrvapakṣa split on this passage
scope                        local (V2-L), not systematic
```

This object is `MACHINE_PROPOSED → CANDIDATE`. It is NOT yet `MULTI_MODEL_CORROBORATED`,
`SCHOLARLY_CORROBORATED`, or `INDEPENDENT_REVIEWED`. The gate remains real; the evidence vector only
makes the current (low) status explicit rather than hiding it behind a binary label.

---

## ARG-001 / ARG-003 / ARG-004 / ARG-005

Built in the same A–H structure from the machine packet
(`benchmarks/v0/review/ARG-GOLD-REVIEW-PACKET-v2.json`). Primary sources:

| Arg | Passage | Key primary spans (L0) | MODEL-1 |
|---|---|---|---|
| 001 | V2-O (saptamo vimarśa) | `L32:T115` (tattatpadārthakramarūṣitā), `L44:T168` (sakramatvādi…), `L30:T108` (tam ekam āśrayam) | REVISE (MAJOR) |
| 003 | V2-O (reductio) | `L26:T52` (āśrayasya), `L74:T616` (kramavattvalakṣaṇāt) | REJECT_AS_TEXTUAL_GOLD (see risk below) |
| 004 | V2-H (prakāśa/vimarśa) | `L9:T23` (prakāśo), `L9:T66` (bhedena hi parāmarśe), `L142:T2396` (sphurad api) | REVISE (MODERATE) |
| 005 | V3-I (difference/action) | `L9:T5` (sattvam), `L9:T840` (yo bhedaḥ), `L18:T1083` (bhedas tu) | REVISE (MAJOR) |

**ARG-003 specific risk (do not anchor):** MODEL-1 ruled the *regress* reconstruction is not licensed as
textual gold (it is a rational reconstruction). Treat `G3-ASSUM`/`G3-REG`/`G3-ABS` as
RECONSTRUCTED_NECESSARY — a reviewer should judge whether the reductio is *defensible*, not whether the
passage literally states it. This is exactly the case where a scholar may accept the Sanskrit grounding
but reject the reconstruction — the two must not collapse into one verdict.

## Evidence vectors (honest current state — not binary gold labels)

Each argument carries an evidence vector, not a forced ACCEPT/REJECT. `state` reflects the
evidence-hierarchy ladder (CLAIMS.md). Everything here is `MACHINE_PROPOSED → CANDIDATE`; the vector
only makes the (low) status explicit.

| Arg | state | primary grounding | morphology | scholar corrob | model agree | rival | attribution | scope |
|---|---|---|---|---|---|---|---|---|
| 001 | SCHOLARLY_UNREVIEWED · CANDIDATE | strong (all → L0) | supported | not collected | not run | present (orderless≠ordered) | high (siddhānta) | local (V2-O) |
| 002 | SCHOLARLY_UNREVIEWED · CANDIDATE | strong (kārikā 1) | supported | not collected | not run | present (no universal subject) | high (siddhānta/pūrvapakṣa) | local (V2-L) |
| 003 | SCHOLARLY_UNREVIEWED · CANDIDATE | strong on āśraya/akrama; regress RECONSTRUCTED_NECESSARY | supported | not collected | not run | present (regress vs literal text) | disputed (regress is reconstruction) | local (V2-O) |
| 004 | SCHOLARLY_UNREVIEWED · CANDIDATE | strong (prakāśa/vimarśa) | supported | not collected | not run | present (vimarśa-as-essence vs inferred) | high (siddhānta) | local (V2-H) |
| 005 | SCHOLARLY_UNREVIEWED · CANDIDATE | strong (bheda/action) | supported | not collected | not run | present (local vs systematic) | high (siddhānta) | local→systematic (open) |

**To promote these:** (1) published-scholar corroboration (exact passages, Ratié/Torella/etc.);
(2) blind multi-model reconstruction agreement (Sanskrit+L0 only); (3) contrast-set semantic
discrimination; and only then (4) independent human review — the real gate.

---

*Reviewer's output should name, for each of the four questions, the decision + the primary evidence (or
absence of it) that drove the decision. Every correction is captured as a ReviewEvent and becomes a
benchmark candidate.*
