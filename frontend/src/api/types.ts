// Shared TypeScript types mirroring backend Pydantic schemas.

export type SkillFamily = "self" | "competitor" | "e2e";

export interface SkillBrief {
  id: string;
  family: SkillFamily;
  code: string;
  name_zh: string;
  name_en: string;
  schema_version: string;
  one_liner?: string;
  golden_case_count: number;
}

export interface SkillDetail extends SkillBrief {
  description?: string;
  path: string;
  dimensions?: { count: number; items: any[]; kind?: string } | null;
  caps?: { count: number; items: any[] } | null;
  root_causes?: { count: number; items: any[]; kind?: string } | null;
  tools?: { count: number; items: any[]; kind?: string } | null;
  updated_at: string;
}

export interface TestCategory {
  code: string;
  slug: string;
  name_zh: string;
  name_en: string;
  description?: string;
  mapped_skill_id?: string | null;
  is_custom: boolean;
}

export interface TestCaseBrief {
  id: string;
  source_id: string;
  category_code: string;
  question: string;
  language: string;
  has_charts: boolean;
  inferred_difficulty: string;
  tags?: string[] | null;
  imported_from: string;
  created_at: string;
}

export interface TestCaseDetail extends TestCaseBrief {
  source: string;
  agent_answer: string;
  reasoning_trace?: any[] | null;
  context_history?: any[] | null;
  tool_set?: string[] | null;
  file_path?: string | null;
  updated_at: string;
}

export interface RouteAlternative {
  skill: string;
  skill_id: string;
  why: string;
}

export interface RouteResponse {
  predicted_skill: string;
  skill_id: string;
  confidence: number;
  reasoning: string;
  alternatives: RouteAlternative[];
  stage_used: "keyword" | "llm" | "fallback" | "hint";
  fallback: boolean;
}

export interface RunBrief {
  id: string;
  batch_id?: string | null;
  testcase_id: string;
  skill_id: string;
  judge_model: string;
  judge_provider: string;
  status:
    | "pending"
    | "routing"
    | "running"
    | "scoring"
    | "done"
    | "failed"
    | "cancelled";
  progress_pct: number;
  current_step: string;
  final_score?: number | null;
  absolute_score_pre_cap?: number | null;
  latency_ms?: number | null;
  tokens_in?: number | null;
  tokens_out?: number | null;
  created_at: string;
  finished_at?: string | null;
  error_msg?: string | null;
}

export interface RunDetail extends RunBrief {
  routing?: any;
  raw_response?: any;
  weight_assignment?: Record<string, any> | null;
  dimension_scores?: Record<string, any> | null;
  caps?: any[] | null;
  root_causes?: any[] | null;
  narrative_review?: any | null;
  matched_golden_cases?: string[] | null;
  skipped_dimensions?: any[] | null;
}

export interface DashboardSummary {
  total_testcases: number;
  total_runs: number;
  avg_score?: number | null;
  pass_rate?: number | null;
  by_skill: Array<{ skill_id: string; name_zh: string; count: number; avg_score?: number | null }>;
  by_l1_root_cause: Array<{ l1: string; count: number }>;
  available_models: string[];
  available_providers: string[];
  last_24h_runs: number;
}

export interface TrendPoint {
  date: string;
  skill_id?: string | null;
  avg_score: number;
  count: number;
}

export interface TopFailureRow {
  run_id: string;
  testcase_id: string;
  question_preview: string;
  skill_id: string;
  final_score: number;
  caps_triggered: string[];
  top_root_cause?: string | null;
  created_at: string;
}

export interface SkillCoverageRow {
  skill_id: string;
  code: string;
  name_zh: string;
  avg_score?: number | null;
  count: number;
}

export interface ModelInfo {
  id: string;
  provider: string;
  label: string;
  context_window: number;
}

export interface AgentSessionBrief {
  id: string;
  title: string;
  model: string;
  created_at: string;
  updated_at: string;
}

export interface AgentMessage {
  id: string;
  session_id: string;
  role: "user" | "assistant" | "tool";
  content: string;
  sql_used?: string | null;
  chart_spec?: any;
  data_preview?: any[] | null;
  created_at: string;
}

export interface AgentSessionDetail extends AgentSessionBrief {
  messages: AgentMessage[];
}

export interface RunBatchOut {
  id: string;
  label: string;
  judge_model: string;
  judge_provider: string;
  total: number;
  done: number;
  failed: number;
  skill_strategy: string;
  created_at: string;
}
