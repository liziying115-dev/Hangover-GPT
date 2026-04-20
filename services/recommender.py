"""AI-powered cocktail recommendations via Minimax API (OpenAI-compatible)."""
from __future__ import annotations

import json
import streamlit as st
from openai import APIConnectionError, APITimeoutError, OpenAI, OpenAIError
from streamlit.errors import StreamlitSecretNotFoundError

DEFAULT_MINIMAX_BASE_URL = "https://api.minimax.chat/v1"
MINIMAX_MODEL = "MiniMax-Text-01"

SYSTEM_PROMPT = (
    "You are a professional cocktail consultant. When given a flavor preference or mood, "
    "return ONLY a JSON array of 3-5 cocktail recommendations. No prose, no markdown fences. "
    "Each object must have: name, description, flavor_tags (array), difficulty (easy/medium/hard), "
    "base_spirit, ingredients (array of strings), why (one sentence explaining the match)."
)


def _get_secret(name: str) -> str | None:
    try:
        value = st.secrets[name]
    except (KeyError, StreamlitSecretNotFoundError):
        return None
    value = str(value).strip()
    return value or None


def _get_base_url() -> str:
    try:
        value = st.secrets.get("MINIMAX_BASE_URL", DEFAULT_MINIMAX_BASE_URL)
    except StreamlitSecretNotFoundError:
        return DEFAULT_MINIMAX_BASE_URL
    value = str(value).strip()
    return value or DEFAULT_MINIMAX_BASE_URL


def _parse_recommendations(content: str) -> list[dict]:
    payload = json.loads(content.strip())
    if not isinstance(payload, list):
        return []
    return payload


def get_recommendations(preference: str) -> list[dict]:
    """Call Minimax API and return 3-5 structured recipe suggestions.

    Returns [] on API failure or unparseable response.
    Caller should cache results in st.session_state['ai_recommendations'].
    """
    api_key = _get_secret("MINIMAX_API_KEY")
    if not api_key:
        return []

    client = OpenAI(api_key=api_key, base_url=_get_base_url())

    try:
        response = client.chat.completions.create(
            model=MINIMAX_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        f"Flavor preference or mood: {preference}\n"
                        "Return only the JSON array."
                    ),
                },
            ],
            max_tokens=1024,
            temperature=0.7,
        )
        content = response.choices[0].message.content or "[]"
        return _parse_recommendations(content)
    except (json.JSONDecodeError, APIConnectionError, APITimeoutError, OpenAIError, OSError):
        return []
