import { http } from "./client";
import type {
  DashboardSummary,
  SkillCoverageRow,
  TopFailureRow,
  TrendPoint,
} from "./types";

export const dashboardApi = {
  summary: () =>
    http
      .get<DashboardSummary>("/api/dashboard/summary", { silent: true })
      .then((r) => r.data),
  trend: (days = 30, skill_id?: string) =>
    http
      .get<TrendPoint[]>("/api/dashboard/trend", {
        params: { days, skill_id },
        silent: true,
      })
      .then((r) => r.data),
  topFailures: (limit = 10) =>
    http
      .get<TopFailureRow[]>("/api/dashboard/top-failures", {
        params: { limit },
        silent: true,
      })
      .then((r) => r.data),
  skillCoverage: () =>
    http
      .get<SkillCoverageRow[]>("/api/dashboard/skill-coverage", { silent: true })
      .then((r) => r.data),
};
