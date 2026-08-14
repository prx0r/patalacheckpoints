# AGENTS.md — read this FIRST. The governing file for every agent in Pāṭala.

*This file is auto-loaded when any agent works in this repo. It is the FIRST thing you read. It exists
because this project repeatedly built "structurally-elegant-but-hollow" objects and reported them as
results. This file prevents that. It covers: (1) the ONE RULE, (2) the agent architecture, (3) Hermes,
(4) the operating axioms, (5) the navigation, and (6) the anti-theatre doctrine.*

---

## 0. THE ONE RULE (everything else follows)

> **Nothing is "real" because code exists. It becomes real only when an independently defined task,
> human-grounded gold, and a reproducible evaluation show that it does what its name claims.**

A tested schema is not a result. A typed container is not an argument. A hardcoded status is not an
audit. "N tests pass" is not "scholarship verified."

---

## 1. THE AGENT ARCHITECTURE (who owns what)

The mature stack (see `handover/agent0-coordinator/AGENT-ARCHITECTURE-VISION.md`):
**durable epistemic responsibility → its own state, invariants, inputs, outputs, failure boundary.**

```text
                    AGENT 0  (governance / routing / infras)
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
      AGENT 1          AGENT 2          AGENT 3
   PHILOSOPHY        CORPUS COMPILER   TRANSLATION
   ENGINE            + INTEGRITY        FACTORY
          │                │                │
          └───────┬────────┴────────┬──────┘
                  ▼                 ▼
              AGENT 4           AGENT 5
           REVIEW /           SYNTHESIS /
         ADJUDICATION         RESEARCH
                  └───────┬────────┘
                          ▼
                       AGENT 6
                    PUBLICATION /
                     PROJECTIONS
                          ▼
                       AGENT 7
                    SCHOLAR NETWORK
                    + INSTITUTION   (A8 acquisition later)
```

**Only A0–A3 need to exist now;** the rest instantiate when the substrate makes their job real.
Current mapping to the spine:

| Agent | Role | Where (NAVIGATION.md) |
|---|---|---|
| **A0** | governance / routing / infra | this file + `handover/agent0-coordinator/` + `contracts/CANONICAL-DAG.yaml` |
| **A1** | philosophy engine (epistemic core) | `machinelearning/research/patala_ml/` (see `docs/process/07-ml-epistemic-core.md`) |
| **A2** | corpus compiler + integrity (the factory) | `pipeline/` (see `docs/process/03-factory.md`) |
| **A3** | translation factory (the live loop) | `pipeline/` (factory_loop.sh + workers) |
| **A4** | review / adjudication | `source-evidence/schema/contracts_human_authority.py` + `pipeline/review_engine.py` |
| **A5** | synthesis / research | `synthesis_core.py` (part of A1's lane) |
| **A6** | publication / projections | `data/atlas/*` + `app/` |
| **A7** | scholar network (future) | — |

The two active working lanes (the "two agents" split):
- **Agent 1 (ML/philosophy)** — upward: C1 → themes → arguments → claims → synthesis → review.
  Question: *does this higher representation legitimately derive from the objects beneath it?*
- **Agent 2 (corpus compiler + integrity)** — vertical: SOURCE → T1 → L0 → … → C1.
  Question: *is this reading licensed by the source?*
- **Join on:** Passage ID / TranslationDecision ID / C1 ID — NEVER fuzzy.

---

## 2. HERMES — the execution kernel (how background work runs)

**Hermes is Pāṭala's replaceable execution kernel; Pāṭala is the durable epistemic state.** Hermes
schedules/executes; it never determines what Pāṭala knows. (`docs/global/HERMES-ORCHESTRATION-REVIEW.md`,
`handover/hermes/CANONICAL.md`)

- **The `patala` Hermes profile exists** (config under `~/.hermes/profiles/patala/`). Run work through
  it: `hermes --profile patala -z "<prompt>"` or `hermes profile use patala`.
- Hermes gives kanban/cron/worktree/hooks/MCP — the execution machinery. Pāṭala owns the epistemic
  graph (registry, review engine, DAG). `Hermes task DONE ≠ Pāṭala object ACCEPTED`.
- The model client `pipeline/model.py` shells to `hermes -z` (with `HERMES_MODEL`). See
  `docs/global/HERMES-CALLING.md`.
- **Important known issue:** the `patala` profile's model default can be empty/broken (audit §1);
  pass `-m deepseek-v4-flash` or set `HERMES_MODEL` if `-z` returns "Model not supported."

---

## 3. THE OPERATING AXIOMS (how to work in this repo — non-negotiable)

1. **Never `sleep` to "wait."** Do other work while long tasks run. Never block on a timer waiting for
   a background job — proceed with the next real task and check back.
2. **Start background processes with `nohup`** (detached, survives shell exit), redirect output to a
   log, and `&` — e.g. `nohup python3 x.py > /tmp/opencode/x.log 2>&1 &`. Then continue working.
   (Prefer `setsid` for full detachment.) Never start a long job in the foreground expecting to wait.
3. **Kill by specific PID, never `pkill`.** `pkill` can kill unrelated processes. Use `kill <pid>`
   (and `kill <child-pid>` for the whole group). Find pids with `ps -eo pid,cmd | grep <name>`.
4. **External sources go to R2, not local disk.** Download → snapshot to R2 (immutable Bronze, via
   `ingestion/r2.py::SnapshotStore`) → then you may delete the local copy. Local `/` and the volume are
   finite; R2 is the source of truth for bytes.
5. **Reuse, don't rebuild.** If a piece is in `docs/process/` or `NAVIGATION.md` as REUSABLE, extend it.
   Check `docs/process/external-tools.md` (62 borrowed tools) + `docs/process/githubclones.md` before
   writing infrastructure.
6. **Respect licenses.** PANDiT etc. are CC BY-NC-SA — discovery/index/provenance, not unrestricted
   commercial. Record license on every imported object.

---

## 4. THE NAVIGATION (read these, in order, before building)

0. **`AGENTS.md`** — this file.
0b. **`NAVIGATION.md`** — the MASTER index (resolve anything → layer/impl/docs/run/Hermes).
0c. **`docs/process/README.md`** — the process how-to reference (ingestion→atlas→factory→R2).
1. **`VISION_AND_NAVIGATION.md`** — the vision + progression.
2. **`docs/INDEX.md`** — the flat canonical map (one source of truth per concern).
3. **`onboarding/README.md`** — the single on-ramp.
4. **`endgamebuild/INFRA-INVENTORY.md`** — WHAT EXISTS / WHERE / DON'T REBUILD.
5. **`endgamebuild/PROJECT-AUDIT.md`** — the current HEALTH check (known gaps).
6. **`docs/global/README.md`** — the thesis.
7. **`docs/global/PATALA-GLOBAL-ARCHITECTURE.md`** — the 7-plane north star.

---

## 5. RUN THE GATE BEFORE YOU CLAIM ANYTHING IS "DONE"

```bash
python3 machinelearning/theatre_check.py --status
```

This prints the honest status of every component. If a component is `EXPERIMENTAL_INFRASTRUCTURE` (not
`CAPABILITY_CANDIDATE`), **do not present it as a working capability.** To promote it you must have the
evidence (gold + blind eval + metric + human adjudication).

---

## 6. THE PERMANENT CHECKPOINT TEST

Before adding a capability, answer:
> **What experiment would convince you this does NOT work?**

And for every claim:
> **Show me the independent evidence that this component performs the semantic function named in its API.**

If the answer is "tests pass / schema validates / looks good / model said so" — it stays experimental.
If it's "here is the frozen gold, the blind prediction, the metric, the failures, the human
adjudication" — it's research.

---

## 7. THE 3 CATEGORIES + THE BANNED WORDS

- **A. INFRASTRUCTURE** (schemas, renderers) · **B. EVIDENCE** (gold, reviews, proofs) ·
  **C. RESULTS** (measured behavior). Never call A → C.
- **Ban:** PROVED · TRUTH · CORRECT · EDITOR APPROVED · BEST · WINS
- **Use:** SUPPORTED BY · PASSED CHECK X · BENCHMARKED ON · MACHINE-PROPOSED · REVIEWED BY · NO CONFLICT DETECTED

---

## 8. RESULT LINEAGE (a result that can't resolve doesn't exist)

Every result carries: `result_id · benchmark_version · gold_version · model_version · code_commit ·
split · seed · config · date`. If "Model X achieved 0.71 F1" can't resolve to an experiment, it's not a
result.

---

## 9. THE ANTI-THEATRE DOCTRINE (the enforcement)

`machinelearning/_ACTIVE/AGENTS-DOCTRINE.md` is the master doctrine (3 categories, 9-field contract,
epistemic labels, banned words, abstention, human adjudication, result lineage,
falsification-before-promotion). `machinelearning/_ACTIVE/CLAIMS.md` is the audit ledger (P-001…P-008).
`COMPONENT-CONTRACTS.md` applies it per component. **This file is the enforcement mechanism for that
doctrine** — the doctrine is not advisory; a new agent that skips it will repeat the theatre-building
failure this project spent a session undoing.

---

*The spine: `ingestion` (sources→objects) → `atlas` (canonical graph) → `factory` (compiler) →
`research` (epistemic moat) → `web`/`apis`/`mcp` (surfaces), held by `evidence` (contracts+adapters+
evals) over `storage` (R2 bytes). Hermes runs the background work; the agents own their lanes; the one
rule gates every claim.*
