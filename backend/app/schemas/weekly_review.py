from __future__ import annotations

from datetime import date

from pydantic import BaseModel

from app.schemas.common import TimestampFields


class WeeklyReviewUpsert(BaseModel):
    week_start: date
    what_went_well: str = ""
    what_was_difficult: str = ""
    focus_for_next_week: str = ""
    notes: str = ""


class WeeklyReviewRead(WeeklyReviewUpsert, TimestampFields):
    id: int
    profile_id: int


class WeeklyReviewSummary(BaseModel):
    week_start: date
    week_end: date
    avg_calories: float
    avg_protein: float
    water_adherence_pct: float
    workout_consistency: int
    outdoor_workout_consistency: int
    weight_change: float
    waist_change: float
    perfect_days: int
    incomplete_days: int
    failed_days: int
    prs: int
    total_workout_volume: float
    cardio_minutes: int
    nutrition_chart: list[dict]
    hydration_chart: list[dict]
    challenge_chart: list[dict]

