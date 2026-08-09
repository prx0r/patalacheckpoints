"use client";

import React, { useMemo, useState, useCallback } from "react";
import ReactFlow, {
  Background,
  Node,
  Edge,
  ReactFlowProvider,
  useNodesState,
  useEdgesState,
} from "reactflow";
import "reactflow/dist/style.css";
import { AnimatePresence } from "framer-motion";
import { atlasEntities, relations } from "@/data/atlas";
import { AtlasNode } from "@/components/atlas/AtlasNode";
import { AtlasEdge } from "@/components/atlas/AtlasEdge";
import { EntityDossier } from "@/components/atlas/EntityDossier";
import { AtlasEntity } from "@/lib/atlas";

const nodeTypes = { atlas: AtlasNode };
const edgeTypes = { atlasEdge: AtlasEdge };

// A simple layered layout — the traditions at the center, texts/people/
// concepts in rings around them. (The canonical reference map's taxonomy,
// rendered as a graph rather than a family tree.)
function layoutPositions() {
  const pos: Record<string, { x: number; y: number }> = {};

  // center hub: the traditions in a pentagon
  const traditions = ["trika", "krama", "kubjika", "kaula", "pratyabhijna", "spanda", "sarvamnyaya"];
  const cx = 0;
  const cy = 0;
  traditions.forEach((t, i) => {
    const angle = (i / traditions.length) * Math.PI * 2 - Math.PI / 2;
    pos[t] = {
      x: cx + Math.cos(angle) * 520,
      y: cy + Math.sin(angle) * 400,
    };
  });

  // ring: texts, people, concepts orbit their tradition
  let angle = 0;
  for (const e of atlasEntities) {
    if (e.type === "tradition") continue;
    angle += 2.4;
    pos[e.id] = {
      x: pos[e.type === "person" ? "pratyabhijna" : "trika"].x +
        Math.cos(angle) * 340,
      y: pos[e.type === "person" ? "pratyabhijna" : "trika"].y +
        Math.sin(angle) * 280,
    };
  }

  return pos;
}

function FlowContent() {
  const [activeEntity, setActiveEntity] = useState<AtlasEntity | null>(null);

  const initialNodes: Node[] = useMemo(() => {
    const pos = layoutPositions();
    return atlasEntities.map((e) => ({
      id: e.id,
      type: "atlas",
      position: pos[e.id] ?? { x: Math.random() * 600, y: Math.random() * 600 },
      data: { entity: e },
      dragHandle: ".retro-title-bar",
    }));
  }, []);

  const initialEdges: Edge[] = useMemo(() => {
    return relations.map((r, i) => ({
      id: `edge-${r.source}-${r.target}-${i}`,
      source: r.source,
      target: r.target,
      type: "atlasEdge",
      data: { type: r.type, confidence: r.confidence, evidence: r.evidence },
    }));
  }, []);

  const [nodes, setNodes, onNodesChange] = useNodesState(initialNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(initialEdges);

  const onNodeClick = useCallback((_: unknown, node: Node) => {
    const entity = atlasEntities.find((e) => e.id === node.id);
    if (entity) setActiveEntity(entity);
  }, []);

  const navigateTo = useCallback((id: string) => {
    const entity = atlasEntities.find((e) => e.id === id);
    if (entity) setActiveEntity(entity);
  }, []);

  return (
    <div className="relative min-h-screen w-full bg-[#d8d0c0] font-sans overflow-hidden">
      <div className="absolute inset-0 z-0">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          onNodeClick={onNodeClick}
          nodeTypes={nodeTypes}
          edgeTypes={edgeTypes}
          fitView
          fitViewOptions={{ padding: 0.25 }}
          nodesConnectable={false}
          className="bg-transparent"
          minZoom={0.15}
          maxZoom={1.6}
        >
          <Background color="#746c5d" gap={44} size={0.6} />
        </ReactFlow>
      </div>

      {/* Branding — the atlas header */}
      {!activeEntity && (
        <div className="absolute bottom-12 left-16 z-[200] pointer-events-none">
          <div className="flex flex-col gap-3 items-start pointer-events-auto">
            <div className="retro-window p-7 border-[3px] border-[#272641] shadow-[20px_20px_0px_rgba(0,0,0,0.18)] bg-[#e8dfcc]">
              <div className="flex flex-col gap-4">
                <div className="relative">
                  <h1 className="text-[#1b1915] text-4xl font-black uppercase tracking-[-0.04em] leading-none mb-2">
                    Śaiva Tantra
                    <span className="text-[#8b3528]"> Atlas</span>
                  </h1>
                  <div className="h-1 w-16 bg-[#c58b36] mb-3" />
                </div>
                <div className="text-[9px] text-[#71695b] font-black uppercase tracking-[0.2em] leading-relaxed">
                  <div>A research workstation for medieval Śaiva texts</div>
                  <div className="mt-1 flex items-center gap-2">
                    <span className="bindu" /> traditions · texts · ācāryas · concepts
                  </div>
                </div>
              </div>
            </div>
            <div className="text-[8px] text-[#71695b] font-mono uppercase tracking-[0.4em] pl-1">
              SYS.ŚIVAVIJÑĀNA.V0.1
            </div>
          </div>
        </div>
      )}

      <AnimatePresence>
        {activeEntity && (
          <EntityDossier
            entity={activeEntity}
            onClose={() => setActiveEntity(null)}
            onNavigate={navigateTo}
          />
        )}
      </AnimatePresence>

      <div className="absolute top-10 right-10 z-[200] pointer-events-none select-none">
        <div className="text-[8px] uppercase tracking-[0.5em] text-[#71695b] font-mono rotate-90 origin-right flex items-center gap-4">
          <span className="h-px w-12 bg-[#b3a488]"></span>
          MANUSCRIPT-TECH · LINKS_LIVE
        </div>
      </div>
    </div>
  );
}

export default function Home() {
  return (
    <ReactFlowProvider>
      <FlowContent />
    </ReactFlowProvider>
  );
}
