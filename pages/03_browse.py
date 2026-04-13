"""Browse all cocktails (HangoverGPT 🍹)."""

from __future__ import annotations

import json
import math
from pathlib import Path

import streamlit as st

_DATA = Path(__file__).resolve().parent.parent / "data" / "recipes.json"
_PAGES_DIR = Path(__file__).resolve().parent

_COLS = 3
_PAGE_SIZE = 24
_COLOR_CYCLE = ("blue", "violet", "orange", "green", "red", "cyan")


def _detail_page_script_path() -> str:
    """First existing detail page for st.switch_page; else fallback."""
    for fname in ("04_detail.py", "03_detail.py", "detail.py"):
        if (_PAGES_DIR / fname).is_file():
            return f"pages/{fname}"
    return "pages/03_detail.py"


@st.cache_data(show_spinner=False)
def _load_recipes() -> list[dict]:
    with _DATA.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise TypeError("recipes.json must be a JSON array")
    return data


def _tag_badges_md(tags: list[str]) -> str:
    parts: list[str] = []
    for i, tag in enumerate(tags):
        color = _COLOR_CYCLE[i % len(_COLOR_CYCLE)]
        parts.append(f":{color}[{tag}]")
    return " &nbsp;".join(parts)


def _render_card(recipe: dict, detail_target: str) -> None:
    name = recipe.get("name", "Untitled")
    rid = str(recipe.get("id", name))
    difficulty = recipe.get("difficulty", "—")
    ingredients = recipe.get("ingredients") or []
    base_spirit = ingredients[0].get("name", "—") if ingredients else "—"
    tags = recipe.get("flavor_tags") or []

    with st.container(border=True):
        st.markdown(f"##### {name}")
        st.markdown(
            f"**Difficulty** · `{difficulty}`  \n**Base spirit** · {base_spirit}"
        )
        if tags:
            st.markdown(_tag_badges_md(tags))
        if st.button(
            "View recipe",
            key=f"browse_open_{rid}",
            use_container_width=True,
        ):
            st.session_state["selected_recipe"] = json.loads(json.dumps(recipe))
            st.switch_page(detail_target)


st.set_page_config(page_title="Browse | HangoverGPT 🍹", page_icon="🍹", layout="wide")

st.markdown("# 🍹 Browse All Cocktails")

recipes = _load_recipes()
total = len(recipes)
_recipe_word = "recipe" if total == 1 else "recipes"
st.markdown(f"**{total}** {_recipe_word} available")
st.divider()

if not recipes:
    st.info("No recipes in the library yet.")
    st.stop()

detail_target = _detail_page_script_path()

if total > _PAGE_SIZE:
    n_pages = max(1, math.ceil(total / _PAGE_SIZE))
    page_ix = st.select_slider(
        "Page",
        options=list(range(n_pages)),
        format_func=lambda i: f"{i + 1} / {n_pages}",
        key="browse_page_slider",
    )
    start = page_ix * _PAGE_SIZE
    visible = recipes[start : start + _PAGE_SIZE]
else:
    visible = recipes

for row_start in range(0, len(visible), _COLS):
    row_items = visible[row_start : row_start + _COLS]
    columns = st.columns(_COLS, gap="medium")
    for col, rec in zip(columns, row_items):
        with col:
            _render_card(rec, detail_target)
