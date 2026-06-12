import { useState } from "react";
import {
  Card,
  Table,
  Tag,
  Select,
  Input,
  Space,
  Button,
  Upload,
  Modal,
  Form,
  message,
  Tree,
  Tooltip,
} from "antd";
import {
  UploadOutlined,
  PlusOutlined,
  CloudDownloadOutlined,
  ReloadOutlined,
  SyncOutlined,
} from "@ant-design/icons";
import { Link, useNavigate } from "react-router-dom";
import useSWR from "swr";
import dayjs from "dayjs";

import { testsetsApi } from "../../api/testsets";
import type { TestCaseBrief } from "../../api/types";

const { Search } = Input;

const DIFFICULTY_COLOR: Record<string, string> = {
  simple: "green",
  medium: "blue",
  complex: "red",
};

export default function TestSets() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<{
    category?: string; language?: string; difficulty?: string; q?: string;
    page: number; page_size: number;
  }>({ page: 1, page_size: 20 });

  const { data: categories } = useSWR("/api/testsets/categories", testsetsApi.categories);
  const key = `/api/testsets?${JSON.stringify(filters)}`;
  const { data, isLoading, mutate } = useSWR(key, () => testsetsApi.list(filters));

  const [showCreate, setShowCreate] = useState(false);
  const [showImport, setShowImport] = useState(false);
  const [showIwencai, setShowIwencai] = useState(false);
  const [createForm] = Form.useForm();
  const [iwencaiForm] = Form.useForm();

  const treeData = [
    {
      title: "全部",
      key: "all",
      children: (categories || []).map((c) => ({
        title: `${c.code} · ${c.name_zh}`,
        key: c.code,
      })),
    },
  ];

  const handleScanDisk = async () => {
    const hide = message.loading("扫描磁盘并同步…", 0);
    try {
      const r = await testsetsApi.scanDisk();
      message.success(`扫描完成:新增 ${r.inserted},更新 ${r.updated},跳过 ${r.skipped}`);
      mutate();
    } finally { hide(); }
  };

  return (
    <div style={{ display: "flex", gap: 16 }}>
      <Card style={{ width: 240 }} size="small" title="分类">
        <Tree
          showLine
          defaultExpandAll
          treeData={treeData}
          onSelect={(keys) => {
            const k = keys[0] as string | undefined;
            setFilters((f) => ({ ...f, category: k === "all" ? undefined : k, page: 1 }));
          }}
          selectedKeys={[filters.category || "all"]}
        />
      </Card>

      <Card
        style={{ flex: 1 }}
        title={`测试样本(共 ${data?.total ?? 0} 条)`}
        extra={
          <Space>
            <Tooltip title="扫描 数据测试集/ 目录,upsert 到数据库">
              <Button icon={<SyncOutlined />} onClick={handleScanDisk}>磁盘同步</Button>
            </Tooltip>
            <Button icon={<CloudDownloadOutlined />} onClick={() => setShowIwencai(true)}>问财拉取</Button>
            <Button icon={<UploadOutlined />} onClick={() => setShowImport(true)}>导入 JSON</Button>
            <Button type="primary" icon={<PlusOutlined />} onClick={() => setShowCreate(true)}>新增</Button>
            <Button icon={<ReloadOutlined />} onClick={() => mutate()} />
          </Space>
        }
      >
        <Space style={{ marginBottom: 12 }} wrap>
          <Select
            placeholder="语言"
            allowClear
            style={{ width: 100 }}
            value={filters.language}
            onChange={(v) => setFilters((f) => ({ ...f, language: v, page: 1 }))}
            options={[
              { value: "zh", label: "中文" },
              { value: "en", label: "英文" },
              { value: "mixed", label: "混合" },
            ]}
          />
          <Select
            placeholder="难度"
            allowClear
            style={{ width: 120 }}
            value={filters.difficulty}
            onChange={(v) => setFilters((f) => ({ ...f, difficulty: v, page: 1 }))}
            options={[
              { value: "simple", label: "简单" },
              { value: "medium", label: "中等" },
              { value: "complex", label: "复杂" },
            ]}
          />
          <Search
            placeholder="问句关键字搜索"
            style={{ width: 280 }}
            allowClear
            onSearch={(v) => setFilters((f) => ({ ...f, q: v || undefined, page: 1 }))}
          />
        </Space>

        <Table<TestCaseBrief>
          loading={isLoading}
          dataSource={data?.items || []}
          rowKey="id"
          size="small"
          pagination={{
            current: filters.page,
            pageSize: filters.page_size,
            total: data?.total ?? 0,
            onChange: (page, page_size) => setFilters((f) => ({ ...f, page, page_size })),
            showSizeChanger: true,
          }}
          columns={[
            {
              title: "分类",
              dataIndex: "category_code",
              key: "category_code",
              width: 80,
              render: (v: string) => <Tag color="blue">{v}</Tag>,
            },
            {
              title: "问题",
              dataIndex: "question",
              key: "question",
              ellipsis: true,
              render: (v: string, row) => (
                <Link to={`/testsets/${row.id}`}>{v.slice(0, 120)}</Link>
              ),
            },
            {
              title: "语言",
              dataIndex: "language",
              key: "language",
              width: 80,
              render: (v: string) => v,
            },
            {
              title: "难度",
              dataIndex: "inferred_difficulty",
              key: "inferred_difficulty",
              width: 100,
              render: (v: string) => (
                <Tag color={DIFFICULTY_COLOR[v] || "default"}>{v}</Tag>
              ),
            },
            {
              title: "图表",
              dataIndex: "has_charts",
              key: "has_charts",
              width: 60,
              render: (v: boolean) => (v ? "📊" : ""),
            },
            {
              title: "来源",
              dataIndex: "imported_from",
              key: "imported_from",
              width: 90,
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
              width: 110,
              render: (_: any, row) => (
                <Space size={4}>
                  <Button size="small" type="link" onClick={() => navigate(`/testsets/${row.id}`)}>
                    详情
                  </Button>
                  <Button
                    size="small"
                    type="link"
                    onClick={() => navigate(`/runs?testcase_id=${row.id}`)}
                  >
                    评测
                  </Button>
                </Space>
              ),
            },
          ]}
        />
      </Card>

      {/* New testcase modal */}
      <Modal
        title="新增测试样本"
        open={showCreate}
        onCancel={() => setShowCreate(false)}
        onOk={async () => {
          const values = await createForm.validateFields();
          await testsetsApi.create(values);
          message.success("已新增");
          setShowCreate(false);
          createForm.resetFields();
          mutate();
        }}
        width={720}
      >
        <Form form={createForm} layout="vertical">
          <Form.Item name="category_code" label="分类" rules={[{ required: true }]}>
            <Select
              placeholder="选择 13 类分类"
              options={(categories || []).map((c) => ({ value: c.code, label: `${c.code} · ${c.name_zh}` }))}
            />
          </Form.Item>
          <Form.Item name="question" label="问题" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 2, maxRows: 5 }} />
          </Form.Item>
          <Form.Item name="expected_answer" label="期望答案 (Markdown)" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 6, maxRows: 16 }} />
          </Form.Item>
        </Form>
      </Modal>

      {/* JSON file import modal */}
      <Modal
        title="导入 JSON 文件"
        open={showImport}
        onCancel={() => setShowImport(false)}
        footer={null}
      >
        <Form layout="vertical">
          <Form.Item label="目标分类" required>
            <Select
              placeholder="选择分类"
              id="import-cat"
              options={(categories || []).map((c) => ({ value: c.code, label: `${c.code} · ${c.name_zh}` }))}
              onChange={(v) => ((window as any).__importCat = v)}
            />
          </Form.Item>
          <Upload
            accept=".json"
            beforeUpload={async (file) => {
              const cat = (window as any).__importCat;
              if (!cat) {
                message.warning("请先选择分类");
                return false;
              }
              try {
                const r = await testsetsApi.importFile(file as File, cat);
                message.success(`已导入 ${r.inserted}/${r.total_in_file}`);
                setShowImport(false);
                mutate();
              } catch {
                /* axios interceptor already shows error */
              }
              return false;
            }}
          >
            <Button icon={<UploadOutlined />}>选择 .json(单条对象或数组)</Button>
          </Upload>
          <div style={{ fontSize: 12, color: "#999", marginTop: 12 }}>
            支持原始测试集格式 (问题/答案/链路数据 中文字段) 或英文 schema。
          </div>
        </Form>
      </Modal>

      {/* iwencai modal */}
      <Modal
        title="从问财 EvalOps 后端拉取"
        open={showIwencai}
        onCancel={() => setShowIwencai(false)}
        onOk={async () => {
          const v = await iwencaiForm.validateFields();
          const record_ids = (v.record_ids as string).split(/[\s,;]+/).filter(Boolean);
          const r = await testsetsApi.importFromIwencai(record_ids, v.category_code);
          message.success(`已导入 ${r.imported} 条,失败 ${r.failed.length} 条`);
          setShowIwencai(false);
          iwencaiForm.resetFields();
          mutate();
        }}
        width={640}
      >
        <Form form={iwencaiForm} layout="vertical">
          <Form.Item name="category_code" label="目标分类" rules={[{ required: true }]}>
            <Select options={(categories || []).map((c) => ({ value: c.code, label: `${c.code} · ${c.name_zh}` }))} />
          </Form.Item>
          <Form.Item name="record_ids" label="record_id 列表(空格/逗号/换行分隔)" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 4, maxRows: 12 }}
              placeholder="iwencai:wencai:01-event-and-concept-stock-selection:debug_xxx" />
          </Form.Item>
          <div style={{ fontSize: 12, color: "#999" }}>
            后端通过环境变量 <code>IWENCAI_BASE_URL</code> 访问内网地址,前端不接触该 URL。
          </div>
        </Form>
      </Modal>
    </div>
  );
}
