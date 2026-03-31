"""Shared 75 Hard challenge calculations."""

from __future__ import annotations

from datetime import date, datetime, timedelta
from typing import Any

import pandas as pd

from db import fetch_df, get_daily_targets, get_or_create_challenge_day, get_setting, save_challenge_day
from utils.calorie_logic import calculate_daily_energy_balance
from utils.nutrition_logic import get_daily_nutrition

REQUIRED_TASK_LABELS = {
    "workout_1_completed": "Workout 1",
    "workout_2_completed": "Workout 2",
    "one_workout_outdoors": "Outdoor workout",
    "followed_diet": "Followed diet",
    "no_cheat_meals": "No cheat meals",
    "no_alcohol": "No alcohol",
    "water_goal_completed": "Water goal",
    "progress_picture_taken": "Progress photo",
}

REQUIRED_TASK_KEYS = list(REQUIRED_TASK_LABELS.keys())


def get_challenge_start_date() -> date:
    raw = str(get_setting("challenge_start_date", date.today().isoformat()))
    return datetime.fromisoformat(raw).date()


def get_challenge_day_number(for_date: date) -> int:
    start_date = get_challenge_start_date()
    return (for_date - start_date).days + 1


def get_challenge_window() -> tuple[date, date]:
    start_date = get_challenge_start_date()
    end_date = start_date + timedelta(days=74)
    return start_date, end_date


def get_challenge_progress(for_date: date | None = None) -> dict[str, Any]:
    today = for_date or date.today()
    start_date, end_date = get_challenge_window()
    day_number = get_challenge_day_number(today)
    remaining = max(0, 75 - max(day_number, 0))
    return {
        "start_date": start_date,
        "end_date": end_date,
        "day_number": day_number,
        "remaining_days": remaining,
        "in_window": start_date <= today <= end_date,
    }


def get_daily_activity(log_date: str) -> dict[str, Any]:
    workouts = fetch_df("SELECT * FROM workout_logs WHERE date = ? ORDER BY id", (log_date,))
    cardio = fetch_df("SELECT * FROM cardio_logs WHERE date = ? ORDER BY id", (log_date,))
    photos = fetch_df("SELECT * FROM progress_photos WHERE date = ? ORDER BY id", (log_date,))
    hydration = fetch_df("SELECT * FROM hydration_logs WHERE date = ? ORDER BY id", (log_date,))
    nutrition = fetch_df("SELECT * FROM nutrition_logs WHERE date = ? ORDER BY id", (log_date,))

    workout_sessions = workouts["session_type"].fillna("Workout 1").replace("", "Workout 1").nunique() if not workouts.empty else 0
    cardio_sessions = int(len(cardio.index)) if not cardio.empty else 0
    total_sessions = workout_sessions + cardio_sessions
    outdoor_workouts = int(workouts["is_outdoor"].fillna(0).sum()) if not workouts.empty else 0
    outdoor_cardio = int(cardio["is_outdoor"].fillna(0).sum()) if not cardio.empty else 0
    water_total_ml = int(hydration["amount_ml"].sum()) if not hydration.empty else 0
    targets = get_daily_targets(log_date)
    water_target_ml = int(float(targets.get("water_target_liters", 4.0) or 4.0) * 1000)

    nutrition_totals = {
        "calories": float(nutrition["calories"].sum()) if not nutrition.empty else 0.0,
        "protein": float(nutrition["protein"].sum()) if not nutrition.empty else 0.0,
        "carbs": float(nutrition["carbs"].sum()) if not nutrition.empty else 0.0,
        "fats": float(nutrition["fats"].sum()) if not nutrition.empty else 0.0,
        "fiber": float(nutrition["fiber"].sum()) if not nutrition.empty else 0.0,
    }

    return {
        "workouts": workouts,
        "cardio": cardio,
        "photos": photos,
        "hydration": hydration,
        "nutrition": nutrition,
        "workout_sessions": workout_sessions,
        "cardio_sessions": cardio_sessions,
        "total_sessions": total_sessions,
        "outdoor_sessions": outdoor_workouts + outdoor_cardio,
        "water_total_ml": water_total_ml,
        "water_target_ml": water_target_ml,
        "nutrition_totals": nutrition_totals,
    }


def derive_compliance_from_sources(log_date: str, existing_day: dict[str, Any] | None = None) -> dict[str, Any]:
    day = existing_day or get_or_create_challenge_day(log_date)
    log_day = datetime.fromisoformat(log_date).date()
    activity = get_daily_activity(log_date)

    workout_1_completed = bool(day.get("workout_1_completed")) or activity["total_sessions"] >= 1
    workout_2_completed = bool(day.get("workout_2_completed")) or activity["total_sessions"] >= 2
    one_workout_outdoors = bool(day.get("one_workout_outdoors")) or activity["outdoor_sessions"] >= 1
    progress_picture_taken = bool(day.get("progress_picture_taken")) or not activity["photos"].empty
    water_goal_completed = bool(day.get("water_goal_completed")) or activity["water_total_ml"] >= activity["water_target_ml"]
    followed_diet = bool(day.get("followed_diet")) or bool(day.get("diet_followed"))
    no_cheat_meals = not bool(day.get("cheat_meal")) if "cheat_meal" in day else bool(day.get("no_cheat_meals", 1))
    if day.get("no_cheat_meals") in (0, 1):
        no_cheat_meals = bool(day.get("no_cheat_meals"))
    no_alcohol = bool(day.get("no_alcohol", 1))

    required_flags = {
        "workout_1_completed": workout_1_completed,
        "workout_2_completed": workout_2_completed,
        "one_workout_outdoors": one_workout_outdoors,
        "followed_diet": followed_diet,
        "no_cheat_meals": no_cheat_meals,
        "no_alcohol": no_alcohol,
        "water_goal_completed": water_goal_completed,
        "progress_picture_taken": progress_picture_taken,
    }
    nutrition = get_daily_nutrition(log_date)
    energy_balance = calculate_daily_energy_balance(log_date)
    bonus_flags = {
        "calorie_target_hit": nutrition["compliance_inputs"]["within_calories"],
        "protein_target_hit": nutrition["compliance_inputs"]["hit_protein_target"],
        "whey_taken": nutrition["compliance_inputs"]["whey_taken"],
        "in_deficit": energy_balance["status"] == "in_deficit",
    }

    lifestyle_flags = {
        "body_weight_logged": day.get("body_weight") not in (None, ""),
        "steps_logged": int(day.get("steps", 0) or 0) > 0,
        "sleep_logged": float(day.get("sleep_hours", 0) or 0) > 0,
        "mood_logged": bool(str(day.get("mood", "")).strip()),
        "energy_logged": int(day.get("energy_level", 0) or 0) > 0,
    }

    required_score = sum(10 for value in required_flags.values() if value)
    lifestyle_score = sum(4 for value in lifestyle_flags.values() if value)
    nutrition_bonus = sum(2.5 for value in bonus_flags.values() if value)
    compliance_score = min(100, required_score + lifestyle_score + nutrition_bonus)

    if all(required_flags.values()):
        day_status = "perfect"
    elif log_day < date.today():
        day_status = "failed"
    else:
        day_status = "incomplete"

    pending_tasks = [REQUIRED_TASK_LABELS[key] for key, value in required_flags.items() if not value]

    return {
        **required_flags,
        "day_status": day_status,
        "compliance_score": compliance_score,
        "pending_tasks": pending_tasks,
        "total_completed": sum(1 for value in required_flags.values() if value),
        "required_total": len(required_flags),
        "activity": activity,
        "nutrition_bonus_flags": bonus_flags,
        "energy_balance": energy_balance,
    }


def sync_challenge_day(log_date: str) -> dict[str, Any]:
    day = get_or_create_challenge_day(log_date)
    progress = get_challenge_progress(datetime.fromisoformat(log_date).date())
    derived = derive_compliance_from_sources(log_date, day)
    payload = {
        **day,
        **{key: int(bool(derived[key])) for key in REQUIRED_TASK_KEYS},
        "date": log_date,
        "challenge_day_number": progress["day_number"],
        "day_status": derived["day_status"],
        "compliance_score": derived["compliance_score"],
    }
    save_challenge_day(payload)
    return {
        **payload,
        "pending_tasks": derived["pending_tasks"],
        "activity": derived["activity"],
        "total_completed": derived["total_completed"],
        "required_total": derived["required_total"],
        "nutrition_bonus_flags": derived["nutrition_bonus_flags"],
        "energy_balance": derived["energy_balance"],
    }


def get_challenge_days_df() -> pd.DataFrame:
    df = fetch_df("SELECT * FROM challenge_days ORDER BY date")
    if not df.empty:
        for _, row in df.iterrows():
            derived = derive_compliance_from_sources(row["date"], row.to_dict())
            save_challenge_day(
                {
                    **row.to_dict(),
                    **{key: int(bool(derived[key])) for key in REQUIRED_TASK_KEYS},
                    "day_status": derived["day_status"],
                    "compliance_score": derived["compliance_score"],
                }
            )
        df = fetch_df("SELECT * FROM challenge_days ORDER BY date")
        df["date"] = pd.to_datetime(df["date"])
    return df


def calculate_streaks() -> dict[str, Any]:
    challenge = get_challenge_days_df()
    if challenge.empty:
        return {"current_streak": 0, "perfect_days": 0, "failed_days": 0, "completion_pct": 0}

    challenge = challenge.sort_values("date")
    perfect_days = int((challenge["day_status"] == "perfect").sum())
    failed_days = int((challenge["day_status"] == "failed").sum())
    current_streak = 0
    cursor = pd.Timestamp(date.today())
    status_by_date = dict(zip(challenge["date"].dt.date, challenge["day_status"]))
    while status_by_date.get(cursor.date()) == "perfect":
        current_streak += 1
        cursor -= pd.Timedelta(days=1)

    completion_pct = round((perfect_days / 75) * 100, 1)
    return {
        "current_streak": current_streak,
        "perfect_days": perfect_days,
        "failed_days": failed_days,
        "completion_pct": completion_pct,
    }


def get_today_snapshot() -> dict[str, Any]:
    today_str = date.today().isoformat()
    progress = get_challenge_progress(date.today())
    day = sync_challenge_day(today_str)
    streaks = calculate_streaks()
    return {**progress, **streaks, **day}


def get_split_plan(reference_date: date | None = None) -> dict[str, str]:
    ref = reference_date or date.today()
    rotation = ["Push", "Pull", "Legs", "Cardio / Outdoor", "Active Recovery"]
    start_date = get_challenge_start_date()
    index = max(0, (ref - start_date).days) % len(rotation)
    today_plan = rotation[index]
    tomorrow_plan = rotation[(index + 1) % len(rotation)]
    challenge = get_challenge_days_df()
    missed_recovery = "Stay on schedule"
    if not challenge.empty:
        recent = challenge.sort_values("date", ascending=False).head(3)
        if (recent["day_status"] == "failed").any():
            missed_recovery = "Prioritize an outdoor cardio session and resume the next split day"
    return {
        "today_plan": today_plan,
        "tomorrow_plan": tomorrow_plan,
        "missed_recovery": missed_recovery,
    }
