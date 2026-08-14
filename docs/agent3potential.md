> **ARCHIVED / SUPERSEDED** — kept for history only. Do NOT follow as current. See `docs/INDEX.md` + `docs/DOCS-AUDIT.json` for the canonical doc for this concern.

# AGENT 3 — POTENTIAL (translation factory worker) — brainstorm + peer review

*2026-08-13. This captures: (1) the case for Agent 3 as a hardcoded factory worker (organisational),
(2) a peer-review of Agent 2's `0cc9c26`/factory work that found three real architectural truth bugs,
(3) the recommended hardening checkpoint (A2-ARCH-HARDEN), and (4) the external architecture stack
(event sourcing, Sigstore/Rekor, SLSA attestations, Hermes Kanban, OpenTelemetry, nanopub/PROV, IPFS).*

---

## 1. IS AGENT 3 REAL? — YES, BUT MOSTLY ORGANISATIONAL

The architecture vision (`handover/agent0-coordinator/AGENT-ARCHITECTURE-VISION.md:180-217`) already
defines A3 — the Translation Factory — as a **separate role** from A2:

```
Agent 2 says WHAT IS ALLOWED   (NEXT_VALID_ACTION from the ledger/registry)
Agent 3 DOES IT                (translation drafts, batch, retry, provenance)
Agent 2 verifies resulting state
```

But what Agent 2 has built (`factory_loop.sh` + `factory_scheduler.py`) is **functionally the A3
worker role, folded into Agent 2**. So splitting out Agent 3 is:

- **Mostly organisational**, not new machinery. The worker daemon already exists; making it "Agent 3"
  is a registration + a clean contract.
- **Contract value**: formalising `A3 = executes NEXT_VALID_ACTION → writes MACHINE_PROPOSED` is what
  unlocks **A4 (review)** cleanly.
- **Matches the MAKE-vs-PROVE split**: A3 makes, A1 proves, A2 gates/verifies.

**Recommendation:** keep the shared code, formalise the **A3 contract** as a distinct role. The worker
daemon = `factory_loop.sh`; Agent 3 is the *owner* of that execution contract.

---

## 2. PEER-REVIEW: THREE REAL ARCHITECTURAL TRUTH BUGS (found by an external agent)

Agent 2 has built something legitimately strong ("corpus OS" framing is earned operationally; the
catalog is the right projection concept). But **not frozen yet**. Three bugs:

### BUG 1 — THREE DEFINITIONS OF THE DAG (the biggest)

- `docs/FACTORY.md` (my doc) says: `SOURCE → T1 → ARGMAP → L0 → L2`
- Locked contract `CANONICAL-LAYER-STACK.md` says: `SOURCE → T1 → L0 → [argument map] → L2`,
  **argument map depends on SOURCE + L0**.
- `factory_scheduler.py` hard-codes `ARGMAP ← T1`, `L0 ← T1`, `L2 ← ARGMAP` — so the live scheduler
  allows **ARGMAP before L0** and **L2 without L0 being load-bearing**.
- `object_registry.py` PREREQS has a *third* model: `ARGMAP ← T1`, `L2 ← L1 + ARGMAP`.

The scheduler claims to derive from `object_registry.PREREQS` but actually uses its own `UPSTREAM`
dict. **All-green tests prove consistency with fixtures, not that the factory follows the locked
scholarly derivation.**

### BUG 2 — "IMMUTABLE APPEND-ONLY REGISTRY" IS AN OVERCLAIM

`object_registry.commit()` → `_save()` **rewrites the whole JSONL**; `set_status()`/`supersede()`
mutate prior records in memory and rewrite. Version-aware + historically recoverable in normal
operation, but **not cryptographically immutable, not literally append-only**.

### BUG 3 — THE OVERNIGHT THROUGHPUT / ARCHITECTURE ISN'T "FROZEN"

Not a bug per se, but the architecture should not be declared frozen until the hardening checkpoint
(A2-ARCH-HARDEN) is done.

---

## 3. THE RECOMMENDED HARDENING CHECKPOINT (A2-ARCH-HARDEN)

```
1. Reconcile FACTORY.md with CANONICAL-LAYER-STACK.
2. Replace scheduler UPSTREAM with canonical multi-parent DAG.
3. Make object_registry.PREREQS derive from the same manifest.
4. Test: no L2 eligibility without current L0 + ARGMAP.
5. Test: no ARGMAP eligibility without L0.
6. Test: changing canonical DAG fails every divergent consumer.
7. Rename registry claim to VERSIONED_REGISTRY (not cryptographically immutable).
8. Introduce append-only ObjectEvent ledger.
9. Derive current state as a projection of that event stream.
10. Hash-chain events.
11. FactoryRunCertificate references exact event range/root hash.
12. Later: anchor release root to Rekor.
```

Then Era C becomes:

```
supersede → event → dependency invalidation → rebuild → event
→ Agent1 re-eval → proof refresh → DependencyImpactReport → ReviewBundle
```

---

## 4. THE EXTERNAL ARCHITECTURE STACK (borrow, in priority order)

The strongest architecture is **not blockchain**. It is four histories that cannot be confused:

```
EXECUTION HISTORY   "what actually ran?"      OpenTelemetry / FactoryRun / Hermes runs
ARTIFACT HISTORY    "what exact objects?"     content hashes + event-sourced registry
TRUST HISTORY       "weren't rewritten?"      signatures + Merkle transparency log (Rekor)
EPISTEMIC HISTORY   "believed/challenged/     Pāṭala ReviewEvent / Adjudication / Supersession
                     reviewed/corrected?"
```

Do not collapse these. Pāṭala's moat = connecting all four.

### 4.1 Make ONE canonical DAG manifest the executable source of truth
`contracts/CANONICAL-DAG.yaml` declares every prerequisite; scheduler, rebuild, catalog, certificate,
tests all compile from it. Represent multi-parent prerequisites:
`ARGMAP: [SOURCE, L0]`, `L2: [L0, ARGMAP]`. **This is the most important fix.**

### 4.2 Event sourcing (append-only ObjectEvent ledger)
Append `OBJECT_CREATED / STATUS_CHANGED / SUPERSEDED / REVIEWED / INVALIDATED / REBUILT`. Current state
= projection. Hash-chain events. Immudb is the database-level option later.

### 4.3 Sigstore/Rekor as the trust layer
Rekor = append-only Merkle transparency log for signed artifact metadata (release checkpoints, not
every worker event). Prove "this exact version existed, not silently replaced."

### 4.4 SLSA-style provenance (PatalaAttestation)
```
subject: object hash
inputs:  SOURCE hash, T1/L0/ARGMAP parent hashes
builder: worker SHA, skill hash, prompt hash, model/provider
run:     run_id, started_at, finished_at
result:  object version, validator result
verification: Agent1 proof refs
```

### 4.5 Hermes Kanban for orchestration ABOVE the corpus
Profiles: `producer-agent2`, `verifier-agent1`, `scholar-evidence`, `reviewer`, `release-manager`.
Hermes owns *who does what + whether the workflow finished*; Pāṭala owns *whether the object is valid*.
**This is probably the next external component to deploy** (not Temporal, not blockchain).

### 4.6 OpenTelemetry (operational evidence, not scholarly evidence)
A factory run = a trace; each layer execution = a span. Inspectable execution history.

### 4.7 Nanopublications + W3C PROV (outward scholarly projection)
Export `Proposition / SourceAssertion / CorroborationEvent / ReviewEvent` with standardised provenance.
Keep Pāṭala's richer canonical semantics native.

### 4.8 IPFS (optional, for published immutable release bundles)
Content-addressed CIDs for release manifests. **Content-addressing does not prove truth.**

### 4.9 Temporal — NOT now
Reference architecture only; Agent 2 already built the needed subset (DAG, retry, resume, watchdog,
idempotency, failure isolation). Revisit only if multi-host / thousands of long-lived jobs / durable
human-in-loop across distributed services.

---

## 5. VERDICT

`0cc9c26` is a good cleanup; the "corpus OS" framing is earned operationally; the catalog is the right
projection concept. **But don't call the architecture frozen yet.** Do A2-ARCH-HARDEN first, then Era C.
Hermes Kanban is the next external component worth deploying.
