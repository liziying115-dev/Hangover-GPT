"""HangoverGPT 🍹 — Streamlit entry point."""

from copy import deepcopy

import streamlit as st

from components.brand import apply_global_style, render_brand_header

DEFAULT_SESSION_STATE = {
    "user_ingredients": [],
    "selected_recipe": {},
    "current_step_index": 0,
    "serving_multiplier": 1,
    "ai_recommendations": [],
    "ai_preference": "",
    "ai_recommendations_error": False,
}


def initialize_session_state() -> None:
    """Populate expected cross-page state on first load."""
    for key, default_value in DEFAULT_SESSION_STATE.items():
        if key not in st.session_state:
            st.session_state[key] = deepcopy(default_value)


st.set_page_config(
    page_title="HangoverGPT 🍹",
    page_icon="🍹",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_session_state()
apply_global_style()

render_brand_header(
    "Pour Decisions",
    "Warm cocktail-bar styling, faster flows, and a clearer way to browse, match, and mix drinks from one Streamlit app.",
    kicker="Cocktail Simulator",
)
st.markdown(
    """
    <div class="pd-chip-row">
      <span class="pd-chip">Ingredient matching</span>
      <span class="pd-chip">AI suggestions</span>
      <span class="pd-chip">Browse and filter</span>
      <span class="pd-chip">Guided mixing</span>
    </div>
    """,
    unsafe_allow_html=True,
)
st.markdown(
    """
    <div class="pd-panel">
      Open <strong>Home</strong> to search from your bar, <strong>Browse Cocktails</strong> to explore the catalog,
      and <strong>Results</strong> or <strong>Recipe Detail</strong> when you want to refine the next pour.
    </div>
    """,
    unsafe_allow_html=True,
)
