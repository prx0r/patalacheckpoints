# 04 — R2 STORAGE (the immutable data lake)

*Part of `docs/process/README.md`. R2 is where the BYTES live — immutable, content-addressed,
never the database. Everything raw (source snapshots, scans, e-texts, artifacts, releases) lands here
once and is read forever. **"Postgres stores what things ARE; R2 stores the bytes."***

## 1. The two layers

- **`infra/r2_assets.py`** — the content-addressed byte store (SHA-256 keyed). The artifact-truth layer. Reusable API: `put_asset`, `get_asset`, `verify_asset`, `head_asset`, `presign_upload`.
- **`ingestion/r2.py`** — `SnapshotStore`, the **Bronze snapshot** layer on top: versioned, immutable `source/ingestion/<SOURCE>/snapshots/<id>/` namespaces + `manifest.json`.

## 2. Object layout (under the `patala` bucket)

```
patala/
  public/       rights-cleared texts, TEI, snapshots, released translations
  source/       factory sources, e-texts, OCR, transcriptions, source PDFs (private default)
    ingestion/<SOURCE>/snapshots/<id>/      ← Bronze source snapshots + manifests
  manuscripts/  user uploads, scans, HTR inputs (very controlled)
  artifacts/    T1/L0/ARGMAP/L2/L200/C1, proof, benchmark outputs (private until promoted)
  releases/     versioned open-data snapshots
  objects/      the content-addressed blob store (sha256/xx/.../blob)
```

## 3. The Bronze snapshot flow (proven, reusable)

```bash
# stage a source on disk → put as an immutable snapshot → delete the local tarball
python3 -m ingestion.r2 --source GRETIL --snapshot-id gretil-tei-2026-08-14 \
    --file /tmp/gretil-tei.tar.gz --license per-file
```
```python
from ingestion.r2 import SnapshotStore
store = SnapshotStore(r2_bucket="patala")
m = store.put_snapshot("GRETIL", "gretil-tei-2026-08-14",
                       {"gretil-tei.tar.gz": data}, license="per-file")
print(store.manifest("GRETIL", "gretil-tei-2026-08-14"))   # read the manifest back
print(store.list_snapshots("GRETIL"))                       # all versions survive
```

## 4. What's already on R2 (as of 2026-08-14)

| Source | Snapshot | Size | Content |
|---|---|---|---|
| GRETIL | `gretil-tei-2026-08-14` | 63 MB | 784 TEI XML (structured primary texts) |
| GRETIL | `gretil-sanskrit-html-2026-08-14` | 103 MB | 3367 IAST HTML (1_sanskr) |
| GRETIL | `gretil-full-corpus-2026-08-14` | 38 MB | Pali/Prakrit/Dravidian/NIA/VAR |
| SARIT | `sarit-tei-2026-08-14` | 34 MB | TEI P5 corpus |
| MUKTABODHA | `muktabodha-library-2026-08-14` | 88 MB | Śaiva Siddhānta IAST texts |
| PATALA | `factory-sources-2026-08-14` | 630 MB | the 73 works the factory runs on |

Plus the separate `sanskritree` bucket (Dyczkowski Tantraloka volumes, Academia.edu bundles, datasets).
PANDiT: awaiting manual CSV export (Cloudflare-blocked, no API) — drop it on disk and it flows through `SnapshotStore` + `SourceAsserter`.

## 5. The rules

1. **Never mutate a snapshot.** A new upstream state = a NEW `snapshot_id`; both survive → reproducibility.
2. **Content-addressed.** Same bytes = same key. Idempotent uploads.
3. **Manifest beside every snapshot** `{source, snapshot_id, files:[{path,sha256,bytes}], license}` so "where did this come from" is always answerable.
4. **R2 is the source of truth for bytes; local disk is only staging.** Download → snapshot → delete the local copy.
5. **Rights:** store per-snapshot license; the `rights` Postgres table holds per-asset policy.

## 6. Storage budget

R2 free tier = 10 GB storage. Current ingestion namespace ≈ 956 MB — comfortably within budget.
OpenAlex bulk (if ever) ~1-2 GB; GRETIL/SARIT/PANDiT all fit.

## 7. Known gap

**R2 is not yet a downstream INPUT** — the intake/queue flow (`register_sources`, `corpus_state`,
`acquire_*`) reads local disk only. `SnapshotStore` is ready; wiring the factory to pull sources from
R2 instead of local disk is the remaining step.
