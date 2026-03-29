"""Nutrition, recipe, and meal-plan calculations."""

from __future__ import annotations

import json
from datetime import date, timedelta
from typing import Any

import pandas as pd

from db import fetch_df, get_daily_targets, get_diet_plan_template, get_recipe_by_name_db, get_recipe_library, get_spicy_snack_presets
from utils.profile_logic import calculate_protein_target
from db import get_user_profile


def get_recipe_by_name(recipe_name: str) -> dict[str, Any] | None:
    recipe = get_recipe_by_name_db(recipe_name)
    if not recipe:
        return None
    recipe["ingredients"] = json.loads(recipe["ingredients_json"])
    recipe["steps"] = json.loads(recipe["steps_json"])
    return recipe


def get_today_meal_plan(log_date: date | str | None = None) -> pd.DataFrame:
    if log_date is None:
        day_value = date.today()
    elif isinstance(log_date, str):
        day_value = date.fromisoformat(log_date)
    else:
        day_value = log_date
    day_name = day_value.strftime("%A")
    return get_diet_plan_template(day_name)


def get_daily_food_totals(log_date: str) -> dict[str, float]:
    meals = fetch_df("SELECT * FROM nutrition_logs WHERE date = ? ORDER BY id", (log_date,))
    return {
        "calories": float(meals["calories"].sum()) if not meals.empty else 0.0,
        "protein": float(meals["protein"].sum()) if not meals.empty else 0.0,
        "carbs": float(meals["carbs"].sum()) if not meals.empty else 0.0,
        "fats": float(meals["fats"].sum()) if not meals.empty else 0.0,
        "fiber": float(meals["fiber"].sum()) if not meals.empty else 0.0,
    }


def calculate_remaining_macros(log_date: str) -> dict[str, float]:
    profile = get_user_profile()
    targets = get_daily_targets(log_date)
    targets["protein_target"] = max(float(targets.get("protein_target") or 0), calculate_protein_target(profile))
    totals = get_daily_food_totals(log_date)
    return {
        "calories": float(targets["calorie_target"]) - totals["calories"],
        "protein": float(targets["protein_target"]) - totals["protein"],
        "carbs": float(targets["carbs_target"]) - totals["carbs"],
        "fats": float(targets["fats_target"]) - totals["fats"],
        "fiber": float(targets["fiber_target"]) - totals["fiber"],
    }


def get_daily_nutrition(log_date: str) -> dict[str, Any]:
    meals = fetch_df("SELECT * FROM nutrition_logs WHERE date = ? ORDER BY id DESC", (log_date,))
    targets = get_daily_targets(log_date)
    profile = get_user_profile()
    targets["protein_target"] = max(float(targets.get("protein_target") or 0), calculate_protein_target(profile))
    totals = get_daily_food_totals(log_date)
    remaining = calculate_remaining_macros(log_date)
    compliance_inputs = {
        "within_calories": totals["calories"] <= float(targets["calorie_target"]),
        "hit_protein_target": totals["protein"] >= float(targets["protein_target"]),
        "whey_taken": bool((meals["food_name"].str.contains("whey", case=False, na=False)).any()) if not meals.empty else False,
    }
    return {
        "meals": meals,
        "targets": targets,
        "totals": totals,
        "remaining": remaining,
        "compliance_inputs": compliance_inputs,
    }


def get_meal_breakdown(log_date: str) -> pd.DataFrame:
    return fetch_df(
        "SELECT meal_type, SUM(calories) AS calories FROM nutrition_logs WHERE date = ? GROUP BY meal_type ORDER BY calories DESC",
        (log_date,),
    )


def get_weekly_nutrition(end_date: date | None = None) -> tuple[pd.DataFrame, dict[str, float]]:
    end = end_date or date.today()
    start = end - timedelta(days=6)
    meals = fetch_df(
        "SELECT date, calories, protein, carbs, fats, fiber FROM nutrition_logs WHERE date BETWEEN ? AND ? ORDER BY date",
        (start.isoformat(), end.isoformat()),
    )
    if meals.empty:
        return meals, {"avg_calories": 0.0, "avg_protein": 0.0}
    meals["date"] = pd.to_datetime(meals["date"])
    by_day = meals.groupby("date", as_index=False).sum(numeric_only=True)
    return by_day, {
        "avg_calories": float(by_day["calories"].mean()),
        "avg_protein": float(by_day["protein"].mean()),
    }


def calculate_diet_compliance_score(log_date: str, followed_plan: bool, no_cheat_meal: bool) -> int:
    daily = get_daily_nutrition(log_date)
    score = 0
    if daily["compliance_inputs"]["within_calories"]:
        score += 25
    if daily["compliance_inputs"]["hit_protein_target"]:
        score += 25
    if daily["compliance_inputs"]["whey_taken"]:
        score += 10
    if no_cheat_meal:
        score += 20
    if followed_plan:
        score += 20
    return score


def get_recipe_library_df() -> pd.DataFrame:
    return get_recipe_library()


def get_spicy_snacks_df() -> pd.DataFrame:
    return get_spicy_snack_presets()
