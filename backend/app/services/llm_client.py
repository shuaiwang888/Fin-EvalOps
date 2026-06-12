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
}


def list_models() -> List[dict]:
    """Filter to models whose provider has an API key configured."""
    out = []
    for m in MODELS.values():
        key_attr = f"{m.provider}_api_key"
        if getattr(settings, key_attr, ""):
            out.append({
                "id": m.id,
                "provider": m.provider,
                "label": m.label,
                "context_window": m.context_window,
            })
    return out


def resolve_model(model_id: Optional[str]) -> ModelSpec:
    """Pick a model: explicit > default > first available."""
    if model_id and model_id in MODELS:
        spec = MODELS[model_id]
        if getattr(settings, f"{spec.provider}_api_key", ""):
            return spec
        log.warning("Requested model %s but its provider key is missing, falling back", model_id)
    default = MODELS.get(settings.default_judge_model)
    if default and getattr(settings, f"{default.provider}_api_key", ""):
        return default
    available = list_models()
    if not available:
        raise RuntimeError(
            "No LLM provider configured. Set at least one of "
            "ANTHROPIC_API_KEY / OPENAI_API_KEY / DASHSCOPE_API_KEY / DEEPSEEK_API_KEY."
        )
    return MODELS[available[0]["id"]]


# ============================================================================
# Provider adapters
# ============================================================================
class LLMError(Exception):
    pass


class SchemaValidationError(LLMError):
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
    elif spec.provider == "openai":
        data, raw, tin, tout = _call_openai(spec, system, user_text, schema, tool_name, max_tokens, temperature)
    elif spec.provider == "dashscope":
        data, raw, tin, tout = _call_dashscope(spec, system, user_text, schema, max_tokens, temperature)
    elif spec.provider == "deepseek":
        data, raw, tin, tout = _call_deepseek(spec, system, user_text, schema, max_tokens, temperature)
    else:
        raise LLMError(f"Unsupported provider {spec.provider}")
    latency_ms = int((time.perf_counter() - t0) * 1000)

    _validate_schema(data, schema)
    return LLMResult(
        data=data, raw_text=raw, tokens_in=tin, tokens_out=tout,
        latency_ms=latency_ms, model=spec.id, provider=spec.provider,
    )


def _validate_schema(data: Dict[str, Any], schema: Dict[str, Any]) -> None:
    try:
        Draft202012Validator(schema).validate(data)
    except Exception as exc:
        raise SchemaValidationError(f"Schema validation failed: {exc}") from exc


# ------------------------- Anthropic -------------------------
def _call_anthropic(
    spec: ModelSpec, system: str, user_text: str, schema: dict,
    tool_name: str, max_tokens: int, temperature: float,
) -> Tuple[dict, str, int, int]:
    from anthropic import Anthropic

    client = Anthropic(api_key=settings.anthropic_api_key)
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
    for block in resp.content:
        if getattr(block, "type", None) == "tool_use" and block.name == tool_name:
            return block.input, json.dumps(block.input, ensure_ascii=False), tin, tout
    raw = json.dumps([b.model_dump() if hasattr(b, "model_dump") else str(b) for b in resp.content])
    raise LLMError(f"Anthropic returned no tool_use block: {raw[:300]}")


# ------------------------- OpenAI -------------------------
def _call_openai(
    spec: ModelSpec, system: str, user_text: str, schema: dict,
    tool_name: str, max_tokens: int, temperature: float,
) -> Tuple[dict, str, int, int]:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
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

    dashscope.api_key = settings.dashscope_api_key
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
        api_key=settings.deepseek_api_key,
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
    if spec.provider == "anthropic":
        from anthropic import Anthropic

        client = Anthropic(api_key=settings.anthropic_api_key)
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
        api_key = getattr(settings, f"{spec.provider}_api_key")
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
