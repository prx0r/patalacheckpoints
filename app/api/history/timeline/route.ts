import timeline from "@/data/atlas/historyTimeline.json";

export async function GET() {
  return Response.json(timeline, {
    headers: { "Cache-Control": "s-maxage=86400, stale-while-revalidate" },
  });
}
