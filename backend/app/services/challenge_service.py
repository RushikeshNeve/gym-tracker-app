from __future__ import annotations

from datetime import date, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.cardio_logs import CardioLog
from app.models.challenge_days import ChallengeDay
from app.models.progress_photos import ProgressPhoto
from app.models.user_profile import UserProfile
from app.models.workouts import Workout
from app.services.calorie_service import calculate_daily_energy_balance
from app.services.hydration_service import get_daily_hydration
from app.services.nutrition_service import compute_diet_score, get_daily_nutrition
from app.utils.calculations import calculate_compliance_score, challenge_progress, derive_day_status
from app.utils.constants import REQUIRED_TASK_KEYS, REQUIRED_TASK_LABELS


def get_or_create_challenge_day(db: Session, profile: UserProfile, log_date: date) -> ChallengeDay:
    day = db.scalar(
        select(ChallengeDay).where(
            ChallengeDay.profile_id == profile.id,
            ChallengeDay.date == log_date,
        )
    )
    if day:
        return day
    progress = challenge_progress(profile.challenge_start_date or (date.today() + timedelta(days=1)), log_date)
    day = ChallengeDay(profile_id=profile.id, date=log_date, challenge_day_number=progress["day_number"])
    db.add(day)
    db.commit()
    db.refresh(day)
    return day


def save_challenge_day(db: Session, profile: UserProfile, payload: dict) -> ChallengeDay:
    day = get_or_create_challenge_day(db, profile, payload["date"])
    for key, value in payload.items():
        setattr(day, key, value)
    db.add(day)
    db.commit()
    db.refresh(day)
    return day


def get_split_plan(profile: UserProfile, reference_date: date | None = None) -> dict[str, str]:
    ref = reference_date or date.today()
    start_date = profile.challenge_start_date or (date.today() + timedelta(days=1))
    rotation = ["Push", "Pull", "Legs", "Cardio / Outdoor", "Active Recovery"]
    index = max(0, (ref - start_date).days) % len(rotation)
    return {
        "today_plan": rotation[index],
        "tomorrow_plan": rotation[(index + 1) % len(rotation)],
        "missed_recovery": "Stay on schedule",
    }


def get_daily_activity(db: Session, profile: UserProfile, log_date: date) -> dict:
    workout_rows = db.execute(
        select(Workout.session_type, Workout.is_outdoor)
        .where(Workout.profile_id == profile.id, Workout.date == log_date)
    ).all()
    cardio_rows = db.execute(
        select(CardioLog.is_outdoor)
        .where(CardioLog.profile_id == profile.id, CardioLog.date == log_date)
    ).all()
    photo_count = db.scalar(
        select(func.count(ProgressPhoto.id)).where(
            ProgressPhoto.profile_id == profile.id,
            ProgressPhoto.date == log_date,
        )
    ) or 0
    hydration = get_daily_hydration(db, profile, log_date)
    nutrition = get_daily_nutrition(db, profile, log_date)
    workout_sessions = len({row.session_type or "Workout 1" for row in workout_rows})
    return {
        "workout_sessions": workout_sessions,
        "cardio_sessions": len(cardio_rows),
        "total_sessions": workout_sessions + len(cardio_rows),
        "outdoor_sessions": sum(1 for row in workout_rows if row.is_outdoor) + sum(1 for row in cardio_rows if row.is_outdoor),
        "photo_count": int(photo_count),
        "water_total_ml": hydration["total_ml"],
        "water_target_ml": hydration["target_ml"],
        "nutrition_totals": nutrition["totals"],
    }


def derive_compliance_from_sources(db: Session, profile: UserProfile, log_date: date, day: ChallengeDay | None = None) -> dict:
    current_day = day or get_or_create_challenge_day(db, profile, log_date)
    activity = get_daily_activity(db, profile, log_date)
    nutrition = get_daily_nutrition(db, profile, log_date)
    energy = calculate_daily_energy_balance(db, profile, log_date)
    required_flags = {
        "workout_1_completed": bool(current_day.workout_1_completed) or activity["total_sessions"] >= 1,
        "one_workout_outdoors": bool(current_day.one_workout_outdoors) or activity["outdoor_sessions"] >= 1,
        "followed_diet": bool(current_day.followed_diet) or bool(current_day.diet_followed),
        "no_cheat_meals": bool(current_day.no_cheat_meals) and not bool(current_day.cheat_meal),
        "water_goal_completed": bool(current_day.water_goal_completed) or activity["water_total_ml"] >= activity["water_target_ml"],
        "progress_picture_taken": bool(current_day.progress_picture_taken) or activity["photo_count"] > 0,
    }
    bonus_flags = {
        "calorie_target_hit": nutrition["compliance_inputs"]["within_calories"],
        "protein_target_hit": nutrition["compliance_inputs"]["hit_protein_target"],
        "whey_taken": nutrition["compliance_inputs"]["whey_taken"],
        "in_deficit": energy["status"] == "in_deficit",
    }
    lifestyle_flags = {
        "body_weight_logged": current_day.body_weight is not None,
        "steps_logged": int(current_day.steps or 0) > 0,
        "sleep_logged": float(current_day.sleep_hours or 0) > 0,
        "mood_logged": bool((current_day.mood or "").strip()),
        "energy_logged": int(current_day.energy_level or 0) > 0,
    }
    return {
        **required_flags,
        "day_status": derive_day_status(required_flags, log_date),
        "compliance_score": calculate_compliance_score(required_flags, lifestyle_flags, bonus_flags),
        "pending_tasks": [REQUIRED_TASK_LABELS[key] for key, value in required_flags.items() if not value],
        "total_completed": sum(1 for value in required_flags.values() if value),
        "required_total": len(required_flags),
        "activity": activity,
        "nutrition_bonus_flags": bonus_flags,
        "energy_balance": energy,
    }


def sync_challenge_day(db: Session, profile: UserProfile, log_date: date) -> ChallengeDay:
    day = get_or_create_challenge_day(db, profile, log_date)
    progress = challenge_progress(profile.challenge_start_date or (date.today() + timedelta(days=1)), log_date)
    derived = derive_compliance_from_sources(db, profile, log_date, day)
    payload = {
        "date": log_date,
        "challenge_day_number": progress["day_number"],
        "day_status": derived["day_status"],
        "compliance_score": derived["compliance_score"],
        **{key: bool(derived[key]) for key in REQUIRED_TASK_KEYS},
    }
    return save_challenge_day(db, profile, payload)


def calculate_streaks(db: Session, profile: UserProfile) -> dict[str, float | int]:
    rows = list(
        db.scalars(
            select(ChallengeDay)
            .where(ChallengeDay.profile_id == profile.id)
            .order_by(ChallengeDay.date.asc())
        ).all()
    )
    if not rows:
        return {"current_streak": 0, "perfect_days": 0, "failed_days": 0, "completion_pct": 0.0}
    status_by_date = {row.date: row.day_status for row in rows}
    perfect_days = sum(1 for row in rows if row.day_status == "perfect")
    failed_days = sum(1 for row in rows if row.day_status == "failed")
    current_streak = 0
    cursor = date.today()
    while status_by_date.get(cursor) == "perfect":
        current_streak += 1
        cursor -= timedelta(days=1)
    return {
        "current_streak": current_streak,
        "perfect_days": perfect_days,
        "failed_days": failed_days,
        "completion_pct": round((perfect_days / 75) * 100, 1),
    }


def get_today_summary(db: Session, profile: UserProfile, log_date: date | None = None) -> dict:
    current_date = log_date or date.today()
    day = sync_challenge_day(db, profile, current_date)
    derived = derive_compliance_from_sources(db, profile, current_date, day)
    progress = challenge_progress(profile.challenge_start_date or (date.today() + timedelta(days=1)), current_date)
    return {
        "date": current_date,
        **progress,
        **calculate_streaks(db, profile),
        "day_status": derived["day_status"],
        "compliance_score": derived["compliance_score"],
        "total_completed": derived["total_completed"],
        "required_total": derived["required_total"],
        "pending_tasks": derived["pending_tasks"],
        "activity": derived["activity"],
        "nutrition_bonus_flags": derived["nutrition_bonus_flags"],
        "energy_balance": derived["energy_balance"],
        "split_plan": get_split_plan(profile, current_date),
        "challenge_day": day,
    }


def upsert_manual_challenge_day(db: Session, profile: UserProfile, payload: dict) -> ChallengeDay:
    existing = get_or_create_challenge_day(db, profile, payload["date"])
    nutrition = get_daily_nutrition(db, profile, payload["date"])
    diet_score = compute_diet_score(
        daily_nutrition=nutrition,
        followed_plan=bool(payload.get("followed_diet", existing.followed_diet)),
        no_cheat_meal=bool(payload.get("no_cheat_meals", existing.no_cheat_meals)) and not bool(payload.get("cheat_meal", existing.cheat_meal)),
    )
    merged = {**existing.__dict__, **payload, "compliance_score": max(float(existing.compliance_score or 0), float(diet_score))}
    merged.pop("_sa_instance_state", None)
    return save_challenge_day(db, profile, merged)
