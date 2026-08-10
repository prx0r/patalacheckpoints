import { NextRequest, NextResponse } from "next/server";
import { resources } from "@/data/atlas/resources";
import type { ResourceType, Tradition } from "@/data/atlas/resourcesTypes";

export async function GET(req: NextRequest) {
  const { searchParams } = new URL(req.url);
  const type = searchParams.get("type") as ResourceType | null;
  const tradition = searchParams.get("tradition") as Tradition | null;
  const access = searchParams.get("access"); // free | free_donation | mixed | paid
  const essential = searchParams.get("essential"); // true | false
  const status = searchParams.get("status"); // public | discovery
  const includeNotes = searchParams.get("includeNotes") !== "false"; // default true

  const filtered = resources.filter((r) => {
    if (type && !r.types.includes(type)) return false;
    if (tradition && !r.traditions.includes(tradition)) return false;
    if (access && r.access !== access) return false;
    if (essential && String(Boolean(r.essential)) !== essential) return false;
    if (status && r.status !== status) return false;
    return true;
  });

  const stripped = includeNotes ? filtered : filtered.map(({ note, ...rest }) => rest);

  return NextResponse.json({
    count: filtered.length,
    query: {
      type: type ?? null,
      tradition: tradition ?? null,
      access: access ?? null,
      essential: essential ?? null,
      status: status ?? null,
      includeNotes,
    },
    resources: stripped,
    provenance: {
      note: "The external-resource federation register. Typed (primary_text/manuscript/translation/scholarship/lecture/oral_transmission/legacy_archive/tool/...) and tradition-tagged. can_rehost:false means index/deep-link only — never rehost without permission (SanskritDocuments, ShivaShakti, Wisdom Library explicitly forbid it). status:public = verified; status:discovery = needs individual review. resource urn = tantra:resource:{id}.",
      api_version: "1.0",
    },
  });
}
