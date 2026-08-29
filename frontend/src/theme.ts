import type { ThemeConfig } from "antd";

export const finTheme: ThemeConfig = {
  token: {
    colorPrimary: "#0071e3",
    colorInfo: "#0071e3",
    colorSuccess: "#248a3d",
    colorWarning: "#b25000",
    colorError: "#d70015",
    colorText: "#1d1d1f",
    colorTextSecondary: "#6e6e73",
    colorBgLayout: "#f5f5f7",
    colorBgContainer: "rgba(255,255,255,0.88)",
    colorBorderSecondary: "rgba(0,0,0,0.07)",
    borderRadius: 12,
    borderRadiusLG: 20,
    controlHeight: 38,
    fontSize: 14,
    fontFamily:
      '-apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", sans-serif',
    boxShadowTertiary: "0 10px 32px rgba(0, 0, 0, 0.06)",
  },
  components: {
    Button: {
      borderRadius: 999,
      primaryShadow: "0 4px 14px rgba(0,113,227,.2)",
      fontWeight: 560,
    },
    Card: {
      paddingLG: 20,
      headerFontSize: 15,
    },
    Drawer: {
      borderRadiusLG: 22,
    },
    Layout: {
      headerBg: "transparent",
      bodyBg: "#f5f5f7",
      siderBg: "transparent",
    },
    Menu: {
      itemBg: "transparent",
      itemSelectedBg: "rgba(0,113,227,.10)",
      itemSelectedColor: "#0066cc",
      itemBorderRadius: 12,
      itemHeight: 42,
      itemMarginInline: 8,
      groupTitleColor: "#86868b",
    },
    Modal: {
      borderRadiusLG: 22,
    },
    Table: {
      headerBg: "rgba(245,245,247,.9)",
      headerColor: "#6e6e73",
      rowHoverBg: "rgba(0,113,227,.035)",
      cellPaddingBlock: 10,
    },
    Tabs: {
      itemSelectedColor: "#0066cc",
      inkBarColor: "#0071e3",
    },
  },
};

export const PALETTE = [
  "#0071e3", "#00a7b5", "#7d43d6", "#e66d00", "#248a3d", "#d30f6c",
  "#8a7400", "#409cff", "#5e8d00", "#d70015", "#8e5dd9", "#007d8a", "#a06400",
];

export const SCORE_BAND = {
  excellent: { min: 85, color: "#248a3d", label: "优秀" },
  good: { min: 70, color: "#0071e3", label: "良好" },
  pass: { min: 60, color: "#b25000", label: "及格" },
  fail: { min: 0, color: "#d70015", label: "不及格" },
};

export function scoreBand(score?: number | null) {
  if (score == null) return null;
  if (score >= SCORE_BAND.excellent.min) return SCORE_BAND.excellent;
  if (score >= SCORE_BAND.good.min) return SCORE_BAND.good;
  if (score >= SCORE_BAND.pass.min) return SCORE_BAND.pass;
  return SCORE_BAND.fail;
}
