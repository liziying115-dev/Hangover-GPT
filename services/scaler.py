"""Serving size scaling for recipe ingredients."""

from copy import deepcopy
from fractions import Fraction


def format_quantity(amount: float) -> str:
    """Render a quantity as a compact fraction when practical."""
    quantity = Fraction(str(amount)).limit_denominator(8)

    if quantity.denominator == 1:
        return str(quantity.numerator)

    whole = quantity.numerator // quantity.denominator
    remainder = quantity - whole
    if whole:
        return f"{whole} {remainder.numerator}/{remainder.denominator}"
    return f"{remainder.numerator}/{remainder.denominator}"


def scale_recipe(recipe: dict, multiplier: int) -> dict:
    """Return a copy of recipe with ingredient amounts scaled by multiplier.

    Ingredients with amount=None (e.g. 'to taste') are left unchanged.
    """
    if multiplier < 1:
        raise ValueError("multiplier must be positive")

    scaled_recipe = deepcopy(recipe)
    scaled_recipe["serving_size"] = recipe.get("serving_size", 1) * multiplier

    scaled_ingredients = []
    for ingredient in recipe.get("ingredients", []):
        scaled_ingredient = deepcopy(ingredient)
        amount = scaled_ingredient.get("amount")
        if amount is not None:
            scaled_ingredient["amount"] = amount * multiplier
        scaled_ingredients.append(scaled_ingredient)

    scaled_recipe["ingredients"] = scaled_ingredients
    return scaled_recipe
