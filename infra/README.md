# infra/ — the confirmed Pāṭala infrastructure

Infrastructure primitives that are **confirmed by the Atlas blueprints** and built as easy wins while
the schemas are being finalised. Nothing here is speculative; each maps to a blueprint I-commit.

## R2 asset store (`r2_assets.py`) — the I2 primitive

The content-addressed artifact store. **Postgres stores what things ARE; R2 stores the bytes.**
Everything is keyed by SHA-256 so the same bytes always have the same identity (immutable artifact
history, no blockchain).

Object layout under the single `patala` R2 bucket (prefix-as-folders):

```text
patala/
  public/       rights-cleared texts, TEI, snapshots, released translations
  source/       factory source files, e-texts, OCR, transcriptions, source PDFs (private by default)
  manuscripts/  user uploads, scans, TIFF/JPEG, HTR inputs (very controlled)
  artifacts/    T1/L0/ARGMAP/L2/L200/C1, proof, benchmark outputs (private until promoted)
  releases/     versioned open-data snapshots
  objects/      the content-addressed blob store (source/manuscripts/.../objects/sha256/xx/.../blob)
```

Operations (the four the blueprint specifies + helpers):

```bash
python3 infra/r2_assets.py put --file <f> --bucket source
python3 infra/r2_assets.py head --sha <sha256> --bucket source
python3 infra/r2_assets.py get  --sha <sha256> --bucket source --out -
python3 infra/r2_assets.py verify --file <f> --sha <sha256> --bucket source
python3 infra/r2_assets.py migrate --dir data/corpus/sources --bucket source
# presign_upload() is available as a Python import for direct browser->R2 uploads
```

Env: `R2_ACCESS_KEY_ID` / `R2_SECRET_ACCESS_KEY` (or `AWS_*`), `R2_ENDPOINT`, `PATALA_R2_BUCKET`.

## Reference docs (the confirmed design)

- `docs/AGENT2-ATLAS-FOUNDATION-PLAN.md` — the active plan (I1 Postgres → I2 R2 → I4 API → vertical)
- `openpatala/README.md` — the "OpenAlex for Sanskrit" build folder
- `docs/vision/atlas/atlas-engineering-blueprint.md` — storage + I1–I6
- `docs/vision/atlas/atlas-cloudflare-edge-layer.md` — Cloudflare edge layer
- `docs/vision/atlas/atlas-performance.md` — performance doctrine
