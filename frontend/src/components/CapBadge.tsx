import { Tag, Tooltip } from "antd";
import type { CSSProperties } from "react";

interface Props {
  caps: Array<{
    rule_id: string;
    triggered: boolean;
    score_ceiling?: number;
    reason?: string;
    evidence?: any[];
  }> | null | undefined;
  inline?: boolean;
}

// Renders triggered caps as red tags + tooltip showing reason.
export default function CapBadge({ caps, inline = false }: Props) {
  const triggered = (caps || []).filter((c) => c?.triggered);
  if (!triggered.length) {
    return inline ? null : (
      <Tag color="green" style={{ marginInlineEnd: 0 }}>
        无封顶触发
      </Tag>
    );
  }
  const style: CSSProperties = inline
    ? { display: "inline-flex", gap: 4, flexWrap: "wrap" }
    : { display: "flex", gap: 4, flexWrap: "wrap" };
  return (
    <div style={style}>
      {triggered.map((c) => (
        <Tooltip
          key={c.rule_id}
          title={
            <div>
              <div><strong>规则:</strong> {c.rule_id}</div>
              {c.score_ceiling != null && (
                <div><strong>上限:</strong> {c.score_ceiling}</div>
              )}
              {c.reason && <div><strong>原因:</strong> {c.reason}</div>}
            </div>
          }
        >
          <Tag color="red">
            ▼{c.score_ceiling ?? "?"} · {c.rule_id.replace(/^cap_/, "")}
          </Tag>
        </Tooltip>
      ))}
    </div>
  );
}
