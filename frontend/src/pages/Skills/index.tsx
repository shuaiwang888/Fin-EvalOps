import { useState } from "react";
import {
  Tabs,
  Card,
  Row,
  Col,
  Tag,
  Empty,
  Statistic,
  Button,
  message,
  Tooltip,
  Space,
} from "antd";
import { ReloadOutlined, ExperimentOutlined } from "@ant-design/icons";
import { Link } from "react-router-dom";
import useSWR from "swr";
import { skillsApi } from "../../api/skills";
import type { SkillFamily, SkillBrief } from "../../api/types";

const FAMILY_LABEL: Record<SkillFamily, string> = {
  self: "自研评测",
  competitor: "竞品对比",
  e2e: "端到端",
};

const FAMILY_DESC: Record<SkillFamily, string> = {
  self: "13 个 Skill。输入用户问句+自研最终答案+完整链路,产出 5 步评测协议 JSON。MVP 已接入。",
  competitor: "14 个 Skill。同 case_id 配对自研与竞品记录,做链路 + 答案对比。二期接入。",
  e2e: "14 个 Skill。同 case_id 配对的最终答案对比(result-only),输出 verdict。二期接入。",
};

export default function Skills() {
  const [family, setFamily] = useState<SkillFamily>("self");
  const { data, isLoading, mutate } = useSWR(
    `/api/skills?family=${family}`,
    () => skillsApi.list(family)
  );

  const handleReload = async () => {
    const hide = message.loading("重新扫描 Skill 目录…", 0);
    try {
      const r = await skillsApi.reload();
      message.success(`同步完成:self=${r.self} competitor=${r.competitor} e2e=${r.e2e}`);
      mutate();
    } finally { hide(); }
  };

  return (
    <Tabs
      activeKey={family}
      onChange={(k) => setFamily(k as SkillFamily)}
      tabBarExtraContent={
        <Button icon={<ReloadOutlined />} onClick={handleReload}>
          重新加载
        </Button>
      }
      items={(["self", "competitor", "e2e"] as SkillFamily[]).map((f) => ({
        key: f,
        label: f === family ? `${FAMILY_LABEL[f]} (${data?.length ?? 0})` : FAMILY_LABEL[f],
        children: (
          <div>
            <div style={{ marginBottom: 16, color: "#666", fontSize: 13 }}>
              {FAMILY_DESC[f]}
            </div>
            <Row gutter={[16, 16]}>
              {isLoading && <Col span={24}><Card loading /></Col>}
              {!isLoading && (!data || data.length === 0) && (
                <Col span={24}>
                  <Empty
                    description={
                      f === "self"
                        ? "尚未发现 Skill。请检查 自研评测Skill/ 目录是否存在,然后点击右上「重新加载」"
                        : `${FAMILY_LABEL[f]} Skill 二期接入`
                    }
                  />
                </Col>
              )}
              {(data || []).map((s) => (
                <Col xs={24} md={12} xl={8} key={s.id}>
                  <SkillCard skill={s} />
                </Col>
              ))}
            </Row>
          </div>
        ),
      }))}
    />
  );
}

function SkillCard({ skill }: { skill: SkillBrief }) {
  return (
    <Card
      hoverable
      size="small"
      title={
        <Space>
          <Tag color="blue">{skill.code}</Tag>
          <Link to={`/skills/${skill.family}/${skill.code}`} style={{ fontSize: 14 }}>
            {skill.name_zh}
          </Link>
        </Space>
      }
      extra={
        <Tooltip title="去 Runs 创建评测">
          <Link to={`/runs?skill_hint=${encodeURIComponent(skill.id)}`}>
            <ExperimentOutlined />
          </Link>
        </Tooltip>
      }
    >
      <div style={{ minHeight: 60, fontSize: 12, color: "#666", marginBottom: 8 }}>
        {skill.one_liner || skill.name_en}
      </div>
      <Row gutter={8}>
        <Col span={8}>
          <Statistic
            title="维度"
            value={skill.golden_case_count || "—"}
            valueStyle={{ fontSize: 18 }}
          />
        </Col>
        <Col span={8}>
          <Statistic
            title="样本(数据测试集)"
            value="5"
            valueStyle={{ fontSize: 18, color: "#999" }}
          />
        </Col>
        <Col span={8}>
          <div style={{ fontSize: 11, color: "#999", marginTop: 4 }}>
            schema
          </div>
          <div style={{ fontSize: 11, color: "#0958d9", wordBreak: "break-all" }}>
            {skill.schema_version}
          </div>
        </Col>
      </Row>
    </Card>
  );
}
