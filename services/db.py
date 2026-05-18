"""Supabase data access layer.

Provides fetch_recipes() which returns all recipe rows from Supabase.
If Supabase credentials are not configured the function returns an empty
list and the caller (matcher.load_recipes) falls back to the local JSON file.
"""
from __future__ import annotations

import streamlit as st
from streamlit.errors import StreamlitSecretNotFoundError


def _get_secret(name: str) -> str | None:
    try:
        value = st.secrets[name]
    except (KeyError, StreamlitSecretNotFoundError):
        return None
    value = str(value).strip()
    return value or None


def fetch_recipes() -> list[dict]:
    """Fetch all recipes from Supabase.

    Returns an empty list if credentials are missing or the query fails,
    allowing the caller to fall back gracefully to the local JSON file.
    """
    url = _get_secret("SUPABASE_URL")
    key = _get_secret("SUPABASE_KEY")
    if not url or not key:
        return []

    try:
        from supabase import create_client  # imported lazily so the app runs without supabase installed

        client = create_client(url, key)
        response = (
            client.table("recipes")
            .select("id, name, description, difficulty, serving_size, base_spirit, flavor_tags, ingredients, steps")
            .order("name")
            .execute()
        )
        return response.data or []
    except Exception:
        return []
