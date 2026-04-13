"""Ingredient-based recipe matching for HangoverGPT 🍹."""

from __future__ import annotations


def _normalize(name: str) -> str:
    return " ".join(str(name).strip().lower().split())


def _normalized_user_set(user_ingredients: list[str]) -> set[str]:
    return {_normalize(x) for x in user_ingredients if x and str(x).strip()}


def _recipe_ingredient_names(recipe: dict) -> list[str]:
    return [ing["name"] for ing in recipe.get("ingredients", [])]


def match_recipes(user_ingredients: list[str], recipes: list[dict]) -> list[dict]:
    """
    Match recipes against a pantry list (case-insensitive).

    - **exact**: user has every recipe ingredient name.
    - **partial**: user matches at least one ingredient but not all.

    Each item is the recipe dict plus ``match_type`` and ``missing_ingredients``
    (original casing from the recipe). Partial matches are sorted by fewest
    missing ingredients first; exact matches precede partials.
    """
    user_set = _normalized_user_set(user_ingredients)
    exact: list[dict] = []
    partial: list[dict] = []

    for recipe in recipes:
        names = _recipe_ingredient_names(recipe)
        if not names:
            continue

        missing: list[str] = []
        for raw_name in names:
            if _normalize(raw_name) not in user_set:
                missing.append(raw_name)

        matched = len(names) - len(missing)
        row = {
            **recipe,
            "match_type": "exact" if not missing else "partial",
            "missing_ingredients": missing,
        }

        if not missing:
            exact.append(row)
        elif matched > 0:
            partial.append(row)

    partial.sort(key=lambda r: len(r["missing_ingredients"]))
    return exact + partial
