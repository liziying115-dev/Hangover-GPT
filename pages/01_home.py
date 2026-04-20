"""Home page — ingredient input and AI preference entry."""

from __future__ import annotations

import streamlit as st

from components.brand import apply_global_style, render_brand_header
from services.matcher import load_recipes
from services.recommender import get_recommendations


st.set_page_config(page_title="Pour Decisions 🍹", page_icon="🍹", layout="wide")


@st.cache_data(show_spinner=False)
def _ingredient_options() -> list[str]:
    ingredients: set[str] = set()
    for recipe in load_recipes():
        for ingredient in recipe.get("ingredients", []):
            ingredients.add(ingredient["name"])
    return sorted(ingredients)


def _parse_custom_ingredients(raw_value: str) -> list[str]:
    normalized = raw_value.replace("\n", ",")
    return [value.strip() for value in normalized.split(",") if value.strip()]


def _reset_result_state() -> None:
    st.session_state["selected_recipe"] = {}
    st.session_state["current_step_index"] = 0


def _submit_ingredient_search(selected_ingredients: list[str], custom_ingredients: str) -> None:
    combined = selected_ingredients + _parse_custom_ingredients(custom_ingredients)
    deduped: list[str] = []
    seen: set[str] = set()
    for ingredient in combined:
        key = ingredient.strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        deduped.append(ingredient.strip())

    st.session_state["user_ingredients"] = deduped
    st.session_state["ai_recommendations"] = []
    st.session_state["ai_preference"] = ""
    st.session_state["ai_recommendations_error"] = False
    _reset_result_state()
    st.switch_page("pages/03_results.py")


def _submit_ai_search(preference: str) -> None:
    preference = preference.strip()
    st.session_state["user_ingredients"] = []
    _reset_result_state()

    cached_preference = st.session_state.get("ai_preference", "")
    cached_recommendations = st.session_state.get("ai_recommendations", [])
    if preference and preference == cached_preference and cached_recommendations:
        st.switch_page("pages/03_results.py")

    with st.spinner("Mixing up recommendations..."):
        recommendations = get_recommendations(preference)

    st.session_state["ai_preference"] = preference
    st.session_state["ai_recommendations"] = recommendations
    st.session_state["ai_recommendations_error"] = not bool(recommendations)
    st.switch_page("pages/03_results.py")


apply_global_style()
render_brand_header(
    "Find Your Next Pour",
    "Start with ingredients you already have, or describe the mood and let the app shape a cocktail direction for you.",
    kicker="Pour Decisions",
)
st.markdown(
    """
    <div class="pd-chip-row">
      <span class="pd-chip">Warm citrus</span>
      <span class="pd-chip">Spirit-forward classics</span>
      <span class="pd-chip">Fruity low-effort picks</span>
      <span class="pd-chip">No blank results</span>
    </div>
    """,
    unsafe_allow_html=True,
)

ingredient_options = _ingredient_options()

search_col, ai_col = st.columns([1, 1], gap="large")

with search_col:
    with st.form("ingredient-match-form"):
        st.subheader("Match cocktails from your bar")
        selected_ingredients = st.multiselect(
            "Select ingredients you already have",
            options=ingredient_options,
            placeholder="Choose one or more ingredients",
        )
        custom_ingredients = st.text_area(
            "Add custom ingredients",
            placeholder="Example: orange juice, soda water, cinnamon syrup",
            help="Use commas or new lines to enter ingredients not listed above.",
        )
        ingredient_submitted = st.form_submit_button("Find matching cocktails", use_container_width=True)

if ingredient_submitted:
    if not selected_ingredients and not custom_ingredients.strip():
        st.warning("Add at least one ingredient before searching.")
    else:
        _submit_ingredient_search(selected_ingredients, custom_ingredients)

with ai_col:
    with st.form("ai-recommendation-form"):
        st.subheader("Get AI recommendations")
        preference = st.text_area(
            "Describe your mood or flavor preference",
            placeholder="Example: something citrusy and refreshing, or rich and spirit-forward",
        )
        ai_submitted = st.form_submit_button("Get AI suggestions", use_container_width=True)

if ai_submitted:
    if not preference.strip():
        st.warning("Enter a mood or flavor preference before asking for AI suggestions.")
    else:
        _submit_ai_search(preference)
