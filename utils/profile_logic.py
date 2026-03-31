"""Profile and maintenance calorie calculations."""

from __future__ import annotations

from typing import Any

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
}


def calculate_bmr(profile: dict[str, Any]) -> float:
    weight = float(profile.get("current_weight_kg", 0) or 0)
    height = float(profile.get("height_cm", 0) or 0)
    age = int(profile.get("age", 0) or 0)
    gender = str(profile.get("gender", "male")).lower()
    if gender == "female":
        return 10 * weight + 6.25 * height - 5 * age - 161
    return 10 * weight + 6.25 * height - 5 * age + 5


def calculate_tdee(profile: dict[str, Any]) -> float:
    bmr = calculate_bmr(profile)
    multiplier = ACTIVITY_MULTIPLIERS.get(str(profile.get("activity_level", "moderately_active")), 1.55)
    return bmr * multiplier


def calculate_target_calories(profile: dict[str, Any]) -> float:
    tdee = calculate_tdee(profile)
    deficit = float(profile.get("desired_deficit", 0) or 0)
    goal = str(profile.get("goal", "fat_loss"))
    if goal == "maintenance":
        return tdee
    if goal == "recomp":
        return tdee - min(deficit, 250)
    return tdee - deficit


def calculate_protein_target(profile: dict[str, Any]) -> float:
    weight = float(profile.get("current_weight_kg", 0) or 0)
    return max(140.0, round(weight * 2.1, 1))
