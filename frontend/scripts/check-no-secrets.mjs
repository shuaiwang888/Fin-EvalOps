#!/usr/bin/env node
// Pre-build self-check: scan the frontend source tree for accidentally
// committed secrets (API keys, internal IPs/hostnames).
// Run as `npm run check-no-secrets`. Failure = non-zero exit.

import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, extname } from "node:path";
import { fileURLToPath } from "node:url";
import { dirname } from "node:path";

const __dirname = dirname(fileURLToPath(import.meta.url));
const root = join(__dirname, "..");

// Patterns we never want in shipped frontend code:
const FORBIDDEN = [
  { re: /117\.50\.195\.94/, label: "iwencai internal IP" },
  { re: /sk-ant-[A-Za-z0-9_-]{20,}/, label: "Anthropic API key" },
  { re: /sk-[A-Za-z0-9]{40,}/, label: "OpenAI/DeepSeek-style key" },
  { re: /sk-cp-[A-Za-z0-9_-]{20,}/, label: "MiniMax API key" },
  { re: /\bDASHSCOPE_API_KEY\s*=\s*['"][^'"]+['"]/, label: "DashScope key literal" },
  { re: /\bMINIMAX_API_KEY\s*=\s*['"][^'"]+['"]/, label: "MiniMax key literal" },
];

const EXCLUDE_DIRS = new Set([
  "node_modules", "dist", ".git", ".vite",
]);

// Allow-list — files where mentioning the pattern is intentional (.env.example, this script)
const ALLOWLIST = new Set([
  ".env.example",
  "check-no-secrets.mjs",
  "README.md",
]);

const EXTS = new Set([".ts", ".tsx", ".js", ".jsx", ".mjs", ".json", ".html", ".env"]);

let violations = 0;

function walk(dir) {
  for (const entry of readdirSync(dir)) {
    if (EXCLUDE_DIRS.has(entry)) continue;
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) {
      walk(full);
      continue;
    }
    if (ALLOWLIST.has(entry)) continue;
    if (!EXTS.has(extname(entry))) continue;
    const text = readFileSync(full, "utf8");
    for (const { re, label } of FORBIDDEN) {
      const m = text.match(re);
      if (m) {
        console.error(`❌ Secret-like pattern (${label}) in ${full}:`);
        console.error(`   match: ${m[0].slice(0, 60)}…`);
        violations++;
      }
    }
  }
}

walk(root);

if (violations > 0) {
  console.error(`\n💥 ${violations} secret-leak violation(s). Refusing to build.`);
  process.exit(1);
}
console.log("✓ no secrets detected in frontend source");
