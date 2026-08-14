#!/usr/bin/env python3
"""ingest_stk.py — register the Sārdhatriśatikālottarāgama into the REAL patala object_registry.

The real commit path (not the lab demo): convert the raw Goodall-edition Stk verses into the
<work>.jsonl format that `register_sources.py` consumes, then register them as SOURCE objects
in the REAL object_registry. This is what actually populates the registry the site reads.

Steps:
  1. Extract the 309 clean Sanskrit verses from the raw Goodall text (// Stk_N.M markers).
  2. Write data/corpus/downloads/translations/sardhatrisatikalottara.jsonl (the real intake format).
  3. Run register_sources.py --work sardhatrisatikalottara → commit as SOURCE in object_registry.
  4. Verify the registry now has the Stk SOURCE objects.

Run: python3 migration/v3/ingest_stk.py [--dry-run]
"""
import sys, os, json, hashlib, re, subprocess
from pathlib import Path

ROOT = Path("/root/projects/patala")
SRC = ROOT / "data" / "corpus" / "sources" / "sardhatrisatikalottara" / "sardhatrisatikalottara.txt"
OUT = ROOT / "data" / "corpus" / "downloads" / "translations" / "sardhatrisatikalottara.jsonl"

def extract_verses():
    """Extract the clean Sanskrit verses (// Stk_N.M markers) from the Goodall text."""
    verses = []
    for line in SRC.read_text().splitlines():
        line = line.strip()
        m = re.search(r"// Stk_([\d.]+)$", line)
        if m and line:
            verse = re.sub(r"\s*// Stk_[\d.]+$", "", line).strip()
            verses.append({"locator": m.group(1), "sanskrit": verse})
    return verses

def main():
    dry = "--dry-run" in sys.argv
    verses = extract_verses()
    print(f"Extracted {len(verses)} clean Sanskrit verses from the Goodall Stk text")

    # write the jsonl in the real intake format
    rows = []
    for i, v in enumerate(verses):
        row = {
            "work": "sardhatrisatikalottara",
            "verse_idx": i,
            "source_sha256": hashlib.sha256(v["sanskrit"].encode()).hexdigest(),
            "sanskrit": v["sanskrit"],
            "locator": v["locator"],
        }
        rows.append(row)
    if not dry:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        with open(OUT, "w") as f:
            for r in rows:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"Wrote {len(rows)} verses to {OUT}")
    else:
        print(f"[dry-run] would write {len(rows)} verses to {OUT}")

    # register into the real object_registry
    if not dry:
        cmd = ["python3", str(ROOT / "pipeline" / "register_sources.py"), "--work", "sardhatrisatikalottara"]
        print(f"Running: {' '.join(cmd)}")
        r = subprocess.run(cmd, capture_output=True, text=True)
        print(r.stdout[-500:] if r.stdout else "")
        if r.stderr: print("stderr:", r.stderr[-300:])

    # verify the real registry
    sys.path.insert(0, str(ROOT / "pipeline"))
    import object_registry as R
    s = R.summary()
    print(f"\n=== REGISTRY AFTER INGEST ===")
    print(f"  SOURCE: {s['SOURCE']['objects']}  T1: {s['T1']['objects']}  L0: {s['L0']['objects']}")

if __name__ == "__main__":
    main()
