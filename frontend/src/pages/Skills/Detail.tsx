import { type ReactNode } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Card,
  Tabs,
  Tag,
  Space,
  Button,
  Descriptions,
  Empty,
  Spin,
  Alert,
} from "antd";
import {
  ArrowLeftOutlined,
  FileTextOutlined,
  BookOutlined,
  ProfileOutlined,
  ToolOutlined,
  CodeOutlined,
  BulbOutlined,
} from "@ant-design/icons";
import useSWR from "swr";
import { skillsApi } from "../../api/skills";
import MarkdownView from "../../components/MarkdownView";

// ---------------------------------------------------------------------------
// The 5 sections that compose a Skill protocol. Each section is rendered as
// a top-level tab; nested sub-tabs hold related files (cap_*.md, dim_*.md
// under rubric; L1/*.md under root-cause; tool/*.md under tool_list).
// ---------------------------------------------------------------------------
type SectionDef = {
  key: string;
  label: string;
  icon: ReactNode;
  /** main file shown first (under this tab) */
  primaryFile: string;
  /** optional sub-directory whose .md files become nested tabs */
  extraDir?: string;
  /** human-readable label for the extra-dir sub-tabs */
  extraLabel?: string;
};

const SECTIONS: SectionDef[] = [
  {
    key: "skill",
    label: "协议文档",
    icon: <BookOutlined />,
    primaryFile: "SKILL_zh.md",
  },
  {
    key: "rubric",
    label: "评分细则",
    icon: <ProfileOutlined />,
    primaryFile: "references/rubric/_index.md",
    extraDir: "references/rubric",
    extraLabel: "细则文件",
  },
  {
    key: "root_cause",
    label: "根因体系",
    icon: <BulbOutlined />,
    primaryFile: "references/root-cause/_index.md",
    extraDir: "references/root-cause",
    extraLabel: "L1 详情",
  },
  {
    key: "tools",
    label: "工具列表",
    icon: <ToolOutlined />,
    primaryFile: "references/tool_list/_index.md",
    extraDir: "references/tool_list",
    extraLabel: "工具详情",
  },
  {
    key: "schema",
    label: "输出契约",
    icon: <CodeOutlined />,
    primaryFile: "references/output-schema_zh.md",
  },
];

export default function SkillDetail() {
  const { family = "self", code = "01" } = useParams();
  const navigate = useNavigate();
  const skillId = `${family}/${code}`;
  const { data, isLoading } = useSWR(`/api/skills/${skillId}`, () =>
    skillsApi.get(skillId)
  );

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
          defaultActiveKey="skill"
          type="card"
          items={SECTIONS.map((s) => ({
            key: s.key,
            label: (
              <Space size={4}>
                {s.icon}
                {s.label}
              </Space>
            ),
            children: <SectionPanel skillId={data.id} section={s} />,
          }))}
        />
      </Card>
    </Space>
  );
}

// ---------------------------------------------------------------------------
// SectionPanel — primary file + nested sub-tabs for extra files
// ---------------------------------------------------------------------------
function SectionPanel({
  skillId,
  section,
}: {
  skillId: string;
  section: SectionDef;
}) {
  if (section.extraDir) {
    return (
      <Tabs
        type="line"
        size="small"
        items={[
          {
            key: "__primary__",
            label: (
              <Space size={4}>
                <FileTextOutlined />
                _index.md
              </Space>
            ),
            children: <FileContent skillId={skillId} rel={section.primaryFile} />,
          },
          {
            key: "__extra__",
            label: (
              <Space size={4}>
                <FileTextOutlined />
                {section.extraLabel}
              </Space>
            ),
            children: <ExtraDirTabs skillId={skillId} dir={section.extraDir} />,
          },
        ]}
      />
    );
  }
  return <FileContent skillId={skillId} rel={section.primaryFile} />;
}

// ---------------------------------------------------------------------------
// ExtraDirTabs — one sub-tab per .md file discovered in the directory
// ---------------------------------------------------------------------------
function ExtraDirTabs({
  skillId,
  dir,
}: {
  skillId: string;
  dir: string;
}) {
  const { data, isLoading, error } = useSWR(
    `/api/skills/${skillId}/tree?dir=${encodeURIComponent(dir)}`,
    () => skillsApi.tree(skillId, dir)
  );
  if (isLoading) return <Spin />;
  if (error) return <Alert type="error" message={`无法列出 ${dir}`} />;
  const files = (data?.files || []).filter((f) => f !== "_index.md");
  if (!files.length) return <Empty description="无文件" />;

  const items = files.map((rel) => ({
    key: rel,
    label: (
      <Space size={4}>
        <FileTextOutlined />
        {rel.split("/").pop()}
      </Space>
    ),
    children: <FileContent skillId={skillId} rel={rel} />,
  }));

  return <Tabs type="card" size="small" items={items} />;
}

// ---------------------------------------------------------------------------
// FileContent — load + render a single .md file
// ---------------------------------------------------------------------------
function FileContent({ skillId, rel }: { skillId: string; rel: string }) {
  const { data, isLoading, error } = useSWR(
    `/api/skills/${skillId}/file?rel=${rel}`,
    () => skillsApi.file(skillId, rel),
    { shouldRetryOnError: false }
  );
  if (isLoading) return <Spin />;
  if (error) return <Empty description={`${rel} 不存在`} />;
  if (!data?.content) return <Empty description={`${rel} 为空`} />;
  return (
    <div style={{ maxHeight: "70vh", overflow: "auto", paddingRight: 8 }}>
      <MarkdownView text={data.content} highlightRefs={false} />
    </div>
  );
}
