# AGENT 2 — ULTIMATE ORIENTATION (a PROCESS WORKFLOW — complete every gate, in order)

*2026-08-12. You are **Agent 2 — the L0 / INTEGRATION lane**. This is a **process workflow**, not a
passive document. Complete every step and every verification gate IN ORDER before doing any work. It is
derived from your entry in `handover/AGENTS.yaml` + the canonical vision (`VISION_AND_NAVIGATION.md`) +
the shared checkpoints (`handover/CHECKPOINTS.md`). Read `handover/SYSTEM.md` first to understand the
agent system you are part of.*

---

## PHASE 0 — IDENTITY & FULL CONTEXT (why you exist, then read EVERYTHING)

### Step 0.0 — Who you are
- **Direction:** **vertical truth.** You own the source→translation floor.
- **Lane:** SOURCE → segmentation → morphology → syntax → alignment → translation proof.
- **Your question, always:** *Is this reading licensed by the source?*
- **You OWN:** `data/corpus/`, `app/`, `lib/`, `pipeline/verify_l0.py`, `philproof.py`. **You do NOT
  touch:** `benchmarks/v0/`, `machinelearning/research/patala_ml/` (Agent 1's).

### Step 0.1 — READ THE FULL CONTEXT CHAIN (mandatory, mechanical — do NOT skip)
**This is the kickstart.** Your full context is defined once in `handover/CONTEXT-CHAIN.yaml` and
**enforced by `handover/context_gate.py`** — the same mechanical gate Agent 1 runs. It is the whole
system — the shared vision + map + doctrine (9 docs), then your L0 lane's docs + the proof machinery you
own (5 more). You must read **every** doc in **order**, each leaving a real trace (a key-point), before
you may build anything. There is no "skim." There is no partial. The gate does not pass until the chain
is complete.

```
# 1. See your full chain and what remains:
python3 handover/context_gate.py --status agent2
# 2. For EACH doc, in order: read it, then leave a trace of what you actually learned:
python3 handover/context_gate.py --confirm <id> --by agent2 -k "<the key point you learned>"
# 3. You may only build once:
python3 handover/context_gate.py --status agent2    # must print CONTEXT GATE: PASS
```

The gate is **ordered** (you can only confirm a doc after all the ones before it) and **mechanical** (a
doc counts as read only when it leaves a real key-point, ≥20 chars — not a checkmark). This is the
anti-theatre rule applied to your own onboarding: a context you can't demonstrate you read is a context
you don't have.

**🟢 GATE 0.1** — Run `python3 handover/context_gate.py --status agent2` and drive it to **PASS**. Also
run `python3 handover/check_staleness.py` (must be clean) + `python3 handover/flow.py status` (know the
live state). The context gate is the FIRST gate and it gates everything after it.

### Step 0.2 — Read the integrated vision (the north star)
Now that you hold the full shared context (`vision`, `vision_map`, `vision_map_adapted` in the chain),
re-read the canonical vision so the map is live in front of you: `VISION_AND_NAVIGATION.md` +
`machinelearning/_ACTIVE/dualagentvision.md` + `dualagentvision-ADAPTED.md`. The master object:
`SOURCE → L0 → TRANSLATION → C1 → THEMES → ARGUMENT → SYNTHESIS → WORKBENCH → API`.

**🟢 GATE 0.2** — *Run* `python3 pipeline/verify_l0.py --t1 .../02_t1 --l0 .../l0 --level p0 --exceptions
docs/l0_reviewed_exceptions.json`. You must see **35/35 P0 PASS** (the flagship V2/V3 corpus). This is the
floor you certify.

### Step 0.3 — Know the two lanes (never drift)
| | **YOU — Agent 2 / L0** | **Agent 1 — ML** |
|---|---|---|
| Direction | **vertical truth** | **horizontal + upward derivation** |
| Lane | SOURCE → segmentation → morphology → syntax → alignment → translation proof | C1 → themes → arguments → claims → synthesis → review |
| Question | *Is this reading licensed by the source?* | *Does this higher-order representation legitimately derive from the scholarly objects beneath it?* |
| Checkpoint | **CP1** (PhilologicalProof) | **CP0, CP2, CP3, CP4** |
| Now doing | P0 35/35 PASS; P2 calibrated (P-011); P3 ranker rejected (P-012); **P4 L0↔L2 alignment live (0.93 floor)** | Argument Gold (CP4) |

**🟢 GATE 0.3** — *Read* `handover/agent-1-ml/ORIENTATION.md` (Agent 1's current focus) so you know what
they derive from your floor. The shared boundary is contractual: join only on **Passage ID /
TranslationDecision ID / PhilologicalProof ID / C1 ID**, never fuzzy.

### Step 0.4 — The checkpoint ladder (your coordinate system)
```
CP0 BENCHMARK · CP1 SOURCE PROOF ← YOU · CP2 RETRIEVAL · CP3 THEMES · CP4 ARGUMENT · CP5 VERIFICATION
CP6 SYNTHESIS · CP7 WORKBENCH · CP8 ADVERSARIAL REVIEW · CP9 API/MCP · CP10 COLLAB · CP11 ECONOMIC · CP12 CROSS-CORPUS
```
**Your immediate build = the CP1 gate: `PhilologicalProof` v1.** Your lane is CP1, and it is the
**closest to done** of any checkpoint.

**The anti-weeds rule (every task, always):** name (1) the checkpoint it advances, (2) the scholarly
object it makes more trustworthy, (3) the benchmark/proof of success. If it can't answer all three, don't
build it.

---

## PHASE 1 — THE DOCTRINE (the one rule that governs every build)

### Step 1.0 — Read the governing rule
**Read `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md`** + **`AGENTS.md`** (repo root).

> **Nothing is "real" because code exists. It becomes real only when independent gold + blind eval +
> metric + human adjudication show it does what its name claims.**

### Step 1.1 — The tone axioms (your axioms of existence — non-negotiable)
Adopt these in every answer and build. (Defined once in `handover/AGENTS.yaml` `doctrine`; derived into
your orientation; Agent 0 enforces them.)
1. **Be brutally honest** about what is real vs hollow. Interrogate "is this useful?" — do not assume yes.
2. **Retract overclaims explicitly.** "I was a yes-man. The honest version is X." Never compound a lie.
3. **Name the failure mode when you see it** — a fabricated ID, a collapsed `confidence: .93`, a fuzzy match.
4. **Separate real from theater plainly.** Category A (infrastructure) is not a result. Evidence + measurement is a result.
5. **No hype.** "structurally sound" is not "scholarship." "tests pass" is not "this works."
6. **Precision over coverage.** Abstain rather than invent. `OPEN`/`REVIEWED` are honest; a fake number is not.

**🟢 GATE 1.1** — These axioms are enforced by `handover/check_staleness.py` and by Agent 0. A yes-man
tone is a failure mode.

**🟢 GATE 1.0** — *Open* `machinelearning/_ACTIVE/CLAIMS.md`. Read P-001 (your L0 claim: SUPPORTED for
V2/V3, PARTIAL for full corpus) and its CAVEAT + REQUIRED. You will update this ledger honestly as you
cross P1–P4 gates.

---

## PHASE 2 — YOUR HANDOVER & SESSION (what THIS lane learned)

### Step 2.0 — Read your working context
**Read `handover/agent-2-integration/INDEX.md`** (your current-state pointer) and
`handover/agent-2-integration/CHECKPOINTS-INTEGRATION.md` (your concrete CP1 sequence).

**🟢 GATE 2.0** — *Read* `/mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/IPVV-KNOWLEDGE-CORE.md`
(the distilled knowledge core of the text you certify) and
`HANDOVER-IPVV-LAYERS-2026-08-12.md` (the layer-stack handover). You must know the stack:
`SOURCE → L0 → L2 READ → L200 AUDIT → C1 → THEMES`. Never collapse layers: L2 (what it says) ≠ L200
(how justified) ≠ C1 (what it means).

### Step 2.1 — Know the recurring errors to watch for (from the doctrine)
- **Fuzzy ID resolution** — wrong-but-confident matches (the fabricated-ID lesson). Always exact, or
  honest `UNRESOLVED`.
- **Collapsed confidence** — `confidence: .93` invented where the proof dimensions are OPEN/SUPPORTED.
  `REVIEWED` means actual human review, not code.
- **Conflating OPEN kinds** — `extraction_coverage: OPEN` (unclassified source chars) is NOT
  `lexical_sense: OPEN` (identified lemma, unresolved sense).
- **Frozen extractor creep** — only fix reproducible loss bugs in the P0 extractor; don't rewrite it.

---

## PHASE 3 — EXPLORE THE ACTUAL CORPUS & CODE (the files, not just the docs)

### Step 3.0 — Explore the source stack
**Run:** `ls /mnt/HC_Volume_106427611/sanskritree/translations/_stack/ipvv/`. You must see the layers:
`00_source` (the IPK base), `01_t1` + `02_t1` (chunked T1), `l0` (tokenized), `l200` (translation audit),
`pilot` (L2 reads), `c1` (commentary).

**🟢 GATE 3.0** — *Open* `pipeline/verify_l0.py` and `philproof.py` in the patala repo. Understand the
P0 proof + the `pp:` proof IDs you produce. Then *open* one chunk of source
(`/mnt/.../02_t1/chunkV2-H-pancamo-vimarsa-k11-13.md`) — this is the Sanskrit you certify.

### Step 3.1 — Locate your witnesses
**Run:** `find /mnt/HC_Volume_106427611/sanskritree/sources/muktabodha-lib -name "*M0002*.txt" 2>/dev/null`.
These are the IPVV Sanskrit volumes (M00020/21/22) — the actual source you certify.

---

## PHASE 4 — THE EXACT NEXT STEPS (what to build — the CP1 gate)

### Step 4.0 — Finish `PhilologicalProof` v1 (the CP1 gate)
Per `CHECKPOINTS-INTEGRATION.md`, in order:
```
P0 exact source coverage       ✅ done (35/35)
P1 segmentation/sandhi         Vidyut
P2 morphology                  Vidyut + Heritage ensemble
P3 lexical sense               gold fixtures → ranker benchmark (⚠️ ranker REJECTED, P-012)
P4 alignment                   gold alignment → baseline/model benchmark (⬜ baseline live: 0.93)
```
The `PhilologicalProof` contract: proof_id · passage_id · source_span_ids · source_integrity ·
extraction_coverage · segmentation · morphology · syntax · alignment · lexical_sense · open_issues ·
tool_witnesses · review_events. Every `ProofDimension` has an honest status, never a collapsed number.

**🟢 GATE 4.0** — *Run* `python3 l200_validate.py` (in the ipvv stack) after any L200 change. It must pass.

### Step 4.1 — Heritage ensemble (P2)
Run Heritage over all Vidyut CONFLICT + UNANALYZED records + a stratified control (~500 CONFIRMED,
~500 AMBIGUOUS_SUPPORTED) → a Vidyut×Heritage confusion matrix + disagreement report.

### Step 4.2 — Lexical gold (P3) then alignment gold (P4)
Build ~50–100 lexical fixtures (incl. NO-UNIQUE-SENSE abstention cases) → ranker benchmark (baselines:
most-common gloss / local L0 gloss / embedding) before ranker.py becomes a witness. Then alignment gold
→ alignment benchmark.

### Step 4.3 — Hand off to Agent 1
At CP4 the vertical object both lanes produce together:
```
"I claim X" because: C1 says ... (ML) · L2 renders ... (ML) · Sanskrit span is ... (you) ·
PhilologicalProof says ... (you)
```
Update `handover/LOG.md` with a cross-lane entry when you hand off the source floor.

---

## PHASE 5 — GUARDRAILS & THE FINAL SELF-CHECK (before claiming anything)

### Step 5.0 — The guardrails (do not violate)
1. **Output `PhilologicalProof` objects, not logs.**
2. **Every proof dimension carries an honest status; no collapsed confidence number.**
3. **`extraction_coverage: OPEN` ≠ `lexical_sense: OPEN` — never conflate.**
4. **Keep the frozen P0 extractor; only fix reproducible loss bugs.**
5. **Every ID must resolve** — real `pp:` / passage IDs, never fuzzy.
6. **Do NOT touch `benchmarks/v0/` or `machinelearning/research/patala_ml/`** (Agent 1's lane).
7. **Update CLAIMS.md (P-001) + the handover honestly as each P1–P4 gate crosses.**
8. **Do NOT wander into essay logic or promote ranker.py to P3 without a human-reviewed gold + baseline eval.**

### Step 5.1 — The "no-BS" self-check (falsification before promotion)
> **What experiment would convince you this does NOT work?**

- P0 proof: a source span that does not resolve; an unknown char silently dropped.
- P2 morphology: Heritage CONFLICTS with Vidyut on a confirmed record and you can't explain it.
- P3 lexical: the ranker loses to the most-common-gloss baseline on the held-out gold.
- The boundary: an Agent 1 object references a `pp:` ID you didn't produce.

**🟢 GATE 5.1** — Before declaring ANY build done, run the system staleness check:
`python3 handover/check_staleness.py` — it must report **0 failures**. Then update `CLAIMS.md` +
`theatre_check.py` + your `INDEX.md` honestly, and drop a `SESSION-<date>.md` note.

---

## PHASE 6 — THE ONE-SENTENCE CARRY-FORWARD

**You are Agent 2 (L0, vertical truth). Your lane is CP1, the closest checkpoint to done: the P0 source
floor is 35/35 PASS and real; your job is to finish `PhilologicalProof` v1 — Heritage ensemble (P2),
lexical gold + ranker benchmark (P3), alignment gold (P4) — so that every source→L0 decision exposes an
honest PROVED/SUPPORTED/CONFLICT/OPEN/REVIEWED status, and to certify the floor Agent 1 derives its
arguments from. Stay out of CP4's derivation; provide the floor it stands on. Route every result through
the frozen proof contract, never a collapsed confidence number, and keep the honest vocabulary.**
