# Pāṭala Docs Site

*The canonical source for **docs.patala.org**. This directory defines the structure;
the content lives in the markdown files (which remain the single source of truth).*

## Approach

1. **Content** — the `docs/*.md` files (canonical, reviewed, versioned).
2. **Structure** — `manifest.yaml` (the nav: sections, order, source mapping).
3. **Generator** (later) — reads the manifest → builds the site nav → renders each
   page from its markdown source. Framework (Docusaurus / VitePress / MkDocs / a
   hand-rolled Next.js docs layout) decided when we host.

This separation means:
- writing a doc = writing markdown + adding a manifest row;
- the manifest is the skeleton the site generator consumes;
- no content is duplicated into a "docs system" that can drift.

## Directories

| Dir | Purpose |
|---|---|
| `manifest.yaml` | the canonical nav (sections, order, source mapping) |
| `api/` `concepts/` `guides/` `pipeline/` `reference/` `status/` | future generated output / site-specific assets |

The manifest maps each page to a `docs/*.md` source. See `manifest.yaml` for the
full mapping.

## Regenerate

When docs change, update the markdown (canonical). Update `manifest.yaml` only when
the *structure* changes (new page, new section, reordering).

## Status

Not yet deployed. The manifest + content are the foundation; the generator + hosting
(Cloudflare Pages, matching the existing site) come after.
