# PĀṬALA — PROGRESS MAP (2026-08-13, end of session)

*The one-page current state: what is proven, what is building, what is next. Read
`docs/global/README.md` (the thesis) for what Pāṭala is; this is where it stands. Companion to
`INFRA-INVENTORY.md` (what exists) + `SESSION-BUILD-RECORD-2026-08-13.md` (what was built).*

---

## THE THESIS (in one line)

> **Pāṭala is an authority graph for historical Sanskrit knowledge — a reconciliation engine that
> turns uncertain, fragmented, external manuscript and scholarship records into increasingly resolved,
> provenance-carrying scholarly objects, with machines proposing structure and scholars able to
> inspect, correct and certify it.**

---

## PROVEN (the machine carries + recovers epistemic structure)

| Capability | Evidence |
|---|---|
| Exact-version plumbing + provenance propagation | factory registry, atomic writes |
| Typed argument representation + perturbation/crux | `crux_engine.py`, `nyayagate.py` |
| ArgumentSynthesis (the convergence object) | `synthesis_core.py` |
| Correction propagation (impact across the chain) | `review_engine.py`, A2-18 |
| **Real IPVV argument recovery** (no gold leakage) | **IPVV-ARGREC-PILOT-001**: machine recovered the V2L objection/reply/crux from real T1/L0/C1, UNSUPPORTED_BRIDGE_RATE=0 |
| Essay/education/review EVALUATORS (judge, not author) | ESSAY-BENCH, EDU-BENCH, RECOVERY-BENCH, warrant |
| Reconciliation engine + fingerprints + ExternalRecord | P2/P3/P4 + `text_fingerprint.py` |
| Atlas backfill + quality scorecard + scholarship side | ATLAS-10 pipeline |

## BUILDING (ATLAS-100 is the main project)

| Item | State |
|---|---|
| Atlas backfill (`audited.ts` → candidates) | ✅ 11 rich works, provenance-carrying |
| ATLAS-10 GOLD + quality scorecard | ✅ instrumented (identity/date/authorship PASS; editions/scholarship sparse) |
| Scholarship side (Ratié/Torella → IPVV) | ✅ populated |
| INCEpTION real gold (20 passages) | ✅ project prepared, ready for human annotation |
| 50-IPVV argument-recovery batch | ✅ scorer + runner ready (sanity: precision 1.0, crux 0.98) |
| Hermes agentic path | ✅ fixed (`chat_agentic`) |
| Adapter coverage | ⚠️ measured: modern-paper adapters ~0% for Sanskrit — local corpus is the real path |

## NOT YET (the honest frontier)

- Scaled argument discovery (the 5-unit pilot → 25 → 50 real windows)
- Scholar acceptance (one real human adjudication on a disputed proposition)
- Reconciliation at the millions-of-records scale (Gyan Bharatam)
- Pedagogical effectiveness (EDU-BENCH measured 0.4 epistemic-valid on the packet)

---

## THE NEXT MILESTONES

1. **ATLAS-10 GOLD** — ten works good enough to show a scholar (identity/authority honest,
   editions/e-texts/witnesses separated, scholarship linked, API works, QA passes).
2. **ATLAS-100 v0.1** — scale the same process to 100 works, then measure completeness/authority-open/
   external-ID/publication/witness/translation coverage.
3. **SCHOLAR-VERTICAL-1** — one proposition, all primary + published evidence, one real human
   adjudication, full downstream impact. ("Show me exactly what my objection changes.")

## OWNER DECISION PENDING

- **Repo history rewrite** (destructive `filter-repo`) — remove the in-copyright PDFs from prior git
  history. Private backup first. Maintenance, not intellectual priority.
