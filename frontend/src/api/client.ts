import axios, { AxiosError } from "axios";
import { message } from "antd";

// Base URL resolution:
// - dev: empty → Vite proxy forwards /api to localhost:8000
// - prod: VITE_API_BASE env at build time → fully-qualified backend URL
const baseURL = import.meta.env.VITE_API_BASE || "";

export const http = axios.create({
  baseURL,
  timeout: 60_000,
  headers: { "Content-Type": "application/json" },
});

http.interceptors.response.use(
  (resp) => resp,
  (err: AxiosError<any>) => {
    const detail =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      err.message ||
      "请求失败";
    // Don't shout about cancelled / SSE-disconnect errors
    if (!axios.isCancel(err) && err.code !== "ERR_CANCELED") {
      // global notice — components can still catch and override
      message.error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }
    return Promise.reject(err);
  }
);

export function asSWRFetcher<T = unknown>(): (url: string) => Promise<T> {
  return (url: string) => http.get<T>(url).then((r) => r.data);
}
