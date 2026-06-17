import { http } from "./client";
import type { SkillBrief, SkillDetail, SkillFamily } from "./types";

export const skillsApi = {
  list: (family?: SkillFamily) =>
    http
      .get<SkillBrief[]>("/api/skills", { params: { family } })
      .then((r) => r.data),
  get: (id: string) =>
    http.get<SkillDetail>(`/api/skills/${id}`).then((r) => r.data),
  file: (id: string, rel: string) =>
    http
      .get<{ skill_id: string; rel: string; content: string }>(
        `/api/skills/${id}/file`,
        { params: { rel } }
      )
      .then((r) => r.data),
  tree: (id: string, dir: string) =>
    http
      .get<{ dir: string; files: string[] }>(
        `/api/skills/${id}/tree`,
        { params: { dir } }
      )
      .then((r) => r.data),
  reload: () =>
    http
      .post<{ self: number; competitor: number; e2e: number; total: number }>(
        "/api/skills/reload"
      )
      .then((r) => r.data),
};
