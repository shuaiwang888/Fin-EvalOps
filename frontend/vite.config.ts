import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "node:path";

// Vite config — only env vars with VITE_ prefix are bundled,
// preventing accidental leakage of backend secrets.
// Base path is set for GitHub Pages sub-path deployment.
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "VITE_");
  return {
    plugins: [react()],
    envPrefix: "VITE_",
    base: env.VITE_BASE_PATH || "/",
    resolve: {
      alias: { "@": path.resolve(__dirname, "src") },
    },
    server: {
      port: 5173,
      proxy: {
        "/api": {
          target: env.VITE_API_BASE || "http://localhost:8000",
          changeOrigin: true,
        },
      },
    },
    build: {
      outDir: "dist",
      sourcemap: false,
      chunkSizeWarningLimit: 1200,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ["react", "react-dom", "react-router-dom"],
            antd: ["antd", "@ant-design/icons"],
            charts: ["echarts", "echarts-for-react"],
          },
        },
      },
    },
  };
});
