from __future__ import annotations

import os
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv():
        return False


load_dotenv()


def resolve_api_key(streamlit_secrets: Any | None = None) -> str | None:
    env_key = os.getenv("OPENAI_API_KEY")
    if env_key:
        return env_key
    if streamlit_secrets is not None:
        try:
            return streamlit_secrets.get("OPENAI_API_KEY") or streamlit_secrets.get("openai_api_key")
        except Exception:
            return None
    return None


def call_openai_chat(messages: list[dict[str, str]], model: str, temperature: float, api_key: str) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(model=model, messages=messages, temperature=temperature)
    return response.choices[0].message.content or ""
