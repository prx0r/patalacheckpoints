# HOW TO CALL HERMES — the correct way (agent, not blind `-z`)

*2026-08-13. Cross-lane, durable reference. Every agent that calls Hermes MUST read this before
writing code that invokes it. The short version: **Hermes is an agent with read/write file access and
the Pāṭala skills — call it as an agent, never as a blind `-z` text model.** This supersedes the old
`-z`-everywhere pattern.*

---

## THE ONE RULE

> **`hermes -z "<prompt>"` is blind.** It is one-shot text completion with **no file access, no tools,
> no skills** — the model cannot read your repo. Anything you would have to hand-stuff into the prompt
> (source text, term packets, reference maps, context) is context Hermes already has via its file tools.
> **Use `hermes chat` (agentic) instead.** This is not a style preference; `-z` is why the translation
> pipeline returned empty/non-JSON output for most verses (~3.8% yield). (Verified 2026-08-13: the same
> request returns a real scholarly translation via `hermes chat`, empty via `hermes -z`.)

---

## THE CORRECT INVOCATION (agentic)

```bash
hermes chat -Q -q "<ask>" \
  --skills <skill> \
  --yolo \
  --max-turns 8
```

- `-Q` — quiet/programmatic mode: suppress banner, spinner, tool previews → **clean final output** (needed to parse structured replies).
- `-q "<ask>"` — non-interactive single query.
- `--skills <skill>` — load a house skill (e.g. `translate-passage`, `raw-l0`). Requires the `patala` profile (below).
- `--yolo` — no approval prompts (unattended).
- `--max-turns 8` — enough turns for the skill's inspection; too low (e.g. 3) hits "reached max iterations" and returns empty.

### Profile + project (so skills + MCP load)
```bash
hermes profile use patala          # the Pāṭala "soul" profile (skills + tantrakosa MCP live here)
hermes project use patala          # anchored to /root/projects/patala
```

### From Python (the reference implementation)
Use `pipeline/agentic_translate.py` as the template — it builds the command above, runs it via
`subprocess`, and robustly extracts the JSON reply. Never re-derive the invocation ad hoc.

---

## THE ANTI-PATTERN — DO NOT USE `-z` FOR REAL WORK

| Symptom | Root cause |
|---|---|
| Empty/`OPEN` output for most verses | model blind to files — it can't read the source/reference/terms |
| "no JSON object in model output" | hand-built mega-prompts the model can't follow |
| `[Errno 7] Argument list too long` | prompt passed as an argv arg exceeds the 2MB OS `ARG_MAX` |

`-z` remains fine for a tiny, self-contained call where no file context is needed. It is **wrong** for
translation, corpus work, or anything that benefits from reading the repo.

---

## WHY THE OLD PATHS BROKE (so nobody repeats it)

The factory + single-file runner called `hermes -z` (blind). To compensate, code hand-built giant
prompts carrying source + tokens + term packets. That (a) still left the model blind to the reference
maps it should read itself, (b) mixed many works per prompt → non-JSON, (c) blew the argv size limit.
The whole tangle existed only because the code refused to use the agent's file access. Don't rebuild
that tangle.

---

## SEE ALSO

- `handover/agent-2-integration/AGENTIC-TRANSLATION.md` — the Pāṭala translation runbook (agentic path).
- `handover/hermes/PATALA-SETUP.md` — how the `patala` profile/skills/MCP are set up.
- `handover/hermes/BACKEND-MODEL.md` — the Hermes-as-execution-engine model.
