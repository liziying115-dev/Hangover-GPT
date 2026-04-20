"""Browse page — full cocktail list with search and filter (Issues #4, #5)."""

from __future__ import annotations

import streamlit as st

from components.brand import apply_global_style, render_brand_header
from components.recipe_card import recipe_card
from services.matcher import load_recipes


st.set_page_config(page_title="Browse Cocktails", page_icon="🍹", layout="wide")
apply_global_style()


@st.cache_data(show_spinner=False)
def get_recipes() -> list[dict]:
    """Load the seeded recipe store once per session."""
    recipes = load_recipes()
    return [recipe for recipe in recipes if isinstance(recipe, dict)]


def _facet_key(value: str) -> str:
    return " ".join(value.strip().lower().replace("-", " ").split())


def _name_key(value: str) -> str:
    return value.strip().casefold()


def _sorted_unique_values(recipes: list[dict], field: str) -> list[str]:
    values: set[str] = set()
    for recipe in recipes:
        raw_value = recipe.get(field)
        if isinstance(raw_value, str) and raw_value.strip():
            values.add(raw_value.strip())
    return sorted(values, key=_facet_key)


def _sorted_unique_tags(recipes: list[dict]) -> list[str]:
    values: set[str] = set()
    for recipe in recipes:
        for tag in recipe.get("flavor_tags") or []:
            if isinstance(tag, str) and tag.strip():
                values.add(tag.strip())
    return sorted(values, key=_facet_key)


def _reset_filters() -> None:
    st.session_state["browse_name_query"] = ""
    st.session_state["browse_base_spirit_filters"] = []
    st.session_state["browse_flavor_profile_filters"] = []
    st.session_state["browse_difficulty_filters"] = []
    st.rerun()


def _matches_filters(
    recipe: dict,
    name_query: str,
    base_spirit_filters: list[str],
    flavor_profile_filters: list[str],
    difficulty_filters: list[str],
) -> bool:
    if name_query and _name_key(name_query) not in _name_key(str(recipe.get("name", ""))):
        return False

    if base_spirit_filters and _facet_key(str(recipe.get("base_spirit", ""))) not in {
        _facet_key(value) for value in base_spirit_filters
    }:
        return False

    if difficulty_filters and _facet_key(str(recipe.get("difficulty", ""))) not in {
        _facet_key(value) for value in difficulty_filters
    }:
        return False

    if flavor_profile_filters:
        recipe_flavors = {_facet_key(tag) for tag in (recipe.get("flavor_tags") or []) if isinstance(tag, str)}
        selected_flavors = {_facet_key(value) for value in flavor_profile_filters}
        if not recipe_flavors.intersection(selected_flavors):
            return False

    return True


def render_recipe_grid(recipes: list[dict]) -> None:
    """Render recipes in a responsive grid."""
    if not recipes:
        st.warning("No cocktails were found in the recipe store.")
        return

    columns_per_row = 3
    for row_start in range(0, len(recipes), columns_per_row):
        row = recipes[row_start : row_start + columns_per_row]
        columns = st.columns(len(row))
        for column, recipe in zip(columns, row):
            with column:
                recipe_card(recipe)


render_brand_header(
    "Browse the Back Bar",
    "Scan the full catalog, then narrow it with search and layered filters until the right glass stands out.",
    kicker="Pour Decisions",
)

recipes = get_recipes()
base_spirit_options = _sorted_unique_values(recipes, "base_spirit")
flavor_profile_options = _sorted_unique_tags(recipes)
difficulty_options = _sorted_unique_values(recipes, "difficulty")

st.subheader("Search and filters")
controls_top, controls_button = st.columns([6, 1], vertical_alignment="bottom")
with controls_top:
    name_query = st.text_input(
        "Search by cocktail name",
        key="browse_name_query",
        placeholder="Type part of a cocktail name",
    )
with controls_button:
    if st.button("Clear filters", use_container_width=True):
        _reset_filters()

filter_col_1, filter_col_2, filter_col_3 = st.columns(3)
with filter_col_1:
    base_spirit_filters = st.multiselect(
        "Base spirit",
        options=base_spirit_options,
        key="browse_base_spirit_filters",
        placeholder="All base spirits",
    )
with filter_col_2:
    flavor_profile_filters = st.multiselect(
        "Flavor profile",
        options=flavor_profile_options,
        key="browse_flavor_profile_filters",
        placeholder="All flavor profiles",
    )
with filter_col_3:
    difficulty_filters = st.multiselect(
        "Difficulty",
        options=difficulty_options,
        key="browse_difficulty_filters",
        placeholder="All difficulty levels",
    )

filtered_recipes = [
    recipe
    for recipe in recipes
    if _matches_filters(recipe, name_query, base_spirit_filters, flavor_profile_filters, difficulty_filters)
]

st.write(f"{len(filtered_recipes)} of {len(recipes)} cocktails match your filters.")

if not filtered_recipes:
    st.info(
        "No cocktails match the current search and filter combination. "
        "Try clearing one filter, broadening your search, or click Clear filters to restore the full list."
    )
else:
    render_recipe_grid(filtered_recipes)
