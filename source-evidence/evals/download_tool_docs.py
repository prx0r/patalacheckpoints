#!/usr/bin/env python3
"""download_tool_docs.py — fetch canonical docs for every S0.1 tool into docs-cache/.

Reads source-evidence/docs/tools/MANIFEST.json. For each tool, downloads the canonical
docs_url page (and, if the site exposes a `mkdocs.yml`, the site sitemap) into
`docs-cache/<slug>/`, writing:
  docs-cache/<slug>/index.md     (the fetched page, converted to Markdown)
  docs-cache/<slug>/SOURCE.txt   (URL + date + content-type)
  docs-cache/<slug>/pages/       (any additional pages fetched from the sitemap)

Rate-limiting etiquette (from the S0 doctrine): one polite GET per tool, a small delay,
and no hammering. Downloads are snapshots for offline reference only — Pāṭala never
treats live docs as canonical state.

Usage:
  python3 source-evidence/evals/download_tool_docs.py [tool1 tool2 ...]
  (no args = all tools in MANIFEST)
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.request
import urllib.parse
from datetime import datetime, timezone

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
MANIFEST = os.path.join(ROOT, "source-evidence/docs/tools/MANIFEST.json")
CACHE = os.path.join(ROOT, "source-evidence/docs/tools/docs-cache")

UA = "Patala-doc-snapshot/0.1 (+offline-reference-only; polite single GET)"
TIMEOUT = 30
DELAY = 0.6  # polite politeness between tools


def fetch(url: str) -> tuple[str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        data = r.read()
        ctype = r.headers.get("Content-Type", "")
    return data.decode("utf-8", errors="replace"), ctype


def html_to_md(html: str, ctype: str) -> str:
    """Minimal HTML->Markdown for docs sites; falls back to raw text if not HTML."""
    if "html" not in ctype.lower():
        return html
    import re
    # drop scripts/styles/nav
    html = re.sub(r"<script.*?</script>", "", html, flags=re.S | re.I)
    html = re.sub(r"<style.*?</style>", "", html, flags=re.S | re.I)
    html = re.sub(r"<nav.*?</nav>", "", html, flags=re.S | re.I)
    # headings
    for i in range(1, 7):
        html = re.sub(rf"<h{i}[^>]*>(.*?)</h{i}>", lambda m: "#" * i + " " + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "\n", html, flags=re.S | re.I)
    # code blocks
    html = re.sub(r"<pre[^>]*><code[^>]*>(.*?)</code></pre>", lambda m: "\n```\n" + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "\n```\n", html, flags=re.S | re.I)
    html = re.sub(r"<code[^>]*>(.*?)</code>", lambda m: "`" + re.sub(r"<[^>]+>", "", m.group(1)).strip() + "`", html, flags=re.S | re.I)
    # links
    html = re.sub(r'<a[^>]+href="([^"]+)"[^>]*>(.*?)</a>', lambda m: f"[{re.sub(r'<[^>]+>', '', m.group(2)).strip()}]({m.group(1)})", html, flags=re.S | re.I)
    # lists / paragraphs
    html = re.sub(r"<li[^>]*>", "\n- ", html)
    html = re.sub(r"<p[^>]*>", "\n\n", html)
    html = re.sub(r"<br\s*/?>", "\n", html)
    # strip remaining tags
    text = re.sub(r"<[^>]+>", "", html)
    # collapse 3+ blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def download_one(slug: str, url: str, cache: str) -> bool:
    out_dir = os.path.join(cache, slug)
    os.makedirs(out_dir, exist_ok=True)
    try:
        data, ctype = fetch(url)
    except Exception as e:  # noqa: BLE001
        print(f"  ✗ {slug:18} FAIL: {e}")
        return False
    md = html_to_md(data, ctype)
    with open(os.path.join(out_dir, "index.md"), "w", encoding="utf-8") as f:
        f.write(md)
    with open(os.path.join(out_dir, "SOURCE.txt"), "w", encoding="utf-8") as f:
        f.write(f"url: {url}\nfetched: {datetime.now(timezone.utc).isoformat(timespec='seconds')}\n"
                f"content-type: {ctype}\nbytes: {len(data)}\n")
    print(f"  ✓ {slug:18} {len(data)} bytes -> {slug}/index.md")
    time.sleep(DELAY)
    return True


def main() -> int:
    with open(MANIFEST, encoding="utf-8") as f:
        manifest = json.load(f)
    tools = manifest["tools"]
    args = sys.argv[1:]
    slugs = args if args else list(tools.keys())

    summary = {"ok": [], "failed": []}
    for slug in slugs:
        if slug not in tools:
            print(f"  ? unknown tool: {slug}")
            continue
        url = tools[slug]["docs_url"]
        print(f"fetching {slug}: {url}")
        if download_one(slug, url, CACHE):
            summary["ok"].append(slug)
        else:
            summary["failed"].append(slug)

    print(f"\ndone: {len(summary['ok'])} ok, {len(summary['failed'])} failed")
    if summary["failed"]:
        print("failed:", ", ".join(summary["failed"]))
    return 1 if summary["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
