import { useParams, Link, useNavigate } from "react-router-dom";
import {
  Card,
  Descriptions,
  Tag,
  Space,
  Button,
  Tabs,
  Popconfirm,
  message,
  Modal,
  Form,
  Input,
} from "antd";
import {
  ArrowLeftOutlined,
  PlayCircleOutlined,
  DeleteOutlined,
  EditOutlined,
} from "@ant-design/icons";
import { useState } from "react";
import useSWR from "swr";
import dayjs from "dayjs";

import { testsetsApi } from "../../api/testsets";
import MarkdownView from "../../components/MarkdownView";
import ChainViewer from "../../components/ChainViewer";

export default function TestSetDetail() {
  const { id = "" } = useParams();
  const navigate = useNavigate();
  const { data, isLoading, mutate } = useSWR(
    id ? `/api/testsets/${id}` : null,
    () => testsetsApi.get(id)
  );
  const [editing, setEditing] = useState(false);
  const [form] = Form.useForm();

  if (isLoading) return <Card loading />;
  if (!data) return <Card>未找到样本 {id}</Card>;

  return (
    <Space direction="vertical" size={16} style={{ width: "100%" }}>
      <Card
        title={
          <Space>
            <Button icon={<ArrowLeftOutlined />} onClick={() => navigate(-1)} />
            <Tag color="blue">{data.category_code}</Tag>
            <span>{data.question.slice(0, 80)}</span>
          </Space>
        }
        extra={
          <Space>
            <Button
              type="primary"
              icon={<PlayCircleOutlined />}
              onClick={() => navigate(`/runs?testcase_id=${data.id}`)}
            >评测</Button>
            <Button icon={<EditOutlined />} onClick={() => {
              form.setFieldsValue({
                question: data.question,
                agent_answer: data.agent_answer,
              });
              setEditing(true);
            }}>编辑</Button>
            <Popconfirm
              title="确定删除此样本?"
              onConfirm={async () => {
                await testsetsApi.remove(data.id);
                message.success("已删除");
                navigate("/testsets");
              }}
            >
              <Button danger icon={<DeleteOutlined />}>删除</Button>
            </Popconfirm>
          </Space>
        }
      >
        <Descriptions size="small" column={3} bordered>
          <Descriptions.Item label="source_id">{data.source_id}</Descriptions.Item>
          <Descriptions.Item label="来源">{data.source}</Descriptions.Item>
          <Descriptions.Item label="导入方式">{data.imported_from}</Descriptions.Item>
          <Descriptions.Item label="语言">{data.language}</Descriptions.Item>
          <Descriptions.Item label="难度">{data.inferred_difficulty}</Descriptions.Item>
          <Descriptions.Item label="包含图表">{data.has_charts ? "是" : "否"}</Descriptions.Item>
          <Descriptions.Item label="工具" span={2}>
            {(data.tool_set || []).map((t) => <Tag key={t}>{t}</Tag>)}
          </Descriptions.Item>
          <Descriptions.Item label="更新时间">
            {dayjs(data.updated_at).format("YYYY-MM-DD HH:mm")}
          </Descriptions.Item>
          {data.file_path && (
            <Descriptions.Item label="原始文件" span={3}>
              <code style={{ fontSize: 11 }}>{data.file_path}</code>
            </Descriptions.Item>
          )}
        </Descriptions>
      </Card>

      <Card>
        <Tabs
          defaultActiveKey="question"
          items={[
            {
              key: "question",
              label: "问题",
              children: (
                <Card type="inner" size="small">
                  <MarkdownView text={data.question} />
                </Card>
              ),
            },
            {
              key: "answer",
              label: "Agent 回答",
              children: (
                <Card type="inner" size="small">
                  <MarkdownView text={data.agent_answer} />
                </Card>
              ),
            },
            {
              key: "chain",
              label: `链路数据 (${data.reasoning_trace?.length || 0} 步)`,
              children: (
                <ChainViewer
                  chain={data.reasoning_trace as any[]}
                  context={data.context_history as any[]}
                />
              ),
            },
            {
              key: "raw",
              label: "原始 JSON",
              children: (
                <pre className="json-viewer">{JSON.stringify(data, null, 2)}</pre>
              ),
            },
          ]}
        />
      </Card>

      <Card title="历史评测">
        <Link to={`/runs?testcase_id=${data.id}`}>跳转到 Runs 页面查看 →</Link>
      </Card>

      <Modal
        title="编辑样本"
        open={editing}
        onCancel={() => setEditing(false)}
        onOk={async () => {
          const v = await form.validateFields();
          await testsetsApi.update(data.id, v);
          message.success("已保存");
          setEditing(false);
          mutate();
        }}
        width={720}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="question" label="问题" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 2, maxRows: 5 }} />
          </Form.Item>
          <Form.Item name="agent_answer" label="Agent 回答 (Markdown)" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 8, maxRows: 20 }} />
          </Form.Item>
        </Form>
      </Modal>
    </Space>
  );
}
