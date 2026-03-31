from __future__ import annotations

from datetime import date

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class ChallengeDayBase(BaseModel):
    date: date
    challenge_day_number: int | None = None
    workout_1_completed: bool = False
    workout_2_completed: bool = False
    one_workout_outdoors: bool = False
    followed_diet: bool = False
    no_cheat_meals: bool = True
    no_alcohol: bool = True
    water_goal_completed: bool = False
    progress_picture_taken: bool = False
    body_weight: float | None = Field(default=None, ge=0)
    steps: int = Field(default=0, ge=0)
    sleep_hours: float = Field(default=0, ge=0)
    mood: str = ""
    energy_level: int = Field(default=0, ge=0, le=10)
    notes: str = ""
    selected_diet_plan: str = ""
    diet_followed: bool = False
    cheat_meal: bool = False
    junk_food: bool = False
    sugary_drinks: bool = False
    hunger_level: int = Field(default=0, ge=0, le=10)
    cravings_level: int = Field(default=0, ge=0, le=10)
    binge_urge: int = Field(default=0, ge=0, le=10)
    diet_notes: str = ""


class ChallengeDayUpsert(ChallengeDayBase):
    pass


class ChallengeDayRead(ChallengeDayBase, TimestampFields):
    id: int
    profile_id: int
    day_status: str
    compliance_score: float


class ActivitySummary(BaseModel):
    workout_sessions: int
    cardio_sessions: int
    total_sessions: int
    outdoor_sessions: int
    water_total_ml: int
    water_target_ml: int
    nutrition_totals: dict[str, float]


class TodaySummary(BaseModel):
    date: date
    day_number: int
    remaining_days: int
    day_status: str
    compliance_score: float
    total_completed: int
    required_total: int
    pending_tasks: list[str]
    current_streak: int
    perfect_days: int
    failed_days: int
    activity: ActivitySummary
    nutrition_bonus_flags: dict[str, bool]
    energy_balance: dict[str, float | str]
    split_plan: dict[str, str]
    challenge_day: ChallengeDayRead

