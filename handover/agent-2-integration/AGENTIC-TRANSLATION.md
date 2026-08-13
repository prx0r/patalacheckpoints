# AGENTIC TRANSLATION — THE ONE CORRECT PATH (read this, stop the mess)

*2026-08-13. After a day of churn, this is the settled, working way to translate raw Sanskrit → English
in Pāṭala. It supersedes the two broken paths below. If you are about to touch translation machinery,
read this first and follow the agentic path — do NOT resurrect the `-z` paths.*

---

## THE ONE-SENTENCE TRUTH

> **Hermes is an AGENT with read/write file access and the Pāṭala skills — so drive it as an agent
> (`hermes chat -Q -q`, under the `patala` profile, with the `translate-passage` skill), and it reads
> the source/reference files itself and returns real translations. Stop calling it as a blind `-z`
> text model.**

## HOW TO RUN IT (the correct path)

```bash
# one work, first N verses:
python3 pipeline/agentic_translate.py --work kubjika --max 50

# loop every registered work overnight:
setsid nohup python3 pipeline/agentic_translate.py --all >> /tmp/opencode/agentic.log 2>&1 < /dev/null &
```

Progress is saved per-verse to `data/corpus/downloads/translations/<work>.jsonl`, deduped by
`source_sha256` — resume-safe, never duplicates, real `MACHINE_PROPOSED` records (empty/corrupt verses
are honest `OPEN`, never fabricated).

**Driver:** `pipeline/agentic_translate.py` · **Skill:** `translate-passage` (loaded via the `patala`
profile) · **Env:** `HERMES_PROFILE=patala`, `HERMES_SKILL=translate-passage`.

## THE PREREQUISITES (already done 2026-08-13)

1. **`patala` hermes profile created + active** — `hermes profile use patala`.
2. **Repo skills installed into the profile** — the 10 skills from `skills/` are copied into
   `/root/.hermes/profiles/patala/skills/` (`translate-passage`, `raw-l0`, `translate-work`,
   `write-commentary`, …). Verified via `hermes skills list` (all `local · enabled`).
3. **`patala` project anchored** — `hermes project add-folder patala /root/projects/patala`.
4. **Agentic invocation proven** — `hermes chat -Q -q "<ask>" --skills translate-passage --yolo
   --max-turns 8` reads files itself and returns real JSON. (`-Q` = quiet/programmatic, `-q` = query.)

### Why these exact flags (so nobody re-breaks it)
- `-Q` = suppress banner/spinner/tool previews → clean final output (for JSON parsing).
- `-q <prompt>` = non-interactive single query.
- `--skills translate-passage` = use the house translation skill.
- `--max-turns 8` = enough turns for the skill's inspection without hitting "max iterations" and
  returning empty.
- `--yolo` = no approval prompts (unattended).

---

## THE TWO PATHS THAT ARE BROKEN — DO NOT USE

| Path | Why it's broken | File(s) |
|---|---|---|
| **Blind `-z` single-file runner** | `hermes -z` = one-shot text, **no file access, no tools** → model blind to the repo → returns **empty** for most verses (~3.8% yield). The `OPEN`/empty records it writes are not real translations. | `pipeline/auto_translate_raw.py`, `pipeline/batch_translate.py` |
| **`-z` factory scheduler** | Built the whole corpus-compiler on the same blind `-z` calls, so it also returns non-JSON / empty; plus two mechanical bugs (batched prompts mixed many works; prompts exceeded the 2MB argv limit). | `pipeline/factory_scheduler.py`, `pipeline/factory_batch.py`, `pipeline/t1_worker.py` |

The mechanical bugs in the factory **were fixed** (see below) but the fundamental design error —
calling a file-access agent as a blind text model — was only corrected by switching to the agentic
path. Do not revert to `-z` for translation.

## THE MECHANICAL FIXES (already applied, committed for history)

- `pipeline/factory_scheduler.py` — batch model calls **per-work** (was: many works per prompt → non-JSON).
- `pipeline/object_registry.py` — **cache `_load`** (was: re-parsing the 35MB registry ~0.6s per read →
  100% CPU doing nothing).
- `pipeline/t1_worker.py` — batch **per-work + byte-capped** (≤800KB, under the 2MB ARG_MAX that caused
  `[Errno 7] Argument list too long`).

These keep the factory path from spinning, but the agentic driver is the primary translation path.

## WHERE THE SKILLS LIVE (so nobody says "they're missing" again)

- **Repo copy:** `/root/projects/patala/skills/*/SKILL.md` (source of truth, git-tracked).
- **Installed copy:** `/root/.hermes/profiles/patala/skills/*/SKILL.md` (what hermes actually loads).
- **Archive:** `data/corpus/downloads/hermes-skills-archive.json` (backup snapshot).
- **Setup plan:** `handover/hermes/PATALA-SETUP.md` (the original intended design; now executed).

## SEE ALSO

- `handover/hermes/PATALA-SETUP.md` — the profile/soul design.
- `docs/agent2nextdev.md` — the longer factory roadmap (provenance chain is the destination).
- `handover/agent-2-integration/CURRENT-STATE.md` — factory status reference.

*Carry-forward: the agentic driver is the path to "leave it running overnight and come back to a pile
of real translations." Once that's solid, layer the canonical registry/provenance stack (L0/ARGMAP/
L2/L200/C1) on top — but translate with the agent, not with blind `-z`.*
