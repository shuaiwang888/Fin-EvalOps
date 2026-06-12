import { useEffect, useState } from "react";
import { Progress, Tag } from "antd";
import { subscribeRun } from "../api/sse";

interface Props {
  runId: string;
  onComplete?: (data: any) => void;
  onError?: (data: any) => void;
}

const STEP_LABELS: Record<number, string> = {
  [-1]: "路由判定",
  0: "分析题目 + 加载协议",
  1: "盲评最终答案",
  2: "链路诊断 + 根因",
  3: "应用封顶规则",
  4: "序列化输出",
};

export default function SSEProgressBar({ runId, onComplete, onError }: Props) {
  const [pct, setPct] = useState(0);
  const [step, setStep] = useState<string>("等待开始…");
  const [status, setStatus] = useState<string>("pending");
  const [doneMeta, setDoneMeta] = useState<any>(null);

  useEffect(() => {
    const stop = subscribeRun(runId, {
      onProgress: (d) => {
        if (typeof d.progress === "number") setPct(d.progress);
        if (d.current_step) setStep(d.current_step);
        if (d.status) setStatus(d.status);
      },
      onStep: (d) => {
        if (typeof d.step === "number") {
          setStep(`${STEP_LABELS[d.step] || d.label || `步骤 ${d.step}`}`);
        }
      },
      onComplete: (d) => {
        setPct(100);
        setStatus("done");
        setStep("完成");
        setDoneMeta(d);
        onComplete?.(d);
      },
      onError: (d) => {
        setStatus("failed");
        setStep("失败");
        onError?.(d);
      },
    });
    return stop;
  }, [runId]);

  const color =
    status === "failed" ? "#ff4d4f" :
    status === "done" ? "#52c41a" : "#0958d9";

  return (
    <div>
      <div style={{ marginBottom: 6, display: "flex", alignItems: "center", gap: 8 }}>
        <Tag color={color === "#0958d9" ? "blue" : color === "#52c41a" ? "green" : "red"}>
          {status}
        </Tag>
        <span style={{ fontSize: 13 }}>{step}</span>
      </div>
      <Progress percent={pct} strokeColor={color} status={status === "failed" ? "exception" : status === "done" ? "success" : "active"} />
      {doneMeta && (
        <div style={{ marginTop: 8, fontSize: 12, color: "#666" }}>
          最终分: <strong>{doneMeta.final_score}</strong> · 加权未封顶: {doneMeta.absolute_score_pre_cap}
          {doneMeta.triggered_caps?.length > 0 && (
            <> · 触发封顶: {doneMeta.triggered_caps.join(", ")}</>
          )}
        </div>
      )}
    </div>
  );
}
