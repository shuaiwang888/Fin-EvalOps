import { lazy, Suspense, useMemo, useState } from "react";
import { Button, Drawer, Layout, Menu, Skeleton, Tooltip } from "antd";
import {
  AppstoreOutlined,
  BarChartOutlined,
  DatabaseOutlined,
  DiffOutlined,
  ExperimentOutlined,
  MenuOutlined,
  PlayCircleOutlined,
  RobotOutlined,
  SettingOutlined,
  TagsOutlined,
} from "@ant-design/icons";
import { Link, Navigate, Route, Routes, useLocation } from "react-router-dom";

import ErrorBoundary from "./components/ErrorBoundary";

const Dashboard = lazy(() => import("./pages/Dashboard"));
const TestSets = lazy(() => import("./pages/TestSets"));
const TestSetDetail = lazy(() => import("./pages/TestSets/Detail"));
const Skills = lazy(() => import("./pages/Skills"));
const SkillDetail = lazy(() => import("./pages/Skills/Detail"));
const Runs = lazy(() => import("./pages/Runs"));
const RunDetail = lazy(() => import("./pages/Runs/Detail"));
const Agent = lazy(() => import("./pages/Agent"));
const Compare = lazy(() => import("./pages/Compare"));
const Annotations = lazy(() => import("./pages/Annotations"));
const Settings = lazy(() => import("./pages/Settings"));

const { Header, Sider, Content } = Layout;

const NAV = [
  {
    type: "group" as const,
    label: "概览",
    children: [
      { key: "/", icon: <BarChartOutlined />, label: <Link to="/">评测概览</Link> },
    ],
  },
  {
    type: "group" as const,
    label: "评测工作台",
    children: [
      { key: "/testsets", icon: <DatabaseOutlined />, label: <Link to="/testsets">测试集</Link> },
      { key: "/skills", icon: <ExperimentOutlined />, label: <Link to="/skills">评测协议</Link> },
      { key: "/runs", icon: <PlayCircleOutlined />, label: <Link to="/runs">评测任务</Link> },
    ],
  },
  {
    type: "group" as const,
    label: "分析与治理",
    children: [
      { key: "/agent", icon: <RobotOutlined />, label: <Link to="/agent">数据助手</Link> },
      { key: "/compare", icon: <DiffOutlined />, label: <Link to="/compare">结果对比</Link> },
      { key: "/annotations", icon: <TagsOutlined />, label: <Link to="/annotations">人工复核</Link> },
      { key: "/settings", icon: <SettingOutlined />, label: <Link to="/settings">系统状态</Link> },
    ],
  },
];

const PAGE_META: Record<string, { title: string; description: string }> = {
  "/": { title: "评测概览", description: "质量、覆盖度与失败根因一屏掌握" },
  "/testsets": { title: "测试集", description: "管理金融问句、Agent 回答与完整链路" },
  "/skills": { title: "评测协议", description: "检查评分维度、封顶规则与根因体系" },
  "/runs": { title: "评测任务", description: "创建、跟踪并复盘每一次评测" },
  "/agent": { title: "数据助手", description: "用自然语言探索评测数据库" },
  "/compare": { title: "结果对比", description: "定位模型、协议与版本间的真实差异" },
  "/annotations": { title: "人工复核", description: "用人工判断校准 LLM Judge" },
  "/settings": { title: "系统状态", description: "确认后端、模型与协议目录是否就绪" },
};

function RouteFallback() {
  return (
    <div className="route-fallback" aria-label="页面加载中">
      <Skeleton active paragraph={{ rows: 8 }} />
    </div>
  );
}

export default function App() {
  const { pathname } = useLocation();
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const top = "/" + (pathname.split("/")[1] || "");
  const selected = top === "//" ? "/" : top;
  const meta = PAGE_META[selected] || PAGE_META["/"];
  const menu = useMemo(
    () => (
      <Menu
        mode="inline"
        selectedKeys={[selected]}
        items={NAV}
        onClick={() => setMobileNavOpen(false)}
        className="app-nav-menu"
      />
    ),
    [selected]
  );

  return (
    <Layout className="app-shell">
      <Header className="app-topbar">
        <div className="app-topbar-inner">
          <Button
            className="mobile-nav-trigger"
            type="text"
            icon={<MenuOutlined />}
            aria-label="打开导航"
            onClick={() => setMobileNavOpen(true)}
          />
          <Link to="/" className="brand" aria-label="Fin EvalOps 首页">
            <span className="brand-mark"><AppstoreOutlined /></span>
            <span className="brand-wordmark">Fin-EvalOps</span>
          </Link>
          <div className="topbar-divider" />
          <div className="page-context">
            <strong>{meta.title}</strong>
            <span>{meta.description}</span>
          </div>
          <div className="topbar-actions">
            <Tooltip title="金融 Agent 评测工作台">
              <span className="service-status"><i /> 工作台</span>
            </Tooltip>
          </div>
        </div>
      </Header>

      <Layout className="app-body">
        <Sider width={228} className="desktop-sidebar" theme="light">
          <nav aria-label="主导航">{menu}</nav>
          <div className="sidebar-footnote">
            <span>金融 Agent 质量工作台</span>
            <small>13 类协议 · 实时 Judge</small>
          </div>
        </Sider>

        <Drawer
          className="mobile-nav-drawer"
          title={<span className="drawer-title">Fin-EvalOps</span>}
          placement="left"
          width={292}
          open={mobileNavOpen}
          onClose={() => setMobileNavOpen(false)}
          styles={{ body: { padding: "8px 12px 20px" } }}
        >
          <nav aria-label="移动端主导航">{menu}</nav>
        </Drawer>

        <Content className="app-content">
          <main className="page-stage">
            <ErrorBoundary resetKey={pathname}>
              <Suspense fallback={<RouteFallback />}>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/testsets" element={<TestSets />} />
                  <Route path="/testsets/:id" element={<TestSetDetail />} />
                  <Route path="/skills" element={<Skills />} />
                  <Route path="/skills/:family/:code" element={<SkillDetail />} />
                  <Route path="/runs" element={<Runs />} />
                  <Route path="/runs/:id" element={<RunDetail />} />
                  <Route path="/agent" element={<Agent />} />
                  <Route path="/compare" element={<Compare />} />
                  <Route path="/annotations" element={<Annotations />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </Suspense>
            </ErrorBoundary>
          </main>
          <footer className="app-footer">Fin-EvalOps · 让每一次评测都有证据、可复现、能行动</footer>
        </Content>
      </Layout>
    </Layout>
  );
}
