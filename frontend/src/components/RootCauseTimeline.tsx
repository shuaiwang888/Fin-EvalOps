import { Timeline, Tag, Empty } from "antd";

interface Props {
  root_causes?: Array<{
    l1?: string;
    l2?: string;
    dimension?: string;
    raw_score?: number;
    confidence?: string;
    summary?: string;
    evidence?: any[];
  }> | null;
}

// L1 stage colors taken from the protocol catalog.
const L1_COLOR: Record<string, string> = {
  intent: "magenta",
  context: "purple",
  coverage: "cyan",
  evidence: "blue",
  tool: "geekblue",
  data_logic: "volcano",
  reasoning: "orange",
  capability_gap: "gold",
  safety_or_compliance: "red",
  latency: "lime",
  composition: "green",
};

export default function RootCauseTimeline({ root_causes }: Props) {
  const items = (root_causes || []).filter(Boolean);
  if (!items.length) {
    return <Empty description="未触发根因 — 维度均已达标" image={Empty.PRESENTED_IMAGE_SIMPLE} />;
  }
  // Sort by raw_score ascending (most impactful first)
  const sorted = [...items].sort(
    (a, b) => (a.raw_score ?? 100) - (b.raw_score ?? 100)
  );
  return (
    <Timeline
      mode="left"
      items={sorted.map((rc) => ({
        color: rc.raw_score != null && rc.raw_score < 40 ? "red" : "orange",
        label: (
          <span style={{ fontSize: 12, color: "#666" }}>
            {rc.dimension || "?"}
            {rc.raw_score != null && (
              <Tag style={{ marginLeft: 6 }} color={rc.raw_score < 40 ? "red" : "orange"}>
                {rc.raw_score}
              </Tag>
            )}
          </span>
        ),
        children: (
          <div>
            <div style={{ marginBottom: 4 }}>
              <Tag color={L1_COLOR[rc.l1 || ""] || "default"}>
                L1 · {rc.l1 || "?"}
              </Tag>
              {rc.l2 && <Tag>L2 · {rc.l2}</Tag>}
              {rc.confidence && (
                <Tag color="cyan">置信度 · {rc.confidence}</Tag>
              )}
            </div>
            {rc.summary && (
              <div style={{ fontSize: 13, color: "#333", marginBottom: 4 }}>
                {rc.summary}
              </div>
            )}
            {rc.evidence && rc.evidence.length > 0 && (
              <details style={{ fontSize: 12, color: "#666" }}>
                <summary>证据 ({rc.evidence.length})</summary>
                <ul style={{ paddingLeft: 18 }}>
                  {rc.evidence.map((e, i) => (
                    <li key={i}>
                      <Tag color="default">{e.source || "?"}</Tag>{" "}
                      {e.summary || e.pointer || JSON.stringify(e).slice(0, 80)}
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </div>
        ),
      }))}
    />
  );
}
