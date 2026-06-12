import ReactECharts from "echarts-for-react";

interface Props {
  dimensions: Array<{ key: string; label?: string; score: number; weight?: number }>;
  height?: number;
  modelLabel?: string;
}

// Radar chart of dimension scores 0-100.
export default function ScoreRadar({ dimensions, height = 320, modelLabel = "评分" }: Props) {
  if (!dimensions.length) {
    return <div style={{ color: "#999", padding: 24 }}>暂无维度评分数据</div>;
  }
  const option = {
    tooltip: { trigger: "item" },
    radar: {
      indicator: dimensions.map((d) => ({
        name: d.label || d.key,
        max: 100,
      })),
      radius: "65%",
      splitArea: { areaStyle: { color: ["#f5faff", "#ffffff"] } },
      axisLabel: { fontSize: 10, color: "#666" },
      name: { textStyle: { fontSize: 11 } },
    },
    series: [{
      type: "radar",
      data: [{
        value: dimensions.map((d) => d.score),
        name: modelLabel,
        areaStyle: { color: "rgba(9,88,217,0.25)" },
        lineStyle: { color: "#0958d9", width: 2 },
        itemStyle: { color: "#0958d9" },
      }],
    }],
  };
  return <ReactECharts option={option} style={{ height, width: "100%" }} notMerge />;
}
