# BUILD: THE CP4 ARGUMENT FRONTIER — the philosophical IR (the moat ip-graph lacks)

*2026-08-14 · status: THE FRONTIER BUILD (for agentgraph) · the precise build spec for the argument
layer — CP4, where both lanes CONVERGE per CHECKPOINTS.md. ip-graph has `verification_ensemble.py` but NO
argument IR, NO crux engine, NO philological proof. OG patala has all of it. Reference the ACTUAL files.*

---

## THE GAP

CHECKPOINTS.md: **"Phase 3 — MACHINE-READABLE PHILOSOPHY (just beginning — CP4 is the frontier)."**
ip-graph has built the spine + the front-end (theme→essay→education→pedagogy→products), but it has NO
argument layer. OG patala has the argument IR + engines. This is the moat, and ip-graph is missing it.

---

## THE REAL OG PATALA FILES (the argument frontier)

### 1. The argument IR spec (the philosophical intermediate representation)
**`/root/projects/patala/machinelearning/_ACTIVE/ARGUMENT-IR-VISION.md`** — the CP4 target:
- The 4 real additions over a naive ontology:
  1. `Commitment` (who asserts/denies/attributes/reconstructs — fixes the pūrvapakṣa-as-Abhinava's-own error)
  2. `ResearchQuestion` as a first-class object (the scholar's navigation unit)
  3. `Position` as a bundle of commitments+arguments under a frame
  4. **Derivational `Proposition`** — every proposition remembers HOW it came into existence
- The 14-object horizon (the schema to freeze, activate only what gold needs)
- The build order: **gold first, ontology second** (ARG-GOLD-002..005 → the objects they force)

### 2. The argument engines (the implemented machinery)
| File | What it is |
|---|---|
| `machinelearning/research/patala_ml/argument.py` | the argument model (premises/inference/conclusion/defeaters) |
| `machinelearning/research/patala_ml/crux_engine.py` | the Crux primitive (the minimum unresolved proposition) |
| `machinelearning/research/patala_ml/nyayagate.py` | the Nyāya gate (validity ≠ soundness, bounded) |
| `machinelearning/research/patala_ml/aspic_adapter.py` | the ASPIC+ argumentation semantics |
| `machinelearning/research/patala_ml/aifgraph.py` | the AIF argument-interchange graph |
| `machinelearning/research/patala_ml/proposition_layer.py` | the proposition layer |
| `machinelearning/research/patala_ml/builders.py` | the argument builders |
| `ai/` (VISION.md, argumentation-ir-frameworks-survey, argumentation-ir-exec-summary) | the deep-research that grounded it |

### 3. The argument golds (the evidence that makes it real)
- `machinelearning/research/patala_ml/gold002.py` … `gold005.py` — ARG-GOLD-002..005 with
  `scholarly_corroboration`
- `pipeline/ingest_ipvv_argmap_golds.py` — ingests the 51 real IPVV ARGMAP golds (50/51 committed)
- `data/evaluation/recovery-gold-v1.json` (51 cases) — the argument-recovery benchmark gold

### 4. The philological proof (CP1, the source→L0 ground for arguments)
- `pipeline/certificate_l0.py` — the deterministic L0 floor cert
- `source-evidence/evals/patala/tasks/atlas_nat.py` — the atlas NAT (grounds propositions to source)

---

## WHAT TO BUILD (wire the argument layer into ip-graph's organism)

### The build:
1. **Port OG's `argument.py` + `crux_engine.py` + `nyayagate.py` + `aspic_adapter.py` + `aifgraph.py` +
   `proposition_layer.py` into ip-graph's kernel set** (they're the CP4 engines ip-graph lacks).
2. **Wire the derivational `Proposition` + `Commitment` + `ResearchQuestion` + `Position`** (from
   ARGUMENT-IR-VISION) into `essay_ingest`'s output — so the essay's claims become first-class argument
   objects, not strings.
3. **Add the crux to `ingestion_organism.refine()`** — the organism's Argument step produces
   propositions → arguments → cruxes (via `crux_engine`), gated by the Nyāya gate.
4. **The argument golds drive it** — `ingest_ipvv_argmap_golds` (51) + the recovery-gold (51) are the
   evidence. The philosophy layer is gold-first.

### The WHY:
The thesis's moat is the **philosophical IR** — "Pāṭala should own the historically grounded philosophical
IR that existing engines cannot provide." ip-graph has the front-end (essay/education) but the ESSAYS need
ARGUMENTS beneath them. Without the argument layer, the essays are prose, not proof-linked claims. CP4 is
where the two lanes converge, and it's the frontier.

---

## THE TEST

```bash
# run the crux engine on a real claim
python3 -c "
import sys; sys.path.insert(0,'/root/projects/patala/machinelearning/research/patala_ml')
from crux_engine import <the crux primitive>
print('crux engine runs on the argument layer')
"
# verify the argument golds are real
python3 /root/projects/patala/pipeline/ingest_ipvv_argmap_golds.py --dry-run
```

**Pass when:** a real IPVV/Stk claim → propositions → argument (AIF) → crux (minimal divergence),
gated by the Nyāya gate, grounded by the philological proof — producing proof-linked arguments that the
essay/education layers consume. That's CP4 real.
