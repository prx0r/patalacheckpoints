// /texts/isvarapratyabhijnavivrtivimarsini — the IPVV overview page.
// The recognition-thesis source: unit summary + per-passage read links into the auditable reader.
import { listUnitPassages } from "@/data/corpus/published";

export const dynamic = "force-static";

export default function IsvarapratyabhijnavivrtivimarsiniPage() {
  const passages = listUnitPassages("isvarapratyabhijnavivrtivimarsini");
  const open = passages.reduce((n, p) => n + p.open_decisions, 0);
  const withTr = passages.filter((p) => p.has_translation).length;
  const withDec = passages.filter((p) => p.decisions > 0).length;

  return (
    <main className="min-h-screen bg-zinc-950 px-6 py-12 text-zinc-200">
      <div className="mx-auto max-w-3xl">
        <header className="mb-8">
          <p className="text-[10px] uppercase tracking-[0.3em] text-[color:var(--saffron)]">patala — tantra hub</p>
          <h1 className="mt-1 font-serif text-3xl text-[color:var(--bone)]">Īśvarapratyabhijñāvivṛtivimarśinī</h1>
          <p className="mt-2 text-sm text-zinc-400">
            Pratyabhijñā · Abhinavagupta on Utpaladeva's lost Vivṛti · the deepest primary source of
            the recognition philosophy, now translated in full. The authority by which Ratié's
            reconstruction is checked.
          </p>
          <div className="mt-3 flex flex-wrap gap-2 text-[11px] text-zinc-400">
            <span className="rounded border border-zinc-700 px-2 py-0.5">{passages.length} passages published</span>
            <span className="rounded border border-zinc-700 px-2 py-0.5">{withTr} with working translation</span>
            <span className="rounded border border-zinc-700 px-2 py-0.5">{withDec} with decisions</span>
            <span className="rounded border border-red-900/60 px-2 py-0.5 text-red-300">{open} OPEN cruxes</span>
          </div>
        </header>

        <section>
          <h2 className="mb-2 font-serif text-lg text-[color:var(--saffron)]">The recognition thesis — the load-bearing passage</h2>
          <p className="mb-3 text-[12px] text-zinc-500">
            IPK 1.5.11 — "The essential nature of light is reflective awareness (vimarśa); otherwise
            light, though 'coloured' by objects, would be similar to an insentient reality, such as
            crystal." The seed of the whole recognition-thesis, expanded by the IPVV.
          </p>
          <ul className="divide-y divide-zinc-800/60 rounded border border-zinc-800/60">
            {passages.map((p) => {
              const loc = p.locator;
              return (
                <li key={p.passage_id} className="flex items-center gap-3 px-4 py-2.5 text-[13px] hover:bg-zinc-900/40">
                  <a href={`/read/isvarapratyabhijnavivrtivimarsini/${loc}`} className="min-w-0 flex-1 text-zinc-300 hover:text-[color:var(--saffron)]">
                    <span className="font-mono text-zinc-500">{loc}</span>
                    <span className="ml-3">vimarśa = the essence of light — the reflexivity claim</span>
                  </a>
                  <span className="flex items-center gap-2 text-[10px]">
                    {p.open_decisions > 0 && <span className="rounded bg-red-950/60 px-1.5 py-0.5 text-red-300">{p.open_decisions} OPEN</span>}
                    {p.decisions > 0 && <span className="rounded bg-zinc-800 px-1.5 py-0.5 text-zinc-400">{p.decisions} dec</span>}
                    <span className="text-zinc-600">Read →</span>
                  </span>
                </li>
              );
            })}
          </ul>
        </section>

        <p className="mt-8 text-[12px] text-zinc-500">
          Working translations are AI-assisted and not peer-reviewed. Decisions are proposals until a
          specialist reviews them. The full IPVV (V1A–N, V2A–S, V3A–P) lives in the project's
          translation stack; this page publishes the recognition-thesis core as an auditable source.
        </p>
      </div>
    </main>
  );
}
