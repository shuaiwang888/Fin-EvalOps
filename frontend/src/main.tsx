import React from "react";
import ReactDOM from "react-dom/client";
import { ConfigProvider } from "antd";
import zhCN from "antd/locale/zh_CN";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import { finTheme } from "./theme";
import "antd/dist/reset.css";
import "./global.css";

const base = (import.meta.env.VITE_BASE_PATH || "/").replace(/\/+$/, "") || "/";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ConfigProvider locale={zhCN} theme={finTheme}>
      <BrowserRouter basename={base === "/" ? undefined : base}>
        <App />
      </BrowserRouter>
    </ConfigProvider>
  </React.StrictMode>
);
