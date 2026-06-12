import { useParams, useNavigate } from "react-router-dom";
import {
  Card,
  Tabs,
  Tag,
  Space,
  Button,
  Descriptions,
  Table,
  Empty,
  Spin,
} from "antd";
import { ArrowLeftOutlined, FileTextOutlined } from "@ant-design/icons";
import useSWR from "swr";
import { skillsApi } from "../../api/skills";
import MarkdownView from "../../components/MarkdownView";

const REL_FILES = [
  { rel: "SKILL_zh.md", label: "SKILL_zh.md(协议主文档)" },
  { rel: "README.md", label: "README.md" },
  { rel: "references/rubric/_index.md", label: "rubric/_index.md" },
  { rel: "references/golden_cases/_index.md", label: "golden_cases/_index.md" },
  { rel: "references/root-cause/_index.md", label: "root-cause/_index.md" },
  { rel: "references/tool_list/_index.md", label: "tool_list/_index.md" },
  { rel: "references/output-schema_zh.md", label: "output-schema_zh.md" },
];

export default function SkillDetail() {
  const { family = "self", code = "01" } = useParams();
  const navigate = useNavigate();
  const skillId = `${family}/${code}`;
  const { data, isLoading } = useSWR(`/api/skills/${skillId}`, () => skillsApi.get(skillId));

  if (isLoading) return <Card loading />;
  if (!data) return <Card>未找到 Skill {skillId}</Card>;

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      <Card
        title={
          <Space>
            <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} />
            <Tag color="blue">{data.code}</Tag>
            <span>{data.name_zh}</span>
            <Tag>{data.schema_version}</Tag>
          </Space>
        }
      >
        <Descriptions size="small" column={2} bordered>
          <Descriptions.Item label="ID">{data.id}</Descriptions.Item>
          <Descriptions.Item label="Family">{data.family}</Descriptions.Item>
          <Descriptions.Item label="英文名">{data.name_en}</Descriptions.Item>
          <Descriptions.Item label="路径">
            <code style={{ fontSize: 11 }}>{data.path}</code>
          </Descriptions.Item>
          <Descriptions.Item label="维度数" span={2}>
            {data.dimensions?.count ?? "—"} 个维度
          </Descriptions.Item>
          <Descriptions.Item label="封顶数">{data.caps?.count ?? "—"} 条</Descriptions.Item>
          <Descriptions.Item label="根因 L1">{data.root_causes?.count ?? "—"} 个</Descriptions.Item>
          <Descriptions.Item label="一句话定位" span={2}>
            {data.one_liner}
          </Descriptions.Item>
          <Descriptions.Item label="描述" span={2}>
            {data.description}
          </Descriptions.Item>
        </Descriptions>
      </Card>

      <Card>
        <Tabs
          defaultActiveKey="overview"
          items={[
            {
              key: "overview",
              label: "维度",
              children: <DimensionList items={data.dimensions?.items || []} />,
            },
            {
              key: "caps",
              label: `封顶规则 (${data.caps?.count ?? 0})`,
              children: <CapList items={data.caps?.items || []} />,
            },
            {
              key: "root",
              label: `根因 L1 (${data.root_causes?.count ?? 0})`,
              children: <KvList items={data.root_causes?.items || []} />,
            },
            {
              key: "tools",
              label: `工具 (${data.tools?.count ?? 0})`,
              children: <KvList items={data.tools?.items || []} />,
            },
            {
              key: "files",
              label: "源文件",
              children: <SkillFiles skillId={data.id} />,
            },
          ]}
        />
      </Card>
    </Space>
  );
}

function DimensionList({ items }: { items: any[] }) {
  if (!items.length) return <Empty />;
  return (
    <Table
      dataSource={items}
      rowKey={(r) => r.key || r.label}
      size="small"
      pagination={false}
      columns={[
        { title: "Key", dataIndex: "key", render: (v: string) => v && <code>{v}</code> },
        { title: "Label", dataIndex: "label", ellipsis: true },
      ]}
    />
  );
}

function CapList({ items }: { items: any[] }) {
  if (!items.length) return <Empty />;
  return (
    <Table
      dataSource={items}
      rowKey="key"
      size="small"
      pagination={false}
      columns={[
        { title: "Rule", dataIndex: "key", render: (v: string) => <code>{v}</code> },
        { title: "Label", dataIndex: "label" },
        {
          title: "Ceiling", dataIndex: "ceiling", width: 90,
          render: (v: number) => v != null ? <Tag color="red">▼{v}</Tag> : "—",
        },
      ]}
    />
  );
}

function KvList({ items }: { items: any[] }) {
  if (!items.length) return <Empty />;
  return (
    <Table
      dataSource={items}
      rowKey={(r, i) => r.key || r.label || String(i)}
      size="small"
      pagination={false}
      columns={[
        { title: "Key", dataIndex: "key", render: (v: string) => v ? <code>{v}</code> : "" },
        { title: "Label", dataIndex: "label" },
      ]}
    />
  );
}

function SkillFiles({ skillId }: { skillId: string }) {
  return (
    <Tabs
      type="card"
      size="small"
      items={REL_FILES.map((f) => ({
        key: f.rel,
        label: <span><FileTextOutlined /> {f.label}</span>,
        children: <FileContent skillId={skillId} rel={f.rel} />,
      }))}
    />
  );
}

function FileContent({ skillId, rel }: { skillId: string; rel: string }) {
  const { data, isLoading, error } = useSWR(
    `/api/skills/${skillId}/file?rel=${rel}`,
    () => skillsApi.file(skillId, rel),
    { shouldRetryOnError: false }
  );
  if (isLoading) return <Spin />;
  if (error) return <Empty description={`${rel} 不存在`} />;
  return <MarkdownView text={data?.content || ""} highlightRefs={false} />;
}
