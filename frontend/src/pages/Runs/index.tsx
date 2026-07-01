import { useEffect, useState } from "react";
import {
  Card,
  Table,
  Tag,
  Space,
  Button,
  Modal,
  Form,
  Input,
  Select,
  message,
  Tooltip,
  Progress,
  Alert,
  Radio,
  Popconfirm,
} from "antd";
import {
  PlusOutlined,
  ReloadOutlined,
  ThunderboltOutlined,
  PlayCircleOutlined,
  DeleteOutlined,
} from "@ant-design/icons";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import useSWR from "swr";
import dayjs from "dayjs";

import { runsApi, routeApi } from "../../api/runs";
import { testsetsApi } from "../../api/testsets";
import { skillsApi } from "../../api/skills";
import ModelPicker from "../../components/ModelPicker";
import { scoreBand } from "../../theme";
import type { RunBrief, RouteResponse } from "../../api/types";

const STATUS_COLOR: Record<string, string> = {
  pending: "default",
  routing: "blue",
  running: "processing",
  scoring: "blue",
  done: "success",
  failed: "error",
  cancelled: "warning",
};

export default function Runs() {
  const navigate = useNavigate();
  const [search] = useSearchParams();
  const presetTcId = search.get("testcase_id") || undefined;
  const presetSkillHint = search.get("skill_hint") || undefined;

  const [filters, setFilters] = useState<any>({
    page: 1, page_size: 20,
    testcase_id: presetTcId,
    sort: "created_at",
    order: "desc",
  });
  const key = `/api/runs?${JSON.stringify(filters)}`;
  const { data, isLoading, mutate } = useSWR(key, () => runsApi.list(filters), {
    refreshInterval: 5_000, // auto-refresh while runs are in flight
  });

  const { data: skills } = useSWR("/api/skills?family=self", () => skillsApi.list("self"));

  // -------- Row selection + bulk delete --------
  const [selectedRunKeys, setSelectedRunKeys] = useState<React.Key[]>([]);
  // Reset selection when the underlying data refreshes (otherwise stale ids
  // for deleted runs linger).
  useEffect(() => {
    const liveIds = new Set((data?.items || []).map((r) => r.id));
    setSelectedRunKeys((keys) => keys.filter((k) => liveIds.has(String(k))));
  }, [data]);

  const handleDeleteSelected = async () => {
    if (selectedRunKeys.length === 0) return;
    try {
      const r = await runsApi.deleteRuns(selectedRunKeys.map(String));
      const parts: string[] = [`已删除 ${r.deleted.length} 条`];
      if (r.skipped_busy.length > 0) parts.push(`${r.skipped_busy.length} 条正在评测中,跳过`);
      if (r.skipped_missing.length > 0) parts.push(`${r.skipped_missing.length} 条不存在`);
      message.success(parts.join(";"));
      setSelectedRunKeys([]);
      mutate();
    } catch {
      /* interceptor shows error */
    }
  };

  const handleDeleteOne = async (id: string) => {
    try {
      await runsApi.deleteRun(id);
      message.success(`已删除 Run ${id.slice(0, 8)}`);
      setSelectedRunKeys((keys) => keys.filter((k) => String(k) !== id));
      mutate();
    } catch (e: any) {
      // 409 case: in-flight run — show the reason
      const msg = e?.response?.data?.detail || "删除失败";
      message.error(msg);
    }
  };

  const [showCreate, setShowCreate] = useState(!!presetTcId || !!presetSkillHint);
  useEffect(() => {
    if (presetTcId || presetSkillHint) setShowCreate(true);
  }, [presetTcId, presetSkillHint]);

  return (
    <>
      <Card
        title={`评测 Runs(${data?.total ?? 0})`}
        extra={
          <Space>
            <Button icon={<ReloadOutlined />} onClick={() => mutate()} />
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setShowCreate(true)}>
              新建评测
            </Button>
            <Popconfirm
              title={`删除选中的 ${selectedRunKeys.length} 条 Run?`}
              description="正在评测中的 Run 会自动跳过;删除后无法恢复"
              okText="删除"
              okButtonProps={{ danger: true, disabled: selectedRunKeys.length === 0 }}
              cancelText="取消"
              onConfirm={handleDeleteSelected}
              disabled={selectedRunKeys.length === 0}
            >
              <Button
                danger
                disabled={selectedRunKeys.length === 0}
                icon={<DeleteOutlined />}
              >
                删除选中{selectedRunKeys.length > 0 ? ` (${selectedRunKeys.length})` : ""}
              </Button>
            </Popconfirm>
          </Space>
        }
      >
        <Space style={{ marginBottom: 12 }} wrap>
          <Select
            placeholder="状态"
            allowClear
            style={{ width: 120 }}
            value={filters.status}
            onChange={(v) => setFilters((f: any) => ({ ...f, status: v, page: 1 }))}
            options={Object.keys(STATUS_COLOR).map((s) => ({ value: s, label: s }))}
          />
          <Select
            placeholder="Skill"
            allowClear
            style={{ width: 200 }}
            value={filters.skill_id}
            onChange={(v) => setFilters((f: any) => ({ ...f, skill_id: v, page: 1 }))}
            options={(skills || []).map((s) => ({ value: s.id, label: `${s.code} · ${s.name_zh}` }))}
          />
          <Select
            placeholder="排序"
            style={{ width: 160 }}
            value={`${filters.sort}|${filters.order}`}
            onChange={(v) => {
              const [sort, order] = v.split("|");
              setFilters((f: any) => ({ ...f, sort, order, page: 1 }));
            }}
            options={[
              { value: "created_at|desc", label: "最新优先" },
              { value: "created_at|asc", label: "最早优先" },
              { value: "final_score|asc", label: "分低优先" },
              { value: "final_score|desc", label: "分高优先" },
              { value: "latency_ms|desc", label: "耗时最长" },
              { value: "tokens_in|desc", label: "Tokens 最多" },
            ]}
          />
          <ModelPicker
            value={filters.judge_model}
            allowClear
            onChange={(v) => setFilters((f: any) => ({ ...f, judge_model: v, page: 1 }))}
          />
        </Space>

        <Table<RunBrief>
          loading={isLoading}
          dataSource={data?.items || []}
          rowKey="id"
          size="small"
          rowSelection={{
            selectedRowKeys: selectedRunKeys,
            onChange: (keys) => setSelectedRunKeys(keys),
            getCheckboxProps: (r) => ({
              disabled: r.status === "pending" || r.status === "routing" ||
                         r.status === "running" || r.status === "scoring",
            }),
            preserveSelectedRowKeys: true,
          }}
          pagination={{
            current: filters.page,
            pageSize: filters.page_size,
            total: data?.total ?? 0,
            onChange: (page, page_size) => setFilters((f: any) => ({ ...f, page, page_size })),
          }}
          columns={[
            {
              title: "状态",
              dataIndex: "status",
              key: "status",
              width: 90,
              render: (v: string, r) => (
                <Space size={4} direction="vertical">
                  <Tag color={STATUS_COLOR[v]}>{v}</Tag>
                  {(v === "running" || v === "routing" || v === "scoring") && (
                    <Progress
                      percent={r.progress_pct}
                      size="small"
                      showInfo={false}
                      style={{ width: 80 }}
                    />
                  )}
                </Space>
              ),
            },
            {
              title: "Run ID",
              dataIndex: "id",
              key: "id",
              width: 110,
              render: (v: string) => (
                <Link to={`/runs/${v}`}><code style={{ fontSize: 11 }}>{v.slice(0, 8)}</code></Link>
              ),
            },
            {
              title: "问题",
              dataIndex: "testcase_question",
              key: "testcase_question",
              ellipsis: true,
              render: (v: string | null | undefined, r) => (
                <Tooltip title={v || ""}>
                  <Link to={`/runs/${r.id}`}>{v ? v.slice(0, 80) : "(样本已删除)"}</Link>
                </Tooltip>
              ),
            },
            {
              title: "Skill",
              dataIndex: "skill_id",
              key: "skill_id",
              width: 140,
              render: (v: string) => <Tag color="blue">{v}</Tag>,
            },
            {
              title: "Judge",
              dataIndex: "judge_model",
              key: "judge_model",
              width: 140,
              render: (v: string, r) => (
                <Tooltip title={r.judge_provider}>
                  <Tag>{v}</Tag>
                </Tooltip>
              ),
            },
            {
              title: "最终分",
              dataIndex: "final_score",
              key: "final_score",
              width: 90,
              align: "right" as const,
              render: (v: number | null) => v != null ? (
                <Tag color={scoreBand(v)?.color}>{v.toFixed(1)}</Tag>
              ) : "—",
            },
            {
              title: "Tokens",
              key: "tokens",
              width: 100,
              render: (_, r) => r.tokens_in != null ?
                `${(r.tokens_in / 1000).toFixed(1)}k · ${(r.tokens_out! / 1000).toFixed(1)}k` : "—",
            },
            {
              title: "耗时",
              dataIndex: "latency_ms",
              key: "latency_ms",
              width: 80,
              render: (v: number | null) => v != null ? `${(v / 1000).toFixed(1)}s` : "—",
            },
            {
              title: "时间",
              dataIndex: "created_at",
              key: "created_at",
              width: 130,
              render: (v: string) => dayjs(v).format("MM-DD HH:mm"),
            },
            {
              title: "操作",
              key: "actions",
              width: 160,
              render: (_, r) => {
                const inFlight = ["pending", "routing", "running", "scoring"].includes(r.status);
                return (
                  <Space size={4}>
                    <Button size="small" type="link" onClick={() => navigate(`/runs/${r.id}`)}>详情</Button>
                    {r.status === "failed" && (
                      <Button size="small" type="link" onClick={async () => {
                        await runsApi.rerun(r.id);
                        message.success("已重试");
                        mutate();
                      }}>重试</Button>
                    )}
                    <Popconfirm
                      title="删除该 Run?"
                      description={inFlight ? "该 Run 正在评测中,无法删除" : "删除后无法恢复"}
                      okText="删除"
                      okButtonProps={{ danger: true, disabled: inFlight }}
                      cancelText="取消"
                      onConfirm={() => handleDeleteOne(r.id)}
                    >
                      <Button
                        size="small"
                        type="link"
                        danger
                        disabled={inFlight}
                        icon={<DeleteOutlined />}
                      >
                        删除
                      </Button>
                    </Popconfirm>
                  </Space>
                );
              },
            },
          ]}
        />
      </Card>

      <CreateRunModal
        open={showCreate}
        onClose={() => { setShowCreate(false); mutate(); }}
        presetTcId={presetTcId}
        presetSkillHint={presetSkillHint}
      />
    </>
  );
}

// ------------------------- Create Run Modal -------------------------
function CreateRunModal({ open, onClose, presetTcId, presetSkillHint }:
  { open: boolean; onClose: () => void; presetTcId?: string; presetSkillHint?: string }
) {
  const [form] = Form.useForm();
  const navigate = useNavigate();
  const [mode, setMode] = useState<"single" | "batch">("single");
  const [tcId, setTcId] = useState<string | undefined>(presetTcId);
  const [routePreview, setRoutePreview] = useState<RouteResponse | null>(null);
  const [skillStrategy, setSkillStrategy] = useState<"auto" | "manual">("auto");

  const { data: testcases } = useSWR(
    open ? "/api/testsets?page_size=200" : null,
    () => testsetsApi.list({ page: 1, page_size: 200 })
  );
  const { data: skills } = useSWR(open ? "/api/skills?family=self" : null,
    () => skillsApi.list("self"));

  const tcDetail = useSWR(tcId ? `/api/testsets/${tcId}` : null,
    () => testsetsApi.get(tcId!));

  useEffect(() => {
    if (open && presetTcId) setTcId(presetTcId);
    if (open && presetSkillHint) {
      form.setFieldValue("skill_id", presetSkillHint);
      setSkillStrategy("manual");
    }
  }, [open]);

  const previewRoute = async () => {
    if (!tcDetail.data) return;
    const r = await routeApi.preview(tcDetail.data.question, form.getFieldValue("judge_model"));
    setRoutePreview(r);
  };

  const submit = async () => {
    const v = await form.validateFields();
    if (mode === "single") {
      if (!tcId) { message.warning("请先选样本"); return; }
      const r = await runsApi.create({
        testcase_id: tcId,
        skill_id: skillStrategy === "manual" ? v.skill_id : undefined,
        judge_model: v.judge_model,
      });
      message.success(`已创建 Run ${r.id.slice(0, 8)} — 跳转查看进度`);
      onClose();
      navigate(`/runs/${r.id}`);
    } else {
      const ids = (testcases?.items || []).map((t) => t.id);
      const r = await runsApi.createBatch({
        testcase_ids: ids,
        skill_strategy: skillStrategy,
        skill_id: skillStrategy === "manual" ? v.skill_id : undefined,
        judge_model: v.judge_model,
        label: v.label,
      });
      message.success(`已创建批次 ${r.id.slice(0, 8)},共 ${r.total} 条`);
      onClose();
    }
  };

  return (
    <Modal
      title={
        <Space>
          <PlayCircleOutlined />
          新建评测
        </Space>
      }
      open={open}
      onCancel={onClose}
      onOk={submit}
      width={720}
      okText="开始评测"
    >
      <Radio.Group value={mode} onChange={(e) => setMode(e.target.value)}
        style={{ marginBottom: 16 }}>
        <Radio.Button value="single">单条</Radio.Button>
        <Radio.Button value="batch">批量(全部已加载样本)</Radio.Button>
      </Radio.Group>

      <Form form={form} layout="vertical">
        {mode === "single" && (
          <Form.Item label="选择测试样本" required>
            <Select
              showSearch
              filterOption={(input, opt) =>
                (opt?.label as string)?.toLowerCase().includes(input.toLowerCase())
              }
              placeholder="搜索样本"
              value={tcId}
              onChange={(v) => { setTcId(v); setRoutePreview(null); }}
              options={(testcases?.items || []).map((t) => ({
                value: t.id,
                label: `[${t.category_code}] ${t.question.slice(0, 60)}`,
              }))}
              style={{ width: "100%" }}
            />
          </Form.Item>
        )}

        <Form.Item label="Skill 选择策略">
          <Radio.Group value={skillStrategy} onChange={(e) => {
            setSkillStrategy(e.target.value);
            setRoutePreview(null);
          }}>
            <Radio.Button value="auto">🤖 智能路由(LLM 自动选 Skill)</Radio.Button>
            <Radio.Button value="manual">手动指定</Radio.Button>
          </Radio.Group>
        </Form.Item>

        {skillStrategy === "manual" && (
          <Form.Item name="skill_id" label="Skill" rules={[{ required: true }]}>
            <Select
              options={(skills || []).map((s) => ({
                value: s.id, label: `${s.code} · ${s.name_zh}`,
              }))}
            />
          </Form.Item>
        )}

        <Form.Item name="judge_model" label="Judge 模型">
          <ModelPicker style={{ width: "100%" }} />
        </Form.Item>

        {mode === "batch" && (
          <Form.Item name="label" label="批次标签">
            <Input placeholder="可选,如 'gpt-4o 全量基线 v1'" />
          </Form.Item>
        )}

        {mode === "single" && skillStrategy === "auto" && tcId && (
          <Card type="inner" size="small" title="🤖 路由预览" extra={
            <Button size="small" icon={<ThunderboltOutlined />} onClick={previewRoute}>
              {routePreview ? "重新预测" : "预测"}
            </Button>
          }>
            {routePreview ? (
              <div>
                <Space>
                  <Tag color="blue">{routePreview.skill_id}</Tag>
                  <span>{routePreview.predicted_skill}</span>
                  <Tag color="cyan">置信 {(routePreview.confidence * 100).toFixed(0)}%</Tag>
                  <Tag>{routePreview.stage_used}</Tag>
                  {routePreview.fallback && <Tag color="orange">fallback</Tag>}
                </Space>
                <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
                  {routePreview.reasoning}
                </div>
                {routePreview.alternatives.length > 0 && (
                  <div style={{ marginTop: 6, fontSize: 11, color: "#999" }}>
                    其他候选: {routePreview.alternatives.map((a) =>
                      `${a.skill_id} (${a.why})`).join(" / ")}
                  </div>
                )}
              </div>
            ) : <span style={{ color: "#999" }}>点击「预测」查看路由结果</span>}
          </Card>
        )}

        {mode === "batch" && (
          <Alert
            type="info"
            showIcon
            message={`将对当前列表加载到的 ${testcases?.items.length || 0} 条样本执行评测`}
            description="如需筛选请先到「测试集」页面缩小范围"
          />
        )}
      </Form>
    </Modal>
  );
}
