import { Select } from "antd";
import useSWR from "swr";
import { modelsApi } from "../api/runs";

interface Props {
  value?: string;
  onChange?: (v: string) => void;
  allowClear?: boolean;
  style?: React.CSSProperties;
  size?: "small" | "middle" | "large";
}

// Reusable dropdown showing only providers whose key is configured server-side.
export default function ModelPicker({ value, onChange, allowClear = false, style, size = "middle" }: Props) {
  const { data: models, isLoading } = useSWR("/api/models", () => modelsApi.list());
  return (
    <Select
      style={{ width: 240, ...style }}
      placeholder={isLoading ? "加载模型中..." : "选择 Judge 模型"}
      loading={isLoading}
      value={value}
      onChange={onChange}
      allowClear={allowClear}
      size={size}
      options={(models || []).map((m) => ({
        label: `${m.label} · ${m.provider}`,
        value: m.id,
      }))}
      notFoundContent={
        <div style={{ padding: 8, color: "#999" }}>
          没有可用模型。<br />
          请在后端环境变量中配置至少一个 API key。
        </div>
      }
    />
  );
}
