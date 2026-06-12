import { Card, Col, Row, Statistic, Table, Tag, Empty, Space, Alert } from "antd";
import {
  ExperimentOutlined,
  DatabaseOutlined,
  PlayCircleOutlined,
  CheckCircleOutlined,
} from "@ant-design/icons";
import { Link } from "react-router-dom";
import useSWR from "swr";
import ReactECharts from "echarts-for-react";
import dayjs from "dayjs";

import { dashboardApi } from "../../api/dashboard";
import { PALETTE, scoreBand } from "../../theme";
import type { TopFailureRow } from "../../api/types";

export default function Dashboard() {
  const { data: summary } = useSWR("/api/dashboard/summary", dashboardApi.summary, {
    refreshInterval: 30_000,
  });
  const { data: coverage } = useSWR(
    "/api/dashboard/skill-coverage",
    dashboardApi.skillCoverage
  );
  const { data: trend } = useSWR(
    "/api/dashboard/trend?days=30",
    () => dashboardApi.trend(30)
  );
  const { data: failures } = useSWR(
    "/api/dashboard/top-failures",
    () => dashboardApi.topFailures(10)
  );

  // 13-axis radar
  const radarIndicators =
    coverage?.map((c) => ({ name: `${c.code} ${c.name_zh.slice(0, 6)}`, max: 100 })) || [];
  const radarValues = coverage?.map((c) => c.avg_score ?? 0) || [];

  const radarOption = {
    tooltip: { trigger: "item" },
    radar: {
      indicator: radarIndicators,
      radius: "65%",
      splitArea: { areaStyle: { color: ["#f5faff", "#ffffff"] } },
      axisLabel: { fontSize: 10, color: "#666" },
      name: { textStyle: { fontSize: 11 } },
    },
    series: [{
      type: "radar",
      data: [{
        value: radarValues,
        name: "13 Skill 均分",
        areaStyle: { color: "rgba(9,88,217,0.25)" },
        lineStyle: { color: "#0958d9", width: 2 },
      }],
    }],
  };

  // Trend (one line per skill or single line if mixed)
  const skillSet = Array.from(new Set((trend || []).map((t) => t.skill_id || "all")));
  const dateSet = Array.from(new Set((trend || []).map((t) => t.date))).sort();
  const trendOption = {
    tooltip: { trigger: "axis" },
    legend: { data: skillSet, type: "scroll", textStyle: { fontSize: 10 } },
    grid: { left: 40, right: 16, top: 32, bottom: 24 },
    xAxis: { type: "category", data: dateSet },
    yAxis: { type: "value", min: 0, max: 100, name: "均分" },
    series: skillSet.map((sid, idx) => ({
      name: sid,
      type: "line",
      smooth: true,
      data: dateSet.map((d) => {
        const p = (trend || []).find((t) => t.date === d && (t.skill_id || "all") === sid);
        return p?.avg_score ?? null;
      }),
      lineStyle: { color: PALETTE[idx % PALETTE.length] },
      itemStyle: { color: PALETTE[idx % PALETTE.length] },
      connectNulls: true,
    })),
  };

  // L1 root-cause distribution bar
  const l1Data = summary?.by_l1_root_cause || [];
  const l1Option = {
    tooltip: { trigger: "axis", axisPointer: { type: "shadow" } },
    grid: { left: 100, right: 16, top: 16, bottom: 24 },
    xAxis: { type: "value" },
    yAxis: { type: "category", data: l1Data.map((d) => d.l1).reverse() },
    series: [{
      type: "bar",
      data: l1Data.map((d) => d.count).reverse(),
      itemStyle: { color: "#fa8c16" },
      label: { show: true, position: "right" },
    }],
  };

  const noModels = summary && summary.available_models.length === 0;

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      {noModels && (
        <Alert
          type="warning"
          showIcon
          message="后端尚未配置任何 LLM Provider"
          description="请在 Render 环境变量中至少设置一个 ANTHROPIC_API_KEY / OPENAI_API_KEY / DASHSCOPE_API_KEY / DEEPSEEK_API_KEY,前端永远不会接触 key。"
        />
      )}

      <Row gutter={16}>
        <Col span={6}>
          <Card>
            <Statistic title="测试样本总数" value={summary?.total_testcases ?? "—"}
              prefix={<DatabaseOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="已完成评测" value={summary?.total_runs ?? "—"}
              prefix={<PlayCircleOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="平均分"
              value={summary?.avg_score ?? "—"}
              precision={2}
              prefix={<ExperimentOutlined />}
              valueStyle={{ color: scoreBand(summary?.avg_score)?.color }}
              suffix={
                summary?.avg_score != null
                  ? scoreBand(summary?.avg_score)?.label
                  : ""
              }
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="通过率 (≥60)"
              value={summary?.pass_rate != null ? Math.round(summary.pass_rate * 1000) / 10 : "—"}
              suffix={summary?.pass_rate != null ? "%" : ""}
              precision={1}
              prefix={<CheckCircleOutlined />}
            />
            <div style={{ fontSize: 12, color: "#999", marginTop: 4 }}>
              最近 24h 新增 {summary?.last_24h_runs ?? 0} 次
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={12}>
          <Card title="13 类 Skill 覆盖均分">
            {coverage && coverage.length > 0 ? (
              <ReactECharts option={radarOption} style={{ height: 380 }} notMerge />
            ) : (
              <Empty description="尚无评测数据 — 请到 Runs 页面创建第一个评测" />
            )}
          </Card>
        </Col>
        <Col span={12}>
          <Card title="L1 根因分布">
            {l1Data.length > 0 ? (
              <ReactECharts option={l1Option} style={{ height: 380 }} notMerge />
            ) : (
              <Empty />
            )}
          </Card>
        </Col>
      </Row>

      <Card title="30 天分数趋势(按 Skill)">
        {(trend?.length || 0) > 0 ? (
          <ReactECharts option={trendOption} style={{ height: 280 }} notMerge />
        ) : (
          <Empty description="暂无趋势数据" />
        )}
      </Card>

      <Card title="Top 10 失败 / 低分样本">
        <Table<TopFailureRow>
          dataSource={failures || []}
          rowKey="run_id"
          size="small"
          pagination={false}
          columns={[
            {
              title: "问题",
              dataIndex: "question_preview",
              key: "question_preview",
              ellipsis: true,
            },
            {
              title: "Skill",
              dataIndex: "skill_id",
              key: "skill_id",
              width: 120,
              render: (v: string) => <Tag color="blue">{v}</Tag>,
            },
            {
              title: "最终分",
              dataIndex: "final_score",
              key: "final_score",
              width: 90,
              align: "right" as const,
              render: (v: number) => (
                <Tag color={scoreBand(v)?.color}>{v.toFixed(1)}</Tag>
              ),
            },
            {
              title: "封顶",
              dataIndex: "caps_triggered",
              key: "caps_triggered",
              width: 200,
              render: (v: string[]) =>
                v && v.length > 0 ? v.map((r) => (
                  <Tag key={r} color="red">{r}</Tag>
                )) : <span style={{ color: "#999" }}>—</span>,
            },
            {
              title: "L1 根因",
              dataIndex: "top_root_cause",
              key: "top_root_cause",
              width: 110,
              render: (v: string | null) => v ? <Tag color="orange">{v}</Tag> : "—",
            },
            {
              title: "时间",
              dataIndex: "created_at",
              key: "created_at",
              width: 160,
              render: (v: string) => dayjs(v).format("MM-DD HH:mm"),
            },
            {
              title: "",
              key: "actions",
              width: 80,
              render: (_: any, row: TopFailureRow) => (
                <Link to={`/runs/${row.run_id}`}>查看</Link>
              ),
            },
          ]}
        />
      </Card>
    </Space>
  );
}
