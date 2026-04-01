from __future__ import annotations

from pydantic import BaseModel


class TimetableExerciseOption(BaseModel):
    id: int
    name: str


class TimetableOptionGroupRead(BaseModel):
    category: str
    sets_reps: str
    options: list[TimetableExerciseOption]


class TimetableDayRead(BaseModel):
    id: str
    day_label: str
    title: str
    subtitle: str
    accent: str
    notes: list[str]
    images: list[str]
    blocks: list[TimetableOptionGroupRead]


class WeeklySplitDayRead(BaseModel):
    day: str
    workout: str


class WorkoutTimetableRead(BaseModel):
    weekly_split: list[WeeklySplitDayRead]
    timetable_days: list[TimetableDayRead]
