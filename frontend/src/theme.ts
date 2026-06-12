import { theme } from "antd";
import type { ThemeConfig } from "antd";

// Financial blue brand. Uses AntD compactAlgorithm for higher data density
// suitable for an ops dashboard.
export const finTheme: ThemeConfig = {
  token: {
    colorPrimary: "#0958d9",
    colorInfo: "#0958d9",
    colorSuccess: "#52c41a",
    colorWarning: "#faad14",
    colorError: "#ff4d4f",
    borderRadius: 6,
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
  },
  algorithm: [theme.defaultAlgorithm, theme.compactAlgorithm],
  components: {
    Layout: {
      headerBg: "#001d66",
      headerColor: "#ffffff",
      headerHeight: 56,
      siderBg: "#f0f5ff",
      bodyBg: "#fafafa",
    },
    Menu: {
      itemSelectedBg: "#bae0ff",
      itemSelectedColor: "#0958d9",
    },
    Table: {
      headerBg: "#f5f5f5",
      cellPaddingBlock: 8,
    },
    Card: {
      paddingLG: 16,
    },
  },
};

// Stage colors used in run-detail timeline + radar
export const PALETTE = [
  "#0958d9",
  "#13c2c2",
  "#722ed1",
  "#fa8c16",
  "#52c41a",
  "#eb2f96",
  "#fadb14",
  "#1677ff",
  "#a0d911",
  "#f5222d",
  "#9254de",
  "#08979c",
  "#d4b106",
];

export const SCORE_BAND = {
  excellent: { min: 85, color: "#52c41a", label: "优秀" },
  good: { min: 70, color: "#1677ff", label: "良好" },
  pass: { min: 60, color: "#faad14", label: "及格" },
  fail: { min: 0, color: "#ff4d4f", label: "不及格" },
};

export function scoreBand(score?: number | null) {
  if (score == null) return null;
  if (score >= SCORE_BAND.excellent.min) return SCORE_BAND.excellent;
  if (score >= SCORE_BAND.good.min) return SCORE_BAND.good;
  if (score >= SCORE_BAND.pass.min) return SCORE_BAND.pass;
  return SCORE_BAND.fail;
}
