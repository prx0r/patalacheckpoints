import { promises as fs } from "fs";
import path from "path";

const ROOT = process.cwd();
const REG = path.join(ROOT, "data/corpus/registries");
const CERTS = path.join(ROOT, "factory-certificates");

async function readJsonl(name: string): Promise<unknown[]> {
  const p = path.join(REG, `${name}-registry.jsonl`);
  try {
    const txt = await fs.readFile(p, "utf-8");
    return txt.split("\n").filter(Boolean).map((l) => JSON.parse(l));
  } catch {
    return [];
  }
}

async function readCert(name: string) {
  const p = path.join(CERTS, name, "results.json");
  try {
    return JSON.parse(await fs.readFile(p, "utf-8"));
  } catch {
    return null;
  }
}

export async function GET() {
  const layers = ["source", "l0", "l1", "l2", "l200", "c1", "theme", "essay", "assertion", "corroboration", "witness", "span"];
  const registry: Record<string, number> = {};
  for (const l of layers) {
    registry[l] = (await readJsonl(l)).length;
  }
  return Response.json({
    registry,
    certificates: {
      L0: await readCert("L0-v1"),
      L200: await readCert("L200-v1"),
    },
    controller: "pipeline/autonomy.py",
    note: "Autonomous translation factory status — registry = canonical state; certificates = the A-H / A-L gates.",
  });
}
