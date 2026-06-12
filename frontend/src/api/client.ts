import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";
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

// Augment Axios config with our custom flag. Components that don't want the
// global error toast (e.g. background polling) can pass `silent: true` per
// request.
declare module "axios" {
  export interface InternalAxiosRequestConfig {
    silent?: boolean;
  }
  export interface AxiosRequestConfig {
    silent?: boolean;
  }
}

http.interceptors.response.use(
  (resp) => resp,
  (err: AxiosError<any>) => {
    const detail =
      err.response?.data?.detail ||
      err.response?.data?.message ||
      err.message ||
      "请求失败";
    const silent = (err.config as InternalAxiosRequestConfig | undefined)?.silent;
    // Don't shout about cancelled / SSE-disconnect errors or opt-out calls.
    if (!silent && !axios.isCancel(err) && err.code !== "ERR_CANCELED") {
      message.error(typeof detail === "string" ? detail : JSON.stringify(detail));
    }
    return Promise.reject(err);
  }
);
