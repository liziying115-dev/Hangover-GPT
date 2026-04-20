"""Reusable recipe card widget."""

from typing import Optional

import streamlit as st


DETAIL_PAGE = "pages/04_detail.py"


def _format_spirit(value: Optional[str]) -> str:
    if not value:
        return "Unknown"
    return value.replace("-", " ").title()


def recipe_card(recipe: dict, show_missing: bool = False) -> None:
    """Render a compact recipe card."""
    recipe_id = recipe.get("id", recipe.get("name", "recipe"))
    name = recipe.get("name", "Untitled cocktail")
    difficulty = recipe.get("difficulty", "unknown").title()
    base_spirit = _format_spirit(recipe.get("base_spirit"))
    flavor_tags = recipe.get("flavor_tags") or []
    missing = recipe.get("missing") or []

    with st.container(border=True):
        st.markdown(f"#### {name}")
        st.caption(f"{difficulty} • {base_spirit}")

        if flavor_tags:
            st.write(" ".join(f"`{tag}`" for tag in flavor_tags))
        else:
            st.caption("No flavor tags available.")

        if show_missing and missing:
            st.caption(f"Missing: {', '.join(missing)}")

        if st.button(
            "View details",
            key=f"recipe-open-{recipe_id}",
            use_container_width=True,
        ):
            st.session_state["selected_recipe"] = recipe
            st.session_state["current_step_index"] = 0
            st.switch_page(DETAIL_PAGE)
