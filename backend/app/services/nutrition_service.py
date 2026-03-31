from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.nutrition_logs import NutritionLog
from app.models.user_profile import UserProfile
from app.schemas.nutrition import NutritionLogCreate, NutritionLogUpdate
from app.services.profile_service import get_or_create_daily_target
from app.utils.calculations import calculate_diet_compliance_score, calculate_protein_target


def create_nutrition_log(db: Session, profile: UserProfile, payload: NutritionLogCreate) -> NutritionLog:
    item = NutritionLog(profile_id=profile.id, **payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_nutrition_log(db: Session, profile: UserProfile, log_id: int, payload: NutritionLogUpdate) -> NutritionLog | None:
    item = db.scalar(select(NutritionLog).where(NutritionLog.id == log_id, NutritionLog.profile_id == profile.id))
    if not item:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_nutrition_log(db: Session, profile: UserProfile, log_id: int) -> bool:
    item = db.scalar(select(NutritionLog).where(NutritionLog.id == log_id, NutritionLog.profile_id == profile.id))
    if not item:
        return False
    db.delete(item)
    db.commit()
    return True


def copy_nutrition_logs(db: Session, profile: UserProfile, source_date: date, target_date: date) -> int:
    rows = list(
        db.scalars(
            select(NutritionLog).where(
                NutritionLog.profile_id == profile.id,
                NutritionLog.date == source_date,
            )
        ).all()
    )
    for row in rows:
        db.add(
            NutritionLog(
                profile_id=profile.id,
                date=target_date,
                meal_type=row.meal_type,
                food_name=row.food_name,
                quantity=row.quantity,
                serving_count=row.serving_count,
                calories=row.calories,
                protein=row.protein,
                carbs=row.carbs,
                fats=row.fats,
                fiber=row.fiber,
                notes=row.notes,
                source_type=row.source_type,
                recipe_name=row.recipe_name,
            )
        )
    db.commit()
    return len(rows)


def get_daily_food_totals(db: Session, profile: UserProfile, log_date: date) -> dict[str, float]:
    row = db.execute(
        select(
            func.coalesce(func.sum(NutritionLog.calories), 0.0),
            func.coalesce(func.sum(NutritionLog.protein), 0.0),
            func.coalesce(func.sum(NutritionLog.carbs), 0.0),
            func.coalesce(func.sum(NutritionLog.fats), 0.0),
            func.coalesce(func.sum(NutritionLog.fiber), 0.0),
        ).where(
            NutritionLog.profile_id == profile.id,
            NutritionLog.date == log_date,
        )
    ).one()
    return {
        "calories": float(row[0] or 0.0),
        "protein": float(row[1] or 0.0),
        "carbs": float(row[2] or 0.0),
        "fats": float(row[3] or 0.0),
        "fiber": float(row[4] or 0.0),
    }


def get_daily_nutrition(db: Session, profile: UserProfile, log_date: date) -> dict:
    meals = list(
        db.scalars(
            select(NutritionLog)
            .where(NutritionLog.profile_id == profile.id, NutritionLog.date == log_date)
            .order_by(NutritionLog.id.desc())
        ).all()
    )
    target = get_or_create_daily_target(db, profile, log_date)
    totals = get_daily_food_totals(db, profile, log_date)
    protein_floor = calculate_protein_target({"current_weight_kg": profile.current_weight_kg})
    protein_target = max(float(target.protein_target or 0), protein_floor)
    targets = {
        "id": target.id,
        "profile_id": target.profile_id,
        "date": target.date,
        "calorie_target": float(target.calorie_target),
        "protein_target": protein_target,
        "carbs_target": float(target.carbs_target),
        "fats_target": float(target.fats_target),
        "fiber_target": float(target.fiber_target),
        "water_target_liters": float(target.water_target_liters),
        "created_at": target.created_at,
        "updated_at": target.updated_at,
    }
    remaining = {
        "calories": float(targets["calorie_target"]) - totals["calories"],
        "protein": float(targets["protein_target"]) - totals["protein"],
        "carbs": float(targets["carbs_target"]) - totals["carbs"],
        "fats": float(targets["fats_target"]) - totals["fats"],
        "fiber": float(targets["fiber_target"]) - totals["fiber"],
    }
    whey_taken = any("whey" in (meal.food_name or "").lower() for meal in meals)
    compliance_inputs = {
        "within_calories": totals["calories"] <= float(targets["calorie_target"]),
        "hit_protein_target": totals["protein"] >= float(targets["protein_target"]),
        "whey_taken": whey_taken,
    }
    return {
        "date": log_date,
        "meals": meals,
        "targets": targets,
        "totals": totals,
        "remaining": remaining,
        "compliance_inputs": compliance_inputs,
    }


def get_weekly_nutrition(db: Session, profile: UserProfile, end_date: date | None = None) -> tuple[list[dict], dict[str, float]]:
    end = end_date or date.today()
    start = end - timedelta(days=6)
    rows = db.execute(
        select(
            NutritionLog.date,
            func.coalesce(func.sum(NutritionLog.calories), 0.0),
            func.coalesce(func.sum(NutritionLog.protein), 0.0),
            func.coalesce(func.sum(NutritionLog.carbs), 0.0),
            func.coalesce(func.sum(NutritionLog.fats), 0.0),
            func.coalesce(func.sum(NutritionLog.fiber), 0.0),
        )
        .where(
            NutritionLog.profile_id == profile.id,
            NutritionLog.date.between(start, end),
        )
        .group_by(NutritionLog.date)
        .order_by(NutritionLog.date.asc())
    ).all()
    chart = [
        {
            "date": row[0],
            "calories": float(row[1]),
            "protein": float(row[2]),
            "carbs": float(row[3]),
            "fats": float(row[4]),
            "fiber": float(row[5]),
        }
        for row in rows
    ]
    avg_calories = sum(item["calories"] for item in chart) / len(chart) if chart else 0.0
    avg_protein = sum(item["protein"] for item in chart) / len(chart) if chart else 0.0
    return chart, {"avg_calories": round(avg_calories, 2), "avg_protein": round(avg_protein, 2)}


def compute_diet_score(*, daily_nutrition: dict, followed_plan: bool, no_cheat_meal: bool) -> int:
    return calculate_diet_compliance_score(
        within_calories=daily_nutrition["compliance_inputs"]["within_calories"],
        hit_protein_target=daily_nutrition["compliance_inputs"]["hit_protein_target"],
        whey_taken=daily_nutrition["compliance_inputs"]["whey_taken"],
        followed_plan=followed_plan,
        no_cheat_meal=no_cheat_meal,
    )

