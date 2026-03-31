from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.daily_targets import DailyTarget
from app.models.user_profile import UserProfile
from app.schemas.profile import UserProfileUpdate
from app.utils.calculations import calculate_bmr, calculate_protein_target, calculate_target_calories, calculate_tdee
from app.utils.constants import DEFAULT_TARGETS


DEFAULT_PROFILE_VALUES = {
    "age": 27,
    "gender": "male",
    "height_cm": 175.0,
    "current_weight_kg": 83.5,
    "activity_level": "moderately_active",
    "goal": "fat_loss",
    "desired_deficit": 450.0,
    "preferred_diet_plan_name": "High protein calorie deficit",
}


def ensure_profile(db: Session, profile_id: int | None = None) -> UserProfile:
    if profile_id is not None:
        profile = db.get(UserProfile, profile_id)
        if profile:
            return profile

    profile = db.scalar(select(UserProfile).order_by(UserProfile.id.asc()).limit(1))
    if profile:
        return profile

    profile = UserProfile(
        **DEFAULT_PROFILE_VALUES,
        challenge_start_date=date.today() + timedelta(days=1),
        target_weight_kg=78.0,
    )
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_profile_summary(profile: UserProfile) -> dict[str, float]:
    payload = {
        "age": profile.age,
        "gender": profile.gender,
        "height_cm": profile.height_cm,
        "current_weight_kg": profile.current_weight_kg,
        "activity_level": profile.activity_level,
        "goal": profile.goal,
        "desired_deficit": profile.desired_deficit,
    }
    return {
        "bmr": round(calculate_bmr(payload), 2),
        "tdee": round(calculate_tdee(payload), 2),
        "target_calories": round(calculate_target_calories(payload), 2),
        "protein_target": round(calculate_protein_target(payload), 2),
    }


def update_profile(db: Session, profile: UserProfile, payload: UserProfileUpdate) -> UserProfile:
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile


def get_or_create_daily_target(db: Session, profile: UserProfile, target_date: date) -> DailyTarget:
    target = db.scalar(
        select(DailyTarget).where(
            DailyTarget.profile_id == profile.id,
            DailyTarget.date == target_date,
        )
    )
    if target:
        return target

    latest = db.scalar(
        select(DailyTarget)
        .where(DailyTarget.profile_id == profile.id)
        .order_by(DailyTarget.date.desc())
        .limit(1)
    )
    if latest:
        target = DailyTarget(
            profile_id=profile.id,
            date=target_date,
            calorie_target=latest.calorie_target,
            protein_target=latest.protein_target,
            carbs_target=latest.carbs_target,
            fats_target=latest.fats_target,
            fiber_target=latest.fiber_target,
            water_target_liters=latest.water_target_liters,
        )
    else:
        summary = get_profile_summary(profile)
        target = DailyTarget(
            profile_id=profile.id,
            date=target_date,
            calorie_target=round(summary["target_calories"] or DEFAULT_TARGETS["calorie_target"]),
            protein_target=round(summary["protein_target"] or DEFAULT_TARGETS["protein_target"]),
            carbs_target=DEFAULT_TARGETS["carbs_target"],
            fats_target=DEFAULT_TARGETS["fats_target"],
            fiber_target=DEFAULT_TARGETS["fiber_target"],
            water_target_liters=DEFAULT_TARGETS["water_target_liters"],
        )
    db.add(target)
    db.commit()
    db.refresh(target)
    return target


def upsert_daily_target(db: Session, profile: UserProfile, payload: dict) -> DailyTarget:
    target = get_or_create_daily_target(db, profile, payload["date"])
    for field, value in payload.items():
        setattr(target, field, value)
    db.add(target)
    db.commit()
    db.refresh(target)
    return target

