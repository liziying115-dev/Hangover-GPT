"""Step-by-step mixing simulation (Issue #7)."""

from __future__ import annotations

import re
import unicodedata

import streamlit as st

from components.brand import apply_global_style, render_brand_header
from components.progress_bar import mixing_progress
from services.scaler import format_quantity, scale_recipe

st.set_page_config(page_title="Mix It Up", page_icon="🍹", layout="centered")
apply_global_style()

_PREFIXES = {"white", "aged", "dark", "light", "fresh"}
_SUFFIXES = {"juice", "leaves", "leaf", "wedge", "wheel", "piece", "pieces", "sprig", "peel", "shell"}


def _ensure_session_state() -> None:
    st.session_state.setdefault("selected_recipe", {})
    st.session_state.setdefault("serving_multiplier", 1)
    st.session_state.setdefault("current_step_index", 0)


def _normalize(text: str) -> str:
    folded = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", folded.lower()).strip()


def _ingredient_aliases(name: str) -> set[str]:
    normalized = _normalize(name)
    if not normalized:
        return set()

    aliases = {normalized}
    parts = normalized.split()

    if len(parts) > 1:
        aliases.add(" ".join(parts[1:]))
        aliases.add(" ".join(parts[:-1]))

        if parts[0] in _PREFIXES:
            aliases.add(" ".join(parts[1:]))

        if parts[-1] in _SUFFIXES:
            aliases.add(" ".join(parts[:-1]))
            aliases.add(parts[0])

    return {alias for alias in aliases if alias}


def _step_ingredient_matches(step_text: str, ingredients: list[dict]) -> list[dict]:
    normalized_step = f" {_normalize(step_text)} "
    matches: list[dict] = []

    for ingredient in ingredients:
        aliases = _ingredient_aliases(ingredient["name"])
        if any(re.search(rf"\b{re.escape(alias)}\b", normalized_step) for alias in aliases):
            matches.append(ingredient)

    return matches


def _stage_ingredients(
    steps: list[dict],
    ingredients: list[dict],
    step_index: int,
) -> tuple[list[dict], str]:
    active: list[dict] = []
    current_explicit = False

    for index in range(step_index + 1):
        stage_text = steps[index]["action"]
        if tip := steps[index].get("tip"):
            stage_text = f"{stage_text} {tip}"

        explicit_matches = _step_ingredient_matches(stage_text, ingredients)
        if explicit_matches:
            for ingredient in explicit_matches:
                if ingredient not in active:
                    active.append(ingredient)
            if index == step_index:
                current_explicit = True

    if current_explicit:
        return active, "Ingredient amounts are inferred cumulatively from the step text."
    if active:
        return active, "No new listed ingredients were explicit in this step, so the previous measured ingredients are carried forward."
    return [], "No listed ingredients could be inferred for this step."


def _format_ingredient_line(ingredient: dict) -> str:
    amount = ingredient.get("amount")
    unit = ingredient.get("unit", "")
    if amount is None:
        detail = "to taste"
        if unit:
            detail = f"{detail} ({unit})"
        return f"**{ingredient['name']}** ({detail})"

    quantity = f"{format_quantity(amount)} {unit}".strip()
    return f"**{quantity}** {ingredient['name']}"


def _reset_step_index() -> None:
    st.session_state["current_step_index"] = 0


def _advance_step(total_steps: int) -> None:
    st.session_state["current_step_index"] = min(
        int(st.session_state.get("current_step_index", 0)) + 1,
        total_steps,
    )


def _render_ingredients(ingredients: list[dict]) -> None:
    if not ingredients:
        st.info("No listed ingredient amounts could be inferred for this step.")
        return

    for ingredient in ingredients:
        st.markdown(f"- {_format_ingredient_line(ingredient)}")


_ensure_session_state()
recipe = st.session_state.get("selected_recipe") or {}
if not recipe or not recipe.get("steps"):
    render_brand_header(
        "Mix It Up",
        "Step through the build one move at a time, with measured guidance that keeps the drink on track.",
        kicker="Pour Decisions",
    )
    st.info("Choose a recipe on the detail page, then click Start Mixing.")
    if st.button("Go to recipe detail", use_container_width=True):
        st.switch_page("pages/04_detail.py")
    st.stop()

multiplier = int(st.session_state.get("serving_multiplier", 1))
scaled_recipe = scale_recipe(recipe, multiplier)
steps = sorted(scaled_recipe.get("steps", []), key=lambda item: item["order"])
total_steps = len(steps)
current_step_index = min(int(st.session_state.get("current_step_index", 0)), total_steps)
if current_step_index != st.session_state.get("current_step_index", 0):
    st.session_state["current_step_index"] = current_step_index

render_brand_header(
    f"Mix It Up: {scaled_recipe['name']}",
    f"Serving size x{multiplier}. Keep the flow deliberate and readable while you build the drink.",
    kicker="Pour Decisions",
)
mixing_progress(current_step_index, total_steps)

if current_step_index >= total_steps:
    st.success(f"{scaled_recipe['name']} is ready to serve.")
    st.write("You reached the end of the guided mix. Start Over to repeat the process from step one.")
    if st.button("Start Over", use_container_width=True):
        _reset_step_index()
        st.rerun()
    st.stop()

step = steps[current_step_index]
active_ingredients, inference_note = _stage_ingredients(steps, scaled_recipe.get("ingredients", []), current_step_index)

st.subheader(f"Step {step['order']}")
st.markdown(step["action"])
if tip := step.get("tip"):
    st.caption(f"Tip: {tip}")

st.markdown("#### Ingredient amounts for this step")
st.caption(inference_note)
_render_ingredients(active_ingredients)

buttons = st.columns(2)
with buttons[0]:
    if st.button("Next Step", use_container_width=True):
        _advance_step(total_steps)
        st.rerun()
with buttons[1]:
    if st.button("Start Over", use_container_width=True):
        _reset_step_index()
        st.rerun()
