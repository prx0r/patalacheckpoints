# IR REVIEW FINDINGS — the ontology broke in useful places (before freeze)

*2026-08-12. Source: `REVIEW-2026-08-12-MODEL-1` (independent model review of ARG-GOLD-001..005 against
the C1+L2 packet). These four findings must be resolved BEFORE IR v1 freezes. They are forced by gold,
not speculative schema design — exactly what gold-first is for.*

| # | Finding | Fix (must be in IR v1) |
|---|---|---|
| **IR-F-01** | **INFERENCE vs DIALECTICAL RELATION are being conflated.** `Objection → Answer` (ARG-005) is not an inference; it is `Answer RESPONDS_TO Objection`. Likewise `Argument A ATTACKS Argument B` is separate from either argument's internal inference. | Keep the **INFERENTIAL graph** (`P1+P2 --Rule→ C`) separate from a **DIALECTICAL graph** (`objection / reply / attack / qualification / counterexample`). These are distinct edge vocabularies. |
| **IR-F-02** | **Evidential grounding is being represented as inference.** ARG-001 `G-INF3` (`order-less support → therefore Great Lord`) and ARG-004 `G4-INF-IC` (`self-aware light → therefore parā-vāk`) — those identifications are simply further things the passage says. | Use a **TEXTUAL_GROUNDING** edge, not a **LOGICAL_DERIVATION** inference, for identifications that the source states directly. (This is the vertical-object `GroundingLink` distinction.) |
| **IR-F-03** | **`support_scope` is genuinely forced by gold** (ARG-005: local claim vs systematic extension). Not speculative. | Model `LOCAL_PASSAGE / LOCAL_SECTION / SAME_WORK / CROSS_WORK / SYSTEMATIC_RECONSTRUCTION` — likely on a `GroundingLink`/proposition-support assertion, not necessarily a new top-level object. |
| **IR-F-04** | **`Commitment` needs a RECONSTRUCTION force.** ARG-003 `G3-REG` had `commitment=ASSERTS`, which silently attributes a modern reconstruction to the author. | Retain `IMPLIES_ON_RECONSTRUCTION` / `EDITORIAL_RATIONAL_RECONSTRUCTION` so model reconstructions can never become author commitments (the pūrvapakṣa error `Commitment` exists to prevent). |

**Status rule this reinforces:** a fixture is `MODEL_INDEPENDENT_REVIEWED` at most from a model review —
never `INDEPENDENT_REVIEWED` / `SPECIALIST_REVIEWED` without a human Sanskritist against the primary text.
