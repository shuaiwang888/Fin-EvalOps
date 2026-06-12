import { Layout, Menu, theme as antdTheme } from "antd";
import {
  DashboardOutlined,
  DatabaseOutlined,
  ExperimentOutlined,
  RobotOutlined,
  PlayCircleOutlined,
  DiffOutlined,
  EditOutlined,
  TagsOutlined,
} from "@ant-design/icons";
import { Link, Route, Routes, useLocation, Navigate } from "react-router-dom";

import Dashboard from "./pages/Dashboard";
import TestSets from "./pages/TestSets";
import TestSetDetail from "./pages/TestSets/Detail";
import Skills from "./pages/Skills";
import SkillDetail from "./pages/Skills/Detail";
import Runs from "./pages/Runs";
import RunDetail from "./pages/Runs/Detail";
import Agent from "./pages/Agent";
import Compare from "./pages/Compare";
import Annotations from "./pages/Annotations";
import Settings from "./pages/Settings";

const { Header, Sider, Content, Footer } = Layout;

const MENU = [
  { key: "/", icon: <DashboardOutlined />, label: <Link to="/">评测首页</Link> },
  { key: "/testsets", icon: <DatabaseOutlined />, label: <Link to="/testsets">测试集</Link> },
  { key: "/skills", icon: <ExperimentOutlined />, label: <Link to="/skills">Skill 管理</Link> },
  { key: "/runs", icon: <PlayCircleOutlined />, label: <Link to="/runs">评测 Runs</Link> },
  { key: "/agent", icon: <RobotOutlined />, label: <Link to="/agent">Data Agent</Link> },
  { key: "/compare", icon: <DiffOutlined />, label: <Link to="/compare">对比</Link> },
  { key: "/annotations", icon: <TagsOutlined />, label: <Link to="/annotations">人工标注</Link> },
  { key: "/settings", icon: <EditOutlined />, label: <Link to="/settings">设置</Link> },
];

export default function App() {
  const { pathname } = useLocation();
  const { token } = antdTheme.useToken();
  // pick top-level segment so /runs/:id still highlights "评测 Runs"
  const top = "/" + (pathname.split("/")[1] || "");
  const selected = MENU.find((m) => m.key === top)?.key || "/";

  return (
    <Layout style={{ minHeight: "100vh" }}>
      <Header
        style={{
          display: "flex",
          alignItems: "center",
          padding: "0 24px",
          color: "#fff",
        }}
      >
        <div style={{ fontWeight: 600, fontSize: 18, letterSpacing: 1 }}>
          🪙 Fin-EvalOps · 金融 Agent 评测运维
        </div>
        <div style={{ flex: 1 }} />
        <div style={{ fontSize: 12, opacity: 0.8 }}>
          v0.1.0
        </div>
      </Header>
      <Layout>
        <Sider width={180} style={{ background: token.colorBgContainer }}>
          <Menu
            mode="inline"
            selectedKeys={[selected]}
            items={MENU}
            style={{ height: "100%", borderRight: 0, paddingTop: 8 }}
          />
        </Sider>
        <Layout style={{ padding: "16px" }}>
          <Content
            style={{
              padding: 16,
              background: token.colorBgContainer,
              borderRadius: token.borderRadius,
              minHeight: "calc(100vh - 56px - 60px - 32px)",
            }}
          >
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
          </Content>
          <Footer style={{ textAlign: "center", padding: 12, fontSize: 12 }}>
            Fin-EvalOps © 2026 · 13 类自研评测 Skill × 多模型 Judge × 实时 SSE
          </Footer>
        </Layout>
      </Layout>
    </Layout>
  );
}
