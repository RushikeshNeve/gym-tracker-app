from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class HydrationLogCreate(BaseModel):
    date: date
    amount_ml: int = Field(ge=1)


class HydrationLogRead(TimestampFields):
    id: int
    profile_id: int
    date: date
    amount_ml: int


class HydrationDailySummary(BaseModel):
    date: date
    total_ml: int
    target_ml: int
    target_liters: float
    remaining_ml: int
    bottle_count: float
    progress_pct: float
    logs: list[HydrationLogRead]


class HydrationChartPoint(BaseModel):
    date: date
    total_ml: int
    target_ml: int
    adherence_pct: float

