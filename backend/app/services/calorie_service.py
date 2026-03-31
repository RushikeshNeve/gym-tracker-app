from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cardio_logs import CardioLog
from app.models.nutrition_logs import NutritionLog
from app.models.user_profile import UserProfile
from app.models.workouts import Workout
from app.services.profile_service import get_or_create_daily_target
from app.utils.calculations import calculate_target_calories, calculate_tdee, estimate_calories_burned


def estimate_activity_burn(activity_type: str, duration_min: int | float, weight_kg: float) -> float:
    return estimate_calories_burned(activity_type, duration_min, weight_kg)


def calculate_daily_energy_balance(db: Session, profile: UserProfile, log_date: date) -> dict:
    target = get_or_create_daily_target(db, profile, log_date)
    nutrition_row = db.execute(
        select(
            func.coalesce(func.sum(NutritionLog.calories), 0.0),
            func.coalesce(func.sum(NutritionLog.protein), 0.0),
        ).where(
            NutritionLog.profile_id == profile.id,
            NutritionLog.date == log_date,
        )
    ).one()
    food_calories = float(nutrition_row[0] or 0.0)
    protein = float(nutrition_row[1] or 0.0)
    workout_burn = db.scalar(
        select(func.coalesce(func.sum(Workout.estimated_calories_burned), 0.0)).where(
            Workout.profile_id == profile.id,
            Workout.date == log_date,
        )
    ) or 0.0
    cardio_burn = db.scalar(
        select(func.coalesce(func.sum(CardioLog.estimated_calories_burned), 0.0)).where(
            CardioLog.profile_id == profile.id,
            CardioLog.date == log_date,
        )
    ) or 0.0
    exercise_calories = float(workout_burn + cardio_burn)
    payload = {
        "age": profile.age,
        "gender": profile.gender,
        "height_cm": profile.height_cm,
        "current_weight_kg": profile.current_weight_kg,
        "activity_level": profile.activity_level,
        "goal": profile.goal,
        "desired_deficit": profile.desired_deficit,
    }
    maintenance = float(calculate_tdee(payload))
    target_calories = float(target.calorie_target or calculate_target_calories(payload))
    net_calories = food_calories - exercise_calories
    deficit_or_surplus = maintenance - net_calories
    if deficit_or_surplus > 150:
        status = "in_deficit"
    elif deficit_or_surplus < -150:
        status = "in_surplus"
    else:
        status = "near_maintenance"
    return {
        "maintenance_calories": round(maintenance, 2),
        "target_calories": round(target_calories, 2),
        "food_calories": round(food_calories, 2),
        "exercise_calories": round(exercise_calories, 2),
        "net_calories": round(net_calories, 2),
        "deficit_or_surplus": round(deficit_or_surplus, 2),
        "status": status,
        "protein": round(protein, 2),
    }


def get_weekly_energy_balance(db: Session, profile: UserProfile, end_date: date | None = None) -> tuple[list[dict], dict[str, float]]:
    end = end_date or date.today()
    rows: list[dict] = []
    for offset in range(6, -1, -1):
        log_date = end - timedelta(days=offset)
        balance = calculate_daily_energy_balance(db, profile, log_date)
        rows.append({"date": log_date, **balance})
    weekly_average_deficit = sum(item["deficit_or_surplus"] for item in rows) / len(rows) if rows else 0.0
    estimated_fat_loss_kg_per_week = sum(item["deficit_or_surplus"] for item in rows) / 7700 if rows else 0.0
    return rows, {
        "weekly_average_deficit": round(weekly_average_deficit, 2),
        "estimated_fat_loss_kg_per_week": round(estimated_fat_loss_kg_per_week, 4),
    }

