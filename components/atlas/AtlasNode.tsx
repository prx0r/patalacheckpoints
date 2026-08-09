"use client";

import { Handle, Position } from "reactflow";
import { AtlasEntity } from "@/lib/atlas";
import { typeColor } from "@/data/atlas";

const TYPE_LABEL: Record<string, string> = {
  tradition: "SAMPRA-DĀYA",
  text: "GRANTHA",
  person: "ĀCĀRYA",
  concept: "SAMJÑĀ",
};

export function AtlasNode({ data }: { data: { entity: AtlasEntity } }) {
  const e = data.entity;
  return (
    <div className="retro-window w-[260px] pointer-events-auto">
      <div className="retro-title-bar">
        <div className="flex items-center gap-2 overflow-hidden">
          <span className="text-[9px] text-saffron">
            {e.sanskrit || "◈"}
          </span>
          <span className="text-[9px] font-bold uppercase tracking-wider text-bone truncate">
            {e.title}
          </span>
        </div>
        <div className="flex gap-1">
          <div className="retro-button">_</div>
          <div className="retro-button">□</div>
          <div className="retro-button">×</div>
        </div>
      </div>

      <div className="p-3 bg-[#e8dfcc] border border-inset border-[#b3a488] m-1 min-h-[86px] flex flex-col gap-2">
        <div className="flex items-center justify-between">
          <span
            className="text-[8px] font-bold uppercase tracking-widest px-1.5 py-0.5 border"
            style={{
              color: typeColor[e.type],
              borderColor: typeColor[e.type],
              background: `${typeColor[e.type]}11`,
            }}
          >
            {TYPE_LABEL[e.type]}
          </span>
          {e.period && (e.period.start || e.period.end) && (
            <span className="text-[8px] text-ink-muted font-mono">
              {e.period.start ?? "?"}–{e.period.end ?? "?"}
            </span>
          )}
        </div>

        <p className="text-[9px] text-ink leading-relaxed font-mono italic line-clamp-3">
          {e.summary}
        </p>

        {e.concepts && e.concepts.length > 0 && (
          <div className="flex gap-1 flex-wrap mt-auto">
            {e.concepts.slice(0, 3).map((c) => (
              <span
                key={c}
                className="text-[8px] px-1.5 py-0.5 bg-[#efe6d2] text-ink-muted border border-[#c9bda0] font-mono"
              >
                {c}
              </span>
            ))}
          </div>
        )}
      </div>

      <Handle type="target" position={Position.Top} className="opacity-0" />
      <Handle type="source" position={Position.Bottom} className="opacity-0" />
    </div>
  );
}
