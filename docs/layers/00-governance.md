# LAYER 00 — GOVERNANCE & RULES

*Part of the `NAVIGATION.md` layer map (the master tree / spine). The constitution every layer obeys.*

## 1. What it is
The governing layer: the anti-theatre doctrine, the operating axioms, and the authority ladder that
every other layer must follow. It exists because the project repeatedly built
"structurally-elegant-but-hollow" objects and reported them as results.

## 2. Purpose
Prevent theatre (a tested schema ≠ a result). Enforce that nothing is "real" without an independently
defined task, human-grounded gold, and a reproducible evaluation. Provide the shared rules all agents
(Hermes + coding agents) follow.

## 3. External tools used
None (this is Pāṭala-native doctrine). Hermes provides the execution layer it governs.

## 4. Data
- `contracts/CANONICAL-DAG.yaml` — the layer dependency graph (single source of truth).
- `machinelearning/_ACTIVE/CLAIMS.md` — the audit ledger (P-001…P-008).
- `machinelearning/_ACTIVE/COMPONENT-CONTRACTS.md` — per-component anti-theatre contracts.

## 5. Processes
```
any claim → is it real? → gold → blind eval → metric → human adjudication → result lineage
```
- The anti-theatre gate: `python3 machinelearning/theatre_check.py --status`
- The permanent checkpoint test: "What experiment would convince you this does NOT work?"

## 6. Implementations
- `AGENTS.md` — the governing file (agent architecture + Hermes + operating axioms).
- `machinelearning/theatre_check.py` — the status gate.
- `contracts/CANONICAL-DAG.yaml` — the DAG.

## 7. Docs
- `AGENTS.md` (root) — the governing file.
- `machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` — the master doctrine.
- `docs/global/README.md` §The Authority Ladder — the thesis doctrine.
- `endgamebuild/PROJECT-AUDIT.md` — the health check (what the rules are protecting against).
