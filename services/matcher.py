"""Ingredient-based recipe matching."""

from __future__ import annotations

import json
from pathlib import Path


def _normalize(value: str) -> str:
    return value.strip().lower()


def load_recipes(path: str = "data/recipes.json") -> list[dict]:
    with Path(path).open() as file:
        return json.load(file)


def match_recipes(user_ingredients: list[str], recipes: list[dict]) -> list[dict]:
    """Return recipes ranked by ingredient overlap.

    Each result is the recipe dict augmented with:
      - match_type: "exact" | "partial"
      - missing: list of ingredient names not supplied by the user
    """
    normalized_ingredients = {_normalize(ingredient) for ingredient in user_ingredients if ingredient.strip()}
    if not normalized_ingredients:
        return []

    matches: list[dict] = []
    for recipe in recipes:
        recipe_ingredients = recipe.get("ingredients", [])
        if not recipe_ingredients:
            continue

        required_ingredients = [_normalize(ingredient["name"]) for ingredient in recipe_ingredients]
        required_set = set(required_ingredients)
        matched = required_set & normalized_ingredients
        if not matched:
            continue

        missing = sorted(required_set - normalized_ingredients)
        matches.append(
            {
                **recipe,
                "match_type": "exact" if not missing else "partial",
                "missing": missing,
                "matched_ingredients": sorted(matched),
                "match_score": len(matched) / len(required_set),
            }
        )

    return sorted(
        matches,
        key=lambda recipe: (
            recipe["match_type"] != "exact",
            -recipe["match_score"],
            len(recipe["missing"]),
            recipe["name"].lower(),
        ),
    )
