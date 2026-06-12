import { useState } from "react";
import { Card, Select, Row, Col, Tag, Empty, Alert, Space } from "antd";
import useSWR from "swr";
import { runsApi } from "../../api/runs";
import { skillsApi } from "../../api/skills";
import ScoreRadar from "../../components/ScoreRadar";
import DimensionTable from "../../components/DimensionTable";
import CapBadge from "../../components/CapBadge";
import { scoreBand } from "../../theme";

// P1 — A/B compare two runs side-by-side.
export default function Compare() {
  const [runA, setRunA] = useState<string>();
  const [runB, setRunB] = useState<string>();
  const { data: skills } = useSWR("/api/skills?family=self", () => skillsApi.list("self"));
  const { data: recent } = useSWR("/api/runs?status=done&page_size=80",
    () => runsApi.list({ status: "done", page_size: 80 }));
  const detailA = useSWR(runA ? `/api/runs/${runA}` : null, () => runsApi.get(runA!));
  const detailB = useSWR(runB ? `/api/runs/${runB}` : null, () => runsApi.get(runB!));

  const options = (recent?.items || []).map((r) => {
    const s = (skills || []).find((x) => x.id === r.skill_id);
    return {
      value: r.id,
      label: `[${s?.code || "?"}] ${r.judge_model} · ${r.final_score?.toFixed(1) ?? "—"} · ${r.id.slice(0, 8)}`,
    };
  });

  const dimsOf = (d: any) => Object.entries(d?.dimension_scores || {})
    .filter(([k]) => (d?.weight_assignment || {})[k]?.applicability !== "not_applicable")
    .map(([k, v]: [string, any]) => ({ key: k, label: k, score: v.raw_score ?? 0 }));

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      <Alert
        type="info"
        showIcon
        message="Run 对比 (P1)"
        description="并排查看两次评测,差异维度高亮。建议选择同 Skill 的不同 Judge Model,或同 TestCase 不同时刻的 Run。"
      />
      <Row gutter={16}>
        <Col span={12}>
          <Card title="Run A" extra={
            <Select
              showSearch
              filterOption={(input, opt) => (opt?.label as string)?.includes(input)}
              placeholder="选 Run A"
              style={{ width: 360 }}
              value={runA}
              options={options}
              onChange={setRunA}
            />
          }>
            {detailA.data ? <RunPanel data={detailA.data} /> : <Empty />}
          </Card>
        </Col>
        <Col span={12}>
          <Card title="Run B" extra={
            <Select
              showSearch
              filterOption={(input, opt) => (opt?.label as string)?.includes(input)}
              placeholder="选 Run B"
              style={{ width: 360 }}
              value={runB}
              options={options}
              onChange={setRunB}
            />
          }>
            {detailB.data ? <RunPanel data={detailB.data} /> : <Empty />}
          </Card>
        </Col>
      </Row>

      {detailA.data && detailB.data && (
        <Card title="差异">
          <DiffSummary a={detailA.data} b={detailB.data} />
        </Card>
      )}
    </Space>
  );
}

function RunPanel({ data }: { data: any }) {
  const dims = Object.entries(data.dimension_scores || {})
    .filter(([k]) => (data.weight_assignment || {})[k]?.applicability !== "not_applicable")
    .map(([k, v]: [string, any]) => ({ key: k, label: k, score: v.raw_score ?? 0 }));
  return (
    <Space direction="vertical" size={12} style={{ width: "100%" }}>
      <Space wrap>
        <Tag color="blue">{data.skill_id}</Tag>
        <Tag>{data.judge_model}</Tag>
        <Tag color={scoreBand(data.final_score)?.color}>
          {data.final_score?.toFixed(1) ?? "—"}
        </Tag>
      </Space>
      <ScoreRadar dimensions={dims} height={280} modelLabel={data.judge_model} />
      <CapBadge caps={data.caps} />
      <DimensionTable
        weight_assignment={data.weight_assignment}
        dimension_scores={data.dimension_scores}
      />
    </Space>
  );
}

function DiffSummary({ a, b }: { a: any; b: any }) {
  const dimsA = a.dimension_scores || {};
  const dimsB = b.dimension_scores || {};
  const allKeys = Array.from(new Set([...Object.keys(dimsA), ...Object.keys(dimsB)]));
  const rows = allKeys.map((k) => {
    const sa = dimsA[k]?.raw_score ?? null;
    const sb = dimsB[k]?.raw_score ?? null;
    const delta = sa != null && sb != null ? sb - sa : null;
    return { key: k, sa, sb, delta };
  }).sort((x, y) => Math.abs(y.delta ?? 0) - Math.abs(x.delta ?? 0));

  return (
    <div>
      <div style={{ marginBottom: 12 }}>
        <strong>最终分:</strong>{" "}
        <Tag color={scoreBand(a.final_score)?.color}>{a.final_score?.toFixed(1)}</Tag>
        →
        <Tag color={scoreBand(b.final_score)?.color}>{b.final_score?.toFixed(1)}</Tag>
        <Tag color={(b.final_score ?? 0) > (a.final_score ?? 0) ? "green" : "red"}>
          Δ {((b.final_score ?? 0) - (a.final_score ?? 0)).toFixed(2)}
        </Tag>
      </div>
      <table style={{ width: "100%", fontSize: 12, borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ background: "#fafafa" }}>
            <th style={td}>维度</th>
            <th style={td}>A</th>
            <th style={td}>B</th>
            <th style={td}>Δ</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((r) => (
            <tr key={r.key} style={r.delta != null && Math.abs(r.delta) >= 20 ? { background: "#fff7e6" } : {}}>
              <td style={td}><code>{r.key}</code></td>
              <td style={td}>{r.sa ?? "—"}</td>
              <td style={td}>{r.sb ?? "—"}</td>
              <td style={td}>{r.delta != null ? r.delta.toFixed(0) : "—"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

const td: React.CSSProperties = { border: "1px solid #f0f0f0", padding: "4px 8px" };
