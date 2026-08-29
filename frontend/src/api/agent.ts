import { http } from "./client";
import type {
  AgentAnalysisContext,
  AgentMessage,
  AgentSessionBrief,
  AgentSessionDetail,
} from "./types";

export const agentApi = {
  listSessions: () =>
    http.get<AgentSessionBrief[]>("/api/agent/sessions").then((r) => r.data),
  createSession: (model?: string) =>
    http
      .post<AgentSessionBrief>("/api/agent/sessions", null, {
        params: { model },
      })
      .then((r) => r.data),
  getSession: (id: string) =>
    http.get<AgentSessionDetail>(`/api/agent/sessions/${id}`).then((r) => r.data),
  deleteSession: (id: string) =>
    http.delete(`/api/agent/sessions/${id}`).then((r) => r.data),
  sendMessage: (
    id: string,
    content: string,
    model?: string,
    context?: AgentAnalysisContext,
  ) =>
    http
      .post<{
        answer: string;
        sql?: string | null;
        chart_spec?: any;
        data_preview?: any[];
        sql_error?: string;
        analysis_error?: string;
        row_count?: number;
      }>(`/api/agent/sessions/${id}/messages`, { content, model, context })
      .then((r) => r.data),
  listMessages: (id: string) =>
    http.get<AgentMessage[]>(`/api/agent/sessions/${id}/messages`).then((r) => r.data),
};
