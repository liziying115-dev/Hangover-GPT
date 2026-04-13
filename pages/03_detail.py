"""Recipe detail stub (HangoverGPT 🍹) — open from Browse."""

from __future__ import annotations

import streamlit as st

st.set_page_config(page_title="Recipe | HangoverGPT 🍹", page_icon="🍹", layout="wide")

recipe = st.session_state.get("selected_recipe")

if not recipe:
    st.info(
        "No cocktail selected yet. Head to **Browse** in the sidebar, pick a drink, "
        "and tap **View recipe** — your recipe will open here."
    )
    st.stop()

st.title(recipe.get("name", "Recipe"))
st.caption(recipe.get("description", ""))
st.write("**Difficulty:**", recipe.get("difficulty", "—"))

ings = recipe.get("ingredients") or []
if ings:
    st.subheader("Ingredients")
    for ing in ings:
        st.write(f"- {ing.get('name', '')} — {ing.get('amount', '')} {ing.get('unit', '')}")

steps = recipe.get("steps") or []
if steps:
    st.subheader("Steps")
    for step in sorted(steps, key=lambda s: s.get("order", 0)):
        st.write(f"{step.get('order', '')}. {step.get('action', '')}")
