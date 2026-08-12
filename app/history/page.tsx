import timeline from "@/data/atlas/historyTimeline.json";
import { getEntity } from "@/data/atlas";

type School = {
  id: string;
  name: string;
  period: number[];
  era: "textual" | "comparative" | "archaeological";
  parent: string | null;
  influences?: string[];
  concepts?: string[];
  anchors?: string[];
  bibliography?: string[];
  hop?: number;
  note?: string;
};

const ERA_META: Record<string, { label: string; color: string; blurb: string }> = {
  textual: { label: "TEXTUAL", color: "#8b3528", blurb: "directly readable sources" },
  comparative: { label: "COMPARATIVE", color: "#75552b", blurb: "comparative reconstruction" },
  archaeological: { label: "ARCHAEOLOGICAL", color: "#928873", blurb: "archaeological correlate" },
};

const atlasTraditionIds = new Set(["trika", "krama", "kubjika", "kaula", "spanda", "pratyabhijna", "sarvamnyaya"]);
const textSlugs = new Set([
  "kaulajnananirnaya", "kubjikamata", "mahanayaprakasha", "maharthamanjari", "spandakarika", "tantraloka",
]);

function fmtPeriod(p: number[]) {
  const f = (n: number) => (n < 0 ? `${Math.abs(n)} BCE` : `${n} CE`);
  return `${f(p[0])} – ${f(p[1])}`;
}

export default function HistoryPage() {
  const schools = (timeline.schools as School[])
    .map((s) => ({ ...s, _trad: atlasTraditionIds.has(s.id) ? getEntity(s.id) : undefined }))
    .sort((a, b) => a.period[0] - b.period[0]);
  const textual = schools.filter((s) => s.era === "textual");
  const reconstructed = schools.filter((s) => s.era !== "textual");

  return (
    <main className="min-h-screen bg-[#d8d0c0] font-sans text-[#1b1915]">
      <div className="mx-auto max-w-4xl px-8 py-14">
        {/* header */}
        <header className="mb-12">
          <div className="retro-window inline-block border-[3px] border-[#272641] bg-[#e8dfcc] p-7 shadow-[12px_12px_0px_rgba(0,0,0,0.15)]">
            <h1 className="text-4xl font-black uppercase tracking-[-0.04em] leading-none">
              Śiva <span className="text-[#8b3528]">Source Tree</span>
            </h1>
            <div className="mt-3 h-1 w-16 bg-[#c58b36]" />
            <div className="mt-3 text-[10px] font-black uppercase tracking-[0.2em] text-[#71695b]">
              schools · traditions · epochs — the diachronic map
            </div>
          </div>
          <p className="mt-4 max-w-2xl text-[13px] leading-relaxed text-[#3a352c]">
            A braided history, not a single lineage: from the reconstructed Proto-Indo-European horizon, through
            Vedic Rudra and Pāśupata, to Abhinavagupta's Trika — and its philosophical interlocutors. Linked to the
            Pāṭala bibliography and tradition pages.
          </p>
          <div className="mt-3 flex flex-wrap gap-3 text-[10px] font-bold uppercase tracking-widest text-[#71695b]">
            {Object.values(ERA_META).map((e) => (
              <span key={e.label} className="flex items-center gap-1.5">
                <span className="bindu" style={{ background: e.color }} /> {e.label} · {e.blurb}
              </span>
            ))}
          </div>
        </header>

        {/* textual timeline */}
        <section className="mb-12">
          <h2 className="mb-1 text-[11px] font-black uppercase tracking-[0.25em] text-[#8b3528]">The readable spine</h2>
          <p className="mb-5 text-[11px] text-[#71695b]">~1200 BCE → 1300 CE · scroll through the schools</p>
          <div className="relative ml-3 border-l-2 border-[#b3a488] pl-6">
            {textual.map((s) => (
              <SchoolCard key={s.id} s={s} />
            ))}
          </div>
        </section>

        {/* reconstructed + parallel */}
        <section className="mb-12 grid gap-8 md:grid-cols-2">
          <div>
            <h2 className="mb-1 text-[11px] font-black uppercase tracking-[0.25em] text-[#75552b]">Reconstructed layers</h2>
            <div className="space-y-3">
              {reconstructed.filter((s) => s.era === "comparative").map((s) => (
                <CompactCard key={s.id} s={s} />
              ))}
            </div>
          </div>
          <div>
            <h2 className="mb-1 text-[11px] font-black uppercase tracking-[0.25em] text-[#71695b]">Parallel branch</h2>
            <div className="space-y-3">
              {reconstructed.filter((s) => s.era === "archaeological").map((s) => (
                <CompactCard key={s.id} s={s} />
              ))}
            </div>
          </div>
        </section>

        {/* transformations */}
        <section className="mb-12">
          <h2 className="mb-3 text-[11px] font-black uppercase tracking-[0.25em] text-[#8b3528]">Diachronic transformations</h2>
          <div className="grid gap-4 md:grid-cols-3">
            {(timeline.chains as { title: string; steps: string[] }[]).map((c) => (
              <div key={c.title} className="retro-window border-2 border-[#272641] bg-[#e8dfcc] p-4">
                <p className="mb-2 text-[12px] font-black uppercase tracking-wide text-[#1b1915]">{c.title}</p>
                <ol className="space-y-1">
                  {c.steps.map((st, i) => (
                    <li key={i} className="flex items-center gap-2 text-[11px] text-[#3a352c]">
                      <span className="text-[#8b3528]">{i === c.steps.length - 1 ? "◆" : "→"}</span>
                      {st}
                    </li>
                  ))}
                </ol>
              </div>
            ))}
          </div>
        </section>

        {/* hop roadmap */}
        <section className="mb-12">
          <h2 className="mb-3 text-[11px] font-black uppercase tracking-[0.25em] text-[#8b3528]">Translation roadmap (leapfrog hops)</h2>
          <div className="flex flex-wrap gap-2">
            {(timeline.hop_roadmap as string[]).map((h) => (
              <span key={h} className="border border-[#272641]/40 bg-[#e8dfcc] px-3 py-1 text-[11px] font-bold text-[#3a352c]">{h}</span>
            ))}
          </div>
        </section>

        <footer className="border-t border-[#b3a488] pt-4 text-[10px] text-[#71695b]">
          sources:{" "}
          {Object.entries(timeline.sources as Record<string, string>)
            .map(([k, v]) => `${k}`)
            .join(" · ")}{" "}
          · api: <code>/api/history/timeline</code>
        </footer>
      </div>
    </main>
  );
}

function BibTag({ id }: { id: string }) {
  const href = textSlugs.has(id) ? `/texts/${id}` : `/bibliography`;
  return (
    <a
      href={href}
      className="border border-[#272641]/30 bg-white/40 px-1.5 py-0.5 text-[10px] font-bold text-[#1b1915] hover:bg-[#c58b36]/30"
    >
      {id}
    </a>
  );
}

function SchoolCard({ s }: { s: School & { _trad?: unknown } }) {
  const influences = s.influences ?? [];
  return (
    <div className="relative mb-4 rounded border-2 border-[#272641] bg-[#e8dfcc] p-4 shadow-[6px_6px_0px_rgba(0,0,0,0.12)]">
      <span className="absolute -left-[26px] top-5 h-2.5 w-2.5 rounded-full bg-[#8b3528]" />
      <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1">
        <h3 className="text-lg font-black uppercase tracking-tight text-[#1b1915]">
          {s._trad ? (
            <a href={`/traditions/${s.id}`} className="hover:text-[#8b3528]">
              {s.name}
            </a>
          ) : (
            s.name
          )}
        </h3>
        <span className="text-[12px] font-bold text-[#8b3528]">{fmtPeriod(s.period)}</span>
        {s.hop ? <span className="border border-[#272641]/40 px-1.5 text-[9px] font-black uppercase text-[#3a352c]">hop {s.hop}</span> : null}
      </div>
      <div className="mt-1 text-[10px] font-bold uppercase tracking-wider text-[#75552b]">
        {ERA_META[s.era].label}
        {s.parent ? <span className="text-[#71695b]"> · ← {s.parent.replace(/_/g, " ")}</span> : null}
      </div>

      {s.concepts && s.concepts.length > 0 && (
        <p className="mt-2 text-[12px] text-[#3a352c]">
          <span className="font-bold text-[#71695b]">concepts:</span> {s.concepts.join(" · ")}
        </p>
      )}
      {s.anchors && s.anchors.length > 0 && (
        <p className="mt-1 text-[12px] text-[#3a352c]">
          <span className="font-bold text-[#71695b]">anchors:</span> {s.anchors.join(" · ")}
        </p>
      )}
      {s.note ? <p className="mt-1 text-[11px] italic text-[#71695b]">{s.note}</p> : null}
      {influences.length > 0 && (
        <p className="mt-2 text-[11px] text-[#71695b]">
          → influences: {influences.map((p) => p.replace(/_/g, " ")).join(", ")}
        </p>
      )}
      {s.bibliography && s.bibliography.length > 0 && (
        <div className="mt-2 flex flex-wrap gap-1.5">
          {s.bibliography.map((b) => (
            <BibTag key={b} id={b} />
          ))}
        </div>
      )}
    </div>
  );
}

function CompactCard({ s }: { s: School }) {
  return (
    <div className="rounded border-2 border-[#272641]/40 bg-[#e8dfcc]/70 p-3">
      <div className="flex items-baseline justify-between gap-2">
        <span className="text-[12px] font-black uppercase text-[#1b1915]">{s.name}</span>
        <span className="text-[10px] font-bold text-[#71695b]">{fmtPeriod(s.period)}</span>
      </div>
      {s.note ? <p className="mt-1 text-[10px] italic text-[#71695b]">{s.note}</p> : null}
    </div>
  );
}
