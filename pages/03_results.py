"""Results page for ingredient matches and AI recommendations."""

from __future__ import annotations

import streamlit as st

from components.brand import apply_global_style, render_brand_header
from services.matcher import load_recipes, match_recipes


st.set_page_config(page_title="Results", page_icon="🍹", layout="wide")
apply_global_style()


@st.cache_data(show_spinner=False)
def _recipes() -> list[dict]:
    return load_recipes()


def _open_detail(recipe: dict) -> None:
    st.session_state["selected_recipe"] = recipe
    st.session_state["serving_multiplier"] = 1
    st.session_state["current_step_index"] = 0
    st.switch_page("pages/04_detail.py")


def _render_match_card(recipe: dict) -> None:
    with st.container(border=True):
        top_left, top_right = st.columns([4, 1])
        with top_left:
            st.markdown(f"### {recipe['name']}")
            st.caption(recipe["description"])
        with top_right:
            st.caption(f"`{recipe['match_type']}`")
            st.caption(recipe["difficulty"].title())

        st.markdown(
            f"**Required ingredients:** {', '.join(ingredient['name'] for ingredient in recipe.get('ingredients', []))}"
        )
        if recipe.get("missing"):
            st.markdown(f"**Missing:** {', '.join(recipe['missing'])}")
        else:
            st.success("You have everything needed for this cocktail.")

        if st.button("View details", key=f"results_{recipe['id']}", use_container_width=True):
            _open_detail(recipe)


def _render_ai_card(recommendation: dict, index: int) -> None:
    name = recommendation.get("name", f"Suggestion {index}")
    description = recommendation.get("description", "No description provided.")
    difficulty = str(recommendation.get("difficulty", "unknown")).title()
    base_spirit = str(recommendation.get("base_spirit", "unknown")).replace("-", " ").title()
    flavor_tags = recommendation.get("flavor_tags") or []
    ingredients = recommendation.get("ingredients") or []
    why = recommendation.get("why", "No recommendation rationale was returned.")

    with st.container(border=True):
        st.markdown(f"### {name}")
        st.caption(description)
        st.markdown(f"**Difficulty:** {difficulty}  |  **Base spirit:** {base_spirit}")
        if flavor_tags:
            st.write(" ".join(f"`{tag}`" for tag in flavor_tags))
        if ingredients:
            st.markdown(f"**Ingredients:** {', '.join(ingredients)}")
        st.markdown(f"**Why this fits:** {why}")


render_brand_header(
    "Results Worth Pouring",
    "Compare exact matches, near misses, and AI suggestions without losing the thread between search and selection.",
    kicker="Pour Decisions",
)

recipes = _recipes()
user_ingredients = st.session_state.get("user_ingredients", [])
ai_preference = st.session_state.get("ai_preference", "").strip()
ai_recommendations = st.session_state.get("ai_recommendations", [])
ai_error = st.session_state.get("ai_recommendations_error", False)
matches = match_recipes(user_ingredients, recipes) if user_ingredients else []

if user_ingredients:
    st.subheader("Ingredient Matches")
    st.caption(f"Searching with: {', '.join(user_ingredients)}")
    if matches:
        exact_matches = [recipe for recipe in matches if recipe["match_type"] == "exact"]
        partial_matches = [recipe for recipe in matches if recipe["match_type"] == "partial"]

        if exact_matches:
            st.markdown("#### Exact matches")
            for recipe in exact_matches:
                _render_match_card(recipe)

        if partial_matches:
            st.markdown("#### Partial matches")
            for recipe in partial_matches:
                _render_match_card(recipe)
    else:
        st.info("No cocktails matched those ingredients yet. Try adding another base spirit, citrus, or sweetener.")
elif not ai_preference:
    st.info("Start from the home page to search by ingredients or request AI suggestions.")

if ai_preference:
    st.subheader("AI Recommendations")
    st.caption(f"Prompt: {ai_preference}")
    if ai_recommendations:
        for index, recommendation in enumerate(ai_recommendations, start=1):
            _render_ai_card(recommendation, index)
    elif ai_error:
        st.warning("The AI recommendation request did not return usable results. Try a different prompt or check your API configuration.")
