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
  Popconfirm,
  Alert,
} from "antd";
import {
  UploadOutlined,
  PlusOutlined,
  CloudDownloadOutlined,
  ReloadOutlined,
  SyncOutlined,
  AppstoreOutlined,
  DeleteOutlined,
  TagsOutlined,
  PlayCircleOutlined,
} from "@ant-design/icons";
import { Link, useNavigate } from "react-router-dom";
import useSWR from "swr";
import dayjs from "dayjs";

import { testsetsApi } from "../../api/testsets";
import { modelsApi, runsApi } from "../../api/runs";
import type { TestCaseBrief, TestCategory } from "../../api/types";

const { Search } = Input;

const DIFFICULTY_COLOR: Record<string, string> = {
  simple: "green",
  medium: "blue",
  complex: "red",
};

// Build a short, slug-ish default code from a Chinese / mixed category name so
// the user only has to type the human label. Falls back to a hash if the name
// strips down to nothing (e.g. all-punctuation).
function suggestCode(name: string, existing: TestCategory[]): string {
  const base = (name || "batch")
    .toLowerCase()
    .replace(/[^a-z0-9一-鿿]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 24) || "batch";
  const codes = new Set(existing.map((c) => c.code));
  if (!codes.has(base)) return base;
  let n = 2;
  while (codes.has(`${base}-${n}`)) n += 1;
  return `${base}-${n}`;
}

export default function TestSets() {
  const navigate = useNavigate();
  const [filters, setFilters] = useState<{
    category?: string; language?: string; difficulty?: string; q?: string;
    page: number; page_size: number;
  }>({ page: 1, page_size: 20 });

  const { data: categories, mutate: mutateCategories } = useSWR(
    "/api/testsets/categories",
    testsetsApi.categories
  );
  const key = `/api/testsets?${JSON.stringify(filters)}`;
  const { data, isLoading, mutate } = useSWR(key, () => testsetsApi.list(filters));

  const [showCreate, setShowCreate] = useState(false);
  const [showImport, setShowImport] = useState(false);
  const [showIwencai, setShowIwencai] = useState(false);
  const [importCat, setImportCat] = useState<string | undefined>();
  // File staged inside the import modal — uploaded only when the user clicks
  // "开始导入". Decoupling selection from upload gives a clear two-step UX
  // and lets the user change the target category after picking a file.
  const [pendingFile, setPendingFile] = useState<File | null>(null);
  const [importing, setImporting] = useState(false);
  const [createForm] = Form.useForm();
  const [iwencaiForm] = Form.useForm();

  const resetImportModal = () => {
    setShowImport(false);
    setImportCat(undefined);
    setPendingFile(null);
    setImporting(false);
  };

  // -------- Batch evaluation --------
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [showBatchEval, setShowBatchEval] = useState(false);
  const [batchJudgeModel, setBatchJudgeModel] = useState<string | undefined>();
  const [batchLabel, setBatchLabel] = useState("");
  const [batchSubmitting, setBatchSubmitting] = useState(false);
  const { data: models } = useSWR("/api/models", () =>
    modelsApi.list()
  );

  const submitBatchEval = async () => {
    if (selectedRowKeys.length === 0) return;
    setBatchSubmitting(true);
    try {
      const r = await runsApi.createBatch({
        testcase_ids: selectedRowKeys.map(String),
        skill_strategy: "auto",
        judge_model: batchJudgeModel,
        label: batchLabel || `批量评测 ${selectedRowKeys.length} 条`,
      });
      message.success(
        `已创建批量评测 (batch=${r.id.slice(0, 8)}, ${selectedRowKeys.length} 条),3 路并发执行中`
      );
      setShowBatchEval(false);
      setSelectedRowKeys([]);
      setBatchJudgeModel(undefined);
      setBatchLabel("");
      navigate(`/runs?batch_id=${r.id}`);
    } catch {
      /* interceptor shows error */
    } finally {
      setBatchSubmitting(false);
    }
  };

  // Category management modal — can be opened in "manage" mode (list + delete)
  // or "create" mode (inline quick-create from a parent modal). `onCreated`
  // lets the parent auto-select the new category after success.
  const [catModal, setCatModal] = useState<
    | { mode: "manage" }
    | { mode: "create"; onCreated?: (cat: TestCategory) => void }
    | null
  >(null);
  const [catForm] = Form.useForm();

  const refreshAll = async () => {
    await mutateCategories();
    await mutate();
  };

  const treeData = [
    {
      title: "全部",
      key: "all",
      children: (categories || []).map((c) => ({
        title: c.is_custom ? `${c.code} · ${c.name_zh} 🏷️` : `${c.code} · ${c.name_zh}`,
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

  const categoryOptions = (categories || []).map((c) => ({
    value: c.code,
    label: c.is_custom ? `${c.code} · ${c.name_zh} 🏷️` : `${c.code} · ${c.name_zh}`,
  }));

  // Inline "+ 新建分类" trigger — opens the create modal and, on success,
  // hands the new category back to the caller so the surrounding Select can
  // auto-select it.
  const renderCategoryPicker = (
    value: string | undefined,
    onChange: (v: string | undefined) => void
  ) => (
    <Space.Compact style={{ width: "100%" }}>
      <Select
        placeholder="选择分类"
        value={value}
        allowClear
        showSearch
        optionFilterProp="label"
        style={{ width: "calc(100% - 110px)" }}
        options={categoryOptions}
        onChange={onChange}
      />
      <Button
        icon={<PlusOutlined />}
        onClick={() =>
          setCatModal({
            mode: "create",
            onCreated: (cat) => onChange(cat.code),
          })
        }
      >
        新建分类
      </Button>
    </Space.Compact>
  );

  return (
    <div className="split-workspace testsets-workspace">
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
          <Space wrap>
            <Tooltip title="扫描 数据测试集/ 目录,upsert 到数据库">
              <Button icon={<SyncOutlined />} onClick={handleScanDisk}>磁盘同步</Button>
            </Tooltip>
            <Tooltip title="创建 / 删除自定义业务分类">
              <Button icon={<AppstoreOutlined />} onClick={() => setCatModal({ mode: "manage" })}>
                分类管理
              </Button>
            </Tooltip>
            <Button icon={<CloudDownloadOutlined />} onClick={() => setShowIwencai(true)}>问财拉取</Button>
            <Button icon={<UploadOutlined />} onClick={() => setShowImport(true)}>导入 JSON</Button>
            <Button
              type={selectedRowKeys.length > 0 ? "primary" : "default"}
              icon={<PlayCircleOutlined />}
              disabled={selectedRowKeys.length === 0}
              onClick={() => setShowBatchEval(true)}
            >
              批量评测{selectedRowKeys.length > 0 ? ` (${selectedRowKeys.length})` : ""}
            </Button>
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
          rowSelection={{
            selectedRowKeys,
            onChange: (keys) => setSelectedRowKeys(keys),
            preserveSelectedRowKeys: true,
          }}
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
              width: 160,
              render: (v: string) => {
                const cat = (categories || []).find((c) => c.code === v);
                const isCustom = cat?.is_custom ?? false;
                return (
                  <Tooltip title={isCustom ? "自定义业务分类" : "系统内置分类"}>
                    <Tag color={isCustom ? "purple" : "blue"} style={{ maxWidth: 150, overflow: "hidden", textOverflow: "ellipsis" }}>
                      {isCustom && "🏷️ "}{v}
                    </Tag>
                  </Tooltip>
                );
              },
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
            {renderCategoryPicker(undefined, (v) =>
              createForm.setFieldValue("category_code", v)
            )}
          </Form.Item>
          <Form.Item name="question" label="问题" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 2, maxRows: 5 }} />
          </Form.Item>
          <Form.Item name="agent_answer" label="Agent 回答 (Markdown)" rules={[{ required: true }]}>
            <Input.TextArea autoSize={{ minRows: 6, maxRows: 16 }} />
          </Form.Item>
        </Form>
      </Modal>

      {/* JSON file import modal */}
      <Modal
        title="导入 JSON 文件"
        open={showImport}
        onCancel={resetImportModal}
        okText="开始导入"
        cancelText="取消"
        okButtonProps={{
          disabled: !importCat || !pendingFile,
          loading: importing,
        }}
        onOk={async () => {
          if (!importCat || !pendingFile) return;
          setImporting(true);
          try {
            const r = await testsetsApi.importFile(pendingFile, importCat);
            message.success(`已导入 ${r.inserted}/${r.total_in_file} 到分类 ${importCat}`);
            resetImportModal();
            mutate();
          } catch {
            /* axios interceptor already shows error */
          } finally {
            setImporting(false);
          }
        }}
      >
        <Form layout="vertical">
          <Form.Item label="目标分类" required>
            {renderCategoryPicker(importCat, setImportCat)}
          </Form.Item>
          <Form.Item label="JSON 文件" required>
            <Upload
              accept=".json"
              multiple={false}
              maxCount={1}
              showUploadList
              beforeUpload={(file) => {
                // Stage the file; actual upload happens on "开始导入".
                setPendingFile(file as File);
                return false;  // prevent antd's auto-upload
              }}
              onRemove={() => setPendingFile(null)}
              fileList={
                pendingFile
                  ? [{
                      uid: "0",
                      name: pendingFile.name,
                      status: "done",
                      size: pendingFile.size,
                    }]
                  : []
              }
            >
              <Button icon={<UploadOutlined />}>选择 .json(单条对象或数组)</Button>
            </Upload>
            {pendingFile && (
              <div style={{ fontSize: 12, color: "#666", marginTop: 6 }}>
                已选 {(pendingFile.size / 1024).toFixed(1)} KB ·
                点 <b>开始导入</b> 上传到分类 <b>{importCat || "(未选)"}</b>
              </div>
            )}
          </Form.Item>
          <div style={{ fontSize: 12, color: "#999", marginTop: 4 }}>
            支持原始测试集格式 (问题/答案/链路数据 中文字段) 或英文 schema。
            分类支持内置 13 类与用户自定义业务分类。
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
            {renderCategoryPicker(undefined, (val) =>
              iwencaiForm.setFieldValue("category_code", val)
            )}
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

      {/* Category management modal — reused for both manage-list and quick-create */}
      <Modal
        title={catModal?.mode === "manage" ? "分类管理" : "新建业务分类"}
        open={!!catModal}
        onCancel={() => {
          setCatModal(null);
          catForm.resetFields();
        }}
        footer={null}
        width={catModal?.mode === "manage" ? 720 : 520}
      >
        {catModal?.mode === "manage" ? (
          <ManageCategories
            categories={categories || []}
            onChanged={refreshAll}
            onCreateClick={() => setCatModal({ mode: "create" })}
          />
        ) : (
          <CategoryQuickCreate
            form={catForm}
            existing={categories || []}
            onCancel={() => {
              setCatModal(null);
              catForm.resetFields();
            }}
            onCreated={async (cat) => {
              await mutateCategories();
              if (catModal?.mode === "create") {
                catModal.onCreated?.(cat);
              }
              setCatModal(null);
              catForm.resetFields();
              message.success(`已创建分类 ${cat.code}`);
            }}
          />
        )}
      </Modal>

      {/* Batch evaluation modal — submits to /api/runs/batch which runs
          up to 3 evals concurrently. After submission, navigates to
          /runs?batch_id=... so the user can watch progress live. */}
      <Modal
        title={`批量评测 (${selectedRowKeys.length} 条)`}
        open={showBatchEval}
        onCancel={() => !batchSubmitting && setShowBatchEval(false)}
        okText="开始评测"
        cancelText="取消"
        confirmLoading={batchSubmitting}
        okButtonProps={{ disabled: (models?.length ?? 0) === 0 }}
        onOk={submitBatchEval}
      >
        <Form layout="vertical">
          {(models?.length ?? 0) === 0 && (
            <Alert
              type="warning"
              showIcon
              message="没有可用的判分模型"
              description="请先在后端配置至少一个 LLM Provider，再开始评测。"
              style={{ marginBottom: 16 }}
            />
          )}
          <Form.Item label="判分模型">
            <Select
              placeholder="默认使用 DEFAULT_JUDGE_MODEL"
              allowClear
              value={batchJudgeModel}
              onChange={setBatchJudgeModel}
              options={(models || []).map((m: any) => ({
                value: m.id,
                label: `${m.label} (${m.id})`,
              }))}
            />
          </Form.Item>
          <Form.Item label="批次备注(可选)">
            <Input
              placeholder={`默认: 批量评测 ${selectedRowKeys.length} 条`}
              value={batchLabel}
              onChange={(e) => setBatchLabel(e.target.value)}
            />
          </Form.Item>
          <div style={{ fontSize: 12, color: "#999", marginTop: -8 }}>
            评测将自动路由到最匹配的 Skill,3 路并发执行。
            创建后可到 <code>Runs</code> 页查看实时进度。
          </div>
        </Form>
      </Modal>
    </div>
  );
}

// ---------------------------------------------------------------------------
// Sub-components
// ---------------------------------------------------------------------------

function CategoryQuickCreate(props: {
  form: any;
  existing: TestCategory[];
  onCancel: () => void;
  onCreated: (cat: TestCategory) => void;
}) {
  const [submitting, setSubmitting] = useState(false);
  return (
    <Form
      form={props.form}
      layout="vertical"
      onFinish={async (values: any) => {
        setSubmitting(true);
        try {
          const cat = await testsetsApi.createCategory({
            code: values.code,
            name_zh: values.name_zh,
            description: values.description,
          });
          props.onCreated(cat);
        } catch {
          /* axios interceptor shows the error */
        } finally {
          setSubmitting(false);
        }
      }}
    >
      <Form.Item
        name="name_zh"
        label="分类名称"
        rules={[{ required: true, message: "请输入分类名称" }]}
      >
        <Input
          placeholder="例如:2025Q3 回归批次"
          onChange={(e) => {
            // Auto-suggest a code only if the user hasn't manually edited it yet.
            const touched = props.form.isFieldTouched("code");
            if (!touched) {
              props.form.setFieldValue(
                "code",
                suggestCode(e.target.value, props.existing)
              );
            }
          }}
        />
      </Form.Item>
      <Form.Item
        name="code"
        label="分类编码"
        extra="1-32 字符,允许中文/字母/数字/-/_,后续作为导入/查询的标识,确定后不可修改"
        rules={[
          { required: true, message: "请输入分类编码" },
          { pattern: /^[\w一-鿿-]+$/u, message: "仅允许中英文字母、数字、下划线、连字符" },
          { max: 32, message: "不可超过 32 字符" },
        ]}
      >
        <Input placeholder="例如:2025q3-batch" />
      </Form.Item>
      <Form.Item name="description" label="备注(可选)">
        <Input.TextArea autoSize={{ minRows: 2, maxRows: 4 }} />
      </Form.Item>
      <Form.Item style={{ marginBottom: 0, textAlign: "right" }}>
        <Space>
          <Button onClick={props.onCancel}>取消</Button>
          <Button type="primary" htmlType="submit" loading={submitting}>创建</Button>
        </Space>
      </Form.Item>
    </Form>
  );
}

function ManageCategories(props: {
  categories: TestCategory[];
  onChanged: () => Promise<void> | void;
  onCreateClick: () => void;
}) {
  const [deleting, setDeleting] = useState<string | null>(null);
  const custom = props.categories.filter((c) => c.is_custom);
  const system = props.categories.filter((c) => !c.is_custom);
  return (
    <div>
      <Space style={{ marginBottom: 12 }}>
        <Button type="primary" icon={<PlusOutlined />} onClick={props.onCreateClick}>
          新建业务分类
        </Button>
        <span style={{ color: "#999", fontSize: 12 }}>
          自定义分类用于按批次/版本/客户隔离评测数据;系统分类不可删除。
        </span>
      </Space>
      <Table<TestCategory>
        size="small"
        rowKey="code"
        pagination={false}
        dataSource={[...custom, ...system]}
        columns={[
          {
            title: "分类",
            dataIndex: "name_zh",
            render: (v: string, row) => (
              <Space>
                {row.is_custom && <Tag color="purple">自定义</Tag>}
                {!row.is_custom && <Tag color="blue">系统</Tag>}
                <span>{v}</span>
              </Space>
            ),
          },
          { title: "编码", dataIndex: "code", width: 160 },
          { title: "slug", dataIndex: "slug", width: 200, render: (v: string) => <code>{v}</code> },
          {
            title: "描述",
            dataIndex: "description",
            ellipsis: true,
            render: (v: string) => v || "—",
          },
          {
            title: "操作",
            width: 100,
            render: (_: any, row) =>
              row.is_custom ? (
                <Popconfirm
                  title="删除该自定义分类?"
                  description="分类下若仍有测试样本则无法删除。"
                  okText="删除"
                  cancelText="取消"
                  okButtonProps={{ danger: true }}
                  onConfirm={async () => {
                    setDeleting(row.code);
                    try {
                      await testsetsApi.deleteCategory(row.code);
                      message.success(`已删除分类 ${row.code}`);
                      await props.onChanged();
                    } catch {
                      /* interceptor shows error */
                    } finally {
                      setDeleting(null);
                    }
                  }}
                >
                  <Button
                    size="small"
                    danger
                    icon={<DeleteOutlined />}
                    loading={deleting === row.code}
                  >
                    删除
                  </Button>
                </Popconfirm>
              ) : (
                <Tooltip title="系统内置分类不可删除">
                  <Button size="small" type="text" disabled icon={<TagsOutlined />}>
                    受保护
                  </Button>
                </Tooltip>
              ),
          },
        ]}
      />
    </div>
  );
}
