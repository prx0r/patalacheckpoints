#!/usr/bin/env python3
"""Generate the docs-site nav JSON from manifest.yaml.

This is the machine-readable contract a docs-site generator consumes to build the
sidebar/nav. Reads docs-site/manifest.yaml and emits docs-site/nav.json.

Usage: python3 docs-site/gen_nav.py [--out docs-site/nav.json]
"""
from __future__ import annotations
import json
import os
import sys

try:
    import yaml
except ImportError:
    print("PyYAML required: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

HERE = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(HERE, "manifest.yaml")
OUT = os.path.join(HERE, "nav.json")


def parse_section_block(lines, start):
    """Parse a `### Title — /path` block into (title, path, items[])."""
    items = []
    i = start
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line.startswith("### "):
            break
        if line.startswith("| "):
            # table row: | Page | Source |
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 2 and cells[0] and cells[1] and not cells[0].startswith("Page"):
                items.append({"title": cells[0], "source": cells[1]})
        i += 1
    return items, i


def parse_manifest():
    lines = open(MANIFEST, encoding="utf-8").read().splitlines()
    nav = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("### "):
            # "### Guides — /guides"
            title, _, path = line[4:].partition("—")
            path = path.strip() or "/"
            items, i = parse_section_block(lines, i + 1)
            nav.append({"section": title.strip(), "path": path, "pages": items})
        else:
            i += 1
    return nav


def main():
    out = OUT
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    nav = parse_manifest()
    json.dump(nav, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"wrote {len(nav)} sections -> {out}")
    for s in nav:
        print(f"  {s['path']:<10} {s['section']} ({len(s['pages'])} pages)")


if __name__ == "__main__":
    main()
