# Manubot — forkable / executable scholarly essays (Vision 07)

**What Pāṭala borrows:** open, Git-versioned collaborative manuscript authoring with automatic citation handling
and HTML/PDF/DOCX output. Vision 07's "papers can be forked / essay is a rendering of the graph" becomes a real
export: an `ArgumentSynthesis → EssayObject → Manubot project → HTML/PDF/DOCX + Git history`, with Pāṭala
IDs/embeds in the HTML. **Do not build a scholarly document production system.**

**License:** open (CC0 / permissive).

## Usage
- Manubot is a Git-based manuscript workflow: author in Markdown, automatic citations (CSL), builds to HTML/PDF/
  DOCX. Forking = Git branching.
- Pāṭala can emit an `EssayObject` → Manubot project with Pāṭala claim refs embedded in the rendered output.

## How Pāṭala consumes it
Export layer for provenance-linked, versioned, forkable scholarly essays that carry Pāṭala IDs — the site and
education already consume the same refs.

**Priority: cheap export proof (prove one EssayObject exports into a citable versioned manuscript).**
