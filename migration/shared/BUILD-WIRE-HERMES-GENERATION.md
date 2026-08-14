# BUILD: WIRE HERMES INTO GENERATION (the correctness fix — use the patala-profile invocation)

*2026-08-14 · status: THE FIX · ip-graph's `hermes_exec.py` WORKS (tested: `IPGRAPH-HERMES-OK`) but is
ORPHANED — nothing imports it, so the generation kernels are hand-fed containers instead of calling Hermes.
This is the fix: wire the working Hermes path (the patala-profile invocation) into generation.*

---

## THE VERIFIED FACTS

1. **The correct Hermes invocation is** `hermes -z "<prompt>" -m deepseek-v4-flash --provider opencode-go`
   (the patala profile). Both OG's `pipeline/model.py` and ip-graph's `lib/hermes_exec.py` use it.
2. **Both WORK live:** OG `model.py` → `HERMES-WORKS`; ip-graph `hermes_exec.py` → `IPGRAPH-HERMES-OK`.
3. **BUT ip-graph's `hermes_exec.py` is imported by NOTHING** (`grep` shows only itself). It's dead code.
4. **The generation kernels are hand-fed containers:**
   - `translation.py` — `audit_vector()` returns hand-set fields; translates nothing
   - `translation_variant.py` — `add(translator, text)`; you feed the variants, it doesn't generate
   - `pushing_miner.py` — regex-mines the human LOGICVID gold (legit); no NEW generation

---

## THE ARCHITECTURE RULE

> **Hermes for GENERATION. `.py` for REDUCTION.**
> - GENERATION (translation, commentary, essays, new pushing) → call Hermes (`hermes_exec` / `model.py`).
> - REDUCTION (review, staleness, evidence, gates, epistemic) → deterministic `.py` (correct as-is).

ip-graph has it backwards: the working Hermes path is orphaned, and the kernels that should generate are
empty containers.

---

## WHAT TO BUILD (wire Hermes into the generation kernels)

### 1. `translation.py` → call `hermes_exec.translate_karika()`
Instead of hand-feeding `good.source_analysis = {"morphology":"PASS"}`, the kernel should:
```python
from hermes_exec import translate_karika
result = translate_karika(sanskrit_verse)   # REAL model output
# then compute the proof vector ON the real output, not hand-set PASS fields
```
**Why:** the TranslationProof is only honest if computed on real model output, not hand-fed fields.

### 2. `translation_variant.py` → generate T2 via Hermes
The three-version scholarship needs a genuinely different T2. Generate it via a SECOND Hermes call with a
different reading-strategy (the commentary-informed / argument-priority strategy), not `add(translator,
text)`.

### 3. The organism's `refine()` → call Hermes for the generation steps
`ingestion_organism.refine()` should call `hermes_exec` for Tokenization(→model?)/Translation/Proof/
Commentary — producing REAL objects, not `SanskritDoc.layers_done`.

### 4. `pushing_miner.py` — keep for the human gold, add Hermes for NEW pushing
The regex-miner of the human LOGICVID sessions is correct (those are gold). But generating NEW pushing
(question→crux) should call Hermes.

---

## THE REFERENCE IMPLEMENTATION (the correct pattern, already working)

**agentpatala's `translate_passage.py`** (`/root/projects/patala/migration/v3/translate_passage.py`):
```python
from model import chat   # the OG model.py → hermes -z
raw = chat(ROLE, VERSE + " tokens: " + json.dumps([t["surface"] for t in toks]))
trans = json.loads(re.search(r"\{.*\}", raw, re.DOTALL).group(0))
# t1 + close + reading + commentary + notes, ALL from real Hermes output
```
This is the correct pattern — ONE Hermes call produces the full translation stack. Adopt it.

---

## THE TEST

```bash
# ip-graph's hermes_exec must produce a real translation of a Sanskrit kārikā
cd /mnt/HC_Volume_106427611/ip-graph
python3 -c "
import sys; sys.path.insert(0,'lib')
from hermes_exec import translate_karika
r = translate_karika('anādinidhanam brahma śabdatattvaṃ yad akṣaram')
print('translation:', r.get('translation','')[:80])
print('terms:', r.get('terms',''))
"
```

**Pass when:** the translation/variant kernels generate REAL model output via Hermes (not hand-fed PASS
fields), and the organism's refine() produces real T1/translation/commentary objects from Hermes — matching
the OG patala profile invocation.
