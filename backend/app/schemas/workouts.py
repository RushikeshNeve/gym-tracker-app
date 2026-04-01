from __future__ import annotations

from datetime import date, time

from pydantic import BaseModel, Field

from app.schemas.common import TimestampFields


class WorkoutExerciseBase(BaseModel):
    exercise_name: str
    muscle_group: str = ""
    weight: float = Field(default=0, ge=0)
    reps: int = Field(default=0, ge=0)
    sets: int = Field(default=1, ge=1)
    duration_seconds: int | None = Field(default=None, ge=1)
    near_failure: bool = False
    notes: str = ""


class WorkoutExerciseCreate(WorkoutExerciseBase):
    pass


class WorkoutExerciseRead(WorkoutExerciseBase, TimestampFields):
    id: int
    workout_id: int
    volume: float
    new_pr: str


class WorkoutBase(BaseModel):
    date: date
    day_type: str
    session_type: str = "Workout 1"
    is_outdoor: bool = False
    duration_min: int = Field(default=0, ge=0)
    start_time: time | None = None
    end_time: time | None = None
    session_notes: str = ""
    estimated_calories_burned: float | None = Field(default=None, ge=0)


class WorkoutCreate(WorkoutBase):
    exercises: list[WorkoutExerciseCreate]


class WorkoutRead(WorkoutBase, TimestampFields):
    id: int
    profile_id: int
    estimated_calories_burned: float
    exercises: list[WorkoutExerciseRead]


class WorkoutHistoryEntry(BaseModel):
    date: date
    exercise_name: str
    weight: float
    reps: int
    sets: int
    duration_seconds: int | None = None
    new_pr: str
    session_type: str
    is_outdoor: bool
