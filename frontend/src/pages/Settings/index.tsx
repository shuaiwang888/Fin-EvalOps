import { useState, type ReactNode } from "react";
import {
  Alert,
  Badge,
  Button,
  Card,
  Col,
  Descriptions,
  Empty,
  Row,
  Space,
  Tag,
  Typography,
  message,
} from "antd";
import {
  ApiOutlined,
  CheckCircleFilled,
  CloudServerOutlined,
  DatabaseOutlined,
  ReloadOutlined,
  WarningFilled,
} from "@ant-design/icons";
import useSWR from "swr";

import { http } from "../../api/client";
import { modelsApi } from "../../api/runs";
import { skillsApi } from "../../api/skills";

interface Health {
  status: string;
  version: string;
  db: string;
  providers: string[];
}

interface PersistenceStatus {
  hf_configured: boolean;
  hf_namespace: string;
  hf_dataset_repo: string;
  hf_push_interval_seconds: number;
  dirty: boolean;
  local_db_bytes: number;
}

function StatusCard({
  title,
  value,
  detail,
  ready,
  icon,
}: {
  title: string;
  value: string;
  detail: string;
  ready: boolean;
  icon: ReactNode;
}) {
  return (
    <Card className="readiness-card">
      <div className="readiness-card-top">
        <span className="readiness-icon">{icon}</span>
        {ready ? <CheckCircleFilled className="ready" /> : <WarningFilled className="attention" />}
      </div>
      <Typography.Text type="secondary">{title}</Typography.Text>
      <Typography.Title level={4}>{value}</Typography.Title>
      <Typography.Text type="secondary">{detail}</Typography.Text>
    </Card>
  );
}

export default function Settings() {
  const [reloading, setReloading] = useState(false);
  const healthQuery = useSWR("/api/health", () =>
    http.get<Health>("/api/health", { silent: true }).then((response) => response.data)
  );
  const skillsQuery = useSWR("/api/skills", () => skillsApi.list());
  const modelsQuery = useSWR("/api/models", () => modelsApi.list());
  const persistenceQuery = useSWR("/api/admin/persistence", () =>
    http
      .get<PersistenceStatus>("/api/admin/persistence", { silent: true })
      .then((response) => response.data)
  );

  const health = healthQuery.data;
  const skills = skillsQuery.data || [];
  const models = modelsQuery.data || [];
  const persistence = persistenceQuery.data;
  const backendReady = health?.status === "ok" && !healthQuery.error;

  const reloadSkills = async () => {
    setReloading(true);
    try {
      const result = await skillsApi.reload();
      await skillsQuery.mutate();
      message.success("已同步 " + result.total + " 个评测协议");
    } finally {
      setReloading(false);
    }
  };

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      {!backendReady && !healthQuery.isLoading && (
        <Alert
          type="error"
          showIcon
          message="后端暂时无法连接"
          description="请确认 VITE_API_BASE、后端进程和跨域设置。页面会在连接恢复后自动重新验证。"
          action={<Button onClick={() => healthQuery.mutate()}>重试</Button>}
        />
      )}

      <Row gutter={[16, 16]}>
        <Col xs={24} sm={12} xl={6}>
          <StatusCard
            title="API 服务"
            value={backendReady ? "运行正常" : "等待连接"}
            detail={health?.version ? "Fin-EvalOps " + health.version : "尚未读取版本"}
            ready={backendReady}
            icon={<ApiOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} xl={6}>
          <StatusCard
            title="评测模型"
            value={models.length + " 个可用"}
            detail={models.length ? new Set(models.map((model) => model.provider)).size + " 个 Provider" : "需要配置 Provider 密钥"}
            ready={models.length > 0}
            icon={<CloudServerOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} xl={6}>
          <StatusCard
            title="评测协议"
            value={skills.length + " 个已加载"}
            detail={skills.filter((skill) => skill.family === "self").length + " 个自研协议"}
            ready={skills.length > 0}
            icon={<ReloadOutlined />}
          />
        </Col>
        <Col xs={24} sm={12} xl={6}>
          <StatusCard
            title="数据持久化"
            value={persistence?.hf_configured ? "云端快照" : "仅本地"}
            detail={persistence?.hf_configured ? (persistence.dirty ? "有变更等待同步" : "数据已同步") : "重启环境前请先备份"}
            ready={Boolean(persistence?.hf_configured)}
            icon={<DatabaseOutlined />}
          />
        </Col>
      </Row>

      <Card title="运行环境">
        <Descriptions bordered size="small" column={{ xs: 1, sm: 2 }}>
          <Descriptions.Item label="后端状态">
            <Badge status={backendReady ? "success" : "error"} text={health?.status || "未知"} />
          </Descriptions.Item>
          <Descriptions.Item label="数据库">{health?.db || "—"}</Descriptions.Item>
          <Descriptions.Item label="LLM Providers">
            <Space wrap>
              {(health?.providers || []).map((provider) => <Tag key={provider}>{provider}</Tag>)}
              {!health?.providers?.length && <Typography.Text type="secondary">未配置</Typography.Text>}
            </Space>
          </Descriptions.Item>
          <Descriptions.Item label="本地数据库">
            {persistence ? (persistence.local_db_bytes / 1024 / 1024).toFixed(2) + " MB" : "—"}
          </Descriptions.Item>
          {persistence?.hf_configured && (
            <>
              <Descriptions.Item label="HF Dataset">
                {persistence.hf_namespace}/{persistence.hf_dataset_repo}
              </Descriptions.Item>
              <Descriptions.Item label="自动同步间隔">
                {persistence.hf_push_interval_seconds} 秒
              </Descriptions.Item>
            </>
          )}
        </Descriptions>
      </Card>

      <Card title={"可用模型 (" + models.length + ")"}>
        {models.length ? (
          <div className="model-grid">
            {models.map((model) => (
              <div className="model-chip" key={model.id}>
                <strong>{model.label}</strong>
                <span>{model.provider} · {(model.context_window / 1000).toFixed(0)}K context</span>
              </div>
            ))}
          </div>
        ) : (
          <Empty
            image={Empty.PRESENTED_IMAGE_SIMPLE}
            description="未配置任何 LLM Provider；创建评测前需在后端环境变量中添加至少一个 API Key。"
          />
        )}
      </Card>

      <Card
        title={"协议目录 (" + skills.length + ")"}
        extra={
          <Button icon={<ReloadOutlined />} loading={reloading} onClick={reloadSkills}>
            重新扫描
          </Button>
        }
      >
        <Space wrap>
          {skills.map((skill) => (
            <Tag key={skill.id} color={skill.family === "self" ? "blue" : "default"}>
              {skill.id} · {skill.name_zh}
            </Tag>
          ))}
        </Space>
      </Card>
    </Space>
  );
}
