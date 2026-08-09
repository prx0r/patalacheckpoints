"use client";

import { getSmoothStepPath, EdgeProps } from "reactflow";
import { relationMeta } from "@/data/atlas";

// The lineage-flow edge: two particles flowing along the relationship —
// one saffron, one dim vermilion. A transmission/lineage-flow feeling,
// not a Windows "electrons" effect.

export function AtlasEdge({
  id,
  sourceX,
  sourceY,
  targetX,
  targetY,
  sourcePosition,
  targetPosition,
  data,
}: EdgeProps) {
  const [edgePath] = getSmoothStepPath({
    sourceX,
    sourceY,
    sourcePosition,
    targetX,
    targetY,
    targetPosition,
    borderRadius: 32,
  });

  const meta = relationMeta[data?.type] ?? {
    label: "RELATES",
    color: "#928873",
  };

  return (
    <>
      <path
        id={id}
        style={{
          stroke: meta.color,
          strokeOpacity: 0.45,
          strokeWidth: 1.2,
          strokeDasharray: meta.dash ?? undefined,
        }}
        className="react-flow__edge-path"
        d={edgePath}
      />

      {/* saffron particle — the transmission */}
      <circle r="2" fill="#c58b36">
        <animateMotion
          dur={`${8 + Math.random() * 4}s`}
          repeatCount="indefinite"
          path={edgePath}
        />
      </circle>

      {/* dim vermilion particle */}
      <circle r="1.4" fill="#8b3528">
        <animateMotion
          dur={`${12 + Math.random() * 4}s`}
          repeatCount="indefinite"
          begin="-3s"
          path={edgePath}
        />
      </circle>
    </>
  );
}
