import { useEffect, useRef, useState } from "react";
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
} from "antd";
import {
  SendOutlined,
  PlusOutlined,
  DeleteOutlined,
  RobotOutlined,
  UserOutlined,
  DatabaseOutlined,
  BarChartOutlined,
} from "@ant-design/icons";
import useSWR from "swr";
import ReactECharts from "echarts-for-react";
import dayjs from "dayjs";

import { agentApi } from "../../api/agent";
import ModelPicker from "../../components/ModelPicker";
import MarkdownView from "../../components/MarkdownView";
import type { AgentMessage } from "../../api/types";

const SAMPLE_PROMPTS = [
  "13 个 Skill 的平均分排序",
  "最近 7 天哪个 Skill 评测次数最多?",
  "Top 3 失败根因 L1 是什么?",
  "DeepSeek 和 Claude 在 03-诊股查数 上的均分对比",
  "我有多少条 12 类样本?",
];

export default function Agent() {
  const [sid, setSid] = useState<string | null>(null);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [model, setModel] = useState<string | undefined>();
  const scrollRef = useRef<HTMLDivElement>(null);

  const { data: sessions, mutate: refreshSessions } = useSWR(
    "/api/agent/sessions",
    agentApi.listSessions
  );
  const { data: messages, mutate: refreshMessages } = useSWR(
    sid ? `/api/agent/sessions/${sid}/messages` : null,
    () => agentApi.listMessages(sid!)
  );

  useEffect(() => {
    if (!sid && sessions && sessions.length > 0) setSid(sessions[0].id);
  }, [sessions, sid]);

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
    if (!sid) {
      const s = await agentApi.createSession(model);
      refreshSessions();
      // Send directly using the freshly-created session id; avoids racing the
      // setSid state update + stale closure on `content`.
      setInput("");
      setSending(true);
      try {
        await agentApi.sendMessage(s.id, content, model);
        refreshSessions();
      } catch (err) {
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
      await agentApi.sendMessage(sid, content, model);
      refreshMessages();
      refreshSessions();
    } finally {
      setSending(false);
    }
  };

  return (
    <div style={{ display: "flex", gap: 16, height: "calc(100vh - 56px - 60px - 32px - 32px)" }}>
      <Card
        size="small"
        title="对话列表"
        style={{ width: 260 }}
        bodyStyle={{ padding: 0, overflow: "auto", flex: 1 }}
        extra={<Button size="small" type="primary" icon={<PlusOutlined />} onClick={newSession}>新建</Button>}
      >
        <List
          dataSource={sessions || []}
          locale={{ emptyText: "尚无对话,新建一个开始" }}
          renderItem={(s) => (
            <List.Item
              style={{
                padding: "8px 12px",
                cursor: "pointer",
                background: s.id === sid ? "#e6f4ff" : "transparent",
              }}
              onClick={() => setSid(s.id)}
              actions={[
                <Popconfirm
                  key="del"
                  title="删除此对话?"
                  onConfirm={async (e) => {
                    e?.stopPropagation();
                    await agentApi.deleteSession(s.id);
                    if (sid === s.id) setSid(null);
                    refreshSessions();
                    message.success("已删除");
                  }}
                >
                  <DeleteOutlined onClick={(e) => e.stopPropagation()} />
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
        bodyStyle={{ flex: 1, display: "flex", flexDirection: "column", padding: 0 }}
      >
        <div ref={scrollRef} style={{ flex: 1, overflowY: "auto", padding: 16 }}>
          {(!messages || messages.length === 0) ? (
            <Empty
              description={
                <Space direction="vertical">
                  <span>开始一段对话,例如:</span>
                  <Space wrap>
                    {SAMPLE_PROMPTS.map((p) => (
                      <Button key={p} size="small" onClick={() => send(p)}>{p}</Button>
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
            disabled={sending}
          />
          <Button
            type="primary"
            icon={<SendOutlined />}
            loading={sending}
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
