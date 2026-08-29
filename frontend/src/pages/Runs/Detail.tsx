import { useNavigate, useParams } from "react-router-dom";
import {
  Card,
  Space,
  Tag,
  Tabs,
  Button,
  Descriptions,
  Statistic,
  Row,
  Col,
  Alert,
  Empty,
} from "antd";
import { ArrowLeftOutlined, ReloadOutlined } from "@ant-design/icons";
import useSWR from "swr";
import dayjs from "dayjs";

import { runsApi } from "../../api/runs";
import { testsetsApi } from "../../api/testsets";
import ScoreRadar from "../../components/ScoreRadar";
import DimensionTable from "../../components/DimensionTable";
import CapBadge from "../../components/CapBadge";
import RootCauseTimeline from "../../components/RootCauseTimeline";
import ChainViewer from "../../components/ChainViewer";
import MarkdownView from "../../components/MarkdownView";
import SSEProgressBar from "../../components/SSEProgressBar";
import { scoreBand } from "../../theme";

export default function RunDetail() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, mutate } = useSWR(
    id ? `/api/runs/${id}` : null,
    () => runsApi.get(id),
    {
      refreshInterval: (latest) =>
        latest && ["pending", "routing", "running", "scoring"].includes(latest.status)
          ? 2_000
          : 0,
      revalidateOnFocus: true,
    }
  );
  const isLive = data && ["pending", "routing", "running", "scoring"].includes(data.status);

  const { data: testcase } = useSWR(
    data?.testcase_id ? `/api/testsets/${data.testcase_id}` : null,
    () => testsetsApi.get(data!.testcase_id)
  );

  if (isLoading) return <Card loading />;
  if (!data) return <Card>未找到 Run {id}</Card>;

  // Build radar dimensions from dimension_scores joined with weight_assignment
  const dims = Object.entries(data.dimension_scores || {})
    .filter(([k]) => (data.weight_assignment || {})[k]?.applicability !== "not_applicable")
    .map(([k, v]: [string, any]) => ({
      key: k,
      label: k,
      score: v.raw_score ?? 0,
      weight: (data.weight_assignment || {})[k]?.dynamic_weight ?? 0,
    }));

  const band = scoreBand(data.final_score);

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      <Card
        title={
          <Space>
            <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} />
            <code style={{ fontSize: 12 }}>{data.id}</code>
            <Tag color={
              data.status === "done" ? "success" :
              data.status === "failed" ? "error" : "processing"
            }>{data.status}</Tag>
            <Tag color="blue">{data.skill_id}</Tag>
            <Tag>{data.judge_model}</Tag>
            <Tag color="cyan">{data.judge_provider}</Tag>
          </Space>
        }
        extra={
          <Space>
            <Button icon={<ReloadOutlined />} onClick={() => mutate()} />
            {data.status === "failed" && (
              <Button type="primary" onClick={async () => {
                const r = await runsApi.rerun(data.id);
                navigate(`/runs/${r.id}`);
              }}>重试</Button>
            )}
          </Space>
        }
      >
        {isLive && (
          <Alert
            type="info"
            showIcon
            message="评测进行中(SSE 实时进度)"
            style={{ marginBottom: 12 }}
            description={<SSEProgressBar runId={data.id} onComplete={() => mutate()} onError={() => mutate()} />}
          />
        )}
        {data.error_msg && (
          <Alert type="error" showIcon message="评测失败" description={data.error_msg}
            style={{ marginBottom: 12 }} />
        )}

        <Row gutter={16}>
          <Col xs={24} sm={12} xl={6}>
            <Statistic
              title="最终分"
              value={data.final_score ?? "—"}
              precision={2}
              valueStyle={{ color: band?.color, fontSize: 32 }}
              suffix={band?.label}
            />
          </Col>
          <Col xs={24} sm={12} xl={6}>
            <Statistic
              title="未封顶加权"
              value={data.absolute_score_pre_cap ?? "—"}
              precision={2}
            />
          </Col>
          <Col xs={24} sm={12} xl={6}>
            <Statistic
              title="Latency"
              value={data.latency_ms != null ? (data.latency_ms / 1000).toFixed(2) : "—"}
              suffix="s"
            />
          </Col>
          <Col xs={24} sm={12} xl={6}>
            <Statistic
              title="Tokens (in/out)"
              value={`${data.tokens_in ?? "—"} / ${data.tokens_out ?? "—"}`}
              valueStyle={{ fontSize: 18 }}
            />
          </Col>
        </Row>

        {data.routing && (
          <Card type="inner" size="small" style={{ marginTop: 16 }} title="🤖 路由结果">
            <Space wrap>
              <Tag color="blue">{(data.routing as any).skill_id}</Tag>
              <span>{(data.routing as any).predicted_skill}</span>
              <Tag color="cyan">
                置信 {(((data.routing as any).confidence || 0) * 100).toFixed(0)}%
              </Tag>
              <Tag>{(data.routing as any).stage_used}</Tag>
              {(data.routing as any).fallback && <Tag color="orange">fallback</Tag>}
            </Space>
            <div style={{ marginTop: 6, fontSize: 12, color: "#666" }}>
              {(data.routing as any).reasoning}
            </div>
          </Card>
        )}
      </Card>

      <Card>
        <Tabs
          defaultActiveKey="scoring"
          items={[
            {
              key: "scoring",
              label: "评分明细",
              children: (
                <Row gutter={16}>
                  <Col xs={24} xl={10}>
                    <Card type="inner" size="small" title="维度雷达">
                      {dims.length > 0 ? (
                        <ScoreRadar dimensions={dims} height={360} modelLabel={data.judge_model} />
                      ) : (
                        <Empty description={isLive ? "等待评测完成…" : "无维度数据"} />
                      )}
                    </Card>
                  </Col>
                  <Col xs={24} xl={14}>
                    <Card type="inner" size="small" title="维度详情">
                      <DimensionTable
                        weight_assignment={data.weight_assignment}
                        dimension_scores={data.dimension_scores}
                        skipped_dimensions={data.skipped_dimensions as any}
                      />
                    </Card>
                  </Col>
                </Row>
              ),
            },
            {
              key: "caps",
              label: `封顶规则 (${(data.caps || []).filter((c: any) => c.triggered).length})`,
              children: <CapBadge caps={data.caps as any} />,
            },
            {
              key: "root",
              label: `根因 (${(data.root_causes || []).length})`,
              children: <RootCauseTimeline root_causes={data.root_causes as any} />,
            },
            {
              key: "narrative",
              label: "评审报告",
              children: <NarrativeView review={data.narrative_review} />,
            },
            {
              key: "question",
              label: "样本",
              children: testcase ? (
                <Tabs items={[
                  {
                    key: "q",
                    label: "问题 + 答案",
                    children: (
                      <Space direction="vertical" style={{ width: "100%" }} size={16}>
                        <Card type="inner" size="small" title="问题">
                          <MarkdownView text={testcase.question} />
                        </Card>
                        <Card type="inner" size="small" title="Agent 回答">
                          <MarkdownView text={testcase.agent_answer} />
                        </Card>
                      </Space>
                    ),
                  },
                  {
                    key: "chain",
                    label: `链路 (${testcase.reasoning_trace?.length || 0} 步)`,
                    children: <ChainViewer
                      chain={testcase.reasoning_trace as any[]}
                      context={testcase.context_history as any[]}
                    />,
                  },
                ]} />
              ) : <Empty />,
            },
            {
              key: "matched",
              label: `命中专家案例 (${(data.matched_golden_cases || []).length})`,
              children: data.matched_golden_cases && data.matched_golden_cases.length > 0 ? (
                <ul>
                  {(data.matched_golden_cases as string[]).map((m) => <li key={m}><code>{m}</code></li>)}
                </ul>
              ) : <Empty />,
            },
            {
              key: "raw",
              label: "原始 JSON",
              children: (
                <pre className="json-viewer">{JSON.stringify(data.raw_response, null, 2)}</pre>
              ),
            },
            {
              key: "meta",
              label: "元数据",
              children: (
                <Descriptions size="small" column={2} bordered>
                  <Descriptions.Item label="Run ID">{data.id}</Descriptions.Item>
                  <Descriptions.Item label="Batch">{data.batch_id || "—"}</Descriptions.Item>
                  <Descriptions.Item label="TestCase">{data.testcase_id}</Descriptions.Item>
                  <Descriptions.Item label="Skill">{data.skill_id}</Descriptions.Item>
                  <Descriptions.Item label="Judge Model">{data.judge_model}</Descriptions.Item>
                  <Descriptions.Item label="Provider">{data.judge_provider}</Descriptions.Item>
                  <Descriptions.Item label="开始">{dayjs(data.created_at).format("YYYY-MM-DD HH:mm:ss")}</Descriptions.Item>
                  <Descriptions.Item label="完成">{data.finished_at ? dayjs(data.finished_at).format("YYYY-MM-DD HH:mm:ss") : "—"}</Descriptions.Item>
                </Descriptions>
              ),
            },
          ]}
        />
      </Card>
    </Space>
  );
}

function NarrativeView({ review }: { review?: any }) {
  if (!review) return <Empty />;
  return (
    <Space direction="vertical" style={{ width: "100%" }} size={16}>
      {review.summary && (
        <Card type="inner" size="small" title="总评">
          <div>{review.summary}</div>
        </Card>
      )}
      <Row gutter={16}>
        <Col xs={24} lg={12}>
          <Card type="inner" size="small" title="✅ 强项">
            <ul>{(review.strengths || []).map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card type="inner" size="small" title="⚠ 弱项">
            <ul>{(review.weaknesses || []).map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>
          </Card>
        </Col>
      </Row>
      {review.next_actions && review.next_actions.length > 0 && (
        <Card type="inner" size="small" title="🎯 下一步建议">
          <ul>{review.next_actions.map((s: string, i: number) => <li key={i}>{s}</li>)}</ul>
        </Card>
      )}
    </Space>
  );
}
