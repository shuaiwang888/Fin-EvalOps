import { http } from "./client";
import type {
  RouteResponse,
  RunBrief,
  RunDetail,
  RunBatchOut,
  ModelInfo,
} from "./types";

export const routeApi = {
  preview: (question: string, judge_model?: string, hint_skill?: string) =>
    http
      .post<RouteResponse>("/api/route", { question, judge_model, hint_skill })
      .then((r) => r.data),
};

export const modelsApi = {
  list: () =>
    http
      .get<{ models: ModelInfo[] }>("/api/models")
      .then((r) => r.data.models),
};

export type RunSortKey =
  | "created_at"
  | "finished_at"
  | "final_score"
  | "latency_ms"
  | "tokens_in"
  | "status"
  | "skill_id"
  | "judge_model";

export const runsApi = {
  list: (params: {
    status?: string;
    skill_id?: string;
    judge_model?: string;
    testcase_id?: string;
    batch_id?: string;
    sort?: RunSortKey;
    order?: "asc" | "desc";
    page?: number;
    page_size?: number;
  } = {}) =>
    http
      .get<{ total: number; page: number; page_size: number; items: RunBrief[] }>(
        "/api/runs",
        { params, silent: true }
      )
      .then((r) => r.data),
  get: (id: string) =>
    http
      .get<RunDetail>(`/api/runs/${id}`, { silent: true })
      .then((r) => r.data),
  create: (body: { testcase_id: string; skill_id?: string; judge_model?: string }) =>
    http.post<RunBrief>("/api/runs", body).then((r) => r.data),
  rerun: (id: string) =>
    http.post<RunBrief>(`/api/runs/${id}/rerun`).then((r) => r.data),
  createBatch: (body: {
    testcase_ids: string[];
    skill_strategy: "auto" | "manual";
    skill_id?: string;
    judge_model?: string;
    label?: string;
  }) => http.post<RunBatchOut>("/api/runs/batch", body).then((r) => r.data),
  listBatches: () =>
    http.get<RunBatchOut[]>("/api/runs/batches", { silent: true }).then((r) => r.data),
  /** Hard-delete a single Run (refuses if status is in-flight). */
  deleteRun: (id: string) =>
    http.delete<{ deleted: string }>(`/api/runs/${id}`).then((r) => r.data),
  /** Bulk-delete Runs. Returns {deleted, skipped_busy, skipped_missing}. */
  deleteRuns: (run_ids: string[]) =>
    http
      .post<{ deleted: string[]; skipped_busy: string[]; skipped_missing: string[] }>(
        "/api/runs/delete-batch",
        { run_ids }
      )
      .then((r) => r.data),
};
