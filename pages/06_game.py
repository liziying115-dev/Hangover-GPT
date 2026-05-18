"""Bartender Challenge — interactive mini-game.

Five rounds: read a cocktail's description and flavor clues (name hidden),
then click the correct spirit bottle. Correct = +10 pts, wrong = -5 pts.
"""
from __future__ import annotations

import random
from pathlib import Path

import streamlit as st

from components.brand import apply_global_style
from services.matcher import load_recipes

st.set_page_config(
    page_title="Bartender Challenge 🎮",
    page_icon="🎮",
    layout="wide",
)
apply_global_style()

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

SPIRIT_BOTTLES: dict[str, str] = {
    "tequila": "bottle/Tequila.png",
    "vodka":   "bottle/Vodka.png",
    "gin":     "bottle/Gin.png",
    "rum":     "bottle/Rum.png",
    "whiskey": "bottle/Whiskey.png",
    "brandy":  "bottle/Brandy.png",
}

SPIRIT_LABELS: dict[str, str] = {
    "tequila": "Tequila",
    "vodka":   "Vodka",
    "gin":     "Gin",
    "rum":     "Rum",
    "whiskey": "Whiskey",
    "brandy":  "Brandy",
}

TOTAL_ROUNDS = 5
PTS_CORRECT  = 10
PTS_WRONG    = -5

RATINGS = [
    (50, "Master Mixologist 🏆",        "Perfect score! You were born behind the bar."),
    (35, "Seasoned Bartender 🥈",        "Great instincts — just a couple of slips."),
    (20, "Bar Apprentice 🥉",            "You know your way around a bottle or two."),
    (0,  "Spilled More Than You Poured 😅", "Keep practicing — the bar will wait."),
]

# ---------------------------------------------------------------------------
# Session-state helpers
# ---------------------------------------------------------------------------

def _init() -> None:
    defaults = {
        "game_phase":    "intro",   # intro | playing | answered | over
        "game_rounds":   [],        # list of recipe dicts for this session
        "game_idx":      0,
        "game_score":    0,
        "game_selected": None,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def _start_game() -> None:
    all_recipes = [
        r for r in load_recipes()
        if r.get("base_spirit") in SPIRIT_BOTTLES
    ]
    pool = random.sample(all_recipes, min(TOTAL_ROUNDS, len(all_recipes)))
    st.session_state["game_rounds"]   = pool
    st.session_state["game_idx"]      = 0
    st.session_state["game_score"]    = 0
    st.session_state["game_selected"] = None
    st.session_state["game_phase"]    = "playing"


def _current_recipe() -> dict:
    return st.session_state["game_rounds"][st.session_state["game_idx"]]


def _pick_rating() -> tuple[str, str]:
    score = st.session_state["game_score"]
    for threshold, title, desc in RATINGS:
        if score >= threshold:
            return title, desc
    return RATINGS[-1][1], RATINGS[-1][2]


# ---------------------------------------------------------------------------
# UI sections
# ---------------------------------------------------------------------------

def _render_scorebar() -> None:
    idx   = st.session_state["game_idx"]
    score = st.session_state["game_score"]
    phase = st.session_state["game_phase"]
    total = len(st.session_state["game_rounds"])
    round_display = min(idx + 1, total) if phase != "over" else total
    st.markdown(
        f"""
        <div style="display:flex;justify-content:space-between;
                    background:#221812;border-radius:8px;
                    padding:10px 20px;margin-bottom:1rem;font-size:0.95rem;">
            <span>🎮 <strong>Bartender Challenge</strong></span>
            <span>Round <strong>{round_display}/{total}</strong></span>
            <span>Score: <strong style="color:#D4AB66">{score}</strong></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_intro() -> None:
    st.markdown(
        """
        <div style="text-align:center;padding:2rem 0 1rem;">
            <div style="font-size:3.5rem;">🍹</div>
            <h1 style="color:#D4AB66;margin:0.5rem 0">Bartender Challenge</h1>
            <p style="color:#c4b49a;max-width:480px;margin:0 auto 1.5rem;">
                Read the cocktail description and flavor clues,
                then tap the right spirit bottle.<br>
                <strong style="color:#D4AB66">+10</strong> for correct &nbsp;|&nbsp;
                <strong style="color:#e07070">−5</strong> for wrong &nbsp;|&nbsp;
                <strong>{} rounds</strong>
            </p>
        </div>
        """.format(TOTAL_ROUNDS),
        unsafe_allow_html=True,
    )
    col = st.columns([1, 2, 1])[1]
    with col:
        if st.button("Start Game 🎯", use_container_width=True, type="primary"):
            _start_game()
            st.rerun()


def _render_clue_card(recipe: dict) -> None:
    tags_html = "".join(
        f'<span style="background:#2e1f10;border:1px solid #D4AB66;'
        f'color:#D4AB66;border-radius:12px;padding:2px 10px;'
        f'font-size:0.8rem;margin:2px">{t}</span>'
        for t in recipe.get("flavor_tags", [])
    )
    difficulty_color = {"easy": "#6dbf6d", "medium": "#D4AB66", "hard": "#e07070"}.get(
        recipe.get("difficulty", ""), "#aaa"
    )
    st.markdown(
        f"""
        <div style="background:#221812;border:1px solid #3a2a1a;
                    border-radius:12px;padding:1.5rem;margin-bottom:1.2rem;">
            <div style="font-size:0.75rem;color:#888;margin-bottom:0.3rem;
                        text-transform:uppercase;letter-spacing:1px;">
                What cocktail is this? Pick the spirit 👇
            </div>
            <p style="font-size:1.15rem;color:#F7EFE2;margin:0.5rem 0 0.8rem;">
                {recipe.get("description", "")}
            </p>
            <div style="margin-bottom:0.5rem">{tags_html}</div>
            <div style="font-size:0.8rem;color:{difficulty_color}">
                Difficulty: {recipe.get("difficulty", "").capitalize()}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_bottles(disabled: bool = False) -> str | None:
    """Render clickable bottle grid; return selected spirit key or None."""
    spirits = list(SPIRIT_BOTTLES.keys())
    cols = st.columns(len(spirits))
    selected = None
    for col, spirit in zip(cols, spirits):
        with col:
            img_path = Path(SPIRIT_BOTTLES[spirit])
            if img_path.exists():
                st.image(str(img_path), use_container_width=True)
            if not disabled:
                if st.button(
                    SPIRIT_LABELS[spirit],
                    key=f"bottle_{spirit}",
                    use_container_width=True,
                ):
                    selected = spirit
    return selected


def _render_feedback(recipe: dict, selected: str) -> None:
    correct = recipe.get("base_spirit", "")
    is_right = selected == correct

    if is_right:
        st.markdown(
            f"""
            <div style="background:#1a3020;border:1px solid #6dbf6d;
                        border-radius:10px;padding:1rem;text-align:center;
                        margin-bottom:1rem;">
                <div style="font-size:1.8rem">✅</div>
                <strong style="color:#6dbf6d;font-size:1.1rem">Correct! +{PTS_CORRECT} pts</strong><br>
                <span style="color:#c4b49a">It's a <strong style="color:#F7EFE2">
                {recipe.get("name","")}</strong> — made with {SPIRIT_LABELS[correct]}.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"""
            <div style="background:#301a1a;border:1px solid #e07070;
                        border-radius:10px;padding:1rem;text-align:center;
                        margin-bottom:1rem;">
                <div style="font-size:1.8rem">❌</div>
                <strong style="color:#e07070;font-size:1.1rem">Wrong! {PTS_WRONG} pts</strong><br>
                <span style="color:#c4b49a">It's a <strong style="color:#F7EFE2">
                {recipe.get("name","")}</strong> — the answer was
                <strong style="color:#D4AB66">{SPIRIT_LABELS.get(correct, correct)}</strong>.</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Show the selected bottle image prominently
    bottle_col = st.columns([1, 2, 1])[1]
    with bottle_col:
        img_path = Path(SPIRIT_BOTTLES.get(correct, ""))
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)

    # Next / Finish button
    idx   = st.session_state["game_idx"]
    total = len(st.session_state["game_rounds"])
    label = "Next Round ➡️" if idx < total - 1 else "See Results 🏆"
    center = st.columns([1, 2, 1])[1]
    with center:
        if st.button(label, use_container_width=True, type="primary"):
            st.session_state["game_idx"] += 1
            st.session_state["game_selected"] = None
            if st.session_state["game_idx"] >= total:
                st.session_state["game_phase"] = "over"
            else:
                st.session_state["game_phase"] = "playing"
            st.rerun()


def _render_game_over() -> None:
    score = st.session_state["game_score"]
    total = len(st.session_state["game_rounds"])
    title, desc = _pick_rating()
    max_score = total * PTS_CORRECT
    pct = max(0, int(score / max_score * 100)) if max_score else 0

    st.markdown(
        f"""
        <div style="text-align:center;padding:2rem 0 1.5rem;">
            <div style="font-size:3rem">{title.split()[-1]}</div>
            <h2 style="color:#D4AB66;margin:0.4rem 0">{" ".join(title.split()[:-1])}</h2>
            <p style="color:#c4b49a;margin:0 0 0.5rem">{desc}</p>
            <div style="font-size:2.5rem;font-weight:bold;color:#F7EFE2">
                {score} <span style="font-size:1rem;color:#888">/ {max_score} pts</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Score bar
    bar_color = "#6dbf6d" if pct >= 70 else "#D4AB66" if pct >= 40 else "#e07070"
    st.markdown(
        f"""
        <div style="background:#221812;border-radius:8px;
                    height:14px;width:100%;margin:0.5rem 0 1.5rem;overflow:hidden;">
            <div style="background:{bar_color};height:100%;
                        width:{pct}%;border-radius:8px;
                        transition:width 0.4s ease;"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Play Again 🔄", use_container_width=True, type="primary"):
            _start_game()
            st.rerun()
    with col2:
        if st.button("Back to Home 🏠", use_container_width=True):
            st.switch_page("pages/01_home.py")


# ---------------------------------------------------------------------------
# Main render
# ---------------------------------------------------------------------------

_init()
phase = st.session_state["game_phase"]

if phase == "intro":
    _render_intro()

elif phase in ("playing", "answered"):
    _render_scorebar()
    recipe = _current_recipe()
    _render_clue_card(recipe)

    if phase == "playing":
        selected = _render_bottles(disabled=False)
        if selected:
            is_right = selected == recipe.get("base_spirit", "")
            st.session_state["game_score"] += PTS_CORRECT if is_right else PTS_WRONG
            st.session_state["game_selected"] = selected
            st.session_state["game_phase"] = "answered"
            st.rerun()
    else:
        _render_bottles(disabled=True)
        _render_feedback(recipe, st.session_state["game_selected"])

elif phase == "over":
    _render_scorebar()
    _render_game_over()
