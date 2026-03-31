from __future__ import annotations

from datetime import date as date_type

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class BodyMetricBase(BaseModel):
    date: date_type
    body_weight: float | None = Field(default=None, ge=0)
    waist: float | None = Field(default=None, ge=0)
    chest: float | None = Field(default=None, ge=0)
    arms: float | None = Field(default=None, ge=0)
    thigh: float | None = Field(default=None, ge=0)
    body_fat_percent: float | None = Field(default=None, ge=0)
    notes: str = ""
    hips: float | None = Field(default=None, ge=0)
    neck: float | None = Field(default=None, ge=0)
    thighs: float | None = Field(default=None, ge=0)
    progress_notes: str = ""


class BodyMetricCreate(BodyMetricBase):
    pass


class BodyMetricUpdate(BaseModel):
    date: date_type | None = None
    body_weight: float | None = Field(default=None, ge=0)
    waist: float | None = Field(default=None, ge=0)
    chest: float | None = Field(default=None, ge=0)
    arms: float | None = Field(default=None, ge=0)
    thigh: float | None = Field(default=None, ge=0)
    body_fat_percent: float | None = Field(default=None, ge=0)
    notes: str | None = None
    hips: float | None = Field(default=None, ge=0)
    neck: float | None = Field(default=None, ge=0)
    thighs: float | None = Field(default=None, ge=0)
    progress_notes: str | None = None


class BodyMetricRead(BodyMetricBase, TimestampFields):
    id: int
    profile_id: int
