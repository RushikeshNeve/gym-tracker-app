from __future__ import annotations

from pydantic import BaseModel


class DashboardMetricSummary(BaseModel):
    streak: int
    weekly_workouts: int
    weekly_volume: float
    weekly_prs: int
    cardio_mins: int
    cardio_cals: int
    latest_weight: float | None
    weekly_score: float
    consistency_pct: int
    perfect_days: int
    failed_days: int


class DashboardResponse(BaseModel):
    metrics: DashboardMetricSummary
    energy: dict
    nutrition: dict
    hydration: dict
    challenge: dict
    recent_activity: list[dict]
    recent_prs: list[dict]
    weekly_energy_chart: list[dict]
    weekly_nutrition_chart: list[dict]
    weekly_hydration_chart: list[dict]
