# AGENT 0 (COORDINATOR) — INDEX (the "what is true RIGHT NOW" pointer)

*2026-08-12. Live pointer — update as you work. Agent 0 governs the agent system, not a scholarly lane.*

---

## What Agent 0 owns (the system)
- `handover/SYSTEM.md` — the agent-system meta-architecture (vision-once + registry + derived orientations + staleness checker)
- `handover/AGENTS.yaml` — the machine-readable agent registry (the contract)
- `handover/check_staleness.py` — the staleness checker (the enforcement)
- `handover/ORIENTATION-AGENT0.md` — this lane's orientation
- `handover/CHECKPOINTS.md` — the shared execution map (governs the CP0–CP4 gates)
- `VISION_AND_NAVIGATION.md` — the canonical vision (lives once, never duplicated)

## Current system state (2026-08-12)
- **Registry:** 3 agents defined (agent0 coordinator, agent1 ML, agent2 L0).
- **Orientations:** agent1 ✅ (process workflow w/ gates) · agent2 ✅ (just built, same template) · agent0 ✅ (this).
- **Staleness checker:** `handover/check_staleness.py` — detects registry↔files, vision-copy, INDEX, gold resolution. **Target: 0 failures.**
- **Agent 1 (CP4):** ARG-001 ✅ + ARG-002 ✅ consistent; ARG-003/004/005 not yet built (sources located + read).
- **Agent 2 (CP1):** P0 35/35 PASS; P1–P5 Vidyut/Heritage witnesses in progress.

## The checkpoint ladder (real state)
```
CP0 DONE · CP1 PARTIAL(L0) · CP2 PARTIAL · CP3 PARTIAL · CP4 PARTIAL · CP5–CP6 PARTIAL · CP7+ NOT STARTED
```

## Current open items (for the coordinator)
- [ ] Run `check_staleness.py` to 0 failures (Agent 2 orientation + Agent 0 dir now exist — verify).
- [ ] Confirm no orientation embeds a verbatim vision copy.
- [ ] Keep the vision live in `VISION_AND_NAVIGATION.md` only.
- [ ] Gate Agent 1's CP4 (5 golds consistent) and Agent 2's CP1 (PhilologicalProof v1 honest).
