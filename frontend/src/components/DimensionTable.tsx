import { Table, Tag } from "antd";

interface Props {
  weight_assignment?: Record<string, any> | null;
  dimension_scores?: Record<string, any> | null;
  skipped_dimensions?: Array<{ dimension: string; reason?: string }> | null;
}

// Tabular view of dimension scores joined with their dynamic weights.
export default function DimensionTable({
  weight_assignment,
  dimension_scores,
  skipped_dimensions,
}: Props) {
  const rows: any[] = [];
  const ws = weight_assignment || {};
  const ds = dimension_scores || {};
  const allKeys = new Set([...Object.keys(ws), ...Object.keys(ds)]);

  for (const key of allKeys) {
    const w = ws[key] || {};
    const d = ds[key] || {};
    rows.push({
      key,
      dimension: key,
      applicability: w.applicability || "relevant",
      weight: w.dynamic_weight ?? null,
      raw_score: d.raw_score ?? null,
      weighted: w.dynamic_weight != null && d.raw_score != null
        ? Math.round((d.raw_score / 100) * w.dynamic_weight * 100) / 100
        : null,
      rationale: w.rationale || "",
      evidence: d.evidence || [],
    });
  }
  rows.sort((a, b) => (b.weight ?? 0) - (a.weight ?? 0));

  const colorOf = (raw: number | null) => {
    if (raw == null) return "default";
    if (raw >= 80) return "green";
    if (raw >= 60) return "blue";
    if (raw >= 40) return "orange";
    return "red";
  };

  return (
    <>
      <Table
        dataSource={rows}
        size="small"
        pagination={false}
        columns={[
          {
            title: "维度",
            dataIndex: "dimension",
            key: "dimension",
            render: (v: string) => <code>{v}</code>,
          },
          {
            title: "适用性",
            dataIndex: "applicability",
            key: "applicability",
            width: 100,
            render: (v: string) => {
              const map: Record<string, string> = {
                relevant: "blue",
                supplementary: "geekblue",
                not_applicable: "default",
              };
              return <Tag color={map[v] || "default"}>{v}</Tag>;
            },
          },
          {
            title: "动态权重",
            dataIndex: "weight",
            key: "weight",
            width: 90,
            align: "right" as const,
            render: (v: number | null) => v ?? "—",
          },
          {
            title: "原始分",
            dataIndex: "raw_score",
            key: "raw_score",
            width: 80,
            align: "right" as const,
            render: (v: number | null) => (
              <Tag color={colorOf(v)}>{v ?? "—"}</Tag>
            ),
          },
          {
            title: "加权分",
            dataIndex: "weighted",
            key: "weighted",
            width: 90,
            align: "right" as const,
            render: (v: number | null) => (v != null ? v.toFixed(2) : "—"),
          },
          {
            title: "权重理由",
            dataIndex: "rationale",
            key: "rationale",
            ellipsis: true,
          },
        ]}
      />
      {skipped_dimensions && skipped_dimensions.length > 0 && (
        <div style={{ marginTop: 12, color: "#999", fontSize: 12 }}>
          <strong>跳过的维度:</strong>{" "}
          {skipped_dimensions.map((s) => (
            <Tag key={s.dimension}>{s.dimension} — {s.reason || ""}</Tag>
          ))}
        </div>
      )}
    </>
  );
}
