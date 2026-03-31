from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import ORMModel, TimestampFields


class UserProfileBase(BaseModel):
    age: int | None = Field(default=None, ge=15, le=90)
    gender: str | None = None
    height_cm: float | None = Field(default=None, ge=100, le=260)
    current_weight_kg: float | None = Field(default=None, ge=30, le=300)
    activity_level: str | None = None
    goal: str | None = None
    desired_deficit: float | None = Field(default=None, ge=0, le=1500)
    challenge_start_date: date | None = None
    target_weight_kg: float | None = Field(default=None, ge=30, le=300)
    preferred_diet_plan_name: str | None = None


class UserProfileCreate(UserProfileBase):
    pass


class UserProfileUpdate(UserProfileBase):
    pass


class UserProfileRead(UserProfileBase, TimestampFields):
    id: int


class ProfileCalorieSummary(BaseModel):
    bmr: float
    tdee: float
    target_calories: float
    protein_target: float


class ProfileWithSummary(BaseModel):
    profile: UserProfileRead
    summary: ProfileCalorieSummary

