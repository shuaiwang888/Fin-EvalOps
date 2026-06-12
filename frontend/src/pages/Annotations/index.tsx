import { useState } from "react";
import {
  Card,
  Table,
  Tag,
  Space,
  Modal,
  Form,
  Input,
  Switch,
  Select,
  message,
  Alert,
} from "antd";
import { PlusOutlined, ReloadOutlined } from "@ant-design/icons";
import useSWR from "swr";
import dayjs from "dayjs";

import { http } from "../../api/client";

interface Annotation {
  id: string;
  run_id: string;
  reviewer: string;
  dim_overrides?: Record<string, number> | null;
  comment: string;
  is_golden: boolean;
  created_at: string;
}

// P1 — human review covering LLM-judged dimensions.
export default function Annotations() {
  const { data, mutate, isLoading } = useSWR("/api/annotations", () =>
    http.get<Annotation[]>("/api/annotations").then((r) => r.data)
  );
  const [open, setOpen] = useState(false);
  const [form] = Form.useForm();

  return (
    <>
      <Alert
        type="info"
        showIcon
        message="人工标注 (P1)"
        description="标注 LLM judge 的结果。可逐维度覆盖打分,标记 golden 后用于回归比对。"
        style={{ marginBottom: 12 }}
      />
      <Card
        title={`标注记录 (${data?.length ?? 0})`}
        extra={
          <Space>
            <a onClick={() => mutate()}><ReloadOutlined /></a>
            <a onClick={() => setOpen(true)}><PlusOutlined /> 新增</a>
          </Space>
        }
      >
        <Table<Annotation>
          loading={isLoading}
          dataSource={data || []}
          rowKey="id"
          size="small"
          columns={[
            {
              title: "Run",
              dataIndex: "run_id",
              key: "run_id",
              render: (v: string) => <a href={`/runs/${v}`}>{v.slice(0, 8)}</a>,
            },
            { title: "评审员", dataIndex: "reviewer", key: "reviewer" },
            {
              title: "维度覆盖",
              dataIndex: "dim_overrides",
              render: (v: Record<string, number> | null) => v ? (
                <Space wrap>
                  {Object.entries(v).map(([k, n]) => (
                    <Tag key={k}>{k}: {n}</Tag>
                  ))}
                </Space>
              ) : "—",
            },
            { title: "评语", dataIndex: "comment", ellipsis: true },
            {
              title: "Golden",
              dataIndex: "is_golden",
              width: 80,
              render: (v: boolean) => v ? <Tag color="gold">⭐ Golden</Tag> : "",
            },
            {
              title: "时间",
              dataIndex: "created_at",
              width: 140,
              render: (v: string) => dayjs(v).format("MM-DD HH:mm"),
            },
          ]}
        />
      </Card>

      <Modal
        title="新增标注"
        open={open}
        onCancel={() => setOpen(false)}
        onOk={async () => {
          const v = await form.validateFields();
          let dim_overrides: Record<string, number> | undefined;
          if (v.dim_overrides_raw) {
            try {
              dim_overrides = JSON.parse(v.dim_overrides_raw);
            } catch {
              message.error("dim_overrides 必须是 JSON 对象");
              return;
            }
          }
          await http.post("/api/annotations", {
            run_id: v.run_id,
            reviewer: v.reviewer || "anonymous",
            comment: v.comment || "",
            is_golden: !!v.is_golden,
            dim_overrides,
          });
          message.success("已新增");
          setOpen(false);
          form.resetFields();
          mutate();
        }}
        width={600}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="run_id" label="Run ID" rules={[{ required: true }]}>
            <Input placeholder="完整 run id" />
          </Form.Item>
          <Form.Item name="reviewer" label="评审员">
            <Input placeholder="留空则 anonymous" />
          </Form.Item>
          <Form.Item name="comment" label="评语">
            <Input.TextArea autoSize={{ minRows: 2, maxRows: 6 }} />
          </Form.Item>
          <Form.Item name="dim_overrides_raw" label='维度覆盖 (JSON 格式,如 {"intent_fulfillment": 60})'>
            <Input.TextArea autoSize={{ minRows: 2, maxRows: 6 }} />
          </Form.Item>
          <Form.Item name="is_golden" valuePropName="checked" label="标为 Golden">
            <Switch />
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
}
