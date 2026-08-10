# Pāṭala Translation Pipeline

The automated, structured, audited translation flow. Turns a Sanskrit source into a
versioned per-passage record through the house pipeline:

```
T1 → R1 → T2 → R2 → T3 → T3.1 → C1
```

The whole thing **builds the material for the commentary** — every stage's output
feeds the next, and the audit validates each level.

> **The model is the translator; the evidence is ground truth.** The pipeline
> calls the model with house prompts; it does NOT invent scholarship. The audit
> catches schema violations and epistemic dishonesty at every stage.

---

## The stages (what each produces)

| Stage | Role | Output |
|---|---|---|
| **T1** | working translation | `close_translation` + `[X]`/typed flags + notes + **time-place-context** (PERIOD/PLACE/GENRE/FRAME) |
| **R1** | intimate peer review of T1 | per-crux verdicts (RIGHT/ERROR/FORK/OPEN) + **commentary stubs**; flags anything vague/unsure |
| **T2** | a **complete alternative** that **actively opposes T1** (informed by R1) | a second reading-strategy; a different interpretation wherever the Sanskrit allows it |
| **R2** | the **synthesis** | hard-core (where T1/T2 agree) · divergence · adjudication (which is best, + readability) · school/period-context research · **expanded commentary** · equally-valid alternates · OPEN markers |
| **T3** | the final resolved text | resolved + open-flags inline + editorial notes |
| **T3.1** | the reading layer (derived from T3, in lock-step) | natural-English, flowing, still accurate |
| **C1** | the commentary | plain-English interpretation; **may overturn T3** if evidence demands |

## The one-line method (the anti-cheat)

R1 reviews T1 intimately. T2 **actively goes against** T1 (not a re-wording — a
different reading). R2 **synthesises**: where they agree is the hard core; where
they diverge is adjudicated with evidence; the adjudication IS the commentary.
A flow that never corrects T1 is a flow not being run.

---

## Files

| File | What it is |
|---|---|
| `schema.py` | the passage-record data structure + stage constructors + lineage |
| `audit.py` | validates a record at every stage (schema + epistemic honesty) |
| `prompts.py` | the house prompts injected into the model per stage |
| `model.py` | the opencode-go model client (the model is the translator) |
| `run.py` | the orchestrator (calls the model, stores + audits each stage) |
| `exemplars.py` | **gold exemplars** — fully-populated reference records from real material (no model) |
| `exemplars_cli.py` | dump / audit / export the gold exemplars |
| `from_t1.py` | build a record from an existing on-disk T1 file (no model) |
| `gold_from_t1.py` | batch-generate gold records from on-disk T1s |
| `gold_records/` | generated gold records (one JSON per verse) |

---

## The data structure (schema.py)

One record per verse:

```json
{
  "passage_id": "tantra:text:kramasadbhava:1.8",
  "work_id": "kramasadbhava",
  "location": { "chapter": 1, "verse": 8 },
  "source": { "source_edition": "...", "source_file": "...", "source_text": "..." },
  "stages": { "T1": {...}, "R1": {...}, "T2": {...}, "R2": {...}, "T3": {...}, "T3.1": {...}, "C1": {...} },
  "audit": { "T1": [...findings...], ... },
  "lineage": [ { "stage": "T1", "created_by": "...", "derived_from": null }, ... ],
  "policy": { "translation_contract": "1.0.0", "style_guide": "1.0.0", "schema": "1.0.0" },
  "review_status": "C1"
}
```

**R2** is the richest stage — it carries the synthesis:

```json
"R2": {
  "chosen": "the resolved reading",
  "reasoning": "why",
  "hard_core": "where T1 and T2 independently agree",
  "divergence": "the difference between T1 and T2",
  "readability": "which reads better and why",
  "school_context": "research into the school/period",
  "commentary": "the expanded commentary (grown from R1's stubs)",
  "equal_alternates": ["an equally-valid alternate reading", "..."],
  "rejected": ["..."],
  "is_open": false
}
```

## The audit (audit.py)

Every stage is audited. Two jobs:
1. **Schema validity** — well-formed ids, locations, enums, ordering (stages must be
   contiguous T1→...→C1; T3 requires a prior R2).
2. **Epistemic honesty** — no empty close/resolved/reading; `[X]`/typed flags valid;
   flags not laundered; machine output never presented as reviewed.

Findings are `error` (fails the stage) or `warn` (flagged for human review).

---

## How to use it

### 1. Gold exemplars (no model — already done)
```bash
python3 pipeline/exemplars_cli.py --audit          # audit the 2 hand-built exemplars
python3 pipeline/gold_from_t1.py --all-kramasadbhava   # build gold records from the on-disk T1s
```

### 2. Run the full flow on one verse (needs the model + OPENCODE_GO_API_KEY)
```bash
export OPENCODE_GO_API_KEY=<key>
python3 pipeline/run.py <source.txt> <work_id> \
  --edition "..." --verse 49 --stages T1,R1,T2,R2,T3,T3.1,C1 --out out.json
```

### 3. Extend
- Add a work's T1s to the batch ingester → more gold records.
- Models populate the review stages guided by `exemplars.py` + the gold records.

---

## What's aligned with the spec docs

- **`corpus/targets/translation_flow_spec.md`** — the 7-stage flow, the T2-opposes-T1
  rule, R2-as-synthesis, C1-may-overturn, the status vocabulary.
- **`translations/_meta/PASS_PROTOCOL.md`** — provenance + time-place-context,
  [G]/[P]/[A]/[R] justification, `[X]` honesty, status vocabulary.
- **`translations/_meta/R1_CONTENT_ENGINEERING.md`** — R1 as prosecutor/reviewer,
  anchor-quotes, cross-text tie-breakers.
- **`docs/STYLE_GUIDE.md`, `EVIDENCE_POLICY.md`, `TRANSLATION_SCHEMA.md`,
  `REVIEW_PROTOCOL.md`** — the house voice, evidence discipline, data shape, workflow.

## Honest gaps

- **Anchor-loading** is not yet wired (the anchor-as-referee should enter at R1/R2).
- **T3.1-in-one-call** batching: generation can be batched, but R1/R2/C1 are
  independent/adversarial calls and must stay separate.
- **Term-proposal promotion** (to `terms.json`) is not yet wired to the records.
