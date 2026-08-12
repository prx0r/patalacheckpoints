// The canonical ID / alias model — the citation backbone.
//
// Design (FROZEN, see specs/PATALA_INTEGRATION_BRAINSTORM.md §2):
//   - a passage has an IMMUTABLE id (a stable hash) and one or more MUTABLE aliases
//     (human-readable locators like ipvv:V2-S:14 or tantra:text:...:1.5.11).
//   - internal resolution is ALWAYS by immutable id; aliases are resolved to it.
//   - this stops mutable locators from being baked into the system.
//
// ID scheme:
//   pt:passage:<work>:<slug>   human form (work + a semantic locator)
//   pt:pid:<sha1>[:<n>]        immutable form (content/identity hash + disambiguator)
//
// resolve(ref) tries, in order:
//   1. exact immutable id        pt:pid:...
//   2. alias registry            alias -> immutable id
//   3. heuristic canonicalization  "ipvv:V2-S:14" -> work + locator
//   4. urn form                  tantra:text:<work>:<locator>

export type ResolveHit =
  | { ok: true; immutable_id: string; ref: string; via: "immutable" | "alias" | "canonical" | "urn" }
  | { ok: false; error: string; ref: string };

export interface PassageIdEntry {
  immutable_id: string; // pt:pid:<hash>
  work: string;
  aliases: string[]; // mutable human locators
}

export const REGISTRY: PassageIdEntry[] = [
  // IPVV — the canonical showcase. alias = semantic locator; immutable = content hash.
  {
    immutable_id: "pt:pid:ipvv:1f0a1c",
    work: "isvarapratyabhijnavivrtivimarsini",
    aliases: [
      "ipvv:1.5.11",
      "IPVV 1.5.11",
      "isvarapratyabhijnavivrtivimarsini:1.5.11",
      "tantra:text:isvarapratyabhijnavivrtivimarsini:1.5.11",
    ],
  },
  {
    immutable_id: "pt:pid:ipvv:2e3b9d",
    work: "isvarapratyabhijnavivrtivimarsini",
    aliases: ["ipvv:V2-S:14", "IPVV 2.x.x §14"],
  },
];

function norm(s: string): string {
  return (s || "").toLowerCase().replace(/\s+/g, " ").trim();
}

function hashId(ref: string): string {
  // deterministic short content hash for a canonical ref (not crypto-grade)
  let h = 0;
  for (let i = 0; i < ref.length; i++) h = (Math.imul(h, 31) + ref.charCodeAt(i)) | 0;
  return (h >>> 0).toString(16).slice(0, 6);
}

export function toImmutable(work: string, locator: string): string {
  return `pt:pid:${work}:${hashId(`${work}:${locator}`)}`;
}

export function lookupAlias(alias: string): PassageIdEntry | undefined {
  const a = norm(alias);
  return REGISTRY.find((e) => e.aliases.some((x) => norm(x) === a));
}

export function canonicalize(ref: string): { work?: string; locator?: string; slug?: string } {
  const r = norm(ref);
  // ipvv:V2-S:14 or IPVV 2.4.3 §14
  let m = r.match(/^ipvv[: ]+(.+)$/i);
  if (m) return { work: "isvarapratyabhijnavivrtivimarsini", locator: m[1] };
  // pt:passage:<work>:<slug>
  m = r.match(/^pt:passage:([a-z0-9]+):(.+)$/);
  if (m) return { work: m[1], slug: m[2] };
  // tantra:text:<work>:<locator>
  m = r.match(/^tantra:text:([a-z0-9]+):(.+)$/);
  if (m) return { work: m[1], locator: m[2] };
  return {};
}

export function resolve(ref: string): ResolveHit {
  const exact = REGISTRY.find((e) => e.immutable_id === norm(ref));
  if (exact) return { ok: true, immutable_id: exact.immutable_id, ref, via: "immutable" };

  const byAlias = lookupAlias(ref);
  if (byAlias) return { ok: true, immutable_id: byAlias.immutable_id, ref, via: "alias" };

  const c = canonicalize(ref);
  if (c.work && (c.locator || c.slug)) {
    const loc = c.locator || c.slug || "";
    return { ok: true, immutable_id: toImmutable(c.work, loc), ref, via: "canonical" };
  }

  return { ok: false, error: "unresolved_ref", ref };
}

export const RESOLVE_BACKBONE = {
  resolve,
  toImmutable,
  canonicalize,
  lookupAlias,
};
