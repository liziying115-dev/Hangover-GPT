"""Browse all cocktails (HangoverGPT 🍹)."""

from __future__ import annotations

import json
import math
import re
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


def _first_ingredient_name(recipe: dict) -> str:
    ingredients = recipe.get("ingredients") or []
    if not ingredients:
        return ""
    return str(ingredients[0].get("name", "")).strip()


def _canonical_base_spirit(first_ingredient: str) -> str:
    """Map first ingredient to a display/filter label (avoid false 'gin' in 'ginger')."""
    if not first_ingredient:
        return "Other"
    lower = first_ingredient.strip().lower()
    if re.search(r"\bvodka\b", lower) or lower.startswith("vodka"):
        return "Vodka"
    if "tequila" in lower or "mezcal" in lower:
        return "Tequila"
    if re.search(
        r"\b(bourbon|whiskey|whisky|scotch|rye)\b",
        lower,
    ) or "whiskey" in lower or "whisky" in lower:
        return "Whiskey"
    if "rum" in lower:
        return "Rum"
    if re.search(r"\bgin\b", lower):
        return "Gin"
    if "brandy" in lower or "cognac" in lower:
        return "Brandy"
    return first_ingredient[:1].upper() + first_ingredient[1:] if first_ingredient else "Other"


def _base_spirit_labels(recipes: list[dict]) -> list[str]:
    labels = {_canonical_base_spirit(_first_ingredient_name(r)) for r in recipes}
    return sorted(labels, key=str.lower)


def _flavor_tag_options(recipes: list[dict]) -> list[str]:
    seen: dict[str, str] = {}
    for r in recipes:
        for t in r.get("flavor_tags") or []:
            s = str(t).strip()
            if not s:
                continue
            key = s.lower()
            if key not in seen:
                seen[key] = s
    return sorted(seen.values(), key=str.lower)


def _recipe_flavor_set(recipe: dict) -> set[str]:
    return {str(t).strip().lower() for t in (recipe.get("flavor_tags") or []) if str(t).strip()}


def _filter_recipes(
    recipes: list[dict],
    search_query: str,
    base_spirits: list[str],
    flavor_profiles: list[str],
    difficulty: str,
) -> list[dict]:
    q = search_query.strip().lower()
    bases_sel = {b.lower() for b in base_spirits}
    flavors_sel = {f.strip().lower() for f in flavor_profiles if f.strip()}
    diff_sel = difficulty.strip().lower()

    out: list[dict] = []
    for r in recipes:
        name = str(r.get("name", "")).lower()
        if q and q not in name:
            continue
        if bases_sel:
            canon = _canonical_base_spirit(_first_ingredient_name(r))
            if canon.lower() not in bases_sel:
                continue
        if flavors_sel:
            r_tags = _recipe_flavor_set(r)
            if not flavors_sel.issubset(r_tags):
                continue
        if diff_sel and diff_sel != "all":
            rd = str(r.get("difficulty", "")).strip().lower()
            if rd != diff_sel:
                continue
        out.append(r)
    return out


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

if not recipes:
    st.info("No recipes in the library yet.")
    st.stop()

total_all = len(recipes)
base_spirits = _base_spirit_labels(recipes)
flavor_profiles = _flavor_tag_options(recipes)

# Initialize defaults BEFORE widgets
if "browse_search_query" not in st.session_state:
    st.session_state["browse_search_query"] = ""
if "browse_base_spirit" not in st.session_state:
    st.session_state["browse_base_spirit"] = []
if "browse_flavor_profile" not in st.session_state:
    st.session_state["browse_flavor_profile"] = []
if "browse_difficulty" not in st.session_state:
    st.session_state["browse_difficulty"] = "All"


# Clear callback - deletes keys so defaults are re-applied on next run
def clear_filters() -> None:
    del st.session_state["browse_search_query"]
    del st.session_state["browse_base_spirit"]
    del st.session_state["browse_flavor_profile"]
    del st.session_state["browse_difficulty"]


st.text_input("Search cocktails", placeholder="Type a name...", key="browse_search_query")

f1, f2, f3, f4 = st.columns([2, 2, 2, 1])
with f1:
    st.multiselect("Base spirit", options=base_spirits, key="browse_base_spirit")
with f2:
    st.multiselect("Flavor profile", options=flavor_profiles, key="browse_flavor_profile")
with f3:
    st.selectbox(
        "Difficulty",
        options=["All", "easy", "medium", "hard"],
        key="browse_difficulty",
    )
with f4:
    st.button("Clear Filters", on_click=clear_filters, use_container_width=True)

filtered = _filter_recipes(
    recipes,
    st.session_state["browse_search_query"],
    st.session_state["browse_base_spirit"],
    st.session_state["browse_flavor_profile"],
    st.session_state["browse_difficulty"],
)

shown = len(filtered)
st.markdown(f"**Showing {shown} of {total_all} recipes**")
st.divider()

if shown == 0:
    st.info("No cocktails found 😢 Try adjusting your filters!")
    st.stop()

detail_target = _detail_page_script_path()

if shown > _PAGE_SIZE:
    n_pages = max(1, math.ceil(shown / _PAGE_SIZE))
    page_ix = st.select_slider(
        "Page",
        options=list(range(n_pages)),
        format_func=lambda i: f"{i + 1} / {n_pages}",
        key="browse_page_slider",
    )
    start = page_ix * _PAGE_SIZE
    visible = filtered[start : start + _PAGE_SIZE]
else:
    visible = filtered

for row_start in range(0, len(visible), _COLS):
    row_items = visible[row_start : row_start + _COLS]
    columns = st.columns(_COLS, gap="medium")
    for col, rec in zip(columns, row_items):
        with col:
            _render_card(rec, detail_target)
