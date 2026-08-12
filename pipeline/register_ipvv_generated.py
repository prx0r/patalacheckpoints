#!/usr/bin/env python3
"""register_ipvv_generated.py — wire the generated IPVV published units into
data/corpus/published.ts so the reader/API can serve them.

Regenerates the import block + registry entries for every
data/corpus/units/isvarapratyabhijnavivrtivimarsini-*-generated.ts, keyed by both
pt:passage: and tantra:text: forms (matching the existing kramasadbhava pattern).

Usage: python3 pipeline/register_ipvv_generated.py [--write]
"""
from __future__ import annotations
import os, re, sys
from pathlib import Path

BASE = Path("/root/projects/patala")
PUBLISHED = BASE / "data/corpus/published.ts"
UNITS = BASE / "data/corpus/units"

WORK = "isvarapratyabhijnavivrtivimarsini"


def build_registry() -> tuple[list[str], list[str]]:
    files = sorted(UNITS.glob(f"{WORK}-*-generated.ts"))
    imports = []
    entries = []
    for f in files:
        stem = f.stem  # isvarapratyabhijnavivrtivimarsini-V3-C-generated
        var = stem.replace("-generated", "").replace(f"{WORK}-", "ipvv").replace("-", "_")
        imports.append(f'import {{ generated as {var} }} from "./units/{stem}";')
        entries.append(f"  ...{var},")
        entries.append(f"  ...Object.fromEntries(Object.entries({var}).map(([pid, p]) => [pid.replace('pt:passage:', 'tantra:text:'), p])),")
    return imports, entries


def rewrite(imports: list[str], entries: list[str]) -> str:
    head = """// The published-translation registry — serves the phrase-click API.
// Milestone: the publishable translation object (see data/corpus/translation.ts).
import type { PublishedTranslation, TranslationDecision, EvidenceItem } from "./translation";
import { published18 } from "./units/kramasadbhava-1.8-published";
import { kramasadbhava_1_25 } from "./units/kramasadbhava-1-25-generated";
import { published1511 } from "./units/isvarapratyabhijnavivrtivimarsini-1.5.11-published";
"""
    body = "\n".join(imports)
    reg = "\n".join(entries)
    return f"""{head}{body}

const PUBLISHED: Record<string, PublishedTranslation> = {{
  "pt:passage:isvarapratyabhijnavivrtivimarsini:1.5.11": published1511,
  "tantra:text:isvarapratyabhijnavivrtivimarsini:1.5.11": published1511,
  "pt:passage:kramasadbhava:1.8": published18,
  "tantra:text:kramasadbhava:1.8": published18,
  // generated 1.1–1.25 — but the hand-authored 1.8 is richer, so keep it.
  ...Object.fromEntries(
    Object.entries(kramasadbhava_1_25).filter(([pid]) => !pid.endsWith(":1.8"))
  ),
  // generated IPVV passages (from the token-gloss T1)
{reg}
}};
// also index by the tantra:text: urn form (skip 1.8, already hand-authored)
for (const [pid, p] of Object.entries(kramasadbhava_1_25)) {{
  if (pid.endsWith(":1.8")) continue;
  PUBLISHED[pid.replace("pt:passage:", "tantra:text:")] = p;
}}
"""


def main() -> None:
    write = "--write" in sys.argv
    imports, entries = build_registry()
    out = rewrite(imports, entries)
    if write:
        PUBLISHED.write_text(out, encoding="utf-8")
        print(f"wrote {len(imports)} imports / {len(entries)//2} unit-keys → {PUBLISHED}")
    else:
        print(f"would write {len(imports)} imports / {len(entries)//2} unit-keys")
        print(out[:600])


if __name__ == "__main__":
    main()
