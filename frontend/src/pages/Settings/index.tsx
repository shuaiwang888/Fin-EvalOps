import { Card, Descriptions, Tag, Space, Alert, Button } from "antd";
import useSWR from "swr";
import { http } from "../../api/client";
import { skillsApi } from "../../api/skills";
import { modelsApi } from "../../api/runs";

// Read-only diagnostics + future Skill editor placeholder.
export default function Settings() {
  const { data: health } = useSWR("/api/health", () =>
    http.get("/api/health").then((r) => r.data)
  );
  const { data: skills, mutate } = useSWR("/api/skills", () => skillsApi.list());
  const { data: models } = useSWR("/api/models", () => modelsApi.list());

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      <Card title="后端健康">
        <Descriptions bordered size="small" column={2}>
          <Descriptions.Item label="状态">
            <Tag color="green">{health?.status ?? "—"}</Tag>
          </Descriptions.Item>
          <Descriptions.Item label="版本">{health?.version ?? "—"}</Descriptions.Item>
          <Descriptions.Item label="DB">{health?.db ?? "—"}</Descriptions.Item>
          <Descriptions.Item label="LLM Providers">
            <Space>
              {(health?.providers || []).map((p: string) => (
                <Tag key={p} color="cyan">{p}</Tag>
              ))}
            </Space>
          </Descriptions.Item>
        </Descriptions>
      </Card>

      <Card title={`可用模型 (${models?.length ?? 0})`}>
        <Space wrap>
          {(models || []).map((m) => (
            <Tag key={m.id} color="blue">
              {m.label} · {m.provider} · ctx={m.context_window.toLocaleString()}
            </Tag>
          ))}
          {(models?.length ?? 0) === 0 && (
            <Alert
              type="warning"
              showIcon
              style={{ width: "100%" }}
              message="未配置任何 LLM Provider"
              description="请在 HF Space → Settings → Variables and secrets 中设置 ANTHROPIC_API_KEY / OPENAI_API_KEY / DASHSCOPE_API_KEY / DEEPSEEK_API_KEY / MINIMAX_API_KEY 中至少一个。Secret 不会出现在 logs。"
            />
          )}
        </Space>
      </Card>

      <Card
        title={`Skill 目录 (${skills?.length ?? 0})`}
        extra={
          <Button type="primary" size="small" onClick={async () => {
            await skillsApi.reload();
            mutate();
          }}>重新扫描</Button>
        }
      >
        <Space wrap>
          {(skills || []).map((s) => (
            <Tag key={s.id} color={s.family === "self" ? "blue" : "default"}>
              {s.id} · {s.name_zh}
            </Tag>
          ))}
        </Space>
      </Card>

      <Alert
        type="info"
        showIcon
        message="Skill 编辑器 (P2)"
        description="后续可在此可视化调整 rubric 维度、动态权重、封顶规则,保存到 SkillOverride 表(不动文件)。"
      />
    </Space>
  );
}
