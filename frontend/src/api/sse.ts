// SSE helper backed by native EventSource.
// EventSource doesn't honour custom headers — that's fine because the backend
// uses CORS-friendly cookies/none, and we never put secrets in the URL.

const base = import.meta.env.VITE_API_BASE || "";

export interface SSEHandlers {
  onOpen?: () => void;
  onProgress?: (data: any) => void;
  onStep?: (data: any) => void;
  onComplete?: (data: any) => void;
  onError?: (err: any) => void;
  onAny?: (event: string, data: any) => void;
}

export function subscribeRun(runId: string, handlers: SSEHandlers): () => void {
  return _subscribe(`/api/sse/runs/${runId}`, handlers);
}

export function subscribeBatch(batchId: string, handlers: SSEHandlers): () => void {
  return _subscribe(`/api/sse/batches/${batchId}`, handlers);
}

function _subscribe(path: string, h: SSEHandlers): () => void {
  const url = `${base}${path}`;
  const es = new EventSource(url, { withCredentials: false });
  es.addEventListener("open", () => h.onOpen?.());

  const safe = (name: string, cb?: (data: any) => void) => {
    es.addEventListener(name, (ev: MessageEvent) => {
      let data: any;
      try {
        data = JSON.parse(ev.data);
      } catch {
        data = ev.data;
      }
      cb?.(data);
      h.onAny?.(name, data);
    });
  };

  safe("hello");
  safe("progress", h.onProgress);
  safe("step", h.onStep);
  safe("complete", (d) => {
    h.onComplete?.(d);
    es.close();
  });
  safe("error", (d) => {
    h.onError?.(d);
    es.close();
  });

  es.onerror = (err) => {
    h.onError?.(err);
    // Don't auto-close on transient errors — browser handles reconnect
  };

  return () => es.close();
}
