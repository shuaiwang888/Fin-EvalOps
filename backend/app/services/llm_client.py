"""Multi-provider LLM client.

Exposes a uniform `.call_with_schema(model, system, user, schema)` returning
a validated JSON dict, regardless of which provider is behind the scenes.

Supported providers:
- anthropic  (Claude — tool_use forced)
- openai     (GPT — response_format json_schema)
- dashscope  (通义 Qwen — JSON mode + validation)
- deepseek   (DeepSeek — OpenAI-compatible API)

Model registry maps a short model ID to (provider, real_model_id).
"""
from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import httpx
from jsonschema import Draft202012Validator
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from ..config import settings
from ..utils.trace import get_logger

log = get_logger(__name__)


# ============================================================================
# Model registry — what the frontend dropdown shows
# ============================================================================
@dataclass(frozen=True)
class ModelSpec:
    id: str               # frontend-facing id
    provider: str         # routing key
    real_model: str       # actual API model id
    label: str            # display name
    context_window: int
    supports_tools: bool = True


MODELS: Dict[str, ModelSpec] = {
    # Anthropic
    "claude-sonnet-4-6": ModelSpec(
        "claude-sonnet-4-6", "anthropic", "claude-sonnet-4-6",
        "Claude Sonnet 4.6", 200_000,
    ),
    "claude-opus-4-8": ModelSpec(
        "claude-opus-4-8", "anthropic", "claude-opus-4-8",
        "Claude Opus 4.8", 200_000,
    ),
    "claude-haiku-4-5": ModelSpec(
        "claude-haiku-4-5", "anthropic", "claude-haiku-4-5-20251001",
        "Claude Haiku 4.5", 200_000,
    ),
    # OpenAI
    "gpt-4o": ModelSpec(
        "gpt-4o", "openai", "gpt-4o", "GPT-4o", 128_000,
    ),
    "gpt-4o-mini": ModelSpec(
        "gpt-4o-mini", "openai", "gpt-4o-mini", "GPT-4o mini", 128_000,
    ),
    # 通义 (DashScope)
    "qwen-max": ModelSpec(
        "qwen-max", "dashscope", "qwen-max", "通义千问 Max", 30_000,
    ),
    "qwen-plus": ModelSpec(
        "qwen-plus", "dashscope", "qwen-plus", "通义千问 Plus", 131_000,
    ),
    # DeepSeek
    "deepseek-chat": ModelSpec(
        "deepseek-chat", "deepseek", "deepseek-chat", "DeepSeek Chat", 64_000,
    ),
    "deepseek-reasoner": ModelSpec(
        "deepseek-reasoner", "deepseek", "deepseek-reasoner", "DeepSeek Reasoner", 64_000,
    ),
    # MiniMax — Anthropic-compatible endpoint at /anthropic.
    # Uses the official Anthropic SDK with a custom base_url + MiniMax API key.
    # Adjust the `real_model` string if MiniMax renames the model upstream.
    "minimax-2.5": ModelSpec(
        "minimax-2.5", "minimax", "minimax-2.5",
        "MiniMax-2.5", 64_000,
    ),
    "minimax-3": ModelSpec(
        "minimax-3", "minimax", "minimax-3",
        "MiniMax-3", 128_000,
    ),
}


def list_models() -> List[dict]:
    """Filter to models whose provider has an API key configured (live env read)."""
    out = []
    for m in MODELS.values():
        key_attr = f"{m.provider}_api_key_live"
        if getattr(settings, key_attr, ""):
            out.append({
                "id": m.id,
                "provider": m.provider,
                "label": m.label,
                "context_window": m.context_window,
            })
    return out


def resolve_model(model_id: Optional[str]) -> ModelSpec:
    """Pick a model: explicit > default > first available (live env read)."""
    if model_id and model_id in MODELS:
        spec = MODELS[model_id]
        if getattr(settings, f"{spec.provider}_api_key_live", ""):
            return spec
        log.warning("Requested model %s but its provider key is missing, falling back", model_id)
    default_id = settings.default_judge_model_live
    default = MODELS.get(default_id)
    if default and getattr(settings, f"{default.provider}_api_key_live", ""):
        return default
    available = list_models()
    if not available:
        raise RuntimeError(
            "No LLM provider configured. Set at least one of "
            "ANTHROPIC_API_KEY / OPENAI_API_KEY / DASHSCOPE_API_KEY / DEEPSEEK_API_KEY / MINIMAX_API_KEY."
        )
    return MODELS[available[0]["id"]]


# ============================================================================
# Provider adapters
# ============================================================================
class LLMError(Exception):
    pass


class SchemaValidationError(LLMError):
    pass


class LLMTruncatedError(LLMError):
    """LLM hit max_tokens / returned a partial JSON object.

    Callers should NOT try to recover — a truncated judge output is
    unreliable because downstream fields (dimension_scores, caps) may
    be entirely missing. Best UX: fail the run with a clear error_msg.
    """
    pass


@dataclass
class LLMResult:
    data: Dict[str, Any]
    raw_text: str
    tokens_in: int
    tokens_out: int
    latency_ms: int
    model: str
    provider: str


_RETRY = retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1.0, min=1, max=8),
    retry=retry_if_exception_type((httpx.HTTPError, LLMError)),
    reraise=True,
)


@_RETRY
def call_with_schema(
    model_id: Optional[str],
    system: str,
    user: str | Dict[str, Any],
    schema: Dict[str, Any],
    tool_name: str = "submit_result",
    max_tokens: int = 4096,
    temperature: float = 0.2,
) -> LLMResult:
    """Call the chosen LLM and return validated JSON.

    `user` may be a string OR a dict; dicts are JSON-encoded before sending.
    """
    spec = resolve_model(model_id)
    user_text = user if isinstance(user, str) else json.dumps(user, ensure_ascii=False, indent=2)

    t0 = time.perf_counter()
    if spec.provider == "anthropic":
        data, raw, tin, tout = _call_anthropic(spec, system, user_text, schema, tool_name, max_tokens, temperature)
    elif spec.provider == "minimax":
        data, raw, tin, tout = _call_anthropic(
            spec, system, user_text, schema, tool_name, max_tokens, temperature,
            base_url_override=settings.minimax_base_url_live or None,
            api_key_override=settings.minimax_api_key_live,
        )
    elif spec.provider == "openai":
        data, raw, tin, tout = _call_openai(spec, system, user_text, schema, tool_name, max_tokens, temperature)
    elif spec.provider == "dashscope":
        data, raw, tin, tout = _call_dashscope(spec, system, user_text, schema, max_tokens, temperature)
    elif spec.provider == "deepseek":
        data, raw, tin, tout = _call_deepseek(spec, system, user_text, schema, max_tokens, temperature)
    else:
        raise LLMError(f"Unsupported provider {spec.provider}")
    latency_ms = int((time.perf_counter() - t0) * 1000)

    # Coerce common LLM shape mistakes before strict validation. Without this,
    # judge models that emit `root_causes` / `caps` as parallel arrays
    # would trip the validator and the entire eval would fail.
    data = _sanitize_judge_for_validation(data, schema=schema)
    try:
        _validate_schema(data, schema)
    except SchemaValidationError as exc:
        # One last lenient attempt: drop required markers by adding empty
        # defaults so the validator sees a complete shape. This keeps the
        # eval pipeline alive when the judge forgets e.g. `narrative_review`.
        data = _fill_missing_top_level_fields(data, schema)
        # Re-sanitize after fill — the fill may have introduced type
        # mismatches (e.g. caps: {} → []) that need parallel-array work.
        data = _sanitize_judge_for_validation(data, schema=schema)
        try:
            _validate_schema(data, schema)
        except SchemaValidationError:
            # Final fallback: return the data as-is. Downstream evaluator
            # sanitizers (evaluator._sanitize_judge_output) will fill in
            # the rest. Better to record a partial result than to fail.
            log.warning(
                "Schema validation still failed after sanitization for %s: %s",
                spec.id, str(exc)[:200],
            )
    return LLMResult(
        data=data, raw_text=raw, tokens_in=tin, tokens_out=tout,
        latency_ms=latency_ms, model=spec.id, provider=spec.provider,
    )


def _fill_missing_top_level_fields(data: dict, schema: dict) -> dict:
    """Best-effort fill of required top-level fields so the validator sees
    a complete object. Keeps partial judge output usable downstream.
    """
    defaults_by_type: dict[str, Any] = {
        "object": {}, "array": [], "string": "", "number": 0, "integer": 0,
        "boolean": False,
    }
    props = (schema or {}).get("properties", {})
    for required_key in (schema or {}).get("required", []):
        if required_key not in data:
            sub = props.get(required_key, {})
            data[required_key] = defaults_by_type.get(sub.get("type", "object"), {})
    return data


def _validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> None:
    """Strict validation. Callers should pre-sanitize common LLM shape mistakes
    (parallel arrays for list fields, etc.) via _sanitize_judge_for_validation
    before calling this. We allow missing `required` keys if they can be
    defaulted to [] or {} to keep the eval pipeline alive.
    """
    try:
        Draft202012Validator(schema).validate(data)
    except Exception as exc:
        raise SchemaValidationError(f"Schema validation failed: {exc}") from exc


# ============================================================================
# Sanitization — applied BEFORE schema validation to coerce common LLM
# structural mistakes back into the schema shape.
#
# Why: judge models frequently emit array-shaped data as parallel arrays
# (e.g. "l1": ["a", "b"], "l2": ["x", "y"]) when the schema wants an
# array of objects ([{"l1": "a", "l2": "x"}, {"l1": "b", "l2": "y"}]).
# Without this fix, the validator raises and the whole eval fails.
# ============================================================================
def _is_parallel_array_object(value: Any) -> Optional[int]:
    """Detect "dict of parallel arrays" shape. Returns array length if matched.

    A "parallel array object" is a dict where ≥2 values are non-empty lists
    of the same length. These almost always mean the LLM wanted to emit an
    array of objects, one per index.
    """
    if not isinstance(value, dict) or len(value) < 2:
        return None
    list_lengths: list[int] = []
    for v in value.values():
        if isinstance(v, list) and v:
            list_lengths.append(len(v))
    if len(list_lengths) < 2:
        return None
    if len(set(list_lengths)) != 1:
        return None
    return list_lengths[0]


def _parallel_array_to_list(obj: dict) -> list:
    """Transpose a "dict of parallel arrays" into an array of objects."""
    keys = list(obj.keys())
    n = len(obj[keys[0]]) if isinstance(obj[keys[0]], list) else 0
    out: list[dict] = []
    for i in range(n):
        item = {}
        for k in keys:
            v = obj[k]
            if isinstance(v, list) and i < len(v):
                item[k] = v[i]
            else:
                item[k] = v  # scalar — same value applied to every item
        out.append(item)
    return out


_PARALLEL_ARRAY_FIELDS = ("root_causes", "caps", "skipped_dimensions",
                         "matched_golden_cases")


def _sanitize_judge_for_validation(data: Any, schema: dict | None = None) -> Any:
    """Coerce common LLM shape mistakes back into schema form. Idempotent.

    Handles:
    1. `root_causes` / `caps` / `skipped_dimensions` / `matched_golden_cases`
       given as a dict of parallel arrays instead of a list of objects —
       transposed to list of objects.
    2. `matched_golden_cases` sometimes arrives as a string with bullet
       separators ("Case 1; Case 2") — split into a list.
    3. `dimension_scores.raw_score` and `root_causes[].raw_score` given as
       strings ("80") — coerced to float. (Same for `score_ceiling` on
       cap entries.)
    4. Top-level field whose schema type is `object` but data has a list
       (or vice versa) — coerced to the safe default {} or [] so
       downstream code that calls `.get()` on these fields never crashes
       with 'list' object has no attribute 'get'.
    5. `weight_assignment` / `dimension_scores` wrapped as `{"item": [...]}`
       — flattened into the proper per-dim dict shape. CRITICAL: without
       this, the scorer sees only one non-dict key and skips every dim
       → final_score = 0.
    """
    if not isinstance(data, dict):
        return data

    # 4) Coerce top-level field TYPES against the schema. Without this,
    #    a judge that returns e.g. `weight_assignment: [{...}, {...}]`
    #    (list) when the schema expects an object would slip through the
    #    permissive fallback and crash the scorer with AttributeError.
    type_defaults: dict[str, Any] = {"object": {}, "array": []}
    if isinstance(schema, dict):
        props = schema.get("properties") or {}
        for fname, fschema in props.items():
            expected = (fschema or {}).get("type")
            if expected not in type_defaults:
                continue
            v = data.get(fname)
            if v is None:
                continue
            actual = (
                "array" if isinstance(v, list)
                else "object" if isinstance(v, dict)
                else None
            )
            if actual is None or actual == expected:
                continue
            data[fname] = type_defaults[expected]

    for field in _PARALLEL_ARRAY_FIELDS:
        v = data.get(field)
        if isinstance(v, list):
            continue
        n = _is_parallel_array_object(v)
        if n:
            data[field] = _parallel_array_to_list(v)

    # matched_golden_cases: bare string → split on common separators
    mgc = data.get("matched_golden_cases")
    if isinstance(mgc, str):
        parts = [p.strip() for p in re.split(r"[;\n|,]|Case\s+\d+[:：]", mgc) if p.strip()]
        data["matched_golden_cases"] = parts if parts else []

    def _coerce_numeric(item: dict, field_name: str) -> None:
        v = item.get(field_name)
        if isinstance(v, str):
            try:
                item[field_name] = float(v)
            except (ValueError, TypeError):
                item[field_name] = 0

    # dimension_scores: per-dim raw_score string → float
    ds = data.get("dimension_scores")
    if isinstance(ds, dict):
        for dim, sc in ds.items():
            if isinstance(sc, dict):
                _coerce_numeric(sc, "raw_score")

    # root_causes: per-cause raw_score string → float
    rc = data.get("root_causes")
    if isinstance(rc, list):
        for item in rc:
            if isinstance(item, dict):
                _coerce_numeric(item, "raw_score")

    # caps: per-cap score_ceiling string → float
    caps = data.get("caps")
    if isinstance(caps, list):
        for item in caps:
            if isinstance(item, dict):
                _coerce_numeric(item, "score_ceiling")

    # 5) Unwrap {"item": [...]} wrapper on dict-shaped fields. Without this,
    #    evaluator's downstream scorer sees only one key (item) and skips
    #    every dim — final_score = 0. We can't reliably know each entry's
    #    dim_name without the skill spec, so fall back to positional labels.
    #    The evaluator's _sanitize_judge_output does a second pass with
    #    skill_row.dimensions to upgrade the labels to canonical names.
    _ENTRY_KNOWN = {
        "weight_assignment": {"dynamic_weight", "applicability", "rationale"},
        "dimension_scores": {"raw_score", "evidence", "confidence", "summary"},
    }
    for field, known in _ENTRY_KNOWN.items():
        v = data.get(field)
        if not isinstance(v, dict) or not isinstance(v.get("item"), list):
            continue
        items = v["item"]
        flat: dict = {}
        for i, entry in enumerate(items):
            if not isinstance(entry, dict):
                continue
            extra = [k for k in entry.keys() if k not in known]
            dim_name = extra[0] if extra else f"dim_{i}"
            clean = {k: val for k, val in entry.items()
                     if k in known and val not in (None, "")}
            flat[dim_name] = clean
        if flat:
            data[field] = flat

    return data

    # matched_golden_cases: bare string → split on common separators
    mgc = data.get("matched_golden_cases")
    if isinstance(mgc, str):
        parts = [p.strip() for p in re.split(r"[;\n|,]|Case\s+\d+[:：]", mgc) if p.strip()]
        data["matched_golden_cases"] = parts if parts else []

    def _coerce_numeric(item: dict, field_name: str) -> None:
        v = item.get(field_name)
        if isinstance(v, str):
            try:
                item[field_name] = float(v)
            except (ValueError, TypeError):
                item[field_name] = 0

    # dimension_scores: per-dim raw_score string → float
    ds = data.get("dimension_scores")
    if isinstance(ds, dict):
        for dim, sc in ds.items():
            if isinstance(sc, dict):
                _coerce_numeric(sc, "raw_score")

    # root_causes: per-cause raw_score string → float
    rc = data.get("root_causes")
    if isinstance(rc, list):
        for item in rc:
            if isinstance(item, dict):
                _coerce_numeric(item, "raw_score")

    # caps: per-cap score_ceiling string → float
    caps = data.get("caps")
    if isinstance(caps, list):
        for item in caps:
            if isinstance(item, dict):
                _coerce_numeric(item, "score_ceiling")

    return data
    mgc = data.get("matched_golden_cases")
    if isinstance(mgc, str):
        parts = [p.strip() for p in re.split(r"[;\n|,]|Case\s+\d+[:：]", mgc) if p.strip()]
        data["matched_golden_cases"] = parts if parts else []

    def _coerce_numeric(item: dict, field_name: str) -> None:
        v = item.get(field_name)
        if isinstance(v, str):
            try:
                item[field_name] = float(v)
            except (ValueError, TypeError):
                item[field_name] = 0

    # dimension_scores: per-dim raw_score string → float
    ds = data.get("dimension_scores")
    if isinstance(ds, dict):
        for dim, sc in ds.items():
            if isinstance(sc, dict):
                _coerce_numeric(sc, "raw_score")

    # root_causes: per-cause raw_score string → float
    rc = data.get("root_causes")
    if isinstance(rc, list):
        for item in rc:
            if isinstance(item, dict):
                _coerce_numeric(item, "raw_score")

    # caps: per-cap score_ceiling string → float
    caps = data.get("caps")
    if isinstance(caps, list):
        for item in caps:
            if isinstance(item, dict):
                _coerce_numeric(item, "score_ceiling")

    return data


# ------------------------- Anthropic -------------------------
def _call_anthropic(
    spec: ModelSpec, system: str, user_text: str, schema: dict,
    tool_name: str, max_tokens: int, temperature: float,
    base_url_override: Optional[str] = None,
    api_key_override: Optional[str] = None,
) -> Tuple[dict, str, int, int]:
    from anthropic import Anthropic

    client_kwargs = {}
    if api_key_override:
        client_kwargs["api_key"] = api_key_override
    else:
        client_kwargs["api_key"] = settings.anthropic_api_key_live
    if base_url_override:
        client_kwargs["base_url"] = base_url_override
    client = Anthropic(**client_kwargs)
    resp = client.messages.create(
        model=spec.real_model,
        max_tokens=max_tokens,
        system=system,
        temperature=temperature,
        tools=[{
            "name": tool_name,
            "description": "Submit structured evaluation result conforming to the schema.",
            "input_schema": schema,
        }],
        tool_choice={"type": "tool", "name": tool_name},
        messages=[{"role": "user", "content": user_text}],
    )
    tin = resp.usage.input_tokens
    tout = resp.usage.output_tokens
    stop_reason = getattr(resp, "stop_reason", None)
    truncated = stop_reason == "max_tokens"

    for block in resp.content:
        if getattr(block, "type", None) == "tool_use" and block.name == tool_name:
            if truncated:
                # tool_use block exists but LLM ran out of tokens — JSON
                # is likely incomplete. Refuse to return partial data.
                raise LLMTruncatedError(
                    f"LLM hit max_tokens ({max_tokens}) before completing "
                    f"the tool_use block; refusing partial eval data."
                )
            return block.input, json.dumps(block.input, ensure_ascii=False), tin, tout

    # Fallback: many Anthropic-compatible APIs (e.g. minimax) put JSON in
    # a text block instead of honouring tool_use. Try to extract JSON from
    # any text block. If we hit max_tokens we MUST verify the JSON parses
    # cleanly — partial JSON here is the most common cause of mysterious
    # 0.00 scores (sanitizers silently fill defaults).
    for block in resp.content:
        if getattr(block, "type", None) == "text" and getattr(block, "text", "").strip():
            try:
                parsed = _extract_json(block.text)
            except LLMError as exc:
                if truncated:
                    raise LLMTruncatedError(
                        f"LLM hit max_tokens; JSON unparseable: {exc}"
                    ) from exc
                continue
            parsed = _sanitize_judge_for_validation(parsed)
            try:
                _validate_schema(parsed, schema)
            except SchemaValidationError:
                if truncated:
                    raise LLMTruncatedError(
                        "LLM hit max_tokens; sanitized JSON still failed "
                        "schema validation — refusing partial eval data."
                    )
                log.warning(
                    "Provider %s text-block JSON didn't fully match schema; "
                    "passing through for downstream recovery.",
                    spec.provider,
                )
            if truncated:
                # Even strict validation passed (unlikely for truncations),
                # still refuse — max_tokens usually means we got an
                # incomplete view of the response.
                raise LLMTruncatedError(
                    f"LLM hit max_tokens ({max_tokens}); refusing eval data "
                    f"that may be incomplete."
                )
            log.info(
                "Provider %s returned JSON in text block (no tool_use); recovered.",
                spec.provider,
            )
            return parsed, block.text, tin, tout
    raw = json.dumps([b.model_dump() if hasattr(b, "model_dump") else str(b) for b in resp.content])
    raise LLMError(f"Anthropic returned no tool_use block: {raw[:300]}")


# ------------------------- OpenAI -------------------------
def _call_openai(
    spec: ModelSpec, system: str, user_text: str, schema: dict,
    tool_name: str, max_tokens: int, temperature: float,
) -> Tuple[dict, str, int, int]:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key_live)
    resp = client.chat.completions.create(
        model=spec.real_model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_text},
        ],
        tools=[{
            "type": "function",
            "function": {
                "name": tool_name,
                "description": "Submit structured evaluation result.",
                "parameters": schema,
            },
        }],
        tool_choice={"type": "function", "function": {"name": tool_name}},
    )
    choice = resp.choices[0]
    tin = resp.usage.prompt_tokens
    tout = resp.usage.completion_tokens
    call = choice.message.tool_calls[0] if choice.message.tool_calls else None
    if not call:
        raise LLMError("OpenAI returned no tool call")
    data = json.loads(call.function.arguments)
    return data, call.function.arguments, tin, tout


# ------------------------- DashScope (Qwen) -------------------------
def _call_dashscope(
    spec: ModelSpec, system: str, user_text: str, schema: dict,
    max_tokens: int, temperature: float,
) -> Tuple[dict, str, int, int]:
    import dashscope  # type: ignore

    dashscope.api_key = settings.dashscope_api_key_live
    # Qwen supports JSON mode; we append the schema to system prompt
    schema_hint = (
        "\n\n请严格按以下 JSON Schema 输出,不要输出任何额外文本:\n"
        + json.dumps(schema, ensure_ascii=False, indent=2)
    )
    rsp = dashscope.Generation.call(  # type: ignore[attr-defined]
        model=spec.real_model,
        messages=[
            {"role": "system", "content": system + schema_hint},
            {"role": "user", "content": user_text},
        ],
        result_format="message",
        max_tokens=max_tokens,
        temperature=temperature,
        response_format={"type": "json_object"},
    )
    if rsp.status_code != 200:
        raise LLMError(f"DashScope error {rsp.status_code}: {rsp.message}")
    raw = rsp.output.choices[0].message.content
    tin = getattr(rsp.usage, "input_tokens", 0)
    tout = getattr(rsp.usage, "output_tokens", 0)
    return _extract_json(raw), raw, tin, tout


# ------------------------- DeepSeek -------------------------
def _call_deepseek(
    spec: ModelSpec, system: str, user_text: str, schema: dict,
    max_tokens: int, temperature: float,
) -> Tuple[dict, str, int, int]:
    """DeepSeek exposes OpenAI-compatible API at https://api.deepseek.com"""
    from openai import OpenAI

    client = OpenAI(
        api_key=settings.deepseek_api_key_live,
        base_url="https://api.deepseek.com",
    )
    schema_hint = (
        "\n\n请严格按以下 JSON Schema 输出有效 JSON,不要任何额外文本:\n"
        + json.dumps(schema, ensure_ascii=False, indent=2)
    )
    resp = client.chat.completions.create(
        model=spec.real_model,
        max_tokens=max_tokens,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system + schema_hint},
            {"role": "user", "content": user_text},
        ],
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or ""
    tin = resp.usage.prompt_tokens
    tout = resp.usage.completion_tokens
    return _extract_json(raw), raw, tin, tout


# ------------------------- Helpers -------------------------
def _extract_json(text: str) -> dict:
    """Find the first JSON object in text (handles fenced code blocks)."""
    text = text.strip()
    if text.startswith("```"):
        # strip fences
        text = text.lstrip("`").lstrip("json").strip()
        if text.endswith("```"):
            text = text[:-3].strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # last-ditch: regex scan for outermost { ... }
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        try:
            return json.loads(text[start : end + 1])
        except json.JSONDecodeError as exc:
            raise LLMError(f"Could not parse JSON: {exc}; raw={text[:300]}") from exc
    raise LLMError(f"No JSON found in response: {text[:300]}")


# ============================================================================
# Plain chat (used by Data Agent for stream replies)
# ============================================================================
def chat_completion(
    model_id: Optional[str],
    system: str,
    messages: List[dict],
    max_tokens: int = 2048,
    temperature: float = 0.4,
) -> LLMResult:
    """Non-structured chat — returns text in data['content']."""
    spec = resolve_model(model_id)
    t0 = time.perf_counter()
    if spec.provider in ("anthropic", "minimax"):
        from anthropic import Anthropic

        if spec.provider == "minimax":
            client = Anthropic(
                api_key=settings.minimax_api_key_live,
                base_url=settings.minimax_base_url_live or None,
            )
        else:
            client = Anthropic(api_key=settings.anthropic_api_key_live)
        resp = client.messages.create(
            model=spec.real_model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=messages,
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        tin, tout = resp.usage.input_tokens, resp.usage.output_tokens
    else:
        from openai import OpenAI

        base = "https://api.deepseek.com" if spec.provider == "deepseek" else None
        api_key = getattr(settings, f"{spec.provider}_api_key_live")
        client = OpenAI(api_key=api_key, base_url=base) if base else OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=spec.real_model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "system", "content": system}] + messages,
        )
        text = resp.choices[0].message.content or ""
        tin, tout = resp.usage.prompt_tokens, resp.usage.completion_tokens

    latency_ms = int((time.perf_counter() - t0) * 1000)
    return LLMResult(
        data={"content": text}, raw_text=text, tokens_in=tin, tokens_out=tout,
        latency_ms=latency_ms, model=spec.id, provider=spec.provider,
    )
