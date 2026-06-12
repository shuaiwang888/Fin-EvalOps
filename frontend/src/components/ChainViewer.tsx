import { Collapse, Tag, Empty } from "antd";

interface ChainStep {
  plan: string;
  tools: Array<{ name: string; input: string; output: string }>;
}

interface Props {
  chain?: ChainStep[] | null;
  context?: any[] | null;
}

// Renders the reasoning trace (链路数据) as collapsible steps.
export default function ChainViewer({ chain, context }: Props) {
  if ((!chain || chain.length === 0) && (!context || context.length === 0)) {
    return <Empty description="无链路数据" image={Empty.PRESENTED_IMAGE_SIMPLE} />;
  }

  const items: any[] = [];
  if (context && context.length > 0) {
    items.push({
      key: "context",
      label: (
        <span>
          <Tag color="cyan">前序上下文</Tag>
          {context.length} 轮历史对话
        </span>
      ),
      children: (
        <div>
          {context.map((turn: any, i: number) => (
            <div key={i} style={{ marginBottom: 12, padding: 8, background: "#f5faff", borderRadius: 4 }}>
              <div style={{ marginBottom: 4 }}>
                <strong>Q{i + 1}:</strong> {turn.Q || turn.question || ""}
              </div>
              <div style={{ color: "#666" }}>
                <strong>A{i + 1}:</strong> {(turn.A || turn.answer || "").slice(0, 200)}
                {(turn.A || turn.answer || "").length > 200 ? "…" : ""}
              </div>
            </div>
          ))}
        </div>
      ),
    });
  }

  (chain || []).forEach((step, idx) => {
    items.push({
      key: String(idx),
      label: (
        <span>
          <Tag color="blue">步骤 {idx + 1}</Tag>
          {step.plan?.slice(0, 60) || "(无 plan)"}
          {step.plan?.length > 60 ? "…" : ""}
          <span style={{ marginLeft: 8, color: "#999", fontSize: 11 }}>
            {step.tools?.length || 0} 个工具调用
          </span>
        </span>
      ),
      children: (
        <div>
          {step.plan && (
            <div style={{ marginBottom: 8 }}>
              <strong>Plan:</strong> {step.plan}
            </div>
          )}
          {(step.tools || []).map((t, ti) => (
            <details
              key={ti}
              style={{ marginBottom: 8, border: "1px solid #e6e6e6", padding: 8, borderRadius: 4 }}
            >
              <summary>
                <Tag color="geekblue">{t.name || "tool"}</Tag>
                <span style={{ color: "#999", fontSize: 12 }}>
                  input {t.input?.length || 0}b · output {t.output?.length || 0}b
                </span>
              </summary>
              <div style={{ marginTop: 8 }}>
                <div style={{ fontSize: 11, color: "#999" }}>Input:</div>
                <pre style={{ marginTop: 4 }}>{t.input?.slice(0, 1500) || "—"}</pre>
                <div style={{ fontSize: 11, color: "#999" }}>Output:</div>
                <pre style={{ marginTop: 4 }}>{t.output?.slice(0, 1500) || "—"}</pre>
              </div>
            </details>
          ))}
        </div>
      ),
    });
  });

  return <Collapse items={items} size="small" />;
}
