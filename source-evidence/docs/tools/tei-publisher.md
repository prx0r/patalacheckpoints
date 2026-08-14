# TEI Publisher — scholarly edition publication interface

**What Pāṭala borrows:** turning TEI data + templates + a processing model into scholarly publication
interfaces. Modern TEI Publisher is modular. SARIT used TEI Publisher-related infrastructure
(`sarit/sarit-existdb`).

**License:** GPL. Repo: `eeditiones/tei-publisher-app`.

## How Pāṭala consumes it
**DOCS_ONLY.** Adapter for archival scholarly-edition export:
```
canonical Pāṭala objects
   → Pāṭala React reader (our own)
   → TEI export
   → archival scholarly edition (TEI Publisher)
```

## Doctrine
Adapter for archival export, not the core reader.
