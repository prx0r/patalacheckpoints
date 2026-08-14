# BUILD: THE CANONICAL CONTRACT CONVERGENCE (kill the divergent ReviewEvent/Authority)

*2026-08-14 · status: THE #1 BUILD (for both agentgraph + agentpatala) · the precise spec for converging
the divergent core contracts — the "five canonical contracts" specced in CHECKPOINTS.md exist in SIX
divergent forms across the two repos. This is the schema-divergence the whole project warns about, now at
the contract level. Reference the ACTUAL files.*

---

## THE PROBLEM (verified — 6 divergent definitions)

The CHECKPOINTS.md "five canonical contracts" (Ref · ReviewState/ReviewEvent · BenchmarkFixture ·
PhilologicalProof · EvidenceCandidate) exist in **six divergent implementations**:

### In OG patala (`/root/projects/patala/`)
| File | Defines |
|---|---|
| `source-evidence/schema/contracts_human_authority.py` | `ReviewEvent` (v1), `ReviewProposal`, `Adjudication`, `PromotionEvent` — "ReviewEvent ≠ status mutation; it's EVIDENCE ABOUT the target" |
| `source-evidence/schema/typed_scholarly_object.py` | `ReviewEventContent`, `ReviewProposalContent`, `ReviewEventObject` (Pydantic) |
| `python/patala_core/objects.py` | `ReviewEventContent`, `ReviewProposalContent`, `ReviewEventObject` (ANOTHER Pydantic set) |
| `pipeline/review_engine.py` | `ReviewEvent` (the ledger record) + `ReviewState` + the reducer |

### In ip-graph (`/mnt/HC_Volume_106427611/ip-graph/`)
| File | Defines |
|---|---|
| `lib/review.py` | `ReviewState` (4 phases: AWAITING/REVIEWING/CORRECTION/ALIGNED/HUMAN_OVERRIDE) + the herdr reducer |
| `lib/epistemic.py` | `Authority` (4-axis) + `EpistemicEnvelope` (the ceiling) |

**That's 4 ReviewEvent/state defs in OG + 2 in ip-graph = 6 that must become ONE.**

---

## THE WHY (the anti-theatre core)

The thesis says a tested schema ≠ a result; only independent gold + blind eval + human adjudication makes
something real. But if the *schema itself* is divergent — 6 different ReviewEvent types — then the same
scholarly review is represented incompatibly, and the "canonical contract" that CHECKPOINTS.md says to
freeze is NOT frozen. Every downstream capability (argument, synthesis, scholar attestation) embeds this
drift. **This must converge BEFORE building more on top.**

---

## THE CONVERGENCE TARGET (one contract set)

The five canonical contracts, one definition each:
```text
1. Ref                       — every ID resolves (OG: patala_core/ids.py + the pt: URN scheme)
2. ReviewState / ReviewEvent — the honest status ladder + the evidence-about-target contract
3. BenchmarkFixture / BenchmarkRun — the frozen evaluation objects
4. PhilologicalProof         — the source→L0 proof
5. EvidenceCandidate / EvidenceUse — retrieval returns scholarly candidates, not strings
```

**The decision:** pick ONE home for each. The strongest candidate:
- `python/patala_core/objects.py` + `authority.py` (has the cleanest AuthorityVector — 4 axes, gate
  predicates, NO scalar rank — which is the mixxii-review-correct design)
- `source-evidence/schema/` for the contract types (the frozen interface)
- `pipeline/review_engine.py` + `lib/review.py` collapse into ONE reducer
- ip-graph's `lib/review.py` + `lib/epistemic.py` adapt to the OG canonical (or vice versa — DECIDE)

---

## WHAT TO BUILD

1. **Freeze ONE `ReviewEvent`/`ReviewState`** — pick the home (recommend `patala_core/objects.py` +
   `contracts_human_authority.py` as canonical), and make `lib/review.py` (ip-graph) + `review_engine.py`
   (OG) import it. Delete the other 3.
2. **Freeze ONE `Authority`** — `patala_core/authority.py` (the 4-axis, non-scalar design) as canonical;
   `lib/epistemic.py`'s `Authority`/`Envelope` adapt to it.
3. **The 5 contracts as a generated schema** — via `lib/schema.py` (ip-graph's single-source compiler) →
   compiled TS/Python/JSON (the Stencila schema-drift answer).
4. **A parity test** — the same review event, represented via OG + ip-graph, must reduce to the same
   state (proves convergence).

---

## THE TEST (parity)

```bash
# the same ReviewEvent through both reducers must give the same phase
python3 -c "
import sys
sys.path.insert(0,'/root/projects/patala/source-evidence/schema')
sys.path.insert(0,'/root/projects/patala/pipeline')
sys.path.insert(0,'/mnt/HC_Volume_106427611/ip-graph/lib')
# after convergence: ONE ReviewEvent type, both reducers agree
print('ReviewEvent converges to one type')
"
```

**Pass when:** a single ReviewEvent (evidence about a target) flows through the OG reducer AND the
ip-graph reducer with the SAME result — proving there is ONE canonical contract, not six.

---

## THE RULE

> **Nothing builds on top until the 5 contracts converge.** This is the anti-theatre gate for the
> contract layer. Both sides must use the SAME Ref, ReviewState, BenchmarkFixture, PhilologicalProof,
> EvidenceCandidate — or the "canonical graph" is a lie.

---

*This is the #1 build. The six divergent ReviewEvent/Authority definitions are the schema-drift disease at
the contract level. Converge them (one home each), generated from one schema, with a parity test — before
building more on top.*
