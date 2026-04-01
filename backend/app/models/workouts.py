from __future__ import annotations

from datetime import date, time

from sqlalchemy import Date, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base, TimestampMixin


class Workout(TimestampMixin, Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    profile_id: Mapped[int] = mapped_column(ForeignKey("user_profile.id", ondelete="CASCADE"), index=True)
    date: Mapped[date] = mapped_column(Date, index=True)
    day_type: Mapped[str] = mapped_column(String(64))
    session_type: Mapped[str] = mapped_column(String(32), default="Workout 1")
    is_outdoor: Mapped[bool] = mapped_column(default=False)
    duration_min: Mapped[int] = mapped_column(Integer, default=0)
    start_time: Mapped[time | None]
    end_time: Mapped[time | None]
    session_notes: Mapped[str] = mapped_column(Text, default="")
    estimated_calories_burned: Mapped[float] = mapped_column(Float, default=0.0)

    profile = relationship("UserProfile", back_populates="workouts")
    exercises = relationship("WorkoutExercise", back_populates="workout", cascade="all, delete-orphan")


class WorkoutExercise(TimestampMixin, Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id", ondelete="CASCADE"), index=True)
    exercise_name: Mapped[str] = mapped_column(String(255), index=True)
    muscle_group: Mapped[str] = mapped_column(String(128), default="")
    weight: Mapped[float] = mapped_column(Float, default=0.0)
    reps: Mapped[int] = mapped_column(Integer, default=0)
    sets: Mapped[int] = mapped_column(Integer, default=1)
    duration_seconds: Mapped[int | None] = mapped_column(Integer, nullable=True)
    volume: Mapped[float] = mapped_column(Float, default=0.0)
    near_failure: Mapped[bool] = mapped_column(default=False)
    new_pr: Mapped[str] = mapped_column(String(32), default="")
    notes: Mapped[str] = mapped_column(Text, default="")

    workout = relationship("Workout", back_populates="exercises")
