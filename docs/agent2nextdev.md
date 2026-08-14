> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# AGENT 2 — NEXT DEV (the production-grade autonomous corpus compiler)

*2026-08-13. The definitive long-horizon roadmap for Agent 2. The culmination is NOT "a bunch of
workers." It is a **production-grade autonomous corpus compiler** that takes a registered Sanskrit work
and keeps advancing it through the canonical stack without babysitting. This is the permanent north star:

> **Given canonical sources, contracts and upstream corrections, continuously materialize the entire
> downstream scholarly object graph correctly, reproducibly and autonomously.**

---

## 0. THE END-TO-END FACTORY (what Agent 2 builds)

```
REGISTER WORK
   ↓
SOURCE
   ↓
T1              AI
   ↓
L0              deterministic
   ↓
ARGUMENT MAP    AI
   ↓
L2              AI
   ↓
L200            constrained AI
   ↓
C1              AI
   ↓
COMMIT + TRACK + REPORT
   ↓
NEXT PASSAGE / NEXT WORK
```

The user experience is one command:
```bash
patala ingest kubjikamata        # or: patala factory run --work kubjikamata
```
and the system knows `SOURCE 100/100 · T1 38/42 · L0 38/38 · ARGMAP 31/38 · L2 29/31 · L200 22/29 ·
C1 20/22` and simply continues from the correct frontier. Workers become implementation details.

---

## 1. THE FOUR THINGS AGENT 2 MUST FINISH

### 1.1 Every canonical layer has a real autonomous producer
Not placeholders, not test scaffolds. Each layer has: `worker · validator · registry · dependency
declaration · retry behavior · failure state · supersession behavior · production certificate`. Then:
```
T1/L0/ARGMAP/L2/L200/C1  AUTONOMOUSLY_PRODUCIBLE
```
while semantic quality remains Agent 1's separate axis.

### 1.2 One controller owns the whole work lifecycle
The controller advances a work from its current frontier, never requiring manual `worker_a.py` +
`worker_b.py` + `fix_registry.py` invocation.

### 1.3 The corpus ledger is the operational truth
One canonical view per work: `SOURCE 100/100 · T1 97/100 · L0 97/97 · ARGMAP 88/97 · L2 84/88 · L200
79/84 · C1 76/79 · FAILED 3 · OPEN 8 · STALE 2 · RETRYABLE 4`. The **registry**, not prose docs, is
authoritative. Docs explain architecture; runtime state says what is actually done.

### 1.4 Prove whole-work autonomy (the graduation test)
Take ONE fresh Sanskrit work not used to build the workers; process it unattended from registered source
through C1. Prove: multiple passages · multiple model calls · timeouts · malformed responses · retry ·
one failed passage doesn't block neighbors · crash+restart · resume from registry · zero duplicate
commits · correct parent hashes · correct model/prompt/skill provenance · stale dependency handling ·
final corpus report. Then replay: `0 duplicate canonical objects · 0 unnecessary regeneration`.

---

## 2. THE THREE ERAS

### Era A — Factory completion (NOW)
```
A2-1 SOURCE→T1      A2-2 T1→L0      A2-3 ARGMAP
A2-4 L2             A2-5 L200       A2-6 C1
A2-7 full fresh-work unattended proof
```
**Exit:** one real work autonomously compiles through C1.

### Era B — Corpus compiler
```
A2-8  backlog scheduler      A2-9  multi-work execution
A2-10 resource/rate limiting A2-11 durable failure/retry queues
A2-12 corpus progress dashboard/state   A2-13 unattended bulk translation
```
**Exit:** Pāṭala continuously turns a corpus backlog into SOURCE→C1 objects.

### Era C — Living rebuild engine
```
A2-14 supersession propagation      A2-15 dependency invalidation
A2-16 targeted regeneration         A2-17 correction shock test
A2-18 ImpactReport integration      A2-19 review-bundle generation
A2-20 release/package builds
```
**Exit:** correcting one upstream scholarly object automatically updates every affected downstream
machine artifact without corrupting provenance.

---

## 3. THE FINAL DEMONSTRATION
1. Register new Sanskrit text.
2. Agent 2 autonomously compiles 100 passages through C1.
3. Agent 1 evaluates outputs + attaches machine proofs.
4. Scholar corrects one technical term in passage 37.
5. Pāṭala versions the correction.
6. Agent 2 detects 14 affected downstream objects.
7. Only those objects are invalidated/rebuilt.
8. Agent 1 re-evaluates them.
9. Scholar/product surfaces update.
10. Full before/after impact report preserved.

At that point Agent 2 = **a continuous scholarly compilation system** — the analogy is
`git + compiler + build graph + CI` for scholarship.

---

## 4. WHAT AGENT 2 DOES NOT OWN
After the autonomous SOURCE→C1 factory is proven, Agent 2 stops expanding sideways into: ML benchmark
research · scholar evidence retrieval · argument validity research · human review infrastructure · peer
assessment · external baseline studies. Its core competency = **reliable generation and dependency-aware
corpus maintenance**. Agent 1 = epistemic QA/research lab · Agent 2 = compiler + CI/CD system · Scholars
= reviewers/editors · Pāṭala graph = canonical repo · Products = views over compiled artifacts.

## 5. THE MAINTENANCE-ENGINE ROLE (later)
Agent 1 decides epistemically what changed; Agent 2 executes the rebuild graph:
```
source change → rebuild all dependent     T1 correction → rebuild L0 onward
ARGMAP correction → rebuild L2 onward     L2 correction → rebuild L200/C1
scholar review only → may change status, not regenerate
```
Agent 1: "This interpretation is revised." Agent 2: "These 37 objects depend on it; I have invalidated
and rebuilt the affected machine outputs."

---

## 6. TARGET REPO SHAPE (on completion)
```
pipeline/  controller/  workers/{source,t1,l0,argument_map,l2,l200,c1}.py  validators/  registry/
           dependencies/  reports/
contracts/ canonical-layer-stack...
skills/    translate-t1/  argument-map/  translate-l2/  audit-l200/  commentary-c1/
data/      corpus/registries/  runs/  works/
handover/agent-2-integration/  ORIENTATION.md  DEV-PLAN.md  CHECKPOINTS.md  CURRENT-STATE.md
```
**Retire/mark obsolete old scripts** — no six competing ways to do the same thing. That cleanup is part
of completion.

---

## 7. IMMEDIATE EXECUTION (this session — Era A)
Work ONE LAYER AT A TIME, validated against the real IPVV exemplars, then prove whole-work autonomy.
Current layer frontier: **T1 is verified against the IPVV exemplar gold (PASS)**. Next: L0 verified vs
`l0/*.l0.jsonl`, then ARGMAP, then L2/L200/C1, then the A2-7 fresh-work unattended proof.
