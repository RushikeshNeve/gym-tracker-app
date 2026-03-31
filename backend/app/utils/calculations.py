from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from app.utils.constants import REQUIRED_TASK_KEYS

ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "lightly_active": 1.375,
    "moderately_active": 1.55,
    "very_active": 1.725,
}

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
    "rowing machine": 7.0,
    "rowing": 7.0,
    "elliptical": 5.5,
    "jump rope": 10.0,
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


def estimate_calories_burned(activity_type: str, duration_min: int | float, weight_kg: float) -> float:
    lookup = MET_VALUES.get(str(activity_type).strip().lower(), 5.0)
    hours = float(duration_min or 0) / 60
    return round(lookup * float(weight_kg or 0) * hours, 1)


def calculate_diet_compliance_score(
    *,
    within_calories: bool,
    hit_protein_target: bool,
    whey_taken: bool,
    followed_plan: bool,
    no_cheat_meal: bool,
) -> int:
    score = 0
    if within_calories:
        score += 25
    if hit_protein_target:
        score += 25
    if whey_taken:
        score += 10
    if no_cheat_meal:
        score += 20
    if followed_plan:
        score += 20
    return score


def derive_day_status(required_flags: dict[str, bool], log_day: date) -> str:
    if all(required_flags.values()):
        return "perfect"
    if log_day < date.today():
        return "failed"
    return "incomplete"


def calculate_compliance_score(
    required_flags: dict[str, bool],
    lifestyle_flags: dict[str, bool],
    bonus_flags: dict[str, bool],
) -> float:
    required_score = sum(10 for key in REQUIRED_TASK_KEYS if required_flags.get(key))
    lifestyle_score = sum(4 for value in lifestyle_flags.values() if value)
    nutrition_bonus = sum(2.5 for value in bonus_flags.values() if value)
    return min(100.0, required_score + lifestyle_score + nutrition_bonus)


def challenge_day_number(start_date: date, for_date: date) -> int:
    return (for_date - start_date).days + 1


def challenge_progress(start_date: date, for_date: date | None = None) -> dict[str, Any]:
    current = for_date or date.today()
    day_number = challenge_day_number(start_date, current)
    end_date = start_date + timedelta(days=74)
    remaining = max(0, 75 - max(day_number, 0))
    return {
        "start_date": start_date,
        "end_date": end_date,
        "day_number": day_number,
        "remaining_days": remaining,
        "in_window": start_date <= current <= end_date,
    }

