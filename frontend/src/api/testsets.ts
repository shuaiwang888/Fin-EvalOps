import { http } from "./client";
import type {
  TestCategory,
  TestCaseBrief,
  TestCaseDetail,
} from "./types";

export const testsetsApi = {
  categories: () =>
    http
      .get<TestCategory[]>("/api/testsets/categories")
      .then((r) => r.data),

  createCategory: (body: {
    code: string;
    name_zh: string;
    name_en?: string;
    description?: string;
    slug?: string;
  }) =>
    http
      .post<TestCategory>("/api/testsets/categories", body)
      .then((r) => r.data),

  deleteCategory: (code: string) =>
    http
      .delete<{ deleted: string }>(`/api/testsets/categories/${encodeURIComponent(code)}`)
      .then((r) => r.data),

  list: (params: {
    category?: string;
    language?: string;
    difficulty?: string;
    q?: string;
    page?: number;
    page_size?: number;
  } = {}) =>
    http
      .get<{
        total: number;
        page: number;
        page_size: number;
        items: TestCaseBrief[];
      }>("/api/testsets", { params, silent: true })
      .then((r) => r.data),

  get: (id: string) =>
    http.get<TestCaseDetail>(`/api/testsets/${id}`).then((r) => r.data),

  create: (body: any) =>
    http.post<TestCaseDetail>("/api/testsets", body).then((r) => r.data),

  update: (id: string, body: any) =>
    http.patch<TestCaseDetail>(`/api/testsets/${id}`, body).then((r) => r.data),

  remove: (id: string) =>
    http.delete<{ deleted: string }>(`/api/testsets/${id}`).then((r) => r.data),

  importFile: (file: File, category_code: string) => {
    const fd = new FormData();
    fd.append("file", file);
    return http
      .post(`/api/testsets/import-file?category_code=${category_code}`, fd, {
        headers: { "Content-Type": "multipart/form-data" },
      })
      .then((r) => r.data);
  },

  importFromIwencai: (record_ids: string[], category_code: string) =>
    http
      .post<{ imported: number; failed: { record_id: string; error: string }[] }>(
        "/api/testsets/import-from-iwencai",
        { record_ids, category_code }
      )
      .then((r) => r.data),

  scanDisk: () =>
    http
      .post<{ scanned: number; inserted: number; updated: number; skipped: number }>(
        "/api/testsets/scan-disk"
      )
      .then((r) => r.data),
};
