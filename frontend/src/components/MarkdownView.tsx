import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  text: string;
  /** Render reference_v2 placeholders as info chips. */
  highlightRefs?: boolean;
}

// Markdown view used for question/answer rendering.
// reference_v2 placeholders are stripped and shown as `📎 引用` chips.
export default function MarkdownView({ text, highlightRefs = true }: Props) {
  let processed = text || "";
  if (highlightRefs) {
    processed = processed.replace(
      /```reference_v2\s*([\s\S]*?)```/g,
      "> 📎 _引用资源_: `$1`"
    );
  }
  return (
    <div className="markdown-body">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>{processed}</ReactMarkdown>
    </div>
  );
}
