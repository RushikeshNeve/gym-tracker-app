from __future__ import annotations

from pydantic import BaseModel

from app.schemas.common import TimestampFields


class RecipeRead(TimestampFields):
    id: int
    recipe_name: str
    meal_type: str
    ingredients_json: list[dict]
    steps_json: list[str]
    calories: float
    protein: float
    carbs: float
    fats: float
    fiber: float
    portion_note: str
    is_spicy: bool
    is_vegetarian: bool
    is_egg_based: bool
    is_soya_based: bool


class MealPlanTemplateRead(TimestampFields):
    id: int
    day_name: str
    meal_type: str
    option_1: str | None
    option_2: str | None
    option_3: str | None
    option_4: str | None
    notes: str

