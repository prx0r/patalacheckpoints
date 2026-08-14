#!/usr/bin/env python3
"""pipeline/pandit_download.py — download the PANDiT dataset via a real browser (Playwright).

PANDiT (panditproject.org) has no public API and is behind Cloudflare's bot challenge, so a plain
curl/requests gets a 403 "Just a moment". The app's export endpoint is
`/search/pandit-entities-export?_format=csv` but it 403s when the request lacks a valid search
context (the JS `settings.extraData` / `id` is null). This script drives a REAL browser so:

  1. Cloudflare's interactive challenge resolves automatically (real browser fingerprint).
  2. A search is actually run first, so the export carries a valid search context.

It then downloads the CSV export(s) to a local staging dir for the ingestion layer.

NOTE on scope: PANDiT exports are paginated/per-entity-type. Broad searches may be capped. This
script does one search + export per entity type (Work, Person, Manuscript, ...) so the full dataset
(~69k entities) is captured across files.

Usage:
  python3 pipeline/pandit_download.py --out /mnt/HC_Volume_106427611/patala-ingest/staging \
      --headless          # run without showing a browser (default)
      --visible           # show the browser (better for manual Cloudflare pass if needed)
      --types Work Person  # entity types to export (default: Work,Person,Manuscript)
"""
from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

OUT_DEFAULT = "/mnt/HC_Volume_106427611/patala-ingest/staging"
BASE = "https://panditproject.org/search"

# entity types to export (PANDiT's core catalogue types)
DEFAULT_TYPES = ["Work", "Person", "Manuscript"]


def run(out: str, headless: bool, types: list[str], timeout_ms: int = 120000) -> int:
    from playwright.sync_api import sync_playwright

    Path(out).mkdir(parents=True, exist_ok=True)
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        ctx = browser.new_context(
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/120.0 Safari/537.36"),
            viewport={"width": 1440, "height": 900},
            accept_downloads=True,
        )
        page = ctx.new_page()

        for et in types:
            print(f"\n=== exporting type: {et} ===")
            try:
                page.goto(BASE, wait_until="domcontentloaded", timeout=timeout_ms)
            except Exception as e:  # noqa: BLE001
                print(f"  goto failed: {e}")
                continue

            # wait out Cloudflare challenge (a real browser usually passes in ~5-10s)
            print("  waiting for Cloudflare/JS challenge to pass...")
            try:
                page.wait_for_load_state("networkidle", timeout=timeout_ms)
            except Exception:  # noqa: BLE001
                pass
            page.wait_for_timeout(6000)

            # if there's an entity-type filter, set it; otherwise fall back to a generic search
            try:
                # set the entity type filter if present
                type_input = page.locator("select[name*='type'], select[name*='entity']").first
                if type_input.count() > 0:
                    type_input.select_option(label=et)
                    page.wait_for_timeout(1500)
            except Exception:  # noqa: BLE001
                pass

            # run a search (empty query = broad catalogue for this type)
            try:
                search_input = page.locator("input[name*='search'], input[name*='query'], #edit-keywords").first
                if search_input.count() > 0:
                    search_input.fill("")
                    search_input.press("Enter")
                    page.wait_for_timeout(4000)
                    try:
                        page.wait_for_load_state("networkidle", timeout=30000)
                    except Exception:  # noqa: BLE001
                        pass
            except Exception:  # noqa: BLE001
                pass

            # trigger the CSV export download
            csv_file = Path(out) / f"pandit-{et.lower()}-export.csv"
            try:
                with page.expect_download(timeout=timeout_ms) as dl_info:
                    # try the direct export endpoint first (it may 302 to a real download once a
                    # search context exists), else click the Download CSV button.
                    try:
                        page.goto(f"{BASE}/pandit-entities-export?_format=csv",
                                  wait_until="domcontentloaded", timeout=30000)
                    except Exception:  # noqa: BLE001
                        page.locator("text=Download CSV").first.click(timeout=20000)
                dl = dl_info.value
                dl.save_as(str(csv_file))
                print(f"  DOWNLOADED -> {csv_file} ({Path(csv_file).stat().st_size} bytes)")
                results.append(str(csv_file))
            except Exception as e:  # noqa: BLE001
                # fallback: try clicking the export button
                print(f"  export via endpoint failed: {e}; trying button...")
                try:
                    with page.expect_download(timeout=timeout_ms) as dl_info:
                        page.locator("text=Download CSV, text=Download CSV, button:has-text('CSV')").first.click(timeout=20000)
                    dl = dl_info.value
                    dl.save_as(str(csv_file))
                    print(f"  DOWNLOADED -> {csv_file} ({Path(csv_file).stat().st_size} bytes)")
                    results.append(str(csv_file))
                except Exception as e2:  # noqa: BLE001
                    print(f"  button export failed: {e2}")
                    print("  page title:", page.title())

        browser.close()

    print("\n=== results ===")
    for r in results:
        print("  ", r)
    if not results:
        print("  none downloaded. The Cloudflare challenge or the search context may need manual "
              "interaction — try --visible and complete the challenge, or export manually.")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Download PANDiT CSV exports via a real browser.")
    ap.add_argument("--out", default=OUT_DEFAULT)
    ap.add_argument("--headless", action="store_true", help="run headless (default)")
    ap.add_argument("--visible", action="store_true", help="show the browser (needs a display)")
    ap.add_argument("--types", nargs="*", default=DEFAULT_TYPES)
    a = ap.parse_args()
    return run(a.out, not a.visible, a.types)


if __name__ == "__main__":
    sys.exit(main())
