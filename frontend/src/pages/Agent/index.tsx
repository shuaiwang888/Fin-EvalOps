import { useEffect, useMemo, useRef, useState } from "react";
import {
  Card,
  Input,
  Button,
  List,
  Space,
  Tag,
  Avatar,
  Empty,
  Popconfirm,
  message,
  Alert,
  Select,
  Segmented,
  Typography,
} from "antd";
import {
  SendOutlined,
  PlusOutlined,
  DeleteOutlined,
  RobotOutlined,
  UserOutlined,
  DatabaseOutlined,
  BarChartOutlined,
  FolderOpenOutlined,
  FileSearchOutlined,
  GlobalOutlined,
} from "@ant-design/icons";
import useSWR from "swr";
import ReactECharts from "echarts-for-react";
import dayjs from "dayjs";
import { Link } from "react-router-dom";

import { agentApi } from "../../api/agent";
import { modelsApi } from "../../api/runs";
import { testsetsApi } from "../../api/testsets";
import ModelPicker from "../../components/ModelPicker";
import MarkdownView from "../../components/MarkdownView";
import type { AgentAnalysisContext, AgentMessage } from "../../api/types";

const { Text, Paragraph } = Typography;

type AnalysisScope = "all" | "category" | "testcase";

const SAMPLE_PROMPTS = [
  "13 个 Skill 的平均分排序",
  "最近 7 天哪个 Skill 评测次数最多?",
  "Top 3 失败根因 L1 是什么?",
  "DeepSeek 和 Claude 在 03-诊股查数 上的均分对比",
  "我有多少条 12 类样本?",
];

const CATEGORY_PROMPTS = [
  "总结这个分类的整体评测表现，并给出 Top 3 根因",
  "区分有效低分、真实 0 分和执行失败，并建议优先修复顺序",
  "找出这个分类最值得复盘的测试案例",
];

const TESTCASE_PROMPTS = [
  "总结这个测试案例，并给出主要失败归因和证据",
  "比较这个案例的历次评测结果，解释分数变化",
  "基于题目、回答和链路，给出可直接执行的改进方案",
];

export default function Agent() {
  const [sid, setSid] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [model, setModel] = useState<string | undefined>();
  const [scope, setScope] = useState<AnalysisScope>("all");
  const [categoryCode, setCategoryCode] = useState<string>();
  const [testcaseId, setTestcaseId] = useState<string>();
  const scrollRef = useRef<HTMLDivElement>(null);

  const { data: sessions, mutate: refreshSessions } = useSWR(
    "/api/agent/sessions",
    agentApi.listSessions
  );
  const activeSid = sid ?? sessions?.[0]?.id ?? null;
  const { data: availableModels } = useSWR("/api/models", modelsApi.list);
  const hasModel = (availableModels?.length ?? 0) > 0;
  const { data: categories } = useSWR(
    "/api/testsets/categories",
    testsetsApi.categories,
  );
  const { data: testcasePage, isLoading: loadingTestcases } = useSWR(
    scope === "testcase"
      ? `/api/testsets?agent=1&category=${categoryCode ?? ""}`
      : null,
    () => testsetsApi.list({ category: categoryCode, page: 1, page_size: 200 }),
  );
  const selectedCategory = categories?.find((item) => item.code === categoryCode);
  const selectedTestcase = testcasePage?.items.find((item) => item.id === testcaseId);
  const analysisContext = useMemo<AgentAnalysisContext | undefined>(() => {
    if (scope === "category" && categoryCode) {
      return { scope: "category", category_code: categoryCode };
    }
    if (scope === "testcase" && testcaseId) {
      return { scope: "testcase", testcase_id: testcaseId };
    }
    return undefined;
  }, [categoryCode, scope, testcaseId]);
  const contextReady = scope === "all" || Boolean(analysisContext);
  const promptOptions = scope === "category"
    ? CATEGORY_PROMPTS
    : scope === "testcase"
      ? TESTCASE_PROMPTS
      : SAMPLE_PROMPTS;
  const { data: messages, mutate: refreshMessages } = useSWR(
    activeSid ? `/api/agent/sessions/${activeSid}/messages` : null,
    () => agentApi.listMessages(activeSid!)
  );

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages?.length]);

  const newSession = async () => {
    const s = await agentApi.createSession(model);
    refreshSessions();
    setSid(s.id);
  };

  const send = async (text?: string) => {
    const content = (text ?? input).trim();
    if (!content) return;
    if (!activeSid) {
      const s = await agentApi.createSession(model);
      refreshSessions();
      // Send directly using the freshly-created session id; avoids racing the
      // setSid state update + stale closure on `content`.
      setInput("");
      setSending(true);
      try {
        await agentApi.sendMessage(s.id, content, model, analysisContext);
        refreshSessions();
      } catch {
        setInput(content);
        message.error("发送失败,请重试");
      } finally {
        setSending(false);
        // Refresh once so the new session appears selected
        setTimeout(() => setSid(s.id), 0);
      }
      return;
    }
    setInput("");
    setSending(true);
    try {
      await agentApi.sendMessage(activeSid, content, model, analysisContext);
      refreshMessages();
      refreshSessions();
    } catch {
      setInput(content);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="agent-workspace">
      <Card
        size="small"
        title="对话列表"
        className="agent-sessions"
        styles={{ body: { padding: 0, overflow: "auto", flex: 1 } }}
        extra={<Button size="small" type="primary" disabled={!hasModel} icon={<PlusOutlined />} onClick={newSession}>新建</Button>}
      >
        <List
          dataSource={sessions || []}
          locale={{ emptyText: "尚无对话,新建一个开始" }}
          renderItem={(s) => (
            <List.Item
              style={{
                padding: "8px 12px",
                cursor: "pointer",
                background: s.id === activeSid ? "rgba(0,113,227,.08)" : "transparent",
              }}
              onClick={() => setSid(s.id)}
              actions={[
                <Popconfirm
                  key="del"
                  title="删除此对话?"
                  onConfirm={async (e) => {
                    e?.stopPropagation();
                    await agentApi.deleteSession(s.id);
                    if (activeSid === s.id) {
                      setSid(sessions?.find((item) => item.id !== s.id)?.id ?? null);
                    }
                    refreshSessions();
                    message.success("已删除");
                  }}
                >
                  <Button
                    type="text"
                    size="small"
                    danger
                    aria-label={`删除对话 ${s.title || "新对话"}`}
                    icon={<DeleteOutlined />}
                    onClick={(e) => e.stopPropagation()}
                  />
                </Popconfirm>,
              ]}
            >
              <div style={{ flex: 1, overflow: "hidden" }}>
                <div style={{ fontSize: 13, fontWeight: 500, whiteSpace: "nowrap",
                  overflow: "hidden", textOverflow: "ellipsis" }}>
                  {s.title || "新对话"}
                </div>
                <div style={{ fontSize: 11, color: "#999" }}>
                  {dayjs(s.updated_at).format("MM-DD HH:mm")}
                  {s.model && <Tag style={{ marginLeft: 4, fontSize: 10 }}>{s.model}</Tag>}
                </div>
              </div>
            </List.Item>
          )}
        />
      </Card>

      <Card
        size="small"
        title={
          <Space>
            <RobotOutlined />
            Data Agent · 自然语言分析评测数据
          </Space>
        }
        extra={<ModelPicker value={model} onChange={setModel} allowClear />}
        style={{ flex: 1, display: "flex", flexDirection: "column" }}
        styles={{ body: { flex: 1, display: "flex", flexDirection: "column", padding: 0 } }}
      >
        {!hasModel && (
          <Alert
            type="warning"
            showIcon
            banner
            message="配置至少一个 LLM Provider 后即可开始数据分析"
          />
        )}
        <div className="agent-context-panel">
          <div className="agent-context-heading">
            <div>
              <Text strong>分析范围</Text>
              <Text type="secondary"> 选择全库、测试集分类或具体案例作为对话证据</Text>
            </div>
            <Segmented
              value={scope}
              onChange={(value) => {
                setScope(value as AnalysisScope);
                setTestcaseId(undefined);
              }}
              options={[
                { label: "全库", value: "all", icon: <GlobalOutlined /> },
                { label: "按分类", value: "category", icon: <FolderOpenOutlined /> },
                { label: "按案例", value: "testcase", icon: <FileSearchOutlined /> },
              ]}
            />
          </div>

          {scope !== "all" && (
            <div className="agent-context-selectors">
              <Select
                showSearch
                allowClear={scope === "testcase"}
                value={categoryCode}
                placeholder={scope === "category" ? "选择测试集分类" : "先按分类筛选（可选）"}
                optionFilterProp="label"
                onChange={(value) => {
                  setCategoryCode(value);
                  setTestcaseId(undefined);
                }}
                options={(categories || []).map((item) => ({
                  value: item.code,
                  label: `${item.code} · ${item.name_zh}`,
                }))}
              />
              {scope === "testcase" && (
                <Select
                  showSearch
                  value={testcaseId}
                  loading={loadingTestcases}
                  placeholder="搜索并选择测试案例"
                  optionFilterProp="label"
                  onChange={setTestcaseId}
                  options={(testcasePage?.items || []).map((item) => ({
                    value: item.id,
                    label: item.question,
                  }))}
                />
              )}
            </div>
          )}

          {scope === "category" && selectedCategory && (
            <div className="agent-context-summary">
              <Tag color="blue">分类 {selectedCategory.code}</Tag>
              <Text strong>{selectedCategory.name_zh}</Text>
              {selectedCategory.description && (
                <Text type="secondary">{selectedCategory.description}</Text>
              )}
            </div>
          )}
          {scope === "testcase" && selectedTestcase && (
            <div className="agent-context-summary">
              <Tag color="purple">案例</Tag>
              <Paragraph ellipsis={{ rows: 2 }} style={{ margin: 0, flex: 1 }}>
                {selectedTestcase.question}
              </Paragraph>
              <Link to={`/testsets/${selectedTestcase.id}`}>查看详情</Link>
            </div>
          )}
          {!contextReady && (
            <Text type="warning">
              {scope === "category" ? "请选择一个测试集分类" : "请选择一个测试案例"}
            </Text>
          )}
        </div>
        <div ref={scrollRef} style={{ flex: 1, overflowY: "auto", padding: 16 }}>
          {(!messages || messages.length === 0) ? (
            <Empty
              description={
                <Space direction="vertical">
                  <span>开始一段对话,例如:</span>
                  <Space wrap>
                    {promptOptions.map((p) => (
                      <Button key={p} size="small" disabled={!hasModel || !contextReady} onClick={() => send(p)}>{p}</Button>
                    ))}
                  </Space>
                </Space>
              }
            />
          ) : (
            (messages || []).map((m) => <MessageBubble key={m.id} m={m} />)
          )}
        </div>

        <div style={{ borderTop: "1px solid #f0f0f0", padding: 12, display: "flex", gap: 8 }}>
          <Input.TextArea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="问点什么…(回车发送,Shift+回车换行)"
            autoSize={{ minRows: 1, maxRows: 4 }}
            onPressEnter={(e) => {
              if (!e.shiftKey) {
                e.preventDefault();
                send();
              }
            }}
            disabled={sending || !hasModel || !contextReady}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            loading={sending}
            disabled={!hasModel || !contextReady}
            onClick={() => send()}
          >发送</Button>
        </div>
      </Card>
    </div>
  );
}

function MessageBubble({ m }: { m: AgentMessage }) {
  const isUser = m.role === "user";
  return (
    <div style={{
      display: "flex",
      flexDirection: isUser ? "row-reverse" : "row",
      marginBottom: 16,
      gap: 12,
    }}>
      <Avatar
        icon={isUser ? <UserOutlined /> : <RobotOutlined />}
        style={{ background: isUser ? "#0958d9" : "#722ed1" }}
      />
      <div style={{ maxWidth: "75%" }}>
        <div style={{
          background: isUser ? "#e6f4ff" : "#fafafa",
          padding: 10,
          borderRadius: 8,
          fontSize: 13,
        }}>
          <MarkdownView text={m.content || ""} highlightRefs={false} />
          {m.sql_used && (
            <div style={{ marginTop: 8 }}>
              <Tag color="purple" icon={<DatabaseOutlined />}>SQL</Tag>
              <pre style={{ marginTop: 4, fontSize: 11 }}>{m.sql_used}</pre>
            </div>
          )}
          {m.data_preview && m.data_preview.length > 0 && (
            <details style={{ marginTop: 8 }}>
              <summary style={{ fontSize: 12, color: "#666", cursor: "pointer" }}>
                数据预览 ({m.data_preview.length} 行)
              </summary>
              <pre style={{ fontSize: 11, marginTop: 4 }}>
                {JSON.stringify(m.data_preview.slice(0, 20), null, 2)}
              </pre>
            </details>
          )}
          {m.chart_spec && (
            <div style={{ marginTop: 8 }}>
              <Tag color="blue" icon={<BarChartOutlined />}>图表</Tag>
              <div style={{ height: 280, marginTop: 4 }}>
                <ReactECharts option={m.chart_spec} style={{ height: "100%" }} notMerge />
              </div>
            </div>
          )}
        </div>
        <div style={{ fontSize: 10, color: "#999", marginTop: 4,
          textAlign: isUser ? "right" : "left" }}>
          {dayjs(m.created_at).format("HH:mm")}
        </div>
      </div>
    </div>
  );
}
