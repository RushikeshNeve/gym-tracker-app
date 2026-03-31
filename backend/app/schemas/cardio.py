from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class CardioLogBase(BaseModel):
    date: date
    cardio_type: str
    duration_min: int = Field(ge=1)
    calories: int | None = Field(default=None, ge=0)
    intensity: str | None = None
    notes: str = ""
    is_outdoor: bool = False
    distance_km: float = Field(default=0, ge=0)
    pace_text: str = ""
    estimated_calories_burned: float | None = Field(default=None, ge=0)


class CardioLogCreate(CardioLogBase):
    pass


class CardioLogRead(CardioLogBase, TimestampFields):
    id: int
    profile_id: int
    estimated_calories_burned: float

