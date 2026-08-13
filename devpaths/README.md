# DEVPATH ROADMAP — status index

*Local devpath tracking for the endgame build (Agent 1 lane, verification + epistemic core).
Each route is self-contained: objective, work, acceptance, status. Update the status line as routes
close. The sequence comes from `endgamebuild/HANDOVER-TO-NEW-AGENT.md` (the a1b branch).*

---

## The sequence

```
devpath1 ──► wire Nyāya gate + build ARGMAP NAT harness        STATUS: ✅ CLOSED (2026-08-13)
devpath2 ──► G2: close the T1/L0 correction loop              STATUS: ⛔ BLOCKED (needs Agent 2 factory_rebuild)
devpath3 ──► G3A: ARGMAP NAT on real Agent 2 output           STATUS: ⛔ BLOCKED (needs real ARGMAP batch)
devpath4 ──► G3B: Proposition core                             STATUS: ✅ CLOSED (2026-08-13)
devpath5 ──► G3C: Crux + arguments + Nyāya-profile             STATUS: ✅ CLOSED (2026-08-13)
devpath6 ──► G4: Human authority path + first UI               STATUS: 🔄 IN PROGRESS
```

---

## Status legend

| Mark | Meaning |
|---|---|
| ✅ CLOSED | fully built, tested, committed |
| ⛔ BLOCKED | gated on another lane's output (Agent 2) |
| ⏳ READY | can start (unblocked), not yet started |
| 🔄 IN PROGRESS | currently being worked |

---

## Cross-lane gates

- **devpath2 (G2)** needs Agent 2 to: consume the 6-finding bundle (`data/evaluation/findings/`)
  → fix the segmentation root class → `factory_rebuild(cidgagana:v1)` → emit an `EvaluationCandidate`
  (new exact version) + `ImpactReport` (trigger=`EF-T1-2026-0003`).
- **devpath3 (G3A)** needs Agent 2's factory to emit a real ARGMAP batch (the worker is done;
  corpus pending). The ARGMAP NAT harness from devpath1 is ready to consume it.

---

## Per-route notes

- `devpaths/devpath1.md` — ✅ complete
- `devpaths/devpath2.md` — blocked (G2 correction loop)
- `devpaths/devpath3.md` — blocked (G3A ARGMAP NAT on real output)
- `devpaths/devpath4.md` — ✅ complete
- `devpaths/devpath5.md` — ✅ complete
- `devpaths/devpath6.md` — human authority path + first UI (in progress)
