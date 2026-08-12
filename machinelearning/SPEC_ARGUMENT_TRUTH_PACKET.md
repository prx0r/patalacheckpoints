# SPEC — THE ARGUMENT AS A TRUTH-PACKET (translation-like, strength-graded) — LIGHT

*2026-08-12. The idea, kept deliberately light (per the instruction not to overengineer): treat a
formal logical argument almost like a translation — an auditable object with a resolvable path, a
proof status, and a **derived claim-strength** you can cite in an essay. This is the bridge between
the PUSHING method (`SPEC_PUSHING_METHOD.md` / `PUSHING_GUIDE.md`) and the essays.*

---

## 1. The analogy (why it works)

Just as a translation is `source → target → decisions → evidence → resolve`, an argument is:

| Translation | Argument |
|---|---|
| source_spans | premises (each resolves to a passage) |
| target_spans | the claim / conclusion |
| decisions | the inference + hidden-premise choices |
| evidence | the quoted passages |
| review_state | claim strength (PROVED → SPECULATIVE) |
| resolve | trace any claim back to Sanskrit |

So the argument becomes a **truth-packet**: self-contained, auditable, strength-graded — citable in
an essay like a translation, with SHOW EVIDENCE resolving to the passages.

---

## 2. The minimal argument object (no over-engineering)

```ts
interface ArgumentTruthPacket {
  id: string;            // pt:argument:<work>:<slug>
  work_id: string;
  title: string;
  kind: "reductio" | "analogy" | "identity" | "entailment" | "decomposition";
  premises: { text: string; passage_ids: string[] }[];
  inference: string;     // the typed move
  conclusion: { text: string; passage_ids: string[] };
  tension_id: string;    // the PUSHING question it resolves
  proof?: "PROVED" | "OUTSIDE_FORMAL" | "HOLLOW";   // from the truth engine (nyāya/Lean)
  status: "MACHINE_DRAFT" | "REVIEWED";             // human review promotes it
}
```

The **auditable path** is: conclusion → inference → premises → each premise resolves to its passage
(via `/api/resolve`). No new engine — it reuses the resolve kernel + the passage store.

---

## 3. Claim strength — DERIVED, not hand-waved

Attach a strength that follows from the argument object, so essays cite at the right level:

```
PROVED          a formal proof exists (truth engine / Lean)
REVIEWED        human review accepted reconstruction + provenance
WELL_SUPPORTED  premises resolve, inference sound, no surviving prosecution
PLAUSIBLE       coherent reconstruction with a live objection (the tension stands)
SPECULATIVE     a probe — explicitly NOT asserted as the text's claim
```

A claim's strength = **derived from** the argument's `proof` + `status` + the surviving objections
from Pass B (prosecution). The essay can then say "the text's position (WELL_SUPPORTED, prem. A–C)"
vs "a possible reading (SPECULATIVE)" — never overclaiming.

---

## 4. The strength ladder maps to the existing verification floor

This aligns with the deterministic floor already shipped:
- **WELL_SUPPORTED** requires the premises to resolve (the `/api/verify/claim-structure` check).
- **PROVED** requires a truth-engine proof (the nyāya/Lean link, `nyayaengine.py`).
- **REVIEWED** requires a human review event (the review ledger / `MACHINE_DRAFT → REVIEWED`).
- **SPECULATIVE** is the honest "probe, not claim" level — the term-probes-vs-identities rule.

So the strength is **enforceable by the existing primitives**, not a new subsystem.

---

## 5. Where this lives

- The argument objects are `pt:argument:` nodes, tracked on the source hub (`/api/hub`) with
  `passage_ids`.
- Essays cite them at their claim-strength (SHOW EVIDENCE → the argument → premises → passages).
- Agent 1 owns the schema + the truth-engine link; Agent 2 owns exposing them on the hub.

---

## 6. Deliberately NOT built yet (keep it light)

- No new proof engine — reuse `nyayaengine.py`/Lean.
- No new verification service — reuse `/api/verify/*` + `/api/resolve`.
- No claim-strength scoring model — the strength is a *derived label* from existing fields until a
  benchmark justifies a learned version.

The next build: the `pt:argument:` schema + one worked truth-packet (e.g. the reflexivity tension)
to prove the loop end-to-end.
