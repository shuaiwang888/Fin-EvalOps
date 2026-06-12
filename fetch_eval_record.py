#!/usr/bin/env python3
"""
fetch_eval_record.py — 从问财 EvalOps 后端拉取评测明细并导出为原始测试集格式

用法:
    # 单条
    python fetch_eval_record.py iwencai:wencai:01-event-and-concept-stock-selection:debug_platform_xxx

    # 批量(命令行多个 id)
    python fetch_eval_record.py id1 id2 id3

    # 批量(从文件逐行,空行 / # 开头跳过)
    python fetch_eval_record.py --file ids.txt

    # 批量(从 stdin)
    cat ids.txt | python fetch_eval_record.py -

    # 自定义输出目录
    python fetch_eval_record.py --out-dir ./samples id1

    # 保留原始 HTML(便于排错)
    python fetch_eval_record.py --keep-html id1

    # 单文件多样本合并(把所有样本写到一个 list JSON 里)
    python fetch_eval_record.py --merged-out all.json --file ids.txt

输出文件命名: <问题前N字>_<id哈希8位>.json  (默认 N=12)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path
from typing import Iterable

DEFAULT_BASE_URL = "https://117.50.195.94:2879"
DETAIL_PATH = "/review/detail/"
DEFAULT_OUT_DIR = "数据测试集/ 事件"
DEFAULT_QUESTION_PREFIX_LEN = 12


# ---------------------- 网络层 ----------------------
def _build_ssl_context(insecure: bool):
    """构造 SSL context;insecure=True 时跳过证书校验(适合自签证书内网服务)"""
    import ssl
    if insecure:
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    return ssl.create_default_context()


def fetch_html(record_id: str, base_url: str = DEFAULT_BASE_URL, timeout: int = 30,
               insecure: bool = True) -> str:
    """拉取 /review/detail/{record_id} 的 HTML"""
    encoded = urllib.parse.quote(record_id, safe="")
    url = f"{base_url}{DETAIL_PATH}{encoded}"
    req = urllib.request.Request(url, headers={"User-Agent": "fetch_eval_record/1.0"})
    ctx = _build_ssl_context(insecure)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        return resp.read().decode("utf-8")


# ---------------------- 解析层 ----------------------
_QUESTION_RE = re.compile(r'<div class="question"[^>]*>([^<]+)</div>')
_ANSWER_RE = re.compile(
    r'<div class="answer-content model-answer-content"[^>]*>(.*?)</div>\s*</div>\s*</div>',
    re.DOTALL,
)
_CHAIN_CONTAINER_RE = re.compile(
    r'<div class="chain-steps">(.*?)</div>\s*</div>\s*</div>\s*</details>', re.DOTALL
)
_STEP_SPLIT_RE = re.compile(
    r'(?=<div class="chain-step"[^>]*data-pointer="chain\[\d+\]\.plan")'
)
_TOOL_SPLIT_RE = re.compile(
    r'(?=<div class="chain-tool"[^>]*data-pointer="chain\[\d+\]\.tools\[\d+\]\.output")'
)
_PLAN_RE = re.compile(r'<p class="chain-plan">(.*?)</p>', re.DOTALL)
_TOOL_NAME_RE = re.compile(r'<span class="chain-tool-name">([^<]+)</span>')
_TOOL_INPUT_RE = re.compile(
    r'<details class="chain-io-block chain-tool-input">.*?<div class="chain-io-content[^"]*"[^>]*>(.*?)</div>\s*</details>',
    re.DOTALL,
)
_TOOL_OUTPUT_RE = re.compile(
    r'<details class="chain-io-block chain-tool-output">.*?<div class="chain-io-content[^"]*"[^>]*>(.*?)</div>\s*</details>',
    re.DOTALL,
)
_CONTEXT_RE = re.compile(
    r'<details class="collapse-section[^"]*review-context-card"[^>]*>(.*?)</details>',
    re.DOTALL,
)
_CONTEXT_EMPTY_RE = re.compile(r'<div class="empty-state[^"]*review-context-empty"[^>]*>[^<]*</div>')
_CONTEXT_TURN_RE = re.compile(
    r'<details class="context-turn[^"]*"[^>]*>(.*?)</details>',
    re.DOTALL,
)
_CONTEXT_Q_RE = re.compile(
    r'<span class="context-turn-q-text"[^>]*>(.*?)</span>',
    re.DOTALL,
)
_CONTEXT_A_RE = re.compile(
    r'<div class="context-turn-a[^"]*"[^>]*>(.*?)</div>\s*(?=<details\b|</details>|$)',
    re.DOTALL,
)


def parse_record(html: str) -> dict:
    """把 /review/detail 的 HTML 解析成 {来源, id, 问题, 答案, 链路数据}"""
    # 1) question
    qm = _QUESTION_RE.search(html)
    if not qm:
        raise ValueError("未找到 question 字段")
    question = unescape(qm.group(1)).strip()

    # 2) answer
    am = _ANSWER_RE.search(html)
    if not am:
        raise ValueError("未找到 answer 字段")
    answer = unescape(am.group(1)).strip()

    # 3) chain
    cm = _CHAIN_CONTAINER_RE.search(html)
    if not cm:
        raise ValueError("未找到 chain-steps 容器")
    chain_inner = cm.group(1)

    steps = []
    for part in _STEP_SPLIT_RE.split(chain_inner):
        part = part.strip()
        if not part.startswith('<div class="chain-step"'):
            continue
        plan_m = _PLAN_RE.search(part)
        plan = unescape(plan_m.group(1)).strip() if plan_m else ""
        tools = []
        for tp in _TOOL_SPLIT_RE.split(part):
            if not tp.strip().startswith('<div class="chain-tool"'):
                continue
            name_m = _TOOL_NAME_RE.search(tp)
            inp_m = _TOOL_INPUT_RE.search(tp)
            out_m = _TOOL_OUTPUT_RE.search(tp)
            tools.append({
                "name": name_m.group(1).strip() if name_m else "",
                "input": unescape(inp_m.group(1)).strip() if inp_m else "",
                "output": unescape(out_m.group(1)).strip() if out_m else "",
            })
        steps.append({"plan": plan, "tools": tools})

    # 4) 上下文(可选,部分样本有,多轮对话用 turns 列表,单轮直接用字符串)
    context = None
    cm = _CONTEXT_RE.search(html)
    if cm:
        # 关键:外层 <details> 与内层 <details class="context-turn..."> 都有 </details>,
        # 简单的 (.*?)</details> 非贪婪会匹到内层第一个 close。改用平衡计数定位外层 close。
        outer_open = cm.start()
        open_re = re.compile(r'<details\b')
        close_re = re.compile(r'</details>')
        # 从 outer_open 开始,depth=0,遇到 <details>+1,</details>-1,首次回到 0 即外层 close
        depth = 0
        end_pos = None
        for tok in re.finditer(r'<(/?)details\b|</details>', html[outer_open:]):
            content = tok.group(0)
            if content.startswith('</'):
                depth -= 1
                if depth == 0:
                    end_pos = outer_open + tok.end()
                    break
            else:
                depth += 1
        if end_pos:
            ctx_body = html[outer_open:end_pos]
        else:
            ctx_body = cm.group(1)

        if not _CONTEXT_EMPTY_RE.search(ctx_body):
            turns = []
            for tm in _CONTEXT_TURN_RE.finditer(ctx_body):
                turn_body = tm.group(1)
                qm = _CONTEXT_Q_RE.search(turn_body)
                am = _CONTEXT_A_RE.search(turn_body)
                q = unescape(qm.group(1)).strip() if qm else ""
                a = unescape(am.group(1)).strip() if am else ""
                if q or a:
                    turns.append({"Q": q, "A": a})
            if turns:
                # 一律保存为 turns 列表(单轮也保留 Q),不再简化为字符串
                context = turns

    # 5) sample id (与原文件风格一致:ans_<md5_24>)
    sample_id = "ans_" + hashlib.md5(question.encode("utf-8")).hexdigest()[:24]

    out = {
        "来源": "iwencai",
        "id": sample_id,
        "问题": question,
        "答案": answer,
        "链路数据": steps,
    }
    if context:
        out["上下文"] = context
    return out


# ---------------------- 文件输出 ----------------------
_FILENAME_INVALID = re.compile(r'[\\/:*?"<>|\s]+')


def sanitize_prefix(question: str, n: int = DEFAULT_QUESTION_PREFIX_LEN) -> str:
    """取问题前 N 字,清洗成安全文件名片段"""
    s = question[:n].strip()
    s = _FILENAME_INVALID.sub("", s)
    return s or "untitled"


def output_filename(record: dict, record_id: str) -> str:
    qhash = hashlib.md5(record_id.encode("utf-8")).hexdigest()[:8]
    prefix = sanitize_prefix(record["问题"])
    return f"{prefix}_{qhash}.json"


def _read_back_record(out_dir: str, record_id: str) -> dict | None:
    """Locate the just-written JSON file for `record_id` and return its dict.

    We can't compute the exact filename without re-parsing the question, so we
    fall back to a glob on the md5 prefix which is unique to the record_id.
    """
    qhash = hashlib.md5(record_id.encode("utf-8")).hexdigest()[:8]
    matches = list(Path(out_dir).glob(f"*_{qhash}.json"))
    if not matches:
        return None
    return json.loads(matches[0].read_text(encoding="utf-8"))


# ---------------------- 批量输入 ----------------------
def read_ids_from_stdin() -> list[str]:
    return [line.strip() for line in sys.stdin if line.strip() and not line.strip().startswith("#")]


def read_ids_from_file(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(path)
    return [line.strip() for line in p.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.strip().startswith("#")]


# ---------------------- 主流程 ----------------------
def process_one(record_id: str, args) -> tuple[bool, str]:
    """处理单条 record_id,返回 (success, message)"""
    try:
        html = fetch_html(record_id, args.base_url, args.timeout, insecure=not args.secure)
    except Exception as e:
        return False, f"[NET] {e}"

    # 可选保留原始 HTML
    if args.keep_html:
        raw_path = Path(args.out_dir) / f"{sanitize_prefix('raw')}_{hashlib.md5(record_id.encode()).hexdigest()[:8]}.html"
        try:
            raw_path.write_text(html, encoding="utf-8")
        except Exception:
            pass

    try:
        record = parse_record(html)
    except Exception as e:
        return False, f"[PARSE] {e}"

    out_path = Path(args.out_dir) / output_filename(record, record_id)
    out_path.write_text(
        json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    size = out_path.stat().st_size
    n_tools = sum(len(s["tools"]) for s in record["链路数据"])
    return True, f"{out_path.name}  ({size:,}B, {len(record['链路数据'])}步, {n_tools}工具)"


def main():
    ap = argparse.ArgumentParser(
        description="从问财 EvalOps 拉取评测明细并导出为原始测试集格式",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    ap.add_argument("ids", nargs="*", help="record_id(可多个)")
    ap.add_argument("--file", "-f", help="从文件逐行读 id")
    ap.add_argument("--out-dir", "-o", default=DEFAULT_OUT_DIR, help=f"输出目录(默认 {DEFAULT_OUT_DIR!r})")
    ap.add_argument("--category", "-c", help="分类名(会在 --out-dir 下创建子目录,例如 '01-event-and-concept-stock-selection')")
    ap.add_argument("--base-url", default=DEFAULT_BASE_URL, help="后端 base URL")
    ap.add_argument("--timeout", type=int, default=30, help="单条超时秒数")
    ap.add_argument("--secure", action="store_true", help="启用严格 SSL 校验(默认跳过,适合自签内网)")
    ap.add_argument("--keep-html", action="store_true", help="保留原始 HTML 用于排错")
    ap.add_argument("--merged-out", help="把所有成功样本合并写入一个 list JSON(默认每个样本独立文件)")
    ap.add_argument("--prefix-len", type=int, default=DEFAULT_QUESTION_PREFIX_LEN, help="文件名问题前缀长度")
    ap.add_argument("--rate", type=float, default=0.0, help="每条之间 sleep 秒数(避免打爆后端)")

    args = ap.parse_args()

    # 收集 ids
    ids: list[str] = list(args.ids)
    if args.file:
        ids.extend(read_ids_from_file(args.file))
    if not ids and not sys.stdin.isatty():
        ids.extend(read_ids_from_stdin())
    if "-" in ids:
        ids.remove("-")
        ids.extend(read_ids_from_stdin())

    if not ids:
        ap.error("没有提供 record_id(可用位置参数 / --file / stdin)")

    # 去重保序
    seen, ordered = set(), []
    for i in ids:
        if i not in seen:
            seen.add(i)
            ordered.append(i)
    ids = ordered

    # 如果指定了 --category,输出目录追加一层
    if args.category:
        args.out_dir = str(Path(args.out_dir) / args.category)

    Path(args.out_dir).mkdir(parents=True, exist_ok=True)

    print(f"📦 待处理: {len(ids)} 条  →  {args.out_dir}")
    print()

    ok_records: list[dict] = []
    ok_ids: list[str] = []
    fail: list[tuple[str, str]] = []
    t0 = time.time()
    for idx, rid in enumerate(ids, 1):
        print(f"[{idx}/{len(ids)}] {rid[:80]}{'...' if len(rid) > 80 else ''}")
        ok, msg = process_one(rid, args)
        if ok:
            print(f"   ✅ {msg}")
            # Read back the just-written file (no extra HTTP call)
            try:
                record = _read_back_record(args.out_dir, rid)
                if record is not None:
                    ok_records.append(record)
                    ok_ids.append(rid)
            except Exception:
                pass
        else:
            print(f"   ❌ {msg}")
            fail.append((rid, msg))
        if args.rate and idx < len(ids):
            time.sleep(args.rate)

    # 合并输出
    if args.merged_out and ok_records:
        mp = Path(args.merged_out)
        mp.parent.mkdir(parents=True, exist_ok=True)
        mp.write_text(json.dumps(ok_records, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n📚 合并文件: {mp}  ({len(ok_records)} 条)")

    # 汇总
    dt = time.time() - t0
    print()
    print("=" * 60)
    print(f"成功: {len(ok_records)}/{len(ids)}  失败: {len(fail)}  耗时: {dt:.1f}s")
    if fail:
        print("\n失败明细:")
        for rid, msg in fail:
            print(f"  - {rid}\n      {msg}")
    print("=" * 60)
    sys.exit(0 if not fail else 1)


if __name__ == "__main__":
    main()
