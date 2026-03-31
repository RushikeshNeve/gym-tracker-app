"""Weekly summary helpers for 75 Hard reviews."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import pandas as pd

from db import fetch_df
from utils.challenge_logic import get_challenge_days_df
from utils.hydration_logic import get_weekly_hydration
from utils.nutrition_logic import get_weekly_nutrition


def get_week_start(reference_date: date | None = None) -> date:
    ref = reference_date or date.today()
    return ref - timedelta(days=ref.weekday())


def get_weekly_summary(week_start: date | None = None) -> dict[str, Any]:
    start = week_start or get_week_start()
    end = start + timedelta(days=6)
    start_str, end_str = start.isoformat(), end.isoformat()

    workouts = fetch_df("SELECT * FROM workout_logs WHERE date BETWEEN ? AND ? ORDER BY date", (start_str, end_str))
    cardio = fetch_df("SELECT * FROM cardio_logs WHERE date BETWEEN ? AND ? ORDER BY date", (start_str, end_str))
    body = fetch_df("SELECT * FROM body_metrics WHERE date BETWEEN ? AND ? ORDER BY date", (start_str, end_str))
    challenge = get_challenge_days_df()
    if not challenge.empty:
        challenge = challenge[(challenge["date"].dt.date >= start) & (challenge["date"].dt.date <= end)]

    nutrition, nutrition_summary = get_weekly_nutrition(end)
    hydration = get_weekly_hydration(end)
    if not hydration.empty:
        hydration = hydration[(hydration["date"].dt.date >= start) & (hydration["date"].dt.date <= end)]

    total_volume = float(workouts["volume"].sum()) if not workouts.empty else 0.0
    workout_days = int(pd.to_datetime(workouts["date"]).dt.date.nunique()) if not workouts.empty else 0
    outdoor_consistency = int(cardio["is_outdoor"].fillna(0).sum()) + int(workouts["is_outdoor"].fillna(0).sum()) if not cardio.empty or not workouts.empty else 0
    cardio_minutes = int(cardio["duration_min"].sum()) if not cardio.empty else 0
    prs = int(workouts["new_pr"].isin(["PR", "First"]).sum()) if not workouts.empty else 0

    weight_change = 0.0
    waist_change = 0.0
    if not body.empty and len(body.index) >= 2:
        weight_change = float(body.iloc[-1]["body_weight"] - body.iloc[0]["body_weight"]) if pd.notna(body.iloc[0]["body_weight"]) else 0.0
        waist_change = float(body.iloc[-1]["waist"] - body.iloc[0]["waist"]) if pd.notna(body.iloc[0]["waist"]) else 0.0

    water_adherence = float(hydration["adherence_pct"].mean()) if not hydration.empty else 0.0
    perfect_days = int((challenge["day_status"] == "perfect").sum()) if not challenge.empty else 0
    incomplete_days = int((challenge["day_status"] == "incomplete").sum()) if not challenge.empty else 0
    failed_days = int((challenge["day_status"] == "failed").sum()) if not challenge.empty else 0

    return {
        "week_start": start,
        "week_end": end,
        "avg_calories": nutrition_summary["avg_calories"],
        "avg_protein": nutrition_summary["avg_protein"],
        "water_adherence_pct": water_adherence,
        "workout_consistency": workout_days,
        "outdoor_workout_consistency": outdoor_consistency,
        "weight_change": weight_change,
        "waist_change": waist_change,
        "perfect_days": perfect_days,
        "incomplete_days": incomplete_days,
        "failed_days": failed_days,
        "prs": prs,
        "total_workout_volume": total_volume,
        "cardio_minutes": cardio_minutes,
        "nutrition_df": nutrition,
        "hydration_df": hydration,
        "challenge_df": challenge,
        "workouts_df": workouts,
        "cardio_df": cardio,
        "body_df": body,
    }
