"""
config.py — Model registry and API clients for Group 7 LLM robustness tests.
All models referenced correspond to those tested in the original papers,
plus current frontier equivalents for updated verification.
"""

import os
import base64
import json
from dataclasses import dataclass
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ─────────────────────────────────────────────
# Model Registry
# Maps current API model IDs to paper context
# ─────────────────────────────────────────────

MODELS = {
    # OpenAI
    "gpt-4o": {
        "api": "openai",
        "model_id": "gpt-4o",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_GPT_4O", "openai/gpt-4o"),
        "vision": True,
        "notes": "Successor to GPT-4V tested in Chen 2024, Mecattaf 2024, Zhang 2024c",
        "paper_equivalent": "GPT-4V / GPT-4o (Rahmanzadehgervi 2024)"
    },
    "gpt-5": {
        "api": "openrouter",
        "model_id": "gpt-5",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_GPT_5", "openai/gpt-5.4"),
        "vision": True,
        "notes": "Newer GPT-5 family model via OpenRouter",
        "paper_equivalent": None
    },
    "gpt-5-mini": {
        "api": "openrouter",
        "model_id": "gpt-5-mini",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_GPT_5_MINI", "openai/gpt-5.4-mini"),
        "vision": True,
        "notes": "Smaller GPT-5 family model via OpenRouter",
        "paper_equivalent": None
    },
    "gpt-4o-mini": {
        "api": "openai",
        "model_id": "gpt-4o-mini",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_GPT_4O_MINI", "openai/gpt-4.1-mini"),
        "vision": True,
        "notes": "Lightweight GPT-4o for cost-effective batch testing",
        "paper_equivalent": None
    },
    "o3-mini": {
        "api": "openai",
        "model_id": "o3-mini",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_O3_MINI", "openai/o3-mini"),
        "vision": False,
        "notes": "Reasoning model tested in Rezaei 2025 (EgoNormia) — chose railing over photo",
        "paper_equivalent": "o3-mini (Rezaei 2025)"
    },
    # Anthropic
    "claude-sonnet-4-6": {
        "api": "anthropic",
        "model_id": "claude-sonnet-4-6",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_CLAUDE", "anthropic/claude-sonnet-4.6"),
        "vision": True,
        "notes": "Current Claude. Predecessor Sonnet-3/3.5 tested in Rahmanzadehgervi 2024",
        "paper_equivalent": "Claude Sonnet-3.5 (Rahmanzadehgervi 2024)"
    },
    "claude-3-7-sonnet": {
        "api": "openrouter",
        "model_id": "claude-3-7-sonnet",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_CLAUDE_3_7", "anthropic/claude-3.7-sonnet"),
        "vision": True,
        "notes": "Legacy Claude Sonnet baseline via OpenRouter",
        "paper_equivalent": "Claude Sonnet-3.5 class baseline"
    },
    "claude-3-5-haiku": {
        "api": "openrouter",
        "model_id": "claude-3-5-haiku",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_CLAUDE_HAIKU", "anthropic/claude-3.5-haiku"),
        "vision": True,
        "notes": "Claude Haiku baseline via OpenRouter",
        "paper_equivalent": None
    },
    "gemini-2-5-pro": {
        "api": "openrouter",
        "model_id": "gemini-2-5-pro",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_GEMINI_2_5", "google/gemini-2.5-pro"),
        "vision": True,
        "notes": "Google Gemini 2.5 Pro via OpenRouter",
        "paper_equivalent": "Gemini family baseline"
    },
    "gemini-3-1-pro": {
        "api": "openrouter",
        "model_id": "gemini-3-1-pro",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_GEMINI_3_1", "google/gemini-3.1-pro-preview"),
        "vision": True,
        "notes": "Newer Gemini 3.1 Pro preview via OpenRouter",
        "paper_equivalent": None
    },
    "llama-3-3-70b": {
        "api": "openrouter",
        "model_id": "llama-3-3-70b",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_LLAMA_3_3", "meta-llama/llama-3.3-70b-instruct"),
        "vision": False,
        "notes": "Open-source Llama 3.3 70B via OpenRouter",
        "paper_equivalent": "LLaMA-family open model"
    },
    "qwen3-next-80b": {
        "api": "openrouter",
        "model_id": "qwen3-next-80b",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_QWEN3_NEXT", "qwen/qwen3-next-80b-a3b-instruct"),
        "vision": False,
        "notes": "Open-source Qwen3 Next 80B via OpenRouter",
        "paper_equivalent": "Qwen-family open model"
    },
    "deepseek-r1": {
        "api": "openrouter",
        "model_id": "deepseek-r1",
        "openrouter_model_id": os.getenv("OPENROUTER_MODEL_DEEPSEEK_R1", "deepseek/deepseek-r1"),
        "vision": False,
        "notes": "Open-source DeepSeek R1 reasoning model via OpenRouter",
        "paper_equivalent": "DeepSeek-R1 class model"
    },
}

# Models tested in each paper (for documentation/reporting)
PAPER_MODELS = {
    "whoops_bitton2023":          ["BLIP-2", "LLaVA-1.3", "MiniGPT-4", "OFA"],
    "blindtest_rahmanzadehgervi2024": ["GPT-4o", "Gemini-1.5", "Claude Sonnet-3", "Claude Sonnet-3.5"],
    "rome_zhou2023":              ["CLIP-ViT-L/14", "BLIP-2", "OFA", "GPT-4V"],
    "visual_spatial_liu2023":     ["OFA", "BLIP", "FLAVA", "VinVL", "ViLBERT", "ALBEF", "TCL", "12+ VLMs"],
    "binding_campbell2025":       ["GPT-4V", "LLaVA-1.6-34B", "InstructBLIP", "IDEFICS-80B"],
    "ambiguous_spatial_zhao2024": ["GPT-4V", "Gemini-Pro-Vision", "LLaVA-1.5-13B"],
    "spatialvlm_chen2024":        ["GPT-4V", "LLaVA-1.5", "InstructBLIP", "BLIP-2"],
    "embodied_mecattaf2024":      ["GPT-4", "GPT-3.5-turbo", "LLaMA-2-70B", "Gemini-Pro"],
    "tool_use_xu2023":            ["GPT-4", "GPT-3.5-turbo", "Codex (code-davinci-002)"],
    "alphamaze_dao2025":          ["LLaMA-3.1-8B-Instruct", "Qwen2.5-7B", "DeepSeek-R1-Distill"],
    "robotic_guran2024":          ["GPT-4V", "LLaVA-1.5-13B", "CogVLM-17B"],
    "code_as_policies_liang2023": ["Codex (code-davinci-002)", "GPT-3", "GPT-3.5-turbo"],
    "badrobot_zhang2024":         ["GPT-4V", "LLaVA-1.5-13B", "MiniGPT-4-13B"],
    "egonormia_rezaei2025":       ["o3-mini", "GPT-4o", "Claude-3.5-Sonnet"],
}


# ─────────────────────────────────────────────
# API Clients
# ─────────────────────────────────────────────

def get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_openrouter_client():
    from openai import OpenAI

    headers = {}
    site_url = os.getenv("OPENROUTER_SITE_URL")
    app_name = os.getenv("OPENROUTER_APP_NAME")
    if site_url:
        headers["HTTP-Referer"] = site_url
    if app_name:
        headers["X-Title"] = app_name

    return OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url=os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"),
        default_headers=headers or None,
    )


def get_anthropic_client():
    import anthropic
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def call_model(model_key: str, prompt: str, image_path: Optional[str] = None,
               system: Optional[str] = None, max_tokens: int = 512) -> str:
    """
    Unified call interface for all models.
    Returns the model's text response.
    """
    cfg = MODELS[model_key]

    use_openrouter = bool(os.getenv("OPENROUTER_API_KEY"))

    if use_openrouter:
        client = get_openrouter_client()
        model_id = cfg.get("openrouter_model_id") or cfg["model_id"]

        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        if image_path and cfg["vision"]:
            b64 = image_to_base64(image_path)
            ext = image_path.rsplit(".", 1)[-1].lower()
            mime = f"image/{ext}" if ext in ("png", "jpg", "jpeg", "webp", "gif") else "image/png"
            messages.append({
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    {"type": "text", "text": prompt}
                ]
            })
        else:
            messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": model_id,
            "messages": messages,
        }

        normalized_id = model_id.split("/", 1)[-1]
        if normalized_id.startswith("o"):
            kwargs["max_completion_tokens"] = max(max_tokens, 512)
        elif "gemini" in normalized_id:
            kwargs["max_tokens"] = max(max_tokens, 256)
        else:
            kwargs["max_tokens"] = max_tokens

        response = client.chat.completions.create(**kwargs)
        content = response.choices[0].message.content
        if isinstance(content, str):
            return content.strip()
        if isinstance(content, list):
            parts = []
            for item in content:
                text = item.get("text") if isinstance(item, dict) else getattr(item, "text", "")
                if text:
                    parts.append(text)
            return "\n".join(parts).strip()
        return ""

    if cfg["api"] == "openrouter":
        raise ValueError(
            f"Model '{model_key}' requires OpenRouter. Set OPENROUTER_API_KEY in environment."
        )

    if cfg["api"] == "openai":
        client = get_openai_client()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})

        if image_path and cfg["vision"]:
            b64 = image_to_base64(image_path)
            ext = image_path.rsplit(".", 1)[-1].lower()
            mime = f"image/{ext}" if ext in ("png", "jpg", "jpeg", "webp", "gif") else "image/png"
            messages.append({
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    {"type": "text", "text": prompt}
                ]
            })
        else:
            messages.append({"role": "user", "content": prompt})

        kwargs = {
            "model": cfg["model_id"],
            "messages": messages,
        }
        if cfg["model_id"].startswith("o"):
            kwargs["max_completion_tokens"] = max(max_tokens, 512)
        else:
            kwargs["max_tokens"] = max_tokens

        response = client.chat.completions.create(**kwargs)
        return response.choices[0].message.content.strip()

    elif cfg["api"] == "anthropic":
        client = get_anthropic_client()
        content = []
        if image_path and cfg["vision"]:
            b64 = image_to_base64(image_path)
            ext = image_path.rsplit(".", 1)[-1].lower()
            mime = f"image/{ext}" if ext in ("png", "jpg", "jpeg", "webp", "gif") else "image/png"
            content.append({"type": "image", "source": {"type": "base64", "media_type": mime, "data": b64}})
        content.append({"type": "text", "text": prompt})

        kwargs = {
            "model": cfg["model_id"],
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": content}]
        }
        if system:
            kwargs["system"] = system

        response = client.messages.create(**kwargs)
        return response.content[0].text.strip()

    raise ValueError(f"Unknown API for model: {model_key}")


# ─────────────────────────────────────────────
# Result Logger
# ─────────────────────────────────────────────

def log_result(paper: str, test_id: str, failure_type: str, model: str,
               prompt: str, expected: str, actual: str, passed: bool, notes: str = ""):
    result = {
        "paper": paper,
        "test_id": test_id,
        "failure_type": failure_type,
        "model": model,
        "paper_models": PAPER_MODELS.get(test_id, []),
        "prompt": prompt[:300] + "..." if len(prompt) > 300 else prompt,
        "expected_answer": expected,
        "model_answer": actual[:200] if actual else "",
        "passed": passed,
        "notes": notes
    }
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {test_id} | {model} | expected={expected!r} | got={actual[:60]!r}")
    return result
