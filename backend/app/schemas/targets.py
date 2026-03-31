from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class DailyTargetBase(BaseModel):
    date: date
    calorie_target: float = Field(default=2200, ge=0)
    protein_target: float = Field(default=180, ge=0)
    carbs_target: float = Field(default=200, ge=0)
    fats_target: float = Field(default=70, ge=0)
    fiber_target: float = Field(default=30, ge=0)
    water_target_liters: float = Field(default=4.0, ge=0)


class DailyTargetUpsert(DailyTargetBase):
    pass


class DailyTargetRead(DailyTargetBase, TimestampFields):
    id: int
    profile_id: int

