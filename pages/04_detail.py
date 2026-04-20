"""Recipe detail page with serving size scaler."""

from __future__ import annotations

import streamlit as st

from components.brand import apply_global_style, render_brand_header
from services.matcher import load_recipes
from services.scaler import format_quantity, scale_recipe


st.set_page_config(page_title="Recipe Detail", page_icon="🍹", layout="centered")
apply_global_style()


def _ensure_session_state() -> None:
    st.session_state.setdefault("selected_recipe", {})
    st.session_state.setdefault("serving_multiplier", 1)
    st.session_state.setdefault("current_step_index", 0)


@st.cache_data(show_spinner=False)
def _recipes() -> list[dict]:
    return load_recipes()


def _recipe_index(recipes: list[dict], selected_id: str | None) -> int:
    for index, recipe in enumerate(recipes):
        if recipe["id"] == selected_id:
            return index
    return 0


def _recipe_summary(recipe: dict, multiplier: int) -> None:
    columns = st.columns(3)
    with columns[0]:
        st.metric("Difficulty", recipe["difficulty"].title())
    with columns[1]:
        st.metric("Base spirit", recipe["base_spirit"].title())
    with columns[2]:
        st.metric("Serving scale", f"x{multiplier}")

    st.markdown(f"**Flavor tags:** {', '.join(recipe['flavor_tags'])}")


def _render_ingredients(recipe: dict) -> None:
    st.subheader("Ingredients")
    for ingredient in recipe.get("ingredients", []):
        amount = ingredient.get("amount")
        name = ingredient["name"]
        unit = ingredient.get("unit", "")
        if amount is None:
            detail = "to taste"
            if unit:
                detail = f"{detail} ({unit})"
            st.markdown(f"- **{name}** ({detail})")
            continue

        quantity = f"{format_quantity(amount)} {unit}".strip()
        st.markdown(f"- **{quantity}** {name}")


def _render_steps(recipe: dict) -> None:
    st.subheader("Preparation")
    for step in sorted(recipe.get("steps", []), key=lambda item: item["order"]):
        st.markdown(f"{step['order']}. {step['action']}")
        if tip := step.get("tip"):
            st.caption(f"Tip: {tip}")


def _open_mix_page(recipe: dict, multiplier: int) -> None:
    st.session_state["selected_recipe"] = recipe
    st.session_state["serving_multiplier"] = multiplier
    st.session_state["current_step_index"] = 0
    st.switch_page("pages/05_mix.py")


_ensure_session_state()
recipes = _recipes()
recipes_by_id = {recipe["id"]: recipe for recipe in recipes}
current_recipe_id = st.session_state["selected_recipe"].get("id")
current_multiplier = st.session_state["serving_multiplier"]
multiplier_options = [1, 2, 4]
multiplier_index = multiplier_options.index(current_multiplier) if current_multiplier in multiplier_options else 0

render_brand_header(
    "Recipe Detail",
    "Inspect the full build, adjust serving size, and move straight into the guided mix when the recipe feels right.",
    kicker="Pour Decisions",
)

selected_recipe_id = st.selectbox(
    "Recipe",
    options=[recipe["id"] for recipe in recipes],
    index=_recipe_index(recipes, current_recipe_id),
    format_func=lambda recipe_id: recipes_by_id[recipe_id]["name"],
)

if selected_recipe_id != current_recipe_id:
    st.session_state["selected_recipe"] = recipes_by_id[selected_recipe_id]
    st.session_state["serving_multiplier"] = 1
    st.session_state["current_step_index"] = 0
    st.rerun()

base_recipe = recipes_by_id[selected_recipe_id]
st.session_state["selected_recipe"] = base_recipe

st.markdown(f"<div class='pd-panel'>{base_recipe['description']}</div>", unsafe_allow_html=True)

multiplier = st.radio(
    "Serving size",
    options=multiplier_options,
    index=multiplier_index,
    horizontal=True,
    format_func=lambda value: f"x{value}",
)
st.session_state["serving_multiplier"] = multiplier

scaled_recipe = scale_recipe(base_recipe, multiplier)
_recipe_summary(base_recipe, multiplier)
st.caption(f"Scaled from the base recipe to make {scaled_recipe['serving_size']} servings.")

_render_ingredients(scaled_recipe)
st.divider()
_render_steps(scaled_recipe)

st.divider()
if st.button("Start Mixing"):
    _open_mix_page(base_recipe, multiplier)
