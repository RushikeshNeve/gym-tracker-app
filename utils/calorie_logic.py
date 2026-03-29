"""Daily exercise burn and energy balance calculations."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from db import fetch_df, get_daily_targets, get_user_profile
from utils.profile_logic import calculate_target_calories, calculate_tdee

MET_VALUES = {
    "strength training": 6.0,
    "push": 6.0,
    "pull": 6.0,
    "legs": 6.2,
    "upper": 5.8,
    "lower": 6.0,
    "full body": 6.2,
    "active recovery": 3.0,
    "walking": 3.5,
    "outdoor walk": 3.8,
    "incline walking": 5.5,
    "cycling": 6.8,
    "stairmaster": 8.5,
    "running": 9.8,
    "outdoor run": 9.8,
    "rowing": 7.0,
    "elliptical": 5.5,
    "jump rope": 10.0,
}


def estimate_calories_burned(activity_type: str, duration_min: int | float, weight_kg: float) -> float:
    lookup = MET_VALUES.get(str(activity_type).strip().lower(), 5.0)
    hours = float(duration_min or 0) / 60
    return round(lookup * float(weight_kg or 0) * hours, 1)


def calculate_daily_exercise_burn(log_date: str) -> dict[str, Any]:
    logs = fetch_df(
        "SELECT * FROM exercise_calorie_logs WHERE date = ? ORDER BY created_at DESC, id DESC",
        (log_date,),
    )
    if logs.empty:
        return {"logs": logs, "total_burned": 0.0}
    return {"logs": logs, "total_burned": float(logs["calories_burned"].sum())}


def calculate_daily_energy_balance(log_date: str) -> dict[str, Any]:
    profile = get_user_profile()
    targets = get_daily_targets(log_date)
    nutrition = fetch_df(
        "SELECT SUM(calories) AS calories, SUM(protein) AS protein FROM nutrition_logs WHERE date = ?",
        (log_date,),
    )
    food_calories = float(nutrition.iloc[0]["calories"]) if not nutrition.empty and pd.notna(nutrition.iloc[0]["calories"]) else 0.0
    protein = float(nutrition.iloc[0]["protein"]) if not nutrition.empty and pd.notna(nutrition.iloc[0]["protein"]) else 0.0
    exercise = calculate_daily_exercise_burn(log_date)
    maintenance = float(calculate_tdee(profile))
    target_calories = float(targets.get("calorie_target") or calculate_target_calories(profile))
    net_calories = food_calories - exercise["total_burned"]
    deficit_or_surplus = maintenance - net_calories
    if deficit_or_surplus > 150:
        status = "in_deficit"
    elif deficit_or_surplus < -150:
        status = "in_surplus"
    else:
        status = "near_maintenance"
    return {
        "maintenance_calories": maintenance,
        "target_calories": target_calories,
        "food_calories": food_calories,
        "exercise_calories": exercise["total_burned"],
        "net_calories": net_calories,
        "deficit_or_surplus": deficit_or_surplus,
        "status": status,
        "protein": protein,
        "exercise_logs": exercise["logs"],
    }


def get_weekly_energy_balance(end_date: date | None = None) -> tuple[pd.DataFrame, dict[str, float]]:
    end = end_date or date.today()
    rows = []
    for offset in range(6, -1, -1):
        log_date = (end - timedelta(days=offset)).isoformat()
        balance = calculate_daily_energy_balance(log_date)
        rows.append(
            {
                "date": pd.to_datetime(log_date),
                "food_calories": balance["food_calories"],
                "exercise_calories": balance["exercise_calories"],
                "net_calories": balance["net_calories"],
                "deficit_or_surplus": balance["deficit_or_surplus"],
                "protein": balance["protein"],
            }
        )
    df = pd.DataFrame(rows)
    summary = {
        "weekly_average_deficit": float(df["deficit_or_surplus"].mean()) if not df.empty else 0.0,
        "estimated_fat_loss_kg_per_week": float(df["deficit_or_surplus"].sum() / 7700) if not df.empty else 0.0,
    }
    return df, summary
